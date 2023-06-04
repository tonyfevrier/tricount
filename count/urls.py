from django.contrib import admin
from django.urls import path
from count import views as countviews

urlpatterns = [
    path('',countviews.listecount,name = 'listecount'),
    path('newcount',countviews.newcount, name = 'newcount'),
]