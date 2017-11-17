import requests
from bs4 import BeautifulSoup
from utils import get_request_headers
from db import Mdb
from config import *


class Php:
    def __init__(self):
        self.mdb = Mdb()

    def scrap_result_row(self, div):
        print "<<=================================PHP>>"
        ################################
        #       Company title          #
        ################################
        title = ''
        span = div.find('span', class_='company')
        if span:
            title = span.text.strip()
            print "company title: %s" % title
        else:
            print "company title: %s" % span

        ################################
        #       Company location       #
        ################################
        span = div.find('span', class_='location')
        location = span.text.strip()

        print "company Location: %s" % location

        ################################
        #       Company salary         #
        ################################
        salary = ''
        span = div.find('span', class_='no-wrap')
        if span:
            salary = span.text.strip()
            print "Salary: %s" % salary
        else:
            print "salary: %s" % span

        ################################
        #       Company summary        #
        ################################
        span = div.find('span', class_='summary')
        summary = span.text.strip()

        print "Summery: %s" % summary

        self.mdb.add_vacancy(title, location, salary, summary)

    def scrap_php_developer(self, url):

        print "\nScrapping Php Developer: %s \n" % url

        r = requests.get(url, headers=get_request_headers())

        if not r.status_code == 200:
            print "Failed to get content of url: %s" % url
            return
        html_doc = r.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        # parsing html content  to fet information about python developer
        # for div in soup.find_all('div', class_='brdr'):
        for div in soup.find_all('div'):
            # ignore divs with classes
            if not div.attrs.has_key('class'):
                continue

            cls = div.attrs['class']
            if 'row' in cls and 'result' in cls:
                self.scrap_result_row(div)
                # break
if __name__ == '__main__':
    php = Php()

    # testing for php data scrapping
    # php.scrap_php_developer()
