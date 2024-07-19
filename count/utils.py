from count.models import Counts
from count.calculation import Participant, Tricount
import requests

def majuscule(chaine):
    """
    Function which puts the first letter in majuscule
    """
    return chaine[0].upper() + chaine[1:]

def update_tricount_after_new_spending(id_count, spender, dico_receivers):
    """
    Fonction qui permet de modifier les crédits de chacun dans le tricount après une dépense puis d'enregistrer dans la bdd

    Inputs : 
        id_count (int) : number of tricount
        spender (dict) : {payer (str): amount(float)}
        dico_receivers (dict) : keys are participants and values are the amount they have to reimburse to the payer.  
    """

    count = Counts.objects.get(id = id_count)
    tricount = Tricount.from_json(count.data)
    tricount.spending_update(spender, dico_receivers)
    count.data = tricount.to_json()
    count.save()

def update_tricount_after_new_receiving(id_count, receiver, dico_payers):
    """
    Fonction qui permet de modifier les crédits de chacun dans le tricount après une dépense puis d'enregistrer dans la bdd

    Inputs : 
        id_count (int) : number of tricount
        spender (dict) : {payer (str): amount(float)}
        dico_receivers (dict) : keys are participants and values are the amount they have to reimburse to the payer.  
    """

    count = Counts.objects.get(id = id_count)
    tricount = Tricount.from_json(count.data)
    tricount.receiving_update(receiver, dico_payers)
    count.data = tricount.to_json()
    count.save()

def add_new_participants_to_a_tricount(count,participants):  
    """
    Function which checks if there are new participants in participants and creates an object Participant and add it for future credits calculations.

    Inputs : 
        - count (object): an instanciation of the class Counts (models).
        - participants (list) : a list of participants.

    Output : 
        - count : updated.
    """
    tricount = Tricount.from_json(count.data) 
    for participant in participants:
        if participant not in count.participants:
            receivers = [receiver for receiver in count.participants if receiver != participant]
            tricount.dict_participants[participant] = Participant(participant,receivers)
            for receiver in receivers:
                tricount.dict_participants[receiver].credits[participant] = 0
    count.participants = participants
    count.data = tricount.to_json()
    return count

def useAPICurrency(currency_to, currency_from):
    """
    Fonction qui donne le taux de change d'une monnaie à une autre.

    Inputs : 
        -currency_to (str): monnaie dont veut le taux pour 1 unité de la monnaie convertie. 
        -currency_from (str): monnaie qu'on veut convertir.
    
    Output : 
        - response.json() (str) : le taux de change. 
    """
    """
    url = "https://exchange-rate-api1.p.rapidapi.com/latest"

    querystring = {"base":currency_from}

    headers = {
	    "x-rapidapi-key": "260ce107f1msh4a1b88e31999632p116730jsnec29696c42e6",
	    "x-rapidapi-host": "exchange-rate-api1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring) 
    
    return response.json()['rates'][currency_to]
    """

    url = "https://api.freecurrencyapi.com/v1/latest"
    
    headers = {
        "apikey" : "fca_live_WBlOtjh3ldI46OSl1jGUzQQFXzz7XvkO1G8dreQl",
    }
    querystring = {"base_currency":currency_from, "currencies":[currency_to]}

    response = requests.get(url, headers=headers, params= querystring)
 
    return response.json()["data"][currency_to]

def convertSpendingCurrency(currency_to, currency_from, amount):
    """
    Function converting an amount in an other currency

    Inputs:
        - currency_to (str): the currency in which to convert.
        - currency_from (str) : the initial currency
        - amount (float)

    Output :
        -amount converted.
    """
    rate = float(useAPICurrency(currency_to, currency_from))
    amount = rate*float(amount)
    return amount

def createReceiversDictionaryOfASpending(newcurrency, tricount_currency, request, *participants):
    """
    Function which creates the dictionnary containing the amount of each participant to a spending.

    Inputs : 
        - newcurrency (str) : the currency entered for the spending.
        - tricount_currency (str) : the currency registered when the tricount was created.
        - request (obj) 
        - participants (list[str]) : list containing the receivers of the spending.
    Output : 
        - dico_receivers (dictionary) : keys are participants to the spending, values are their amount.  

    """
    dico_receivers = {}
    for receiver in participants: 
        if newcurrency == tricount_currency:  
            dico_receivers[receiver] = float(request.POST[receiver])
        else: #Convert the amounts of receivers in the tricount currency
            dico_receivers[receiver] = convertSpendingCurrency(tricount_currency,newcurrency,request.POST[receiver])
    return dico_receivers

    



    