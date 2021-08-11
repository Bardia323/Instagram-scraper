from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime

def login(webdriver):
    webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    sleep(3)
    username = webdriver.find_element_by_name('username')
    username.send_keys('psychonartists')
    sleep(1)
    password = webdriver.find_element_by_name('password')
    password.send_keys('Ensmsscdb123')
    sleep(2)
    """ try:
        button_login = webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button')
        try:
            notnow = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
            notnow.click()
        except:
            pass
        button_login.click()
    except:
        webdriver.find_element_by_css_selector("#react-root > section > main > article > div > div > div > form > div:nth-child(7) > button > div").click()
        sleep(2)
        try:
            webdriver.find_element_by_css_selector("#react-root > section > main > div > button").click()
        except:
            sleep(3)
            webdriver.find_element_by_css_selector("#react-root > section > main > div > button").click()

        sleep(2)
        webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm").click()
    sleep(4) """

    
