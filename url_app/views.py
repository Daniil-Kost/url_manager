# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper
from django.urls import reverse, reverse_lazy
from crispy_forms.bootstrap import FormActions
from django.http import HttpResponseRedirect, Http404
from url_app.models import Url
from url_app import util
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from url_app.serializer import UrlSerializer
from url_manager.settings import DEFAULT_DOMAIN


def url_get_add(request):
    if request.method == "POST":
        if request.POST.get('create_url') is not None:
            errors = {}
            data = {'long_url': request.POST.get('long_url')}
            val = URLValidator()

            try:
                val(data["long_url"])
                title = util.get_title(data["long_url"])
            except ValidationError:
                errors['long_url'] = u"Your long URL is invalid"
                title = ""

            if request.POST.get('short_url') != "":
                data["short_url"] = request.POST.get('short_url')
                if 4 > len(data["short_url"]) or len(data["short_url"]) > 8:
                    errors['short_url'] = "Short URL will be at least" \
                                          "4 chars and max 8 chars"

            if not errors and request.POST.get('short_url') == "":
                url = Url(url=data["long_url"],
                          title=title,
                          short_url=f'{DEFAULT_DOMAIN}{util.short_url_generator()}')
                url.save()
                return HttpResponseRedirect(
                    '%s?status_message=Url successfully added!' %
                    reverse('home'))

            elif not errors and request.POST.get('short_url') != "":
                url = Url(url=data["long_url"],
                          title=title,
                          short_url=f'{DEFAULT_DOMAIN}{data["short_url"]}')
                url.save()
                return HttpResponseRedirect(
                    '%s?status_message=Url successfully added!' %
                    reverse('home'))

            else:
                urls = Url.objects.all()
                paginator = Paginator(urls, 5)
                page = request.GET.get('page')
                try:
                    my_urls = paginator.page(page)
                except PageNotAnInteger:
                    my_urls = paginator.page(1)
                except EmptyPage:
                    my_urls = paginator.page(paginator.num_pages)
                return render(request, 'pages/main.html',
                              {'my_urls': my_urls,
                               'errors': errors})
    else:
        urls = Url.objects.all()
        paginator = Paginator(urls, 5)
        page = request.GET.get('page')
        try:
            my_urls = paginator.page(page)
        except PageNotAnInteger:
            my_urls = paginator.page(1)
        except EmptyPage:
            my_urls = paginator.page(paginator.num_pages)
        return render(request, 'pages/main.html',
                      {'my_urls': my_urls})


class UrlUpdateForm(ModelForm):
    class Meta:
        model = Url

        exclude = ("slug",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set from tag attributes
        self.helper.form_action = reverse('url_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-4 control label'
        self.helper.field_class = 'col-sm-8'

        # add buttons
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


class MyUrlList(APIView):
    """
    List of all data with urls, or create a new short url.
    """

    def get(self, request):
        urls = Url.objects.all()
        serializer = UrlSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UrlDetail(APIView):
    """Get or delete selected data by id"""

    def _get_object(self, pk):
        try:
            return Url.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk):
        url = self._get_object(pk)
        serializer = UrlSerializer(url)
        return Response(serializer.data)

    def delete(self, request, pk):
        url = self._get_object(pk)
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
