"""url_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from url_app.views import (
    url_get_add,
    UrlUpdateView,
    UrlDeleteView,
    UrlRedirectView,
    UrlList,
    UrlDetail,
)

api_version = "api/v1/"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', url_get_add, name='home'),

    path('url/<int:pk>/edit/', UrlUpdateView.as_view(), name='url_edit'),

    path('url/<int:pk>/delete/', UrlDeleteView.as_view(), name='url_delete'),

    path(f'{api_version}urls/', UrlList.as_view()),

    path(f'{api_version}urls/<int:pk>/', UrlDetail.as_view()),

    url(r'^(?P<slug>[-\w]+)/$', UrlRedirectView.as_view(),
        name='url_redirect'),

    url(r'^api-auth/', include('rest_framework.urls')),

]
