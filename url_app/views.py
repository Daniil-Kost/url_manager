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
from django.http import HttpResponseRedirect
from url_app.models import MyUrl
from url_app import util
from django.shortcuts import redirect
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from url_app.serializer import MyUrlSerializer


def url_get_add(request):
    # was form posted?
    if request.method == "POST":
        # was form add button clicked?
        if request.POST.get('create_url') is not None:
            # errors collection
            errors = {}

            # data for MyUrl object
            data = {'long_url': request.POST.get('long_url')}

            val = URLValidator()
            try:
                val(data["long_url"])
                text = util.get_text(data["long_url"])
            except ValidationError:
                errors['long_url'] = u"Your long URL is invalid"
                text = ""

            if request.POST.get('short_url') != "":
                data["short_url"] = request.POST.get('short_url')
                if 4 > len(data["short_url"]) or len(data["short_url"]) > 6:
                    errors['short_url'] = "Short URL will be at least"  \
                                          "4 chars and max 6 chars"

            # save MyUrl
            if not errors and request.POST.get('short_url') == "":
                my_url = MyUrl(url=data["long_url"],
                               text=util.edit_text(text),
                               short_url=util.short_url_generator())
                my_url.save()

                # redirect to main page
                return HttpResponseRedirect(
                    '%s?status_message=Url successfully added!' %
                    reverse('home'))
                # save MyUrl
            elif not errors and request.POST.get('short_url') != "":
                my_url = MyUrl(url=data["long_url"],
                               text=util.edit_text(text),
                               short_url=data["short_url"])
                my_url.save()

                # redirect to main page
                return HttpResponseRedirect(
                    '%s?status_message=Url successfully added!' %
                    reverse('home'))
            else:
                my_urls = MyUrl.objects.all()
                paginator = Paginator(my_urls, 5)
                page = request.GET.get('page')
                try:
                    my_urls = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    my_urls = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999),
                    # deliver last page of results.
                    my_urls = paginator.page(paginator.num_pages)
                # render form with errors and previous user input
                return render(request, 'pages/main.html',
                              {'my_urls': my_urls,
                               'errors': errors})
    else:
        # initial form render
        my_urls = MyUrl.objects.all()
        paginator = Paginator(my_urls, 5)
        page = request.GET.get('page')
        try:
            my_urls = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            my_urls = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999),
            # deliver last page of results.
            my_urls = paginator.page(paginator.num_pages)
        # render form with errors and previous user input
        return render(request, 'pages/main.html',
                      {'my_urls': my_urls})


class MyUrlUpdateForm(ModelForm):
    class Meta:
        model = MyUrl

        exclude = ("slug",)

    def __init__(self, *args, **kwargs):
        super(MyUrlUpdateForm, self).__init__(*args, **kwargs)

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


class MyUrlUpdateView(UpdateView):
    """docstring for MyUrlUpdateView"""

    model = MyUrl
    template_name = 'pages/url_edit.html'

    form_class = MyUrlUpdateForm

    success_url = '/'
    success_message = "MyUrl updated successfully !"

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(
                MyUrlUpdateView, self).post(request, *args, **kwargs)


class MyUrlDeleteView(DeleteView):
    """docstring for MyUrlDeleteView"""
    model = MyUrl
    template_name = 'pages/url_delete.html'

    success_url = reverse_lazy('home')
    success_message = "MyUrl successfully deleted !"

    def delete(self, request, *args, **kwargs):
        return super(MyUrlDeleteView, self).delete(request, *args, **kwargs)


class UrlRedirectView(UpdateView):
    """docstring for UrlRedirectView"""

    model = MyUrl
    template_name = 'pages/base.html'

    exclude = ("",)

    def get(self, request, **kwargs):
        path = request.path
        new_path = path[1:len(path) - 1]
        obj = MyUrl.objects.get(short_url=new_path)
        obj.clicks += 1
        obj.save()
        return redirect(obj.url)


class MyUrlList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = MyUrl.objects.all()
        serializer = MyUrlSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MyUrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
