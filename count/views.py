from django.shortcuts import render,redirect 
from django.contrib import messages
from django.contrib.auth.models import User, auth
from count.models import Counts, Spending
from count.utils import *
from count import calculation
from datetime import date
from count.calculation import *
import json, requests

def welcome(request):  
    return render(request, "welcome.html")

def login(request): 
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
        return redirect('/welcome/')
    elif User.objects.filter(email = email).exists(): 
        messages.info(request, 'This email already exists')
        return redirect('/welcome/')
    else:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.save()
        return redirect('/login/')

def log(request):
    """
    Function logging the user and redirecting to the list of counts page of the corresponding user. 
    """ 

    username = request.POST["username"]
    password = request.POST["password"]

    user = auth.authenticate(username = username, password = password) 
    if user is not None:
        auth.login(request,user)
        return redirect(f'/count/{username}') #l'adresse devra être spécifique à l'utilisateur.
    else:
        return redirect('/login/')

def logout(request,user):
    """
    Function to go to the logout page containing the parameters.
    """
    userObject = User.objects.get(username = user)
    return render(request, "logout.html",context = {'userobject':userObject})

def delog(request,user):
    """
    Function which is delogging the user
    """
    auth.logout(request)
    return redirect('/welcome/')

def listecount(request, user): 
    items = Counts.objects.all() 
    return render(request,'index.html',context ={'counts' : items, 'user' : user})

def newcount(request,user):  
    currency = "EUR" 
    return render(request, 'newcount.html',context={'user':user, 'currency': currency})
    

def addcount(request,user):
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
            count = Counts.objects.create(title = majuscule(titre), description = phrase, currency = request.POST["newtricount_currency"], category = request.POST["newtricount_category"], participants = participts, data = tricount.to_json())
            return redirect(f'/count/{user}/tricount/'+ str(count.id))
    else:  
        return render(request,'newcount.html', context={'titre':False})

def choosecurrency(request,user):
    """
    Function which leads to the choice of the payment currency
    """  
    file = open('static/json/currency.json','r')
    currencies = json.load(file) 
    file.close() 
    return render(request, 'currency.html', context = {'currencies' : currencies, 'user':user})

def spending(request,user ,id_count):
    """
    Function which leads to the spending of a given tricount.
    """
    count = Counts.objects.get(id=id_count)  
    participants = count.participants 
    spending = Spending.objects.filter(number = id_count)

    tricount = Tricount.from_json(count.data) 
    total_credit_owner = tricount.calculate_total_credit()[user] 
    total_cost = tricount.total_cost 

    rate = useAPICurrency("GBP", "EUR")
    total_cost_in_pound = rate * float(total_cost)
    print(total_cost, rate, total_cost_in_pound)

    context = {
        'user':user,
        'count':count,
        'names':participants,
        'spending' : spending,
        'credit_owner' : total_credit_owner,
        'totalcost' : total_cost,
        'totalpound' : total_cost_in_pound,
    }
    return render(request, "spending.html", context = context)

def spendingEquilibria(request,user ,id_count):
    """
    Function which leads to the equilibria of a given tricount.
    """
    count = Counts.objects.get(id=id_count)  

    #Deserialisation and calculation of ways to go the equilibrium
    tricount = Tricount.from_json(count.data)
    total_credit,transfert_to_equilibrium = tricount.calculate_total_credit_and_resolve_solution() 
    return render(request, "spendingEquilibria.html", context = {'user':user,'count':count,'total_credit' : total_credit,'transfert_to_equilibrium' : transfert_to_equilibrium})

def newspending(request,user ,id_count):
    """
    Function which render the template when we want to add a new spending
    """
    count = Counts.objects.get(id = id_count)
    participants = count.participants
    currency = count.currency
    return render(request, 'newspending.html',context={'user':user,'idcount': id_count, 'participants':participants, 'currency': currency})

def addspending(request,user ,id_count):
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
        
        return redirect(f'/count/{user}/tricount/{id_count}')
    else: #Lack of title needs an error message.
        count = Counts.objects.get(id = id_count)
        participants = count.participants
        return render(request, 'newspending.html',context={'idcount': id_count, 'participants':participants,'titre':False})
        
def spending_details(request,user , id_count, id_spending):
    """
    Function to see the details of a given spending
    """
    spending = Spending.objects.get(id = id_spending)
    number_of_spending = Spending.objects.count()
    context = {'user':user,'idcount' : id_count, 'idspending' : id_spending,'previousidspending' : id_spending - 1 , 'followingidspending' : id_spending + 1,'spending': spending, 'number_of_spending' : number_of_spending}
    return render(request,"spending-details.html",context)

def chat(request, user,id_count):
    """
    Function to go to the chat view
    """
    return render(request,'chat.html')