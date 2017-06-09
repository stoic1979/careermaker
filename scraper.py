import requests
from bs4 import BeautifulSoup
from utils import get_request_headers
from config import *
from db import Mdb


class Scrapper:
    def __init__(self):
        self.mdb = Mdb(DB_HOST, DB_PORT, AUTH_DB_NAME,
                       DB_NAME, DB_USER, DB_PASS)

    def scrap_python_developer(self):
        # scrap python Developer in mohali
        python_url = "https://www.indeed.co.in/" \
                     "jobs?q=python+developer&l=Mohali%2C+Punjab"

        self.scrap_developer(python_url)

    def scrap_result_row(self, div):

        title = div.find('span', class_='company').text.strip()
        print "company title: %s" % title

        span = div.find('span', class_='location')
        location = span.text.strip()

        print "company Location: %s" % location

        salary = ''
        span = div.find('span', class_='no-wrap')
        if span:
            salary = span.text.strip()
            print "Salary: %s" % salary
        else:
            print "salary: %s" % span

        span = div.find('span', class_='summary')
        summary = span.text.strip()

        print "Summery: %s" % summary

        self.mdb.add_vacancy(title, location, salary, summary)

    def scrap_developer(self, url):
        print "\nScrapping python Developer: %sdb.mycol.find() \n" % url

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
    scrapper = Scrapper()
    scrapper.scrap_python_developer()
