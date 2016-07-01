"""signalserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from fileuploads import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^show/(?P<video_videofile_name>[\w.]{0,256})$',
        views.show_video, name='show_video'),
    url(r'^show/result/(?P<video_videofile_name>[\w.]{0,256})$',
        views.show_result, name='show_result'),
    url(r'^process/$', views.process, name='process'),
    url(r'^search/$', views.search, name='search'),
    url(r'^status/$', views.status, name='status'),
    url(r'^save_group/$', views.save_group, name='save_group'),
    url(r'^group_process/$', views.group_process, name='group_process'),
    url(r'^fileuploads/', include('fileuploads.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^delete-video/(?P<video_videofile_name>[\w.]{0,256})$',
        views.delete_video, name='delete_video'),
    url(r'^operations/', include('operations.urls')),
    url(r'^upload', views.upload, name='upload'),
] + static(settings.BOWER_COMPONENTS_URL,
           document_root=settings.BOWER_COMPONENTS_ROOT)
