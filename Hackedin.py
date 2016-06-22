__author__ = 'vikram modifying harithans code'
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
user = 'username here'
passw = 'password here'


class Automaton:

    def __init__(self):
        self.links = []
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('https://www.linkedin.com')
        self.username = self.driver.find_element_by_id('login-email')
        self.password = self.driver.find_element_by_id('login-password')
        self.submit_button = self.driver.find_element_by_name('submit')
        self.username.send_keys(user)
        self.password.send_keys(passw)
        self.submit_button.submit()

    def getFirstSearchLink(self, searchString):
        self.searchStr = searchString.replace(' ', '+')
        self.driver.get('https://www.linkedin.com/vsearch/f?type=all&keywords='+ self.searchStr + '&orig=GLHD&rsid=548370671466554148033&pageKey=voltron_federated_search_internal_jsp&trkInfo=&search=Search')
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, 'results_count')))
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.link = self.soup.find(attrs={'class': 'title main-headline'})['href']
        return self.link

    def loopThroughLinks(self):
        self.driver.get(self.link)
        WebDriverWait(self.driver, 15).until(ec.presence_of_element_located((By.ID, 'control_gen_4')))
        self.soup = BeautifulSoup(self.driver.page_source, 'xml')
        try:
            self.ul = self.soup.find(attrs={'class': 'browse-map-list'})
            self.a = self.ul.findAll('a')
            z = randint(0,7)*2 + 1
            self.links.append(self.a[z]['href'])
            print self.links[-1]
            self.link = self.links[-1]
        except AttributeError:
            self.link = self.links[-2]
            del self.links[-1]
            print'Oops blacklisted by linkedIn if this message repeats more than twice'
        except IndexError:
            pass
        except :
            self.link = self.links[-2]
            print'Oops blacklisted by linkedIn if this message repeats more than twice'

x = 1
drv1 = Automaton()
drv2 = Automaton()
print drv1.getFirstSearchLink("software recruiter NYC")
print drv2.getFirstSearchLink("software recruiter San Diego")
while 1:
    print x, ": 1"
    x += 1
    drv1.loopThroughLinks()
    x += 1
    print x, ": 2"
    drv2.loopThroughLinks()