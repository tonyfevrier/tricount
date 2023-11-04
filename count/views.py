from django.shortcuts import render,redirect
from django.http import HttpResponse
from count.models import Counts, Spending
from count.func import *
from count import calculation
from datetime import date
from count.calculation import *

# Create your views here.

def listecount(request):    
    items = Counts.objects.all() 
    return render(request,'index.html',context ={'counts' : items})

def newcount(request): 
    return render(request, 'newcount.html')

def addcount(request):
    """
    Fonction qui permet d'ajouter un nouveau tricount. S'il n'y a pas de titre, elle renvoie à la même page html.
    """ 

    titre = request.POST["newtricount_title"]
    descption = request.POST["newtricount_description"]
    participts = request.POST.getlist('nameparticipant')

    if titre != "": 
        if len(participts) <= 1:
            #No participants have been added.
            return render(request,'newcount.html', context={'ptcpt':False})
        else:
            if descption != "": 
                phrase = majuscule(descption)
            else:
                phrase = "Pas de description" 
            #Creation of the object for calculations
            tricount = Tricount(*participts)
            count = Counts.objects.create(title = majuscule(titre), description = phrase,category = request.POST["newtricount_category"], participants = participts, data = tricount.to_json())
            return redirect('/count/tricount/'+ str(count.id))
    else:  
        return render(request,'newcount.html', context={'titre':False})

def choosecurrency(request):
    """
    Function which leads to the choice of the payment currency
    """
    return render(request, 'currency.html')

def spending(request,id_count):
    """
    Function which leads to the spending of a given tricount.
    """
    count = Counts.objects.get(id=id_count)  
    participants = count.participants 
    spending = Spending.objects.filter(number = id_count)
    return render(request, "spending.html", context = {'count':count,'names':participants, 'spending' : spending})

def spendingEquilibria(request,id_count):
    """
    Function which leads to the equilibria of a given tricount.
    """
    count = Counts.objects.get(id=id_count)  
    participants = count.participants
    return render(request, "spendingEquilibria.html", context = {'count':count,'names':participants})

def newspending(request,id_count):
    """
    Function which render the template when we want to add a new spending
    """
    count = Counts.objects.get(id = id_count)
    participants = count.participants
    return render(request, 'newspending.html',context={'idcount': id_count, 'participants':participants})

def addspending(request,id_count):
    """
    Function to recover the data of the form of newspending and redirect to the spending list. 
    """ 

    titre =  request.POST["title"]
    amount = request.POST["amount"] 

    if titre != '':
        if amount == '':
            amount = 0.
        
        receivers = request.POST.getlist("receiver")
        spender = request.POST["spender"]

        #On récupère aussi les montants des personnes cochées pour les mettre dans un dictionnaire passé à la bdd.
        dico_receivers = {}
        for receiver in receivers: 
            dico_receivers[receiver] = float(request.POST[receiver]) 
        
        Spending.objects.create(title = titre, amount = float(amount) , payer = spender , receivers = dico_receivers, number = id_count, date = date.today())
        update_tricount_after_new_spending(id_count, {spender : float(amount)}, dico_receivers)
        
        return redirect(f'/count/tricount/{id_count}')
    else: #Lack of title needs an error message.
        count = Counts.objects.get(id = id_count)
        participants = count.participants
        return render(request, 'newspending.html',context={'idcount': id_count, 'participants':participants,'titre':False})
        
def spending_details(request, id_count, id_spending):
    """
    Function to see the details of a given spending
    """
    spending = Spending.objects.get(id = id_spending)
    number_of_spending = Spending.objects.count()
    context = {'idcount' : id_count, 'idspending' : id_spending,'previousidspending' : id_spending - 1 , 'followingidspending' : id_spending + 1,'spending': spending, 'number_of_spending' : number_of_spending}
    return render(request,"spending-details.html",context)
    

