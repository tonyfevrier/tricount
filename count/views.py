from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def listecount(request): 
    return render(request,'index.html')

def newcount(request):
    return render(request, 'newcount.html')