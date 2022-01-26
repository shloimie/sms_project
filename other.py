import re

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


class Gmessage():
    def __init__(self):
        self.part = "?itemId=t.%2B"
        self.google_account = "1"
        self.link = "https://voice.google.com/u/"+self.google_account+"/messages"
        self.unread_numbers = []
        options = Options()
        # options.add_argument('--profile-directory=Profile 1')
        options.add_argument('--profile-directory=Default')
        options.add_argument("user-data-dir=C:\\Users\\hshlo\\AppData\\Local\\Google\\Chrome\\User Data\\")
        options.add_argument("--window-size=1920,1080")
        # options.add_argument("--headless")
        f = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=f, options=options)

    def sleep(self, tim=3):
        time.sleep(tim)

    def send_text(self, number, text):
        self.driver.get(self.link)
        self.sleep()
        new_contact = self.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div[2]/div[2]/div/gv-messaging-view/div/div/md-content/div/div/div')
        new_contact.click()
        self.sleep(1)
        to = self.driver.find_element(By.ID, "input_0")
        to.click()
        to.send_keys(number, Keys.ENTER)
        self.sleep(1)
        message = self.driver.find_element(By.ID, "input_1")
        message.click()
        message.send_keys(text, Keys.ENTER)

    def get_unread_numbers(self):
        self.driver.get(self.link)
        self.sleep()
        conversation_selector = self.driver.find_elements(By.CLASS_NAME, "rkljfb-H9tDt")
        new_messages = []
        for convo in conversation_selector:
            color = convo.value_of_css_property("color")
            if color == "rgba(32, 33, 36, 1)":
                new_messages.append(convo.text)
                print("added new convo to new messages")
        a = self.clean_up(new_messages)
        print(a)


    def clean_up(self,els):
        final = []
        for thing in els:
            print(f"cleaning up {thing}")
            e = thing.split("\n")
            main,new,i = [],[],0
            for t in e:
                i += 1
                new.append(t)
                if i > 2:
                    main.append(new)
                    #reset
                    new ,i = [] ,0
            for thing in main:
                new_char = ""
                for char in thing[0]:
                    if char not in ["+", "-", " ", "\u202a", "\u202c","(",")"]:
                        new_char += char
                main[main.index(thing)][0] = new_char
                final.append(main)
        final = [final[0][0], final[1][0]]
        # final2 = [final[0][0][0], final[1][0][0]]
        print(f"final is {final}")
        # print(f"final2 is {final2}")
        return final

    def read_texts(self,number):
        if number[0] != "1":
            number = "1" + number
        self.driver.get(self.link + self.part + number)
        self.sleep()
        aclass= "ZRgO8c-PWtBwb ZRgO8c-MJZihc"

    def close(self,u=0):
        self.sleep(5+u)
        self.driver.quit()





