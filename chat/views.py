from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import Chat
from count.models import Counts

@login_required
def chat(request, id_count):
    """
    Function to go to the chat view
    """
    messages = Chat.objects.filter(tricount_id=id_count) 

    return render(request,'chat.html',context={'id':id_count,
                                               'user': request.user.username,
                                               'messages': [message.serialize() for message in messages]})