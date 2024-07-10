from django.test import TestCase
from bs4 import BeautifulSoup 

class UnitaryTestMethods(TestCase):
    """
    Class of methods used in server tests
    """
    def extract_and_click_on_link(self,content,id):
        """
        Function to extract a link from a html content and click on it. The link is identified by its id.

        Inputs : 
            - content : the html content
            - id (str) : id identifying the html link <a>.

        Output : 
            - link : result of clicking on the link
        """
        soup = BeautifulSoup(content,'html.parser')  
        link = soup.select_one(f'a#{id}')['href'] #on clique sur le + : sorte de send_keys 
        return link
    
    def create_a_tricount(self,title,password,description, currency,category,*participants):  
        """
        Function to create a tricount.

        Inputs : 
            - title (str)
            - password (str)
            - description (str)
            - currency (str)
            - category (str)
            - participants (list[str])

        Output : 
            - response (object) : contains the characteristics of the response to the request post. 
        """  
        response = self.client.post("/count/Tony/newcount/addcount",
                                    data = {"newtricount_title":title, 
                                            "newtricount_pwd":password, 
                                            "newtricount_description":description, 
                                            "newtricount_currency" : currency, 
                                            "newtricount_category":category, 
                                            "nameparticipant": participants})
        
        return response
    
    def modify_a_tricount(self, idcount, title, description, *participants):
        """
        Function which modifies an existing tricount.

        Inputs : 
            - title (str) 
            - description (str) 
            - participants (list[str])
        
        Output : 
            - response (object) : contains the characteristics of the response to the request post. 
        """
        response = self.client.post(f"/count/Tony/tricount/{idcount}/modifycountregister", data = {'tricount_title' : title,
                                                                               'tricount_description' : description, 
                                                                               'nameparticipant' : participants})
        return response
    
    def clone_a_tricount(self, people, title, password):
        """
        Inputs : 
            - people (str) : who wants to clone the tricount.
            - title (str)
            - password (str)
        """
        self.client.post(f"/count/{people}/newcount/count-pwd", data = {"tricount-title":title, "password":password})

    def create_a_spending(self,title,amount,currency,spender, receivers, respective_amounts):
        """
        Inputs :
            - title (str) 
            - amount (float) : amount of the spending
            - spender (str) : who pays
            - receivers (list[str]) : people the spender pay for
            - respective_amounts (list[float]) : amount of each receiver paid by the spender

        Output : 
            - response (object) : contains the characteristics of the response to the request post. 
        """ 
        data = {'title': title, 'amount': amount, 'spender': spender,  'receiver': receivers, 'newtricount_currency':currency} 
        for i in range(len(receivers)):
            data[receivers[i]] = respective_amounts[i]

        response = self.client.post('/count/Tony/tricount/1/addspending', data)
        return response
    
    def modify_a_spending(self, idcount, idspending, title, amount, currency, spender, receivers, respective_amounts):
        """
        Function which modifies an existing spending.

        Inputs : 
            - title (str) 
            - amount (str) 
            - currency (str) 
            - spender (str) 
            - receivers (list[str])
            - respective_amounts (list[float]) : amount of each receiver paid by the spender

        Output : 
            - response (object) : contains the characteristics of the response to the request post. 
        """
        data = {'title': title, 'amount': amount, 'spender': spender,  'receiver': receivers, 'newtricount_currency':currency} 
        for i in range(len(receivers)):
            data[receivers[i]] = respective_amounts[i]

        response = self.client.post(f"/count/Tony/tricount/{idcount}/spending/{idspending}/modifyspendingregister", data)
        return response

    def register_someone(self, username, password, email):
        response = self.client.post('/welcome/register', data = {'username':username, 'password':password, 'email' : email})        
        return response
    
    def login_someone(self, username, password):
        response = self.client.post('/login/log', data = {'username':username, 'password':password}) 
        return response
    
    def logout_someone(self):
        response = self.client.post('/count/Tony/logout/delog')
        return response