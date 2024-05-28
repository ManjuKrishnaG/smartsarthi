"""
URL configuration for smartwearable project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from ticketapp.views import handle_not_found,serve_media_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ticketapp.urls')),
    path('',include('user_module.urls')),
    path('',include('logistics.urls')),
    re_path(r'^media/attachments/(?P<file_name>.+)$', serve_media_file, name='serve_media_file'),
    path('<path:not_found>', handle_not_found),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'ticketapp.views.handle_not_found'