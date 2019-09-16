"""TIMEOUT URL Configuration

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
from django.contrib import admin
from django.urls import path, include
import mainapp.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.views.index, name='index'),
    path('login/', mainapp.views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('portfolio/', mainapp.views.portfolio, name='portfolio'),
    path('check/', mainapp.views.check, name='check'),
    path('invite/', mainapp.views.invite, name='invite'),
    path('yes/<int:inv_id>', mainapp.views.yes, name='yes'),
    path('no/', mainapp.views.no, name='no'),
    path('home/', mainapp.views.home, name='home'),
    path('logout/', mainapp.views.logout, name='logout'),
    path('group/<int:group_id>',mainapp.views.group, name='group'),
    path('group/<int:group_id>/new',mainapp.views.newSchedule, name='newSche'),
    path('group/<int:group_id>/create', mainapp.views.create , name='create'),
    path('delete/', mainapp.views.delete, name='delete'),
    path('map/', mainapp.views.map, name='map'),
    path('search/', mainapp.views.search, name='search'),
    path('confirm/<int:first_id>', mainapp.views.confirm, name='confirm'),
    path('scheDelete/<int:first_id>', mainapp.views.scheDelete, name='scheDelete'),
    path('home/charge/<int:user_id>', mainapp.views.charge , name='charge'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

