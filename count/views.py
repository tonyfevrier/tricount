from django.shortcuts import render,redirect
from django.http import HttpResponse
from count.models import Counts
from count.func import majuscule

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
    if titre != "":
        if descption != "":
            Counts.objects.create(title = majuscule(titre), description = majuscule(descption),category = request.POST["newtricount_category"] )
        else:
            Counts.objects.create(title = majuscule(titre), description = "Pas de description",category = request.POST["newtricount_category"] )
        return redirect('/count/')
    else: 
        return render(request,'newcount.html', context={'titre':False})