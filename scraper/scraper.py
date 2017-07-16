
from config import *
from db import Mdb
from python import Python
from android import Android
from php import Php
from utils import sleep_scrapper, txt_write
from multiprocessing import Process
import os
import traceback


class Scrapper:

    def __init__(self):
        self.mdb = Mdb()
        self.python = Python()
        self.android = Android()
        self.php = Php()

    def scrap_python_developer(self):
        # scrap python Developer in mohali
        dir_path = os.path.realpath(__file__)
        file_data = "%s/%s" % (dir_path, PROGRESS_PYTHON)

        if not os.path.isfile(file_data):
            print("Error: %s file not found" % file_data)
            txt_write(PROGRESS_PYTHON, "10")

        print("file is exist %s ..." % file_data)
        f = open(PROGRESS_PYTHON, "r")
        i = int(f.readline())

        base_url = "https://www.indeed.co.in/jobs?q=python+developer&l=Mohali%2C+Punjab&start="
        for j in range(i, 100, 10):
            try:
                python_url = base_url + str(j)
                self.python.scrap_python_developer(python_url)

                # update scrapping progress in Python progress file
                txt_write(PROGRESS_PYTHON, str(j))

                # sleep scrapper for a while
                sleep_scrapper("Python-Scrapper")

            except Exception as exp:
                print "scrap_python_developer() :: Got exception: %s" %exp
                print(traceback.format_exc())

    def scrap_android_developer(self):
        dir_path = os.path.realpath(__file__)
        file_data = "%s/%s" % (dir_path, PROGRESS_ANDROID)

        if not os.path.isfile(file_data):
            print("Error: %s file not found" % file_data)
            txt_write(PROGRESS_ANDROID, "10")

        print("file is exist %s ..." % file_data)
        f = open(PROGRESS_ANDROID, "r")
        i = int(f.readline())
        base_url = "https://www.indeed.co.in/jobs?q=android+developer&l=Mohali%2C+Punjab&start="

        for j in range(i, 100, 10):
            try:
                android_url = base_url + str(j)
                self.android.scrap_android_developer(android_url)

                # update scrapping progress in Android progress file
                txt_write(PROGRESS_ANDROID, str(j))

                # sleep scrapper for a while
                sleep_scrapper("Android-Scrapper")
            except Exception as exp:
                print "scrap_android_developer() :: Got exception: %s" % exp
                print(traceback.format_exc())

    def scrap_php_developer(self):

        base_url = "https://www.indeed.co.in/jobs?q=php+developer&l=Mohali%2C+Punjab&start="
        for i in range(10, 100, 10):
            try:
                php_url = base_url + str(i)
                self.php.scrap_php_developer(php_url)

                sleep_scrapper("Php-Scrapper")
            except Exception as exp:
                print "scrap_php_developer() :: Got exception: %s" % exp
                print(traceback.format_exc())


if __name__ == '__main__':
    scrapper = Scrapper()

    p1 = Process(target=scrapper.scrap_python_developer)
    p1.start()
    p2 = Process(target=scrapper.scrap_android_developer)
    p2.start()
    p3 = Process(target=scrapper.scrap_php_developer)
    p3.start()

