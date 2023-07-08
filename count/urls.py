from django.contrib import admin
from django.urls import path
from count import views as countviews

urlpatterns = [
    path('',countviews.listecount,name = 'listecount'),
    path('newcount',countviews.newcount, name = 'newcount'),
    path('newcount/addcount', countviews.addcount, name = 'addcount'),
    path('newcount/addcount/addparticipant',countviews.addparticipant, name = "addparticipant"),
    path('newcount/currency',countviews.choosecurrency,name = "choosecurrency"),
]