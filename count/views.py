from django.shortcuts import render,redirect
from django.http import HttpResponse
from count.models import Counts, Participants
from count.func import majuscule

# Create your views here.

def listecount(request):    
    #If tricount is not created, participants created are deleted    
    if Participants.objects.last() != None:
        if Participants.objects.last().number != Counts.objects.count():
            Participants.objects.filter(number = Participants.objects.last().number).delete()

    items = Counts.objects.all() 
    return render(request,'index.html',context ={'counts' : items})

def newcount(request): 
    items = Participants.objects.filter(number = Counts.objects.count() + 1) 
    return render(request, 'newcount.html',context={'participants':items, 'number_participants': items.count()})

def addcount(request):
    """
    Fonction qui permet d'ajouter un nouveau tricount. S'il n'y a pas de titre, elle renvoie à la même page html.
    """
    titre = request.POST["newtricount_title"]
    descption = request.POST["newtricount_description"]
    participants = Participants.objects.all()
    if titre != "":
        if descption != "":
            count = Counts.objects.create(title = majuscule(titre), description = majuscule(descption),category = request.POST["newtricount_category"] )
        else:
            count = Counts.objects.create(title = majuscule(titre), description = "Pas de description",category = request.POST["newtricount_category"] )
        #We associate new participants to the tricount
        for participant in participants:
            if participant.number == Counts.objects.count() :
                count.participants.add(participant)
        return redirect('/count/')
    else: 
        return render(request,'newcount.html', context={'titre':False})
    
def addparticipant(request):
    """ 
    Fonction qui récupère les participants créés, les met en bdd puis rédirige vers la page du nouveau tricount.

    Je récupère les participts et les metsdans la bdd participts,
    Dans newcount, je le mets dans context pr les envoyer à la page.
    Dans addcount, je crée le tricount avec en argument la liste des participants (en ajoutant tous les participants de la bdd)
    Autre solution je peux associer un numéro à chaque participant et n'ajouter au tricount que ce numéro là.
    (Version +) Dans addcount, je supprime la classe si l'utilisateur retourne en arrière
    """

    #Creation of the participant assignated to a tricount number.
    Participants.objects.create(name = request.POST["new_participant"], number = Counts.objects.count() + 1)
    return redirect('/count/newcount')

def choosecurrency(request):
    """
    Function which leads to the choice of the payment currency
    """
    return render(request, 'currency.html')