from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.models import Chat
from count.models import Counts

@login_required
def chat(request, id_count):
    """
    Function to go to the chat view
    """
    # Create a dictionary sorting messages by date
    messages = Chat.objects.filter(tricountid=id_count) 
    dates = [chat.date for chat in messages]
    date_messages = {}
    for date in dates: 
        date_messages[date.strftime("%b %d %Y")] = messages.filter(date=date)

    return render(request,'chat.html',context={'id':id_count,
                                               'user': request.user.username,
                                               'date_messages': date_messages}) 