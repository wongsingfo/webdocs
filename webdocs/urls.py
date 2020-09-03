"""webdocs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

""" Until Django 1.11 there was nothing called a path to define app urls. Django 2.0 introduces path as a replacement
for URL. Since you have just started with Django stick with 2.0 documentation and keep in mind that every forum you
check will have solutions for older versions of Django """

# argument for path()
# 1. route
# 2. view
# 3. kwargs
# 4. name: Naming your URL lets you refer to it unambiguously from elsewhere
#    in Django, especially from within templates. This powerful feature allows
#    you to make global changes to the URL patterns of your project while only touching a single file.

urlpatterns = [
    path('api/', include('page.urls')),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
