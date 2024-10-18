from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat(request, id_count):
    """
    Function to go to the chat view
    """
    return render(request,'chat.html',context={'id':id_count})