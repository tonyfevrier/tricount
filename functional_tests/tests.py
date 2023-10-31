#from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from count.models import Counts
from functional_tests import user_experience 

class NewVisitorTest(StaticLiveServerTestCase,user_experience.Click): 
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self): 
        self.browser.quit()

    def test_tricount_creation(self):
        #Le visiteur arrive sur la page il voit le titre. 
        url = self.live_server_url  
        self.browser.get(url + '/count')  
        time.sleep(2)

        self.assertIn('Tricount',self.browser.title)
        
        #Il voit la liste des tricount présents ou absents et clique sur le lien pour créer un nouveau tricount
        self.click_on_a_link(By.ID,'id_newcount')
        
        self.assertEqual(self.browser.current_url, url + '/count/newcount') 
    
        #Il commence par remplir les différents participants à son premier tricount : les participants apparaissent sur la page du tricount ainsi que le nombre de participants qui s'incrémente
        self.add_participants('Jean')

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/newcount")
        
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants") 

        self.assertIn('Jean', [participant.get_attribute("value") for participant in participants])
        self.assertEqual(number_participants.text,"Participants (1/50)") 

        self.add_participants('Heeeeeenri')

        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants")

        self.assertIn('Heeeeeenri', [participant.get_attribute("value") for participant in participants])
        self.assertEqual(number_participants.text,"Participants (2/50)")

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.add_tricount_characteristics('Tricount 1','Description 1','trip')

        #He arrives on the good url 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/tricount/1')

        self.click_on_a_link(By.CLASS_NAME,'backtolistecount')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/')
        self.assertIn('Tricount',self.browser.title)

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')

        self.assertIn('Tricount 1',[titre.text for titre in title]) 
        self.assertIn('Description 1',[desc.text for desc in description])
       
        #Il reclique pour recréer un second tricount. 
        self.click_on_a_link(By.ID,'id_newcount')
        
        self.assertEqual(self.browser.current_url, url + '/count/newcount') 
        
        #Il remplit les différents participants d'un second tricount : les participants apparaissent sur la page du tricount mais pas ceux du tricount précédemment créé.
        self.add_participants('Tony','Dulcinée','Annie')
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")

        self.assertNotIn('Jean', [participant.text for participant in participants])
        self.assertNotIn('Heeeeeenri', [participant.text for participant in participants])

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.add_tricount_characteristics('Tricount 2','Description 2','project')

        #He arrives on the good url 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/tricount/2' )
 
        self.click_on_a_link(By.CLASS_NAME,'backtolistecount')

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')

        self.assertIn('Tricount 2',[titre.text for titre in title]) 
        self.assertIn('Description 2',[desc.text for desc in description])
        
        #Il reclique pour recréer un second tricount 
        self.click_on_a_link(By.ID,'id_newcount')

        # Il remplit les données d'un nouveau tricount mais oublie de mettre un titre
        # Il est renvoyé vers l'url de remplissagedu tricount avec un message d'erreur affiché en rouge 
        self.add_tricount_characteristics('','description 3','project')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/newcount/addcount')

        msg = self.browser.find_element(By.CLASS_NAME,'error')

        self.assertIn('Le titre doit comporter au moins un caractère.',msg.text)
 
        #Du coup, il rajoute un titre mais oublie de mettre des participants:    
        self.add_tricount_characteristics('Tricount 3','','project')
        participant_error = self.browser.find_element(By.CLASS_NAME,'participant-error')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/newcount/addcount')
        self.assertIn("Il faut au moins un participant",participant_error.text) 
 
        #Il met des participants puis crée son tricount. 
        self.create_a_tricount('Tricount 3','','project','Totolitoto','Biloute','Anne')

        self.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')

        self.assertIn('Pas de description',[desc.text for desc in description])

        #Il veut créer un nouveau tricount mais change d'avis et après avoir rentré un participant appuie sur le bouton retour en arrière
        #Il atterrit à nouveau sur la liste des tricount. 
        self.click_on_a_link(By.ID,'id_newcount') 
        self.add_participants('Jeanine') 
        self.click_on_a_link(By.CLASS_NAME,'backtotricount')

        self.assertEqual(self.browser.current_url, url + '/count/')
        
        #Il clique pour créer un nouveau tricount et voit que les participants précédemment entrés ne sont pas sur la page
        self.click_on_a_link(By.ID,'id_newcount')
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")

        self.assertNotIn('Jeanine',[participant.text for participant in participants])

        self.click_on_a_link(By.CLASS_NAME,'backtotricount')

        #Il clique maintenant sur les tricounts existant pour vérifier que les informations du tricount sont correctes. 
        self.click_on_an_existing_tricount(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/1")

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")
        count = Counts.objects.get(id=1)
        
        self.assertEqual(tricount_title.text, count.title)
        self.assertIn('Jean', [name.text for name in tricount_participants])  
        
        self.click_on_a_link(By.CLASS_NAME,'backtolistecount') 
        self.click_on_an_existing_tricount(2)

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/2")

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")
        count = Counts.objects.get(id=2)
        
        self.assertEqual(tricount_title.text, count.title)
        self.assertIn('Dulcinée', [name.text for name in tricount_participants]) 
        self.assertIn('Annie', [name.text for name in tricount_participants]) 
        
class RegisterSpending(StaticLiveServerTestCase,user_experience.Click,user_experience.Check):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_spending_creation(self): 

        #MODIFIER check IN : normalement pas besoin de modifier create spending : devrait créer un dico 

        #A tricount is created et come back to the listecount page
 
        self.create_a_tricount('Tricount1',"Je décris", "project","Jean","Henri")
        self.click_on_a_link(By.CLASS_NAME,'backtolistecount') 

        #The user clicks on an existing tricount 
        self.click_on_an_existing_tricount(1)

        #The user clicks to add a new spending, he has the choice between the participants previously created
        self.click_on_create_spending()

        self.assertEqual(self.browser.current_url,self.live_server_url + '/count/tricount/1/spending')
        
        spender_participant = self.browser.find_elements(By.CLASS_NAME, "spender-participant")
        receiver_participants = self.browser.find_elements(By.CLASS_NAME, "receiver-participant")

        self.assertIn("Jean",[name.text for name in spender_participant])
        self.assertIn("Henri",[name.text for name in spender_participant])
        self.assertIn("Jean",[name.text for name in receiver_participants])
        self.assertIn("Henri",[name.text for name in receiver_participants])

        #He enters the title, amount the payer and for who the payer paid
        self.create_a_spending('Dépense1', 100., 'Jean', ['Henri','Jean'])

        #He is then redirected to the spending list where the name, the amount, the payer appears
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/tricount/1')
        
        spending_title = self.browser.find_elements(By.CLASS_NAME,"spending-title")
        spending_amount = self.browser.find_elements(By.CLASS_NAME,"spending-amount")
        spending_payer = self.browser.find_elements(By.CLASS_NAME,"spending-payer")
         
        self.assertIn('Dépense1',[name.text for name in spending_title])
        self.assertIn(100.,[float(name.text) for name in spending_amount])
        self.assertIn('Jean',[name.text for name in spending_payer])

        #He tries to create a second spending. He forgets to put a title, a message of error appears and he stays on the page.
        self.click_on_create_spending()
        self.create_a_spending('', 100., 'Jean', ['Henri','Jean'])

        notitle = self.browser.find_element(By.CLASS_NAME,"notitle")
        self.assertEqual(notitle.text, "Titre non valable")
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/1/addspending")

        #He forgets to put the amount, a spending is created with amount 0.
        self.create_a_spending('Dépense2', '', 'Jean', ['Henri','Jean'])

        amounts = self.browser.find_elements(By.CLASS_NAME,"spending-amount")
        
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/1")
        self.assertIn('0.0',[amount.text for amount in amounts])

        #He wants to check the current equilibria
        self.click_on_a_link(By.CLASS_NAME,"gotoequilibria")
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/1/equilibria")

        #He clicks back
        self.click_on_a_link(By.CLASS_NAME,"gotospending")
        self.assertEqual(self.browser.current_url,  self.live_server_url + "/count/tricount/1")

        #He forgets to put who is the payer, by default it is the first participant.

        #He forgets to put for who he pays, by default it's for all participants.

    def test_the_page_of_a_spending(self):
        #L'utilisateur crée une dépense et clique dessus
        self.create_a_tricount('Tricount1',"Je décris", "project","Jean","Henri") 

        self.click_on_create_spending()
        self.create_a_spending('Depense1', 100., 'Jean', ['Henri','Jean'])

        self.click_on_an_existing_spending(1)
        time.sleep(3)

        #Il arrive sur la page et il y voit toutes les données qu'il a enregistrées.
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/1/spending/1")
        self.check_informations_of_a_spending('DEPENSE1', '100.0', 'Payé par Jean', ['Henri','Jean'],['50.00 eur', '50.00 eur'])

        #Il revient en arrière et crée trois autres dépenses
        self.click_on_a_link(By.CLASS_NAME,"backtospending")
 
        self.click_on_create_spending()
        self.create_a_spending('Depense2', 10., 'Henri', ['Henri','Jean']) 
        self.click_on_create_spending()
        self.create_a_spending('Depense3', 2., 'Henri', ['Henri','Jean'])

        #Il clique à nouveau sur la première dépense puis sur suivant
        self.click_on_an_existing_spending(1)
        self.click_on_a_link(By.CLASS_NAME,"following")

        #Il voit alors les infos de la seconde dépense et le bouton précédent apparaître
        self.check_informations_of_a_spending('DEPENSE2', '10.0', 'Payé par Henri', ['Henri','Jean'],['5.00 eur', '5.00 eur'])
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME,'previous'))

        #Il clique sur suivant une fois et voit le bouton suivant disparaître
        self.click_on_a_link(By.CLASS_NAME,"following") 
        self.check_informations_of_a_spending('DEPENSE3', '2.0', 'Payé par Henri', ['Henri','Jean'],['1.00 eur', '1.00 eur'])
        #self.assertIsNone(self.browser.find_element(By.CLASS_NAME,'following'))

        #Il clique sur précédent trois fois.
        self.click_on_a_link(By.CLASS_NAME,"previous")
        self.click_on_a_link(By.CLASS_NAME,"previous")

    
    def test_modify_a_created_spending(self):
        pass

class JSTest(StaticLiveServerTestCase,user_experience.Click,user_experience.Check):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_JS_of_listecount_page(self):
        #The user arrives on listecount page, no popup is opened : 
        self.browser.get(self.live_server_url+ '/count')
        popup_children = self.browser.find_elements(By.CSS_SELECTOR, "[data-div = hidden] > *")

        for elt in popup_children:
            self.assertEqual(elt.is_displayed(),False) 

        #He creates a tricount and come back.
        self.create_a_tricount('Tricount1',"Je décris", "project","Jean","Henri")
        self.click_on_a_link(By.CLASS_NAME,'backtolistecount')  

        # he clicks on parameters, a popup appears
        self.click_on_a_link(By.CLASS_NAME,"parameters")
        self.check_if_popup_displayed("parameters-options",True) 
        
        #He clicks on a JS button of the popup, an other popup replaces the previous one.
        self.click_on_a_link(By.CLASS_NAME, "conditions") 
        self.check_if_popup_displayed("parameters-options",False)
        self.check_if_popup_displayed("conditions-options",True)

        #He clicks on the link of the tricount and no popup is visible and he stays on the same page.
        self.click_on_a_link(By.CLASS_NAME,"link-tricount")

        popup_children = self.browser.find_elements(By.CSS_SELECTOR, "[data-div = hidden] > *")

        for elt in popup_children:
            self.assertEqual(elt.is_displayed(),False)
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/")

    def test_JS_of_newcount_page(self):
        #The client goes to the creation of a new count
        self.browser.get(self.live_server_url+ '/count')
        self.click_on_a_link(By.CLASS_NAME,'id_newcount')

        #He enters a title and a description, a counter appears and the number of letters corresponds to the length of the word.
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description")  
        
        titlebox.click()
        counter = self.browser.find_element(By.CLASS_NAME, "compteur")
        
        self.assertEqual(counter.text, '0/50')
        self.assertEqual(counter.is_displayed(),True) 

        #He tries to put a more than fifty letters title but he is blocked 
        titlebox.send_keys('t'*51)
        time.sleep(2)
        self.assertEqual(counter.text, '50/50')
        titlebox.clear()

        #So he writes a shorter title
        titlebox.send_keys('titre')
        time.sleep(2)
        self.assertEqual(counter.text, '5/50')

        descriptionbox.send_keys('description')
        self.assertEqual(counter.text, '11/500')
        time.sleep(2)

        
        




