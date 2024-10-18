from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from count.models import Counts, Spending
from count.utils import CurrencyConversion as CC, ModifyTricount as MT, String    
from count.calculation import *
import json

def welcome(request): 
    if request.user.is_authenticated:
        return redirect(reverse('listecount')) 
    return render(request, "welcome.html")

def log(request): 
    if request.user.is_authenticated:
        return redirect(reverse('listecount'))
    return render(request, "login.html")    

def register(request):
    """
    Function registering a new user and redirecting to the login page. It verifies 
    if the username and the email is not already used. 
    """ 
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"] 
 
    if User.objects.filter(username = username).exists():
        messages.info(request, 'This username already exists')
        return redirect(reverse('welcome'))
    elif User.objects.filter(email = email).exists(): 
        messages.info(request, 'This email already exists')
        return redirect(reverse('welcome'))
    else:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.save()
        auth.login(request,user)
        return redirect(reverse('listecount'))

def login(request):
    """
    Function logging the user and redirecting to the list of counts page of the corresponding user. 
    """ 

    username = request.POST["username"]
    password = request.POST["password"]
    
    user = auth.authenticate(username = username, password = password) 

    if user is not None:
        auth.login(request,user)
        return redirect(reverse('listecount'))  
    else:
        messages.info(request, 'Invalid credentials')
        return redirect(reverse('log'))


@login_required
def logout(request):
    """
    Function to go to the logout page containing the parameters.
    """ 
    userObject = User.objects.get(username = request.user.username)
    return render(request, "logout.html",context = {'userobject':userObject})

@login_required
def delog(request):
    """
    Function which is delogging the user
    """
    
    auth.logout(request)
    return redirect(reverse('log'))

@login_required
def listecount(request): 
    """
    Function rendering the list of tricounts of a single user.
    """ 
    counts = Counts.objects.all() 
    items = [] 
    #if not counts.exists():
    if len(counts) > 0:
        #We select only the counts whose the user is an admin.
        for item in counts: 
            if request.user.username in item.admins:
                items.append(item)
    return render(request,'index.html',context ={'counts' : items})


@login_required
def clonecount(request): 
    credentials = json.loads(request.body) 
    item = Counts.objects.filter(title = String.majuscule(credentials['title']), password = credentials["password"])  
    if len(item) > 0:    
        item[0].admins.append(request.user.username)
        item[0].save()
        return JsonResponse({'message': 'Le tricount vient d"être clôné'}, status=200)
    else:
        return JsonResponse({'message':'Les identifiants ne correspondent à aucun tricount'}, status=400)
    

@login_required
def newcount(request):
    """
    Function rendering the page of creation of a tricount
    """  
    currency = "EUR" 
    return render(request, 'newcount.html',context={'user':request.user.username, 'currency': currency})
    

@login_required
def addcount(request):
    """
    Function adding a new tricount. A tricount necessitates a title, a password, a description, some participants and a list of admins
    which increases when someone is cloning the tricount
    """  
    titre = request.POST["newtricount_title"]
    password = request.POST["newtricount_pwd"]
    descption = request.POST["newtricount_description"]
    participts = request.POST.getlist('formparticipant')
    admins = [request.user.username]

    if descption != "": 
        phrase = String.majuscule(descption)
    else:
        phrase = "Pas de description" 
    #Creation of the object for calculations
    tricount = Tricount(*participts)
    count = Counts.objects.create(title = String.majuscule(titre), 
                                  password = password, 
                                  description = phrase, 
                                  currency = request.POST["newtricount_currency"], 
                                  category = request.POST["newtricount_category"], 
                                  participants = participts, 
                                  data = tricount.to_json(),
                                  admins = admins) 
    return redirect(reverse('spending', args=[count.id])) 

@login_required    
def modifycount(request, id_count):
    """
    Function which leads to modify the properties of the tricount.
    """
    count = Counts.objects.get(id = id_count)

    return render(request, "modifycount.html", context={'count':count})

@login_required
def modifycountregister(request, id_count):
    """
    Function which modifies the tricount including the modifications of the user
    """   
    count = Counts.objects.get(id = id_count) 
    newtitle = request.POST['tricount_title'] 
    newdescription = request.POST['tricount_description'] 
    newparticipants = request.POST.getlist('nameparticipant') 
    count.title = newtitle
    count.description = newdescription 
    
    #si les participants ont changé, ajout des nouveaux participants pour les calculs de crédits/dettes
    if set(count.participants) != set(newparticipants):
        count = MT.add_new_participants_to_a_tricount(count,newparticipants)
    count.save() 
 
    return redirect(reverse('spending', args=[id_count]))

@login_required
def deletecount(request, id_count):
    """
    Function which deletes a tricount.
    """ 
    count = Counts.objects.get(id = id_count)
    count.delete()
    return redirect(reverse("listecount"))

@login_required
def choosecurrency(request):
    """
    Function which leads to the choice of the payment currency
    """   
    file = open('static/json/currency.json','r')
    currencies = json.load(file) 
    file.close() 
    return render(request, 'currency.html', context = {'currencies' : currencies, 'user':request.user.username})

@login_required
def spending(request, id_count):
    """
    Function which leads to the page of all spendings of a given tricount.
    """
    count = Counts.objects.get(id=id_count)  
    participants = count.participants 
    spendings = count.spendings.all()
    tricount = Tricount.from_json(count.data)  
    total_credit_owner = tricount.calculate_total_credit()[request.user.username]  
    total_cost = tricount.total_cost 

    rate = 0.84 #useAPICurrency("GBP", "EUR") 
    total_cost_in_pound = rate * float(total_cost) 

    context = {
        'count':count,
        'names':participants,
        'spending' : spendings,
        'credit_owner' : total_credit_owner,
        'totalcost' : total_cost,
        'totalpound' : total_cost_in_pound,
    }
    return render(request, "spending.html", context = context)

@login_required
def spendingEquilibria(request, id_count):
    """
    Function which leads to the page of the equilibria of a given tricount.
    """
    count = Counts.objects.get(id=id_count)  

    #Deserialisation and calculation of ways to go the equilibrium
    tricount = Tricount.from_json(count.data)
    total_credit,transfert_to_equilibrium = tricount.calculate_total_credit_and_resolve_solution() 
    return render(request, "spendingEquilibria.html", context = {'user':request.user.username,'count':count,'total_credit' : total_credit,'transfert_to_equilibrium' : transfert_to_equilibrium})

@login_required
def newspending(request, id_count):
    """
    Function which render the template when we want to add a new spending
    """
    count = Counts.objects.get(id = id_count)
    participants = count.participants
    currency = count.currency
    return render(request, 'newspending.html',context={'idcount': id_count, 'participants':participants, 'currency': currency})

@login_required
def addspending(request, id_count):
    """
    Function to create a new spending and redirecting to the list of tricounts. 
    """ 

    titre =  request.POST["title"]
    amount = request.POST["amount"]
    currency = request.POST["newtricount_currency"]
    receivers = request.POST.getlist("receiver")
    spender = request.POST["spender"]

    #Create the spending with form informations 
    if amount == '':
        amount = 0. 

    #Convert the amount in the tricount currency if necessary
    tricount_currency = Counts.objects.get(id = id_count).currency

    #On récupère aussi les montants des personnes cochées pour les mettre dans un dictionnaire passé à la bdd.

    if currency != tricount_currency:   
        amount = CC.convertSpendingCurrency(tricount_currency,currency,amount)
    
    dico_receivers = MT.createReceiversDictionaryOfASpending(currency, tricount_currency, request, *receivers)
    Spending.objects.create(title = titre, amount = float(amount) , payer = spender , receivers = dico_receivers, tricount = Counts.objects.get(id = id_count))
    MT.update_tricount_after_new_spending(id_count, {spender : float(amount)}, dico_receivers)
        
    return redirect(reverse('spending', args=[id_count]))

@login_required        
def spending_details(request, id_count, id_spending):
    """
    Function to render the page allowing to see the details of a given spending
    """ 
    spending = Spending.objects.get(id = id_spending, tricount = Counts.objects.get(id=id_count)) 
    number_of_spending = Spending.objects.count()
    context = {'idcount' : id_count, 
               'idspending' : id_spending,
               'previousidspending' : id_spending - 1, 
               'followingidspending' : id_spending + 1,
               'spending': spending, 
               'number_of_spending' : number_of_spending}
    return render(request,"spending-details.html",context)

@login_required
def modifyspending(request, id_count, id_spending):
    """
    Function which redirects to the page allowing to modify a given spending.
    """  
    count = Counts.objects.get(id = id_count)
    spending = Spending.objects.get(id = id_spending, tricount = Counts.objects.get(id=id_count)) 
    context = {'count': count, 'spending': spending, 'participants': count.participants}
    return render(request, "modifyspending.html", context = context)

@login_required
def modifyspendingregister(request, id_count, id_spending):
    """
    Function which recovers data obtained from the modification of a spending.
    """      
    count = Counts.objects.get(id = id_count)
    spending = Spending.objects.get(id = id_spending, tricount = Counts.objects.get(id=id_count)) 

    #We first delete the previous spending in the calculation by making the inverse spending : the spender is now a receiver.
    receiver = spending.payer
    payers = spending.receivers
    MT.update_tricount_after_new_receiving(id_count, {receiver : float(spending.amount)}, payers)

    #Then we change data of the spending in the database.
    newtitle = request.POST['title'] 
    newamount = request.POST['amount']
    newcurrency = request.POST['newtricount_currency']
    newspender = request.POST['spender']
    newparticipants = request.POST.getlist('receiver')
 
    spending.title = newtitle 
    spending.payer = newspender
    
    tricount_currency = count.currency 
    spending.receivers = MT.createReceiversDictionaryOfASpending(newcurrency, tricount_currency, request, *newparticipants)
 
    if newcurrency == tricount_currency:  
        spending.amount = newamount 
    else: 
        spending.amount = CC.convertSpendingCurrency(count.currency,newcurrency,newamount)
    
    #We update the calculations with the new spending.
    MT.update_tricount_after_new_spending(id_count, {newspender : float(newamount)}, spending.receivers)
    spending.save()  

    return redirect(reverse('spending-details', args=[id_count, id_spending]))

@login_required
def deletespending(request, id_count, id_spending):
    """
    Function which delete a spending
    """
    #on supprimer la dépense, on redirige vers la page des 
    spending = Spending.objects.get(tricount = Counts.objects.get(id=id_count), id = id_spending)
    spending.delete()
    return redirect(reverse('spending', args=[id_count]))


@login_required
def chat(request, id_count):
    """
    Function to go to the chat view
    """
    return render(request,'chat.html',context={'id':id_count})

