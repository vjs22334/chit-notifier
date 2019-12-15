import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException,TimeoutException    
import os
from .models import *


test_recepients = [
    {
        "name": "Avb",
        "number": "9972233550"
    },
    {   
        "name": "wrong",
        "number": "ajsdiasjd"
    },
    {   
        "name": "revathy",
        "number": "9952417004"
    }
]

def setup_browser():
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['handleAlerts'] = True
    firefox_capabilities['acceptSslCerts'] = True
    firefox_capabilities['acceptInsecureCerts'] = True
    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True

    browser = webdriver.Firefox(firefox_profile=profile,capabilities=firefox_capabilities)
    browser.get(('https://web.whatsapp.com'))
    return browser


def send_messages(recepients):
    browser = setup_browser()
    wait = WebDriverWait(browser, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"_2zCfw")))
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"_2zCfw")))
    # import pdb; pdb.set_trace()
    for recepient in recepients:
        search_input = browser.find_element_by_class_name('_2zCfw')
        search_input.click() #contact search bar

        search_input.clear()
        time.sleep(1)
        search_input.send_keys(recepient['number'])
        time.sleep(5)
        search_input.send_keys('\n')
        try:
            contacts_pane = browser.find_element_by_id('pane-side')
            wait2 = WebDriverWait(browser, 5)
            wait2.until(EC.presence_of_element_located((By.CLASS_NAME,"_13U-5")))
            wait2.until(EC.visibility_of_element_located((By.CLASS_NAME,"_13U-5")))
            contacts_pane.find_element_by_class_name('_13U-5')
            print('no such contact: '+recepient['number']+"skipping")
            messageToSend = WhatsappMessagesToSend.objects.get(name=recepient['name'])
            messageToSend.status = "3"
            messageToSend.save()
            continue
            
        except TimeoutException:

            message_input = browser.find_element_by_class_name('_3u328')
            message_input.send_keys('testing\n')

            menu_button = browser.find_element_by_css_selector('div[title=Attach]')
            menu_button.click()

            if os.path.exists(recepient['path']):
                attach_document_button  = browser.find_elements_by_class_name('Ijb1Q')[2]
                file_input = attach_document_button.find_element_by_css_selector('[type=file]')
                browser.execute_script('arguments[0].style = ""; arguments[0].style.display = "block"; arguments[0].style.visibility = "visible";', file_input)
                print("path: "+recepient['path'])
                file_input.send_keys(recepient['path'])
                wait.until(EC.presence_of_element_located((By.CLASS_NAME,"_1g8sv")))
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"_1g8sv")))
                send_button = browser.find_element_by_class_name('_1g8sv')
                browser.execute_script("arguments[0].scrollIntoView();", send_button)
                send_button.click()
                time.sleep(5)
            messageToSend = WhatsappMessagesToSend.objects.get(name=recepient['name'])
            messageToSend.status = "5"
            messageToSend.save()
        browser.quit()


if __name__ == "__main__":
    send_messages(test_recepients)

