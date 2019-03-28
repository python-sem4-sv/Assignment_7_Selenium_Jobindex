import bs4
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_info(name):
    base_url = 'https://www.jobindex.dk'
    browser = webdriver.Chrome()
    browser.get(base_url)
    browser.implicitly_wait(3)
    
    search_field = browser.find_element_by_name('qs')
    search_field.send_keys(name)
    search_field.submit()

    email_subscription = browser.find_element_by_class_name("close")
    email_subscription.click()
    
    page_source = browser.page_source
    browser.close()
    soup = bs4.BeautifulSoup(page_source, 'html.parser')
    event_cells = soup.find_all('div', {'class': 'checkbox-holder'})

    entries = {}
    for e in event_cells:
            if len(e.select(".area_label")) is not 0:
                region_unparsed = e.select(".area_label")[0].text
                
                region = re.compile(r'([a-zA-ZæøåÆØÅ]+)(\d+)')
                r1 = region.search(region_unparsed)
                entries[r1.group(1)] = int(r1.group(2))

    return entries
