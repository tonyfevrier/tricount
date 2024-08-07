from django.contrib import admin
from django.urls import path
from count import views as countviews

urlpatterns = [
    path('<str:user>',countviews.listecount,name = 'listecount'),
    path('<str:user>/logout',countviews.logout,name = 'logout'),
    path('<str:user>/logout/delog',countviews.delog,name = 'delog'),
    path('<str:user>/newcount/count-pwd',countviews.clonecount, name = 'count-pwd'),
    path('<str:user>/newcount',countviews.newcount, name = 'newcount'),
    path('<str:user>/newcount/addcount', countviews.addcount, name = 'addcount'), 
    path('<str:user>/newcount/currency',countviews.choosecurrency,name = "choosecurrency"),
    path('<str:user>/tricount/<int:id_count>', countviews.spending, name = "spending"), 
    path('<str:user>/tricount/<int:id_count>/modifycount', countviews.modifycount, name = "modifycount"),
    path('<str:user>/tricount/<int:id_count>/modifycountregister', countviews.modifycountregister, name = "modifycountregister"),
    path('<str:user>/tricount/<int:id_count>/deletecount', countviews.deletecount, name = "deletecount"),
    path('<str:user>/tricount/<int:id_count>/chat', countviews.chat, name = "chat"), 
    path('<str:user>/tricount/<int:id_count>/equilibria', countviews.spendingEquilibria, name = "spending-equilibria"), 
    path('<str:user>/tricount/<int:id_count>/spending', countviews.newspending,name = "newspending"),
    path('<str:user>/tricount/<int:id_count>/addspending', countviews.addspending,name = "addspending"),
    path('<str:user>/tricount/<int:id_count>/spending/<int:id_spending>/modifyspending', countviews.modifyspending,name = "modifyspending"),
    path('<str:user>/tricount/<int:id_count>/spending/<int:id_spending>/modifyspendingregister', countviews.modifyspendingregister,name = "modifyspendingregister"),
    path('<str:user>/tricount/<int:id_count>/spending/<int:id_spending>/deletespending', countviews.deletespending, name = "deletespending"),
    path('<str:user>/tricount/<int:id_count>/spending/<int:id_spending>', countviews.spending_details, name = "spending-details"),
]