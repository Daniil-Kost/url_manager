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
from django.contrib.auth import views as auth_views
from django.contrib import admin
from url_app.views import (
    url_get_add,
    signup,
account_activation_sent,
activate,
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

    path(f'{api_version}urls/', UrlList.as_view(), name='api_url_list'),

    path(f'{api_version}urls/<int:pk>/', UrlDetail.as_view()),

    path('signup/', signup, name='signup'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^(?P<slug>[-\w]+)/$', UrlRedirectView.as_view(),
        name='url_redirect'),

    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^account/account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^account/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

]
