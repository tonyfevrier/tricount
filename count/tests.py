from django.test import TestCase
from django.urls import resolve
from django.contrib.auth.models import User
from count.views import listecount 
from count.models import Counts, Spending
from count.calculation import Tricount 
from copy import deepcopy
from count.tests_functions import UnitaryTestMethods
from datetime import date
import json
from bs4 import BeautifulSoup 


# Create your tests here.

class resolveUrl(TestCase):
    
    def test_resolve(self):
        """
        Test if an url is associated with the good view function.
        """
        found = resolve('/count/Toto')

        self.assertEqual(found.func,listecount) 

class HomepageTest(UnitaryTestMethods):
    """
    Class of methods to test registering and logging in the application
    """
    def test_title(self):
        """
        Test if the title appears in the page.
        """
        response = self.client.get('/count/Tony') 

        self.assertIn(b'Tricount',response.content)
        self.assertTemplateUsed(response,'index.html')

    def test_registering_bdd(self):
        """
        Test that the registration of a user works and works only if the username and the password do
        not already exist.
        """
        #We create a user
        response = self.register_someone('Tony','pwd','tony.fevrier62@gmail.com')
        
        self.assertEqual(User.objects.all().count(),1)
        self.assertRedirects(response, '/login/')

        #We tries to create a user with the same username and email.
        response = self.register_someone('Tony','pwd', 'tony.fevrier@gmail.com')
        response = self.register_someone('Dulcinée', 'pwd','tony.fevrier62@gmail.com')

        self.assertEqual(User.objects.all().count(),1)
        self.assertRedirects(response, '/welcome/')


    def test_login(self):
        """
        Test that the authentification has been doned if password and username are correct,
        refused otherwise
        """
       
        response = self.register_someone('Tony','pwd','tony.fevrier62@gmail.com')
        response = self.login_someone('Tony','pwd2') 
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)
        
        response = self.login_someone('Tonton','pwd') 
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

        response = self.login_someone('Tony','pwd') 
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)

    def test_logout(self):
        """
        Test that the logout is correctly done
        """
        response = self.register_someone('Tony','pwd','tony.fevrier62@gmail.com')
        response = self.login_someone('Tony','pwd') 
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)

        response = self.logout_someone()
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)


class NewcountTest(UnitaryTestMethods):
    """
    Class of methods to test the creation of some tricounts
    """
    def test_newcount(self):
        """
        Test that when we click on "create a tricount", the good template is used.
        """ 
        response = self.client.get('/count/Tony')
        link = self.extract_and_click_on_link(response.content , 'countfromzero')
        response2 = self.client.get(link)

        self.assertTemplateUsed(response2, 'newcount.html') 


    def test_newcount_inputs(self):
        """
        Test that data from tricount creation are correctly registered and that the redirection to the list of tricounts works properly.
        """ 
        response = self.create_a_tricount("tricount 1","password","description 1","EUR","Voyage",'Tony','Jean','Henri')
        count = Counts.objects.first()

        self.assertEqual("Tricount 1",count.title)
        self.assertEqual("password", count.password)
        self.assertEqual("Description 1", count.description)
        self.assertEqual("Voyage", count.category)
        self.assertEqual("EUR", count.currency)
        self.assertRedirects(response, '/count/Tony/tricount/1')  

    def test_lack_title_newcountinputs(self):
        """
        Test that if the title of the tricount is forgotten, the database does not change
        """    
        one = Counts.objects.count()
        response = self.create_a_tricount("","password","description 1","EUR","Voyage",'Jean') 
        two = Counts.objects.count() 

        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response,"Le titre doit comporter au moins un caractère.")

    def test_lack_password(self):
        """
        Test that if the password of the tricount is forgotten, the database does not change
        """
        one = Counts.objects.count()
        response = self.create_a_tricount("title","","description 1","EUR","Voyage",'Jean')
        two = Counts.objects.count()
        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response, "Il faut un mot de passe")



    def test_lack_participant_newcountinputs(self):
        """
        Test that if the participants of the tricount are forgotten, the database does not change
        """    
        one = Counts.objects.count()
        response = self.create_a_tricount("Tricount sans participant","pwd", "description 1","EUR", "Voyage")
        two = Counts.objects.count() 

        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response,"Il faut au moins un participant")


    def test_bdd_when_tricounts_created(self):
        """
        Test if after the creation of two tricounts, the data are associated with the good tricount. Data of different tricounts do not mix.
        """  
        self.create_a_tricount("tricount 1","pwd","description 1","EUR","Voyage","Jean","Henri")

        count = Counts.objects.first() 

        self.assertEqual('Jean', count.participants[0])
        self.assertEqual('Henri',count.participants[1]) 
        self.assertEqual(2,len(count.participants))
        self.assertIsNotNone(count.data)

        #Verification of the object Tricount after deserialization.
        data = json.loads(count.data) 

        self.assertListEqual(data['participants'], ['Jean', 'Henri'])
        self.assertEqual(data['total_cost'],0)  
        self.assertDictEqual(data['dict_participants']["Jean"], {'owner' : 'Jean', 'expense': 0, 'credits':{'Henri':0}, 'receivers' : ['Henri']})
        self.assertDictEqual(data['dict_participants']["Henri"], {'owner' : 'Henri', 'expense': 0, 'credits':{'Jean':0}, 'receivers' : ['Jean']})
                                          
        self.create_a_tricount("tricount 2","pwd","description 2","EUR","Voyage","Henri","Henriette","Tony")
        count2 = Counts.objects.get(pk=2) 
        self.assertEqual(3,len(count2.participants))

        self.assertNotIn('Jean', count2.participants)

    def test_click_on_count(self):
        """
        Function checking if we go on the good link after clicking on a tricount.
        """ 
        #We create two tricounts
        self.create_a_tricount("tricount 1", "pwd", "description 1","EUR", "Voyage", "Henri", "Jean")
        self.create_a_tricount("tricount 2", "pwd", "description 2","EUR", "Coloc", "Roberto",'Alfredo')
        
        #We go on the list of the tricounts
        response = self.client.get('/count/Tony') 
        link = self.extract_and_click_on_link(response.content , 'link-tricount-2')  

        self.assertEqual(link,'/count/Tony/tricount/2')

        link = self.extract_and_click_on_link(response.content , 'link-tricount-1')   

        self.assertEqual(link,'/count/Tony/tricount/1')

        #response = self.client.get(link)

        #self.assertIn(b'Henri',response.content)

    def test_currencies_passedto_currencyhtml(self):
        """
        Test if the currencies are printed in the currency page.
        """
        response = self.client.get('/count/Toto/newcount/currency')
        soup = BeautifulSoup(response.content,'html.parser')
 
        self.assertIn("EUR", str(soup))
        self.assertIn("Euro", str(soup))

        

class TestCalculator(TestCase):
    """
    Class of methods to test the calculation application (calculate equilibria, credits, debits)
    """

    def test_class_creation(self):
        """
        Test if credits data are well created.
        """
        participants = ['Tony', 'Marine', 'Henri', 'Yann']
        count = Tricount(*participants)
        
        self.assertEqual(len(count.dict_participants.keys()),4)  
        self.assertEqual(count.dict_participants['Tony'].credits,{'Marine':0, 'Henri':0, 'Yann':0})

    def test_nullity(self):
        """
        Test if for a spending of amount 0 nothing changes in the credits.
        """
        
        participants = ['Tony', 'Marine', 'Henri', 'Yann']
        count = Tricount(*participants)
        old_dict_participants = count.dict_participants
        count.spending_update({'Tony':0.}, {'Marine':0., 'Tony':0.})

        self.assertEqual(old_dict_participants,count.dict_participants) 
         
    def test_spending_update_first(self):
        """
        Test a spending between two participants from a group of four to verify that the credits calculated are correct and
        that the others credits are not modified.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_dict_participants = deepcopy(count.dict_participants)   
        count.spending_update({'Tony':100.}, {'Marine':50., 'Tony':50}) 

        #Change for Tony expense and for Tony and Marine credits but no changes for others.
        self.assertEqual(old_dict_participants['Tony'].expense + 100,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 50, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 50, count.dict_participants['Marine'].credits['Tony'])
        self.assertDictEqual(old_dict_participants['Yann'].credits, count.dict_participants['Yann'].credits)
        self.assertDictEqual(old_dict_participants['Henri'].credits, count.dict_participants['Henri'].credits)

    def test_spending_update_second(self):
        """
        Test a spending between all participants from a group of four to verify that the credits calculated are correct.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_total_cost = count.total_cost
        old_dict_participants = deepcopy(count.dict_participants)  
        count.spending_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})

        self.assertEqual(old_total_cost + 100,count.total_cost)
        self.assertEqual(old_dict_participants['Tony'].expense + 100,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 25, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 25, count.dict_participants['Marine'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Yann'] - 50, count.dict_participants['Tony'].credits['Yann'])
        self.assertEqual(old_dict_participants['Yann'].credits['Tony'] + 50, count.dict_participants['Yann'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Henri'] - 25, count.dict_participants['Tony'].credits['Henri'])
        self.assertEqual(old_dict_participants['Henri'].credits['Tony'] + 25, count.dict_participants['Henri'].credits['Tony'])
        
        for firstparticipant in ['Marine', 'Henri', 'Yann']: 
            self.assertEqual(old_dict_participants[firstparticipant].expense,count.dict_participants[firstparticipant].expense)
            for secondparticipant in ['Marine', 'Henri', 'Yann']:
                if secondparticipant != firstparticipant:
                    self.assertEqual(old_dict_participants[firstparticipant].credits[secondparticipant], count.dict_participants[firstparticipant].credits[secondparticipant])
                    self.assertEqual(old_dict_participants[secondparticipant].credits[firstparticipant], count.dict_participants[secondparticipant].credits[firstparticipant])
                
    def test_receiving_update(self):
        """
        Test a money input between all participants from a group of four to verify that the credits calculated are correct.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_dict_participants = deepcopy(count.dict_participants)  
        count.receiving_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})

        self.assertEqual(old_dict_participants['Tony'].expense - 100,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] + 25, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] - 25, count.dict_participants['Marine'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Yann'] + 50, count.dict_participants['Tony'].credits['Yann'])
        self.assertEqual(old_dict_participants['Yann'].credits['Tony'] - 50, count.dict_participants['Yann'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Henri'] + 25, count.dict_participants['Tony'].credits['Henri'])
        self.assertEqual(old_dict_participants['Henri'].credits['Tony'] - 25, count.dict_participants['Henri'].credits['Tony'])
        
        for firstparticipant in ['Marine', 'Henri', 'Yann']: 
            self.assertEqual(old_dict_participants[firstparticipant].expense,count.dict_participants[firstparticipant].expense)
            for secondparticipant in ['Marine', 'Henri', 'Yann']:
                if secondparticipant != firstparticipant:
                    self.assertEqual(old_dict_participants[firstparticipant].credits[secondparticipant], count.dict_participants[firstparticipant].credits[secondparticipant])
                    self.assertEqual(old_dict_participants[secondparticipant].credits[firstparticipant], count.dict_participants[secondparticipant].credits[firstparticipant])
       
    def test_calculate_total_credit(self):
        """
        Test if the total credit of each participant is correct after spendings.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann') 
        count.spending_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})
        count.spending_update({'Marine':200.}, {'Marine':150., 'Tony':50})
        count.spending_update({'Henri':150.}, {'Marine':25., 'Yann':50, 'Tony':25,'Henri':50})
        
        total_credit = count.calculate_total_credit()

        self.assertEqual(total_credit['Tony'], 25)
        self.assertEqual(total_credit['Marine'], 0)
        self.assertEqual(total_credit['Yann'],-100)
        self.assertEqual(total_credit['Henri'],75)

    def test_resolve_solution(self):
        """
        Test the correctness of the computation of amounts to reach the equilibrium between participants after some spendings.
        """

        count = Tricount('Tony', 'Marine', 'Henri', 'Yann') 
        count.spending_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})
        count.spending_update({'Marine':200.}, {'Marine':150., 'Tony':50})
        count.spending_update({'Henri':150.}, {'Marine':25., 'Yann':50, 'Tony':25,'Henri':50})
        count.spending_update({'Yann':180.}, {'Marine':50., 'Yann':50, 'Tony':50,'Henri':30})
        
        total_credit = count.calculate_total_credit()
        transfert_to_equilibrium = count.resolve_solution(total_credit)

        self.assertEqual(sum(transfert_to_equilibrium['Tony'].values()),25)
        self.assertEqual(sum(transfert_to_equilibrium['Marine'].values()),50)

    def test_moneytransfer(self):
        """
        Test a money transfer between two participants from a group of four to verify that the credits calculated are correct.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_total_cost = count.total_cost
        old_dict_participants = deepcopy(count.dict_participants)   
        count.money_transfer({'Tony':100.}, {'Marine':100.}) 

        #Change for Tony expense and for Tony and Marine credits but no changes for others.
        self.assertEqual(old_total_cost,count.total_cost)
        self.assertEqual(old_dict_participants['Tony'].expense,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 100, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 100, count.dict_participants['Marine'].credits['Tony'])
        self.assertDictEqual(old_dict_participants['Yann'].credits, count.dict_participants['Yann'].credits)
        self.assertDictEqual(old_dict_participants['Henri'].credits, count.dict_participants['Henri'].credits)

class TestSpending(UnitaryTestMethods):
    """
    Class of methods to test the effect of new spendings in a given tricount.
    """

    def test_redirect_after_newspending_inputs(self):
        """
        Test if after a new spending, the redirection is correct.
        """ 
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Tony", "Henri", "Jean")
        response = self.create_a_spending('dépense1', 100, 'Jean', ['Henri','Jean','Tony'], [50,50,0])  

        self.assertRedirects(response,'/count/Tony/tricount/1') 
    
    def test_bdd_newspending_inputs(self):
        """
        Test if after new spending inputs, data are correctly registrated in the database. 
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Jean")

        number = Spending.objects.count()
        self.create_a_spending('dépense1', 100, 'Jean', ['Henri','Jean'], [50,50])  
        spending = Spending.objects.get(pk = 1)
        
        self.assertEqual(number+1, Spending.objects.count())
        self.assertEqual(spending.title, 'dépense1')
        self.assertEqual(spending.amount, 100)
        self.assertEqual(spending.payer, 'Jean')
        self.assertDictEqual(spending.receivers, {'Henri':50,'Jean':50})
        self.assertEqual(spending.number, 1)
        self.assertEqual(spending.date, date.today())
    
    def test_goback_bdd_unchanged(self):
        """
        Test if when we don't complete entirely a spending, no new spending appear in the database.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann")
        response = self.client.get('/count/Tony/tricount/1/spending') 
        nb_spending = Spending.objects.count()
        self.extract_and_click_on_link(response.content , 'backtospending')  

        self.assertEqual(nb_spending,Spending.objects.count()) 

    def test_notitle_bdd_unchanged(self):
        """
        Test if when we create a spending and forget the title, no new spending appear in the database.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Jean")     
        nb_spending = Spending.objects.count()
        response = self.create_a_spending('', 100, 'Jean', ['Henri','Jean'],[50,50])   
        
        self.assertEqual(nb_spending,Spending.objects.count()) 
        self.assertTemplateUsed(response,'newspending.html')
        
    def test_noamount_nullspending(self):
        """
        Test if when we create a spending with no amount, a new spending must appear in the database with amount 0.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Jean")
        nb_spending = Spending.objects.count()
        self.create_a_spending('dépense1', '', 'Jean', ['Henri','Jean'],[0,0])  
        spending = Spending.objects.get(pk = 1)

        self.assertEqual(nb_spending + 1,Spending.objects.count()) 
        self.assertEqual(spending.amount, 0)
 
    def test_multiple_spendings_gives_good_credits_in_bdd(self):
        """
        Test if when we create multiple spendings, the computation made by calculation.py are well transferred to the database.
        """

        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending('dépense1', 100, 'Tony', ['Henri','Yann','Marine','Tony'], [25,50,25,0]) 
        self.create_a_spending('dépense2', 200, 'Marine', ['Henri','Yann','Marine','Tony'], [0,0,150,50]) 
        self.create_a_spending('dépense3', 150, 'Henri', ['Henri','Yann','Marine','Tony'], [50,50,25,25]) 
        self.create_a_spending('dépense4', 180, 'Yann', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 

        #Deserialization of the bdd 
        data = Counts.objects.first().data
        count = Tricount.from_json(data)
 
        self.assertEqual(count.dict_participants["Tony"].expense, 100)
        self.assertEqual(count.dict_participants["Marine"].expense, 200)
        self.assertEqual(count.dict_participants["Henri"].expense, 150)
        self.assertEqual(count.dict_participants["Yann"].expense, 180)
        
        self.assertDictEqual(count.dict_participants["Tony"].credits, {'Marine': 25.0, 'Henri': 0, 'Yann': 0})
        self.assertEqual(count.dict_participants["Marine"].credits, {'Tony': -25.0, 'Henri': 25.0, 'Yann': 50.0})
        self.assertEqual(count.dict_participants["Henri"].credits, {'Tony': 0, 'Marine': -25.0, 'Yann': -20})
        self.assertEqual(count.dict_participants["Yann"].credits, {'Tony': 0, 'Marine': -50.0, 'Henri': 20})
       
 
    