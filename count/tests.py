from django.test import TestCase
from django.urls import resolve
from django.contrib.auth.models import User
from count.views import listecount 
from count.models import Counts, Spending
from count.calculation import Tricount 
from copy import deepcopy
from count.methods_for_tests import UnitaryTestMethods
from datetime import date
import json
from bs4 import BeautifulSoup 
from count.utils import CurrencyConversion as CC 


class resolveUrl(TestCase):
    
    def test_resolve(self):
        """
        Test if an url is associated with the good view function.
        """
        found = resolve('/count')

        self.assertEqual(found.func,listecount) 

class HomepageTest(UnitaryTestMethods):
    """
    Class of methods to test registering and logging in the application
    """

    def test_title(self):
        """
        Test if the title appears in the page.
        """
        self.register_someone('Tony','pwd','tony.fevrier62@gmail.com')
        response = self.client.get('/count') 

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
        self.assertRedirects(response, '/count')
        self.logout_someone()

        #We tries to create a user with the same username and email.
        response = self.register_someone('Tony','pwd', 'tony.fevrier@gmail.com')
        response = self.register_someone('Dulcinée', 'pwd','tony.fevrier62@gmail.com')

        self.assertEqual(User.objects.all().count(),1)
        self.assertRedirects(response, '/')


    def test_login(self):
        """
        Test that the authentification has been doned if password and username are correct,
        refused otherwise
        """
        self.register_someone('Tony', '1234', 'tony@gmail.com')
        self.logout_someone()
        response = self.login_someone('Tony','pwd2') 
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)
        
        response = self.login_someone('Tonton','1234') 
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

        response = self.login_someone('Tony','1234') 
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

    def setUp(self):
        self.register_someone('Tony', '1234', 'tony@gmail.com')

    def test_newcount(self):
        """
        Test that when we click on "create a tricount", the good template is used.
        """ 
        response = self.client.get('/count')
        link = self.extract_and_click_on_link(response.content , 'countfromzero')
        response2 = self.client.get(link)

        self.assertTemplateUsed(response2, 'newcount.html') 

    def test_newcount_without_admin(self):
        """
        Create a tricount with participants who do not include the creator
        """
        self.create_a_tricount("tricount 1","password","description 1","USD","Voyage",'Jean','Henri')
        count = Counts.objects.first()
        self.assertEqual("Tricount 1",count.title)
        self.assertEqual("password", count.password)
        self.assertEqual("Description 1", count.description)
        self.assertEqual("Voyage", count.category)
        self.assertEqual("USD", count.currency)
        self.assertListEqual(count.participants, ['Jean','Henri'])

    def test_newcount_in_other_currency(self):
        """
        Function which creates a tricount in USD and verifies that the database has registered this currency.
        """
        self.create_a_tricount("tricount 1","password","description 1","USD","Voyage",'Tony','Jean','Henri')
        count = Counts.objects.first()

        self.assertEqual(count.currency, 'USD')

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
        self.assertRedirects(response, '/tricount/1')  


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
        response = self.client.get('/count') 
        link = self.extract_and_click_on_link(response.content , 'link-tricount-2')  

        self.assertEqual(link,'/tricount/2')

        link = self.extract_and_click_on_link(response.content , 'link-tricount-1')   

        self.assertEqual(link,'/tricount/1') 

    def test_currencies_passedto_currencyhtml(self):
        """
        Test if the currencies are printed in the currency page.
        """
        response = self.client.get('/choosecurrency')
        soup = BeautifulSoup(response.content,'html.parser')
 
        self.assertIn("EUR", str(soup))
        self.assertIn("Euro", str(soup))
 
    def test_clonecount(self):
        """
        Test if when a tricount is cloned the list of admins change
        """
        #Creation of a tricount by Tony
        self.create_a_tricount("tricount1",'pwd',"description","EUR","Voyage", "Henri", "Jean")
        
        admins = Counts.objects.first().admins
        self.assertListEqual(admins, ['Tony'])

        #Henri tries to clone the tricount
        self.register_someone('Henri', '1234', 'henri@gmail.com')
        response = self.clone_a_tricount("tricount1","pwd") 
        admins = Counts.objects.first().admins
        self.assertListEqual(admins, ['Tony','Henri'])
        self.assertEqual(response.status_code, 200)

        #Jean tries to clone but gives a wrong password and then gives a wrong title
        self.register_someone('Jean', '1234', 'Jean@gmail.com')
        response = self.clone_a_tricount("wrong","pwd") 
        admins = Counts.objects.first().admins
        self.assertListEqual(admins, ['Tony','Henri'])
        self.assertEqual(response.status_code, 400)

        response = self.clone_a_tricount("Tricount1","error")  
        admins = Counts.objects.first().admins
        self.assertListEqual(admins, ['Tony','Henri'])
        self.assertEqual(response.status_code, 400)

        #He gives the good password
        response = self.clone_a_tricount("Tricount1","pwd") 
        admins = Counts.objects.first().admins
        self.assertListEqual(admins, ['Tony','Henri','Jean'])
        self.assertEqual(response.status_code, 200)
        
    def test_modify_tricount(self):
        """
        Test if the modification of a tricount changes effectively the tricount in the database
        """
        #We create a tricount and then try to modify the tricount
        self.create_a_tricount("tricount1",'pwd',"description","EUR","Voyage", "Tony", "Henri", "Jean")
        response = self.modify_a_tricount(1,"tricount2", "Autre", "Tony", "Henri", "Jean", "Robert") 
        count = Counts.objects.first()

        self.assertEqual(count.title, "tricount2")
        self.assertEqual(count.description, "Autre")
        self.assertListEqual(count.participants, ["Tony", "Henri", "Jean", "Robert"])
        self.assertRedirects(response,'/tricount/1')

    def test_delete_tricount(self):
        """
        Test the deletion of a tricount : it must disappear from the database
        """
        self.create_a_tricount("tricount1",'pwd',"description","EUR","Voyage", "Tony", "Henri", "Jean") 
        self.client.get("/deletecount/1")
        count = Counts.objects.all()
        self.assertEqual(len(count), 0)


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
        self.assertEqual(old_total_cost, count.total_cost)
        self.assertEqual(old_dict_participants['Tony'].expense, count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 100, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 100, count.dict_participants['Marine'].credits['Tony'])
        self.assertDictEqual(old_dict_participants['Yann'].credits, count.dict_participants['Yann'].credits)
        self.assertDictEqual(old_dict_participants['Henri'].credits, count.dict_participants['Henri'].credits)


class TestSpending(UnitaryTestMethods):
    """
    Class of methods to test the effect of new spendings in a given tricount.
    """

    def setUp(self):
        self.register_someone('Tony', '1234', 'tony@gmail.com')

    def test_redirect_after_newspending_inputs(self):
        """
        Test if after a new spending, the redirection is correct.
        """ 
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Tony", "Henri", "Jean")
        response = self.create_a_spending(1,'dépense1', 100,'EUR', 'Tony', ['Henri','Jean','Tony'], [50,50,0])  

        self.assertRedirects(response,'/tricount/1') 
    
    def test_bdd_newspending_inputs(self):
        """
        Test if after new spending inputs, data are correctly registrated in the database. 
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Jean")

        number = Spending.objects.count()
        self.create_a_spending(1,'dépense1', 100,'EUR', 'Jean', ['Henri','Jean'], [50,50])  
        spending = Spending.objects.get(pk = 1)
        
        self.assertEqual(number+1, Spending.objects.count())
        self.assertEqual(spending.title, 'dépense1')
        self.assertEqual(spending.amount, 100)
        self.assertEqual(spending.payer, 'Jean')
        self.assertDictEqual(spending.receivers, {'Henri':50,'Jean':50})
        self.assertEqual(spending.tricount, Counts.objects.first())
        self.assertEqual(spending.date, date.today())
    
    def test_goback_bdd_unchanged(self):
        """
        Test if when we don't complete entirely a spending, no new spending appear in the database.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann")
        response = self.client.get('/newspending/1') 
        nb_spending = Spending.objects.count()
        self.extract_and_click_on_link(response.content , 'backtospending')  

        self.assertEqual(nb_spending,Spending.objects.count()) 
        
    def test_noamount_nullspending(self):
        """
        Test if when we create a spending with no amount, a new spending must appear in the database with amount 0.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Jean")
        nb_spending = Spending.objects.count()
        self.create_a_spending(1,'dépense1', '','EUR', 'Jean', ['Henri','Jean'],[0,0])  
        spending = Spending.objects.get(pk = 1)

        self.assertEqual(nb_spending + 1,Spending.objects.count()) 
        self.assertEqual(spending.amount, 0)
 
    def test_multiple_spendings_gives_good_credits_in_bdd(self):
        """
        Test if when we create multiple spendings, the computation made by calculation.py are well transferred to the database.
        """

        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending(1,'dépense1', 100,'EUR', 'Tony', ['Henri','Yann','Marine','Tony'], [25,50,25,0]) 
        self.create_a_spending(1,'dépense2', 200,'EUR', 'Marine', ['Henri','Yann','Marine','Tony'], [0,0,150,50]) 
        self.create_a_spending(1,'dépense3', 150,'EUR', 'Henri', ['Henri','Yann','Marine','Tony'], [50,50,25,25]) 
        self.create_a_spending(1,'dépense4', 180,'EUR', 'Yann', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 

        #Deserialization of the bdd 
        data = Counts.objects.first().data
        count = Tricount.from_json(data)
 
        self.assertEqual(count.dict_participants["Tony"].expense, 100)
        self.assertEqual(count.dict_participants["Marine"].expense, 200)
        self.assertEqual(count.dict_participants["Henri"].expense, 150)
        self.assertEqual(count.dict_participants["Yann"].expense, 180)
        
        self.assertDictEqual(count.dict_participants["Tony"].credits, {'Marine': 25.0, 'Henri': 0, 'Yann': 0})
        self.assertDictEqual(count.dict_participants["Marine"].credits, {'Tony': -25.0, 'Henri': 25.0, 'Yann': 50.0})
        self.assertDictEqual(count.dict_participants["Henri"].credits, {'Tony': 0, 'Marine': -25.0, 'Yann': -20})
        self.assertDictEqual(count.dict_participants["Yann"].credits, {'Tony': 0, 'Marine': -50.0, 'Henri': 20})
       
    def test_spending_after_adding_participant_to_tricount(self):
        """
        Test if calculations are correct when :
        - we create a tricount
        - we add a spending
        - we add a participant to the tricount 
        - we finally add a new spending involving the new participant
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending(1,'dépense', 180,'EUR', 'Yann', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 
        self.modify_a_tricount(1,"tricount1", "description", 'Henri','Yann','Marine','Tony','Robert')
        self.create_a_spending(1,'dépense', 100,'EUR', 'Robert', ['Henri','Yann','Marine','Tony'], [100,0,0,0])
        data = Counts.objects.first().data
        count = Tricount.from_json(data)

        self.assertEqual(count.dict_participants["Tony"].expense, 0)
        self.assertEqual(count.dict_participants["Marine"].expense, 0)
        self.assertEqual(count.dict_participants["Henri"].expense, 0)
        self.assertEqual(count.dict_participants["Yann"].expense, 180)
        self.assertEqual(count.dict_participants["Robert"].expense, 100)

        
        self.assertDictEqual(count.dict_participants["Tony"].credits, {'Marine': 0, 'Henri': 0, 'Yann': 50, 'Robert' : 0 })
        self.assertDictEqual(count.dict_participants["Marine"].credits, {'Tony': 0, 'Henri': 0, 'Yann': 50.0, 'Robert' :0 })
        self.assertDictEqual(count.dict_participants["Henri"].credits, {'Tony': 0, 'Marine': 0, 'Yann': 30, 'Robert' : 100 })
        self.assertDictEqual(count.dict_participants["Yann"].credits, {'Tony': -50, 'Marine': -50.0, 'Henri': -30, 'Robert' : 0 })
        self.assertDictEqual(count.dict_participants["Robert"].credits, {'Tony': 0, 'Marine': 0, 'Henri': -100, 'Yann' : 0})

    def test_spending_after_adding_and_removing_participant_to_tricount(self):
        """
        Test if calculations are correct when :
        - we create a tricount
        - we add a spending
        - we add a participant to the tricount 
        - we finally add a new spending involving the new participant
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending(1,'dépense', 180,'EUR', 'Yann', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 
        self.modify_a_tricount(1, "tricount1", "description", 'Henri','Marine','Tony','Robert')
        self.create_a_spending(1,'dépense', 100,'EUR', 'Robert', ['Henri','Marine','Tony'], [10,10,80])
        data = Counts.objects.first().data
        count = Tricount.from_json(data)

        self.assertEqual(count.dict_participants["Tony"].expense, 0)
        self.assertEqual(count.dict_participants["Marine"].expense, 0)
        self.assertEqual(count.dict_participants["Henri"].expense, 0)
        self.assertEqual(count.dict_participants["Yann"].expense, 180)
        self.assertEqual(count.dict_participants["Robert"].expense, 100)

        
        self.assertDictEqual(count.dict_participants["Tony"].credits, {'Marine': 0, 'Henri': 0, 'Yann': 50, 'Robert' : 80 })
        self.assertDictEqual(count.dict_participants["Marine"].credits, {'Tony': 0, 'Henri': 0, 'Yann': 50.0, 'Robert' :10 })
        self.assertDictEqual(count.dict_participants["Henri"].credits, {'Tony': 0, 'Marine': 0, 'Yann': 30, 'Robert' : 10 })
        self.assertDictEqual(count.dict_participants["Yann"].credits, {'Tony': -50, 'Marine': -50.0, 'Henri': -30, 'Robert' : 0 })
        self.assertDictEqual(count.dict_participants["Robert"].credits, {'Tony': -80, 'Marine': -10, 'Henri': -10, 'Yann' : 0})

    def test_spending_in_other_currency(self):
        """
        Function which creates a spending in pounds and verifies that the amount in euros in correct. This function makes a call to freecurrencyapi.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending(1,'dépense', 100,'GBP', 'Yann', ['Marine','Tony'], [50,50]) 
        spending = Spending.objects.first()

        amount = CC.convertSpendingCurrency('EUR','GBP',100)
        self.assertEqual(spending.amount, amount)

    def test_modify_a_spending(self):
        """
        Function which modifies a spending and checks if data in spending bdd have been modified.
        """
        #We create a tricount, a spending and modify the spending.
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.register_someone('Henri', '1234', 'henri@gmail.com')
        self.create_a_spending(1,'dépense', 180,'EUR', 'Henri', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 
        self.logout_someone()
        response = self.login_someone('Tony', '1234') 
        response = self.modify_a_spending(1,1,"depense2", 180, 'EUR',"Tony", ["Henri", "Yann"], [90,90]) 
        spending = Spending.objects.first()

        self.assertEqual(spending.title, "depense2")
        self.assertEqual(spending.amount, 180) 
        self.assertEqual(spending.payer, 'Tony') 
        self.assertDictEqual(spending.receivers, {"Henri":90, "Yann":90})
        self.assertRedirects(response,'/spending-details/1/1')

        # Verify the total_cost has been correctly calculated
        response = self.client.get('/tricount/1')
        self.assertEqual(response.context['totalcost'], 180)

        #We create a second spending and only modify the currency
        self.login_someone('Henri', '1234')
        self.create_a_spending(1,'dépense', 100,'EUR', 'Henri', ['Henri','Yann'], [50,50]) 
        response = self.modify_a_spending(1,2,"dépense", 100, 'USD',"Henri",['Henri','Yann'], [50,50]) 
        spending2 = Spending.objects.get(id = 2)

        amount = CC.convertSpendingCurrency('EUR','USD',100)
        self.assertEqual(spending2.amount, amount)  
        self.assertListEqual(list(spending2.receivers.keys()), ['Henri', 'Yann'])
        self.assertEqual(spending2.receivers['Henri'], amount/2)
        self.assertEqual(spending2.receivers['Yann'], amount/2)

        # Verify the total_cost has been correctly calculated
        response = self.client.get('/tricount/1')
        totalcost = 180 + amount
        self.assertEqual(response.context['totalcost'], totalcost)

    

    def test_modify_several_spendings_in_different_tricounts(self):
        """
        We create two tricounts in different currencies and verify that spending informations are correct after modifying it.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Jean","Henri","Dulciny")
        self.create_a_tricount('tricount1bis', "pwdbis", 'descriptionbis',"USD", "project", "Jean","Henri","Dulciny")
        self.create_a_spending(1,'dépense', 100,'EUR', 'Jean', ['Henri','Jean'], [50,50]) 

        spending = Spending.objects.get(title = "dépense") 

        self.assertEqual(spending.receivers['Henri'], 50.0)
        self.assertEqual(spending.receivers['Jean'], 50.0)

        self.create_a_spending(1,'dépense', 0,'EUR', 'Jean', ['Henri','Jean'], [0,0]) 
        self.create_a_spending(2,'dépense', 100,'USD', 'Jean', ['Henri','Jean'], [50,50])  
        self.modify_a_spending(1,1, 'New spending', 100, "EUR", 'Jean', ["Dulciny", "Henri"], [50,50]) 

        spending = Spending.objects.get(title = "New spending") 

        self.assertEqual(spending.receivers['Dulciny'], 50.0)
        self.assertEqual(spending.receivers['Henri'], 50.0) 


    def test_credits_after_modify_a_spending(self):
        """
        Function aiming to test if after the modification of a spending, the previous has been withdrawn from the calculations
         of credits and the new spending added to the calculations.
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending(1,'dépense', 180,'EUR', 'Henri', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 
        self.modify_a_spending(1,1,"depense2", 180, 'EUR',"Tony", ["Henri", "Yann"], [90,90]) 

        tricount = Tricount.from_json(Counts.objects.first().data)
        
        self.assertEqual(tricount.total_cost, 180.0)
        self.assertEqual(tricount.dict_participants["Tony"].expense, 180.0)
        self.assertEqual(tricount.dict_participants["Tony"].credits['Henri'], -90.0)
        self.assertEqual(tricount.dict_participants["Tony"].credits['Yann'], -90.0)
        self.assertEqual(tricount.dict_participants["Yann"].credits['Henri'], 0.0)
        self.assertEqual(tricount.dict_participants["Marine"].credits['Henri'], 0.0) 

    def test_delete_a_spending(self):
        """
        Function which deletes a created spending and verifies if the spending has been correctly deleted
        """
        self.create_a_tricount('tricount1', "pwd", 'description',"EUR", "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending(1,'dépense', 180,'EUR', 'Yann', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 
        self.create_a_spending(1,'dépense2', 10,'EUR', 'Henri', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 
        
        self.assertEqual(len(Spending.objects.all()),2)

        self.delete_a_spending(1,2)
        spending = Spending.objects.first()

        self.assertEqual(spending.title, "dépense")
        self.assertEqual(spending.payer, "Yann")
        self.assertEqual(len(Spending.objects.all()),1)

        
        
 
    