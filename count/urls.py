from django.contrib import admin
from django.urls import path
from count import views as countviews

urlpatterns = [
    path('', countviews.welcome, name = 'welcome'),
    path('register', countviews.register, name = 'register'),
    path('login', countviews.login, name = 'login'),
    path('log', countviews.log, name = 'log'),
    path('logout',countviews.logout,name = 'logout'),
    path('delog',countviews.delog,name = 'delog'),
    path('count',countviews.listecount,name = 'listecount'),
    path('clonecount',countviews.clonecount, name = 'clonecount'),
    path('newcount',countviews.newcount, name = 'newcount'),
    path('addcount', countviews.addcount, name = 'addcount'), 
    path('choosecurrency',countviews.choosecurrency,name = "choosecurrency"),
    path('tricount/<int:id_count>', countviews.spending, name = "spending"), 
    path('modifycount/<int:id_count>', countviews.modifycount, name = "modifycount"),
    path('modifycountregister/<int:id_count>', countviews.modifycountregister, name = "modifycountregister"),
    path('deletecount/<int:id_count>', countviews.deletecount, name = "deletecount"),
    path('chat/<int:id_count>', countviews.chat, name = "chat"), 
    path('equilibria/<int:id_count>', countviews.spendingEquilibria, name = "equilibria"), 
    path('newspending/<int:id_count>', countviews.newspending,name = "newspending"),
    path('addspending/<int:id_count>', countviews.addspending,name = "addspending"),
    path('modifyspending/<int:id_count>/<int:id_spending>', countviews.modifyspending,name = "modifyspending"),
    path('modifyspendingregister/<int:id_count>/<int:id_spending>', countviews.modifyspendingregister,name = "modifyspendingregister"),
    path('deletespending/<int:id_count>/<int:id_spending>', countviews.deletespending, name = "deletespending"),
    path('spending-details/<int:id_count>/<int:id_spending>', countviews.spending_details, name = "spending-details"),
]