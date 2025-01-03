"""
URL configuration for tricount project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include 
from count import urls as count_urls
from chat import urls as chat_urls
from count import views as countviews
from chat import views as chatviews

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include(count_urls)),  
    path('', include(chat_urls)),  
]
