from django.test import TestCase
from bs4 import BeautifulSoup 

class UnitaryTestMethods(TestCase):
    def extract_and_click_on_link(self,content,id):
        """
        Function to extract a link from a html content and click on it. The link is identified by its id.

        content : the html content
        id : str
        """
        soup = BeautifulSoup(content,'html.parser')
        link = soup.select_one(f'a#{id}')['href'] #on clique sur le + : sorte de send_keys 
        return link
    
    def create_a_tricount(self,title,password,description, currency,category,*participants):  
        """
        Function to create a tricount.
        """  
        response = self.client.post("/count/Tony/newcount/addcount",data = {"newtricount_title":title, "newtricount_pwd":password, "newtricount_description":description, "newtricount_currency" : currency, "newtricount_category":category, "nameparticipant": participants})
        
        return response
    
    def create_a_spending(self,title,amount,spender, receivers, respective_amounts):
        """
        Inputs :
            title : str
            amount : float
            spender : str
            receivers : list of str

        Output : 
            response : object
        """ 
        data = {'title': title, 'amount': amount, 'spender': spender,  'receiver': receivers} 
        for i in range(len(receivers)):
            data[receivers[i]] = respective_amounts[i]

        response = self.client.post('/count/Tony/tricount/1/addspending', data)
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