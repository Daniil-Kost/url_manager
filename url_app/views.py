from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import forms
from django.contrib.auth import login
from django.views.generic import UpdateView, DeleteView
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from url_app.models import Url
from url_app import util
from url_app.serializer import UrlSerializer
from .tokens import account_activation_token


def account_activation_sent(request):
    return render(request, 'pages/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')

    else:
        return render(request, 'pages/account_activation_invalid.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('username')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('pages/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uuid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})


@login_required(login_url='/login/')
def url_get_add(request):
    user = request.user
    urls = Url.objects.filter(profile=user.profile)
    page = request.GET.get('page')
    if request.method == "POST":
        if request.POST.get('create_url') is not None:
            request_data = {'url': request.POST.get('url'), 'short_url': request.POST.get('short_url')}
            data, errors = util.prepare_url_data(request_data)
            if not errors:
                url = Url(url=data["url"],
                          title=data["title"],
                          short_url=data["short_url"])
                url.save()
                util.save_user_urls(user, url)
                return HttpResponseRedirect(
                    '%s?status_message=Url successfully added!' %
                    reverse('home'))
            else:
                my_urls = util.paginate(urls, page, 5)
                return render(request, 'pages/main.html',
                              {'my_urls': my_urls,
                               'errors': errors})
    else:
        my_urls = util.paginate(urls, page, 5)
        return render(request, 'pages/main.html',
                      {'my_urls': my_urls})


class UrlUpdateForm(ModelForm):
    class Meta:
        model = Url

        exclude = ("slug",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse('url_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-4 control label'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout.append(FormActions(
            Submit('add_button', 'Save',
                   css_class="btn save btn-primary"),
            Submit('cancel_button', 'Cancel',
                   css_class="btn cancel btn-danger"), ))
        self.fields['domain'].widget.attrs = {'disabled': 'disabled'}


class UrlUpdateView(UpdateView):
    """docstring for UrlUpdateView"""
    model = Url
    template_name = 'pages/url_edit.html'
    form_class = UrlUpdateForm
    success_url = '/'
    success_message = "Url updated successfully !"

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super().post(request, *args, **kwargs)


class UrlDeleteView(DeleteView):
    """docstring for UrlDeleteView"""
    model = Url
    template_name = 'pages/url_delete.html'
    success_url = reverse_lazy('home')
    success_message = "Url successfully deleted !"

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UrlRedirectView(UpdateView):
    """docstring for UrlRedirectView"""
    model = Url
    template_name = 'pages/base.html'
    exclude = ("",)

    def get(self, request, **kwargs):
        path = request.path
        new_path = path[1:len(path) - 1]
        obj = Url.objects.get(short_url=new_path)
        obj.clicks += 1
        obj.save()
        return redirect(obj.url)


class UrlList(APIView):
    """
    List of all data with urls, or create a new short url.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        urls = Url.objects.filter(profile=user.profile)
        serializer = UrlSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.data.get("url"):
            return Response({"error": "Invalid data. Please define 'url' in your request data."},
                            status=status.HTTP_400_BAD_REQUEST)
        data, errors = util.prepare_url_data(request.data)
        serializer = UrlSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            url_uuid = dict(serializer.data)["uuid"]
            url = Url.objects.get(uuid=url_uuid)
            util.save_user_urls(request.user, url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UrlDetail(APIView):
    """Get or delete selected data by id"""
    permission_classes = (IsAuthenticated,)

    def _get_object(self, uuid):
        try:
            return Url.objects.get(uuid=uuid)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid):
        url = self._get_object(uuid)
        serializer = UrlSerializer(url)
        return Response(serializer.data)

    def delete(self, request, uuid):
        url = self._get_object(uuid)
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
