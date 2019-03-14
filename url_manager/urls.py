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
from url_app.views import url_get_add, \
    MyUrlUpdateView, MyUrlDeleteView, UrlRedirectView
from rest_framework import routers, serializers, viewsets
from url_app.models import MyUrl


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUrl
        fields = ('url', 'text', 'short_url', 'clicks', 'create_dttm')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUrl.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/v1/urls', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', url_get_add, name='home'),

    path('url/<int:pk>/edit/', MyUrlUpdateView.as_view(), name='url_edit'),

    path('url/<int:pk>/delete/', MyUrlDeleteView.as_view(), name='url_delete'),

    url(r'^(?P<slug>[-\w]+)/$', UrlRedirectView.as_view(),
        name='url_redirect'),

    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^', include(router.urls)),

]
