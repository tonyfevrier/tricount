from count.models import Counts
from count.calculation import Tricount
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
    



    