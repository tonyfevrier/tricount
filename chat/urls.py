from django.contrib import admin
from django.urls import path
from chat import views as chatviews

urlpatterns = [
    path('chat/<int:id_count>', chatviews.chat, name = "chat"),  
]