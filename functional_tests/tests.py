#from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from count.models import Counts

class NewVisitorTest(StaticLiveServerTestCase): 

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def check_participant_appear_on_newcount_page(self,name_participant):
        """
        Fonction qui entre un participant dans un tricount donné et qui regarde si les participants apparaissent
        sur la page
        """
        participantbox = self.browser.find_element(By.NAME,"new_participant")
        buttonbox = self.browser.find_element(By.CLASS_NAME,"add_participant")
        participantbox.send_keys(name_participant)
        buttonbox.send_keys(Keys.ENTER)
        time.sleep(2)

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/newcount")
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        self.assertIn(name_participant, [participant.text for participant in participants])

        
    def check_inputs_appear_on_listecount_Page(self,inputs):
        """
        Fonction qui entre un nouveau tricount et vérifie si les données apparaissent sur la page recensant les tricount.
        """

        #Il remplit les données d'un nouveau tricount et les envoie
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description") 
        categorybox = self.browser.find_element(By.ID,f"{inputs[2]}")
        participants = self.browser.find_elements(By.CLASS_NAME,'printparticipant')
        submitbox = self.browser.find_element(By.NAME,"submit")
        
        titlebox.send_keys(inputs[0])
        descriptionbox.send_keys(inputs[1]) 
        categorybox.click()

        #He chooses to go on the currency page:
        #To complete when JS learned.
        submitbox.send_keys(Keys.ENTER)

        time.sleep(3)

        #Il met un titre :
        if inputs[0] != "" :    
            if len(participants) == 0:
                self.assertEqual(self.browser.current_url, self.live_server_url + '/count/newcount/addcount')

                participant_error = self.browser.find_element(By.CLASS_NAME,'participant-error')
                self.assertIn("Il faut au moins un participant",participant_error.text) 
            else:
                id_count = Counts.objects.count()
                self.assertEqual(self.browser.current_url, self.live_server_url + '/count/tricount/' + str(id_count) ) 

                back = self.browser.find_element(By.CLASS_NAME,'backtolistecount')
                back.send_keys(Keys.ENTER)
                time.sleep(2)

                self.assertEqual(self.browser.current_url, self.live_server_url + '/count/') 

                self.assertIn('Tricount',self.browser.title)

                #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
                title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
                description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
                self.assertIn(inputs[0],[titre.text for titre in title]) 
                self.assertIn(inputs[1] or 'Pas de description',[desc.text for desc in description])
        
        #Il oublie de mettre un titre.
        else:
            self.assertEqual(self.browser.current_url, self.live_server_url + '/count/newcount/addcount')
            msg = self.browser.find_element(By.CLASS_NAME,'error')
            self.assertIn('Le titre doit comporter au moins un caractère.',msg.text)
    
    def check_links_of_listecounts_leads_to_the_good_tricount(self,tricount_number,*participants):
        """
        Function which clicks on a tricount and check the title and the participants are the good ones.
        participants : the participants we want to verify the presence.
        """
        link = self.browser.find_element(By.ID,"link-tricount-" + str(tricount_number))
        link.send_keys(Keys.ENTER)
        time.sleep(2) 

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/tricount/" + str(tricount_number))

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")

        count = Counts.objects.get(id=tricount_number)
        self.assertEqual(tricount_title.text, count.title)
 
        for participant in participants:
            self.assertIn(participant, [name.text for name in tricount_participants])  
        
        back = self.browser.find_element(By.CLASS_NAME,'backtolistecount')
        back.send_keys(Keys.ENTER)
        time.sleep(2)

    def test_tricount_creation(self):
        
        #Le visiteur arrive sur la page il voit le titre. 
        url = self.live_server_url  
        self.browser.get(url + '/count')  
        
        time.sleep(2) 
        self.assertIn('Tricount',self.browser.title)
        
        #Il voit la liste des tricount présents ou absents et clique sur le lien pour créer un nouveau tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        self.assertEqual(self.browser.current_url, url + '/count/newcount') 
    
        #Il commence par remplir les différents participants à son premier tricount : les participants apparaissent sur la page du tricount ainsi que le nombre de participants qui s'incrémente
        self.check_participant_appear_on_newcount_page('Jean')
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants")
        self.assertEqual(number_participants.text,"Participants (1/50)")

        self.check_participant_appear_on_newcount_page('Heeeeeenri')
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants")
        self.assertEqual(number_participants.text,"Participants (2/50)")

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.check_inputs_appear_on_listecount_Page(['Tricount 1','Description 1','trip'])
       
        #Il reclique pour recréer un second tricount.
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  
        
        self.assertEqual(self.browser.current_url, url + '/count/newcount') 
        
        #Il remplit les différents participants d'un second tricount : les participants apparaissent sur la page du tricount mais pas ceux du tricount précédemment créé.
        self.check_participant_appear_on_newcount_page('Tony')
        self.check_participant_appear_on_newcount_page('Dulcinée')
        self.check_participant_appear_on_newcount_page('Annie')

        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        self.assertNotIn('Jean', [participant.text for participant in participants])
        self.assertNotIn('Heeeeeenri', [participant.text for participant in participants])

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.check_inputs_appear_on_listecount_Page(['Tricount 2','Description 2','project'])
        
        #Il reclique pour recréer un second tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  
        

        #Il remplit les données d'un nouveau tricount mais oublie de mettre un titre
        # Il est renvoyé vers l'url de remplissagedu tricount avec un message d'erreur affiché en rouge
        self.check_inputs_appear_on_listecount_Page(['','description 3','project'])
 
        #Du coup, il rajoute un titre mais oublie de mettre des participants:   
        self.check_inputs_appear_on_listecount_Page(['Tricount 3','','project'])
 
        #Il met des participants puis crée son tricount.
        self.check_participant_appear_on_newcount_page('Totolitoto')
        self.check_participant_appear_on_newcount_page('Biloute')
        self.check_participant_appear_on_newcount_page('Anne')
        self.check_inputs_appear_on_listecount_Page(['Tricount 3','','project'])

        #Il veut créer un nouveau tricount mais change d'avis et après avoir rentré un participant appuie sur le bouton retour en arrière
        #Il atterrit à nouveau sur la liste des tricount.
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        self.check_participant_appear_on_newcount_page('Jeanine')
        back = self.browser.find_element(By.CLASS_NAME,'backtotricount')
        back.send_keys(Keys.ENTER)
        time.sleep(2)


        self.assertEqual(self.browser.current_url, url + '/count/')
        
        #Il clique pour créer un nouveau tricount et voit que les participants précédemment entrés ne sont pas sur la page
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        self.assertNotIn('Jeanine',[participant.text for participant in participants])

        back = self.browser.find_element(By.CLASS_NAME,'backtotricount')
        back.send_keys(Keys.ENTER)
        time.sleep(2)
        
        #Il clique maintenant sur les tricounts existant pour vérifier que les informations du tricount sont correctes. 

        self.check_links_of_listecounts_leads_to_the_good_tricount(1,'Jean')
        self.check_links_of_listecounts_leads_to_the_good_tricount(2, 'Tony', 'Dulcinée', 'Annie')
        
class RegisterSpending(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self) -> None:
        self.browser.quit()

    def create_a_tricount(self,title, description, category,*participants):
        self.browser.get(self.live_server_url+ '/count')

        #Clicks to add a tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        #Enter the participants
        participantbox = self.browser.find_element(By.NAME,"new_participant")
        buttonbox = self.browser.find_element(By.CLASS_NAME,"add_participant")
        for participant in participants:
            participantbox.send_keys(participant)
            buttonbox.send_keys(Keys.ENTER)

        #Enter  the other characteristics
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description") 
        categorybox = self.browser.find_element(By.ID,f"{category}") 
        submitbox = self.browser.find_element(By.NAME,"submit")
        
        titlebox.send_keys(title)
        descriptionbox.send_keys(description) 
        categorybox.click()

        #He chooses to go on the currency page: 
        submitbox.send_keys(Keys.ENTER)
        time.sleep(2)

    def click_on_an_exiting_tricount(self,tricount_number):
        """
        Function which clicks on a tricount and check the title and the participants are the good ones.
        participants : the participants we want to verify the presence.
        """
        link = self.browser.find_element(By.ID,"link-tricount-" + str(tricount_number))
        link.send_keys(Keys.ENTER)
        time.sleep(2) 

    def click_on_create_spending(self):
        link_spending = self.browser.find_element(By.CLASS_NAME,'new-spending')
        link_spending.send_keys(Keys.ENTER)
        time.sleep(2)

    def test_spending_creation(self):
        #A tricount is created et come back to the listecount page
        self.create_a_tricount('Tricount1',"Je décris", "project","Jean","Henri")
        back = self.browser.find_element(By.CLASS_NAME,'backtolistecount')
        back.send_keys(Keys.ENTER)
        time.sleep(2)

        #The user clicks on an existing tricount 
        self.click_on_an_exiting_tricount(1)

        #The user clicks to add a new spending
        self.click_on_create_spending()

        self.assertEqual(self.browser.current_url,self.live_server_url + '/count/tricount/1/spending')


        #He enters the title, amount the payer and for who the payer paid

        #He is then redirected to the spending list.

        #He forgets to put a title, a message of error appears and he stays on the page.

        #He forgets to put who is the payer, by default it is the first participant.

        #He forgets to put for who he pays, by default it's for all participants.
        