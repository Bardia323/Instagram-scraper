from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from pywinauto.application import Application
from Login import login


chromedriver_path = 'C:/Users/bardi/chromedriver.exe'
mobile_emulation = { "deviceName": "Pixel 2" }
mobile_options = webdriver.ChromeOptions()
mobile_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = None;

def click(element, driver = driver):
    driver.find_element_by_css_selector(element).click()

def clickPostButton(driver):
    driver.find_element_by_css_selector("#react-root > section > nav.NXc7H.f11OC > div > div > div.KGiwt > div > div > div.q02Nz._0TPg > span").click()


def resolveFilePrompt(filepathToImg):
    app = Application().connect(title = "Open")
    app.Open["Edit"].type_keys(filepathToImg)
    app.Open["Open"].click()

def expandImage(driver):
    driver.find_element_by_css_selector("#react-root > section > div.gH2iS > div.N7f6u.Bc-AD > div > div > div > button.pHnkA > span").click()

def post(driver):
    driver.find_element_by_css_selector("#react-root > section > div.Scmby > header > div > div.mXkkY.KDuQp > button").click()

def writeCaption(driver, caption):
    driver.find_element_by_css_selector("#react-root > section > div.A9bvI > section.IpSxo > div.NfvXc > textarea").send_keys(caption)

def clickAddLocation(driver):
    driver.find_element_by_css_selector("#react-root > section > div.A9bvI > section:nth-child(3) > button > span._7xQkN").click()

def chooseLocation(driver, location):
    driver.find_element_by_css_selector("#react-root > div > div.S9b6j > input").send_keys(location)
    sleep(1)
    locs = driver.find_elements_by_css_selector("#react-root > div > div:nth-child(3) > div > div > button")
    for button in locs:
        if (button.text == location):
            button.click()
            break
        else:
            driver.find_element_by_css_selector("#react-root > div > div.Scmby > header > div > div.mXkkY.HOQT4 > button > svg > path").click()
            sleep(1)
            pass

def share(driver):
    try:
        driver.find_element_by_css_selector("#react-root > section > div.Scmby > header > div > div.mXkkY.KDuQp ").click()
    except: 
        sleep(3)
        e = driver.find_element_by_css_selector("#react-root > section > div.Scmby > header > div > div.mXkkY.KDuQp > button")
        e.click()



APPQ = "body > div.RnEpo.xpORG._9Mt7n > div > div.YkJYY > div > div:nth-child(5) > button"
def postImage(filepathToImg, location = None,caption = None, driver = None):
    if(driver == None):
        driver = webdriver.Chrome(executable_path=chromedriver_path ,desired_capabilities = mobile_options.to_capabilities())
    login(driver)
    clickPostButton(driver)
    sleep(2)
    click(APPQ,driver)
    sleep(1)
    resolveFilePrompt(filepathToImg)
    sleep(2)
    expandImage(driver)
    sleep(1)
    post(driver)
    sleep(1)
    if(caption != None):
        writeCaption(driver,caption)
        driver.find_element_by_css_selector("body").click()
        sleep(1)    
    if(location != None):
        clickAddLocation(driver)
        sleep(1)
        chooseLocation(driver, location)
    return driver

