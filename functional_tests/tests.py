#from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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

        self.assertIn('Jean', [participant.text for participant in participants])
        self.assertEqual(number_participants.text,"Participants (1/50)") 

        self.add_participants('Heeeeeenri')

        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants")

        self.assertIn('Heeeeeenri', [participant.text for participant in participants])
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
        
class RegisterSpending(StaticLiveServerTestCase,user_experience.Click):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self) -> None:
        self.browser.quit()

    def test_spending_creation(self): 
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

        #He forgets to put who is the payer, by default it is the first participant.

        #He forgets to put for who he pays, by default it's for all participants.
        