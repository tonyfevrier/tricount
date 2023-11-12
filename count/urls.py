from django.contrib import admin
from django.urls import path
from count import views as countviews

urlpatterns = [
    path('',countviews.listecount,name = 'listecount'),
    path('logout',countviews.logout,name = 'logout'),
    path('newcount',countviews.newcount, name = 'newcount'),
    path('newcount/addcount', countviews.addcount, name = 'addcount'), 
    path('newcount/currency',countviews.choosecurrency,name = "choosecurrency"),
    path('tricount/<int:id_count>', countviews.spending, name = "spending"), 
    path('tricount/<int:id_count>/equilibria', countviews.spendingEquilibria, name = "spending-equilibria"), 
    path('tricount/<int:id_count>/spending', countviews.newspending,name = "newspending"),
    path('tricount/<int:id_count>/addspending', countviews.addspending,name = "addspending"),
    path('tricount/<int:id_count>/spending/<int:id_spending>', countviews.spending_details, name = "spending-details"),
]