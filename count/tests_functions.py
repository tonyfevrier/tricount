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
    
    def add_participants(self,*participants):
        """
        participants : list of str
        """
        for participant in participants:
            self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":participant})

    def add_tricount_characteristics(self,title, description,category):
        response = self.client.post("/count/newcount/addcount",data = {"newtricount_title":title, "newtricount_description":description, "newtricount_category":category})
        return response
    
    def create_a_tricount(self,title,description,category,*participants):  
        self.add_participants(*participants)
        response = self.add_tricount_characteristics(title,description,category) 
        return response
    
    def create_a_spending(self,title,amount,spender, receivers):
        """
        Inputs :
            title : str
            amount : float
            spender : str
            receivers : list of str

        Output : 
            response : object
        """
        response = self.client.post('/count/tricount/1/addspending', data = {'title': title, 'amount': amount, 'spender': spender,  'receiver': receivers})
        return response

        
        