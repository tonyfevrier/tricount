#from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

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
        categorybox = self.browser.find_element(By.NAME,"newtricount_category")
        submitbox = self.browser.find_element(By.NAME,"submit")
        
        titlebox.send_keys(inputs[0])
        descriptionbox.send_keys(inputs[1])
        categorybox.send_keys(inputs[2])
        
        submitbox.send_keys(Keys.ENTER)

        time.sleep(3)

        if inputs[0] != "":
            self.assertEqual(self.browser.current_url, self.live_server_url + '/count/') 

            self.assertIn('Tricount',self.browser.title)

            #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
            title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
            description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
            self.assertIn(inputs[0],[titre.text for titre in title]) 
            self.assertIn(inputs[1] or 'Pas de description',[desc.text for desc in description])
        
        else:
            self.assertEqual(self.browser.current_url, self.live_server_url + '/count/newcount/addcount')
            msg = self.browser.find_element(By.CLASS_NAME,'error')
            self.assertIn('Le titre doit comporter au moins un caractère.',msg.text)
    
    def test_listecount_Page(self):
        
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
    
        #Il commence par remplir les différents participants à son premier tricount : les participants apparaissent sur la page du tricount
        self.check_participant_appear_on_newcount_page('Jean')
        self.check_participant_appear_on_newcount_page('Heeeeeenri')

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.check_inputs_appear_on_listecount_Page(['Tricount 1','Description 1','Voyage'])
       
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
        self.check_inputs_appear_on_listecount_Page(['Tricount 2','Description 2','Projet'])
    
        #Il reclique pour recréer un second tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  
        
        #Il remplit les données d'un nouveau tricount mais oublie de mettre un titre
        # Il est renvoyé vers l'url de remplissagedu tricount avec un message d'erreur affiché en rouge
        self.check_inputs_appear_on_listecount_Page(['','description 3','Projet'])

        #Du coup, il rajoute un titre :  
        self.check_inputs_appear_on_listecount_Page(['Tricount 3','','Projet'])
