from os import listdir
from random import randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep, time
import platform
import pyperclip
import undetected_chromedriver as uc

class Uploader():

    def __init__(self, DIRECTORY_PATH):

        system = platform.system()

        if system == "Windows":
            self.conjoiner = "\\"
        else:
            self.conjoiner = "/"

        self.DIRECTORY_PATH = DIRECTORY_PATH
        self.OUTPUT_PATH = DIRECTORY_PATH+self.conjoiner+'Output'
        self.PROFILE_PATH = DIRECTORY_PATH+self.conjoiner+'Chrome'
        self.CREDENTIALS_PATH = self.DIRECTORY_PATH+self.conjoiner+'Credentials'
        self.OLD_LATEST_EMAIL = self.getEmails(1, 'setter')
        self.INFORMATION_TEXT_FILE = DIRECTORY_PATH+self.conjoiner+'information.txt'

        if system == "Windows":
            options = webdriver.ChromeOptions()
            options.add_argument(r"--user-data-dir="+self.PROFILE_PATH)
            options.add_argument(r'--profile-directory=Profile 1')
            options.add_argument(r"--disable-notifications")
            self.driver = uc.Chrome(options=options)
        else:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument(r"--disable-notifications")
            self.driver = uc.Chrome(chrome_options=chrome_options)
    
        self.action = ActionChains(self.driver)

    def addToTextfile(self, textfile, addedElement):
        with open(textfile, "a") as f:
            f.write("\n"+addedElement)

    def uploadToYoutube(self, email, password, title, description, beatFolder, imageLocation, noDrumsTaggedFile='empty'):

            self.driver.get("https://www.tunestotube.com/")

            #final beats directory
            if beatFolder != False:
                beatFiles = listdir(beatFolder+self.conjoiner+'Final Beat')
                if '.wav' in beatFiles[0]:
                    taggedFile = beatFiles[1]
                else:
                    taggedFile = beatFiles[0]
            else:
                taggedFile = noDrumsTaggedFile

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'homepage_login')))

                self.driver.get('https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&redirect_uri=https%3A%2F%2Fwww.tunestotube.com%2Flogin%2Findex.php&client_id=503657242195.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube&access_type=offline&approval_prompt=force&state=1964382990&service=lso&o2v=1&flowName=GeneralOAuthFlow')

                try:

                    #click account
                    while(1):
                        try:
                            emailInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-identifier='"+email+"']")))
                            emailInput.click()
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()

                    #allow access to google account
                    while(1):
                        try:
                            allowAccess = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit_approve_access"]/div/button')))
                            allowAccess.click()
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()
                except TimeoutException:
                    pass

                try:
                    
                    #input email
                    while(1):
                        try:
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierId'))).send_keys(email)
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()
                        except ElementNotInteractableException:
                            try:
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]'))).send_keys(email)
                                break
                            except ElementNotInteractableException:
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="identifier"]'))).send_keys(email)
                                break
                    
                    #hit next
                    while(1):
                        try:
                            nextButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierNext')))
                            nextButton.click()
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()

                    #input password
                    while(1):
                        try:
                            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()
                        except ElementNotInteractableException:
                            try:
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).send_keys(password)
                                break
                            except ElementNotInteractableException:
                                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))).send_keys(password)
                                break

                    #hit next
                    while(1):
                        try:
                            nextButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'passwordNext')))
                            nextButton.click()
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()
                    
                    #submit approve access
                    while(1):
                        try:
                            acceptAndApprove = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'submit_approve_access')))
                            acceptAndApprove.click()
                            self.randomSleep()
                            break
                        except StaleElementReferenceException:
                            self.randomSleep()
                    
                except TimeoutException:
                    pass
            
            except TimeoutException:
                pass

            #upload title
            while(1):
                try:
                    titleInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'VideoTitle')))
                    self.randomSleep()
                    titleInput.send_keys(title)
                    self.randomSleep()
                    break
                except StaleElementReferenceException:
                    self.randomSleep()

            #upload description
            while(1):
                try:
                    descriptionInput = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'description')))
                    self.randomSleep()
                    descriptionInput.send_keys(description)
                    self.randomSleep()
                    break
                except StaleElementReferenceException:
                    self.randomSleep()
            
            #upload image
            while(1):
                try:
                    imageLocationButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'file_upload_label_button')))
                    imageLocationButton.send_keys(imageLocation)
                    self.randomSleep()
                    break
                except StaleElementReferenceException:
                    self.randomSleep()
            
            #upload audio
            while(1):
                try:
                    audioUpload = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'file_upload_label_button')))
                    if beatFolder != False:
                        audioUpload.send_keys(beatFolder+self.conjoiner+'Final Beat'+self.conjoiner+taggedFile)
                    else:
                        audioUpload.send_keys(taggedFile)
                    self.randomSleep()
                    break
                except StaleElementReferenceException:
                    self.randomSleep()

            #create video
            while(1):
                try:
                    createVideoButton = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'createVideoButton')))
                    while(createVideoButton.is_enabled() == False):
                        self.randomSleep()
                    createVideoButton.click()
                    self.randomSleep()
                    break
                except StaleElementReferenceException:
                    self.randomSleep()
        
    def uploadTo*********(self, email, password, beatFolder, beatTitle, bpm, imageLocation, untaggedFileNoDrums='empty', stemsNoDrums='empty'):

        self.driver.get('************')

        #login
        try:

            #input username
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "oath-email"))).send_keys(email)
            self.randomSleep()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'btn-submit-oath'))).click()
            self.randomSleep()

            #input password
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'userPassword'))).send_keys(password)
            self.randomSleep()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'btn-submit-oath'))).click()
            self.randomSleep()

        except TimeoutException:
            pass

        #make a new track
        while(1):
            try:
                newTrack = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//bs-square-button[@data-qa='button_add_track']")))
                newTrack.click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()
                
        #final beats directory
        if beatFolder != False:
            beatFiles = listdir(beatFolder+self.conjoiner+'Final Beat')
            if '.wav' in beatFiles[0]:
                untaggedFile = beatFiles[0]
            else:
                untaggedFile = beatFiles[1]
        else:
            untaggedFile = untaggedFileNoDrums

        #hit upload button
        while(1):
            try:
                uploadButtons = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-upload')))
                uploadButtons[0].click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()

        #upload the file
        while(1):
            try:
                dropBoxWav = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'uppy-DragDrop-input')))
                if beatFolder != False:
                    dropBoxWav.send_keys(beatFolder+self.conjoiner+'Final Beat'+self.conjoiner+untaggedFile)
                else:
                    dropBoxWav.send_keys(untaggedFile)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()
        
        #wait until beat upload is complete
        startTime = time()
        while(1):
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Replace')]")))
                if ((startTime - time()) > 120.0):
                    raise Exception("Upload of beat took to long. Restarting.")
                while(1):
                    tabList = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'mat-tab-list')))
                    x = WebDriverWait(tabList, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="tab"]')))
                    if x[1].get_attribute('aria-disabled') == 'false':
                        break
                    self.randomSleep()    
                break
            except TimeoutException:
                pass
            except StaleElementReferenceException:
                self.randomSleep()
                pass
        
        #hit the upload button
        while(1):
            try:
                uploadButtons = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-upload')))
                uploadButtons[1].click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()
        
        #upload the stems
        while(1):
            try:
                dropBoxZip = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'uppy-DragDrop-input')))
                if beatFolder != False:
                    dropBoxZip.send_keys(beatFolder+self.conjoiner+'Stems.zip')
                else:
                    dropBoxZip.send_keys(stemsNoDrums)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()

        #wait until stems upload is complete
        startTime = time()
        while(1):
            try:
                replaceButtons = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Replace')]")))
                if len(replaceButtons) == 3:
                    break
                if ((startTime - time()) > 180.0):
                    raise Exception("Upload of stems took to long. Restarting.")
                sleep(5)
            except TimeoutException:
                pass
            except StaleElementReferenceException:
                self.randomSleep()

        #click next step
        while(1):
            try:
                nextStepButton = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//bs-square-button[@data-qa="button_upload_next"]')))
                while(nextStepButton.is_enabled() == False):
                    self.randomSleep()
                try:
                    nextStepButton.click()
                except ElementNotInteractableException:
                    self.driver.execute_script("arguments[0].click();", nextStepButton)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()

        #upload title
        while(1):
            try:
                titleInput = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'title')))
                titleInput.clear()
                titleInput = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'title')))
                titleInput.send_keys(beatTitle)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()

        #upload image
        while(1):
            try:
                uploadImageButton = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Edit Artwork')]")))
                uploadImageButton.click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()
        while(1):
            try:
                menuButton = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@role="menuitem"]')))[0]
                menuButton.click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()
        while(1):
            try:
                dropBoxImage = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'uppy-DragDrop-input')))
                dropBoxImage.send_keys(imageLocation)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()
        while(1):
            try:
                saveCropButton = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//bs-square-button[@data-qa="button_save_cropt"]')))
                saveCropButton.click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()

        #click next step
        while(1):
            try:
                nextStepButton = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//bs-square-button[@data-qa="button_upload_next"]')))
                while(nextStepButton.is_enabled() == False):
                    self.randomSleep()
                try:
                    nextStepButton.click()
                except ElementNotInteractableException:
                    self.driver.execute_script("arguments[0].click();", nextStepButton)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()    

        #input tags
        group1 = ['example group a tag 1', 'example group a tag 2']
        group2 = ['example group b tag 1', 'example group b tag 2']
        group3 = ['example group c tag 1', 'example group c tag 2']
        
        tags = group1[randint(0, len(group1)-1)]+', '+group2[randint(0, len(group2)-1)]+', '+group3[randint(0, len(group3)-1)]+','
        while(1):
            try:
                inputSections = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mat-input-element')))
                inputSections[0].send_keys(tags)
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep()   
        self.addToTextfile(self.INFORMATION_TEXT_FILE, "******** tags: "+tags)

        #input bpm
        while(1):
            try:
                bpmInputArea = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//bs-text-input[@data-qa="input_bpm"]')))
                bpmInputSpecific = WebDriverWait(bpmInputArea, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@type="number"]')))
                bpmInputSpecific.clear()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep() 
        while(1):
            try:
                bpmInputSpecific = WebDriverWait(bpmInputArea, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@type="number"]')))
                bpmInputSpecific.send_keys(str(bpm))
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep() 

        #publish the beat
        while(1):
            try:
                publishButton = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//bs-square-button[@data-qa="button_upload_publish"]')))
                while(publishButton.is_enabled() == False):
                    self.randomSleep()
                publishButton.click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep() 

        #get the link
        while(1):
            try:
                beatLink = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'clipboard')))
                beatLink.click()
                self.randomSleep()
                break
            except StaleElementReferenceException:
                self.randomSleep() 
        link = pyperclip.paste()
        self.addToTextfile(self.INFORMATION_TEXT_FILE, "********* link: "+link)

        return link
    
    def bigSleep(self):
        sleep(10000)
    
    def randomSleep(self):
        sleep(randint(140,394)/100)