from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chromedriver_path = 'C:/Users/bardi/chromedriver.exe' # Change this to your own chromedriver path!
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

def getNomadList(webdriver):
    webdriver.get("https://nomadlist.com/")
    
webdriver.find_element_by_css_selector("#search").send_keys(location)
webdriver.find_element_by_css_selector("#search").send_keys(Keys.ENTER)