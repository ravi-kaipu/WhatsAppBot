#-------------------------------------------------------------------------------
# Name:        WhatsAppBot
# Purpose:
#
# Author:      Ravi Kaipu
#
# Created:     21-12-2019
# Copyright:   (c) Ravi Kaipu, ravi.rgukt.in@gmail.com 2019
#-------------------------------------------------------------------------------
import time
import threading
import re

from datetime import datetime
from chatbot import ChatBot
from selenium import webdriver

class WhatsAppBot():

    users_action = {}

    waiting_time = 60*30

    #phone number of user
    mynumber = None

    chrome_driverpath = "C:\\Users\\ekairav\\Downloads\\chromedriver_win32\\chromedriver.exe"

    @staticmethod
    def get_current_time():
        """
        Get current local time
        """
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    @staticmethod
    def onblur_action(driver):
        user = WhatsAppBot.finduser(driver, WhatsAppBot.mynumber)
        if user:
            user.click()

    @staticmethod
    def finduser(driver, username):
        username = username.strip()
        tag_search = '//span[@title="{}"]'.format(username)
        try:
            user = driver.find_element_by_xpath(tag_search)
        except:
            #print("{} name doesn't exist.".format(username))
            return None
        else:
            return user

    def send_user_message(driver, user, message, n_times = 1):
        user.click()
        try:
            message_box = driver.find_element_by_class_name('_13mgZ')
        except:
            return -1
        else:
            for i in range(n_times):
                if not message:
                    print ("Message is empty...")
                    return -1
                message_box.clear()
                message_box.send_keys(message)
        try:
            button = driver.find_element_by_class_name('_3M-N-')
        except:
            return -1
        else:
            button.click()
        return 0

    def send_message(driver, username, message, n_times = 1):
        user = WhatsAppBot.finduser(driver, username)
        if not user:
            return -1

        user.click()

        try:
            message_box = driver.find_element_by_class_name('_13mgZ')
        except:
            return -1
        else:
            for i in range(n_times):
                if not message:
                    print ("Message is empty...")
                    return -1
                message_box.clear()
                message_box.send_keys(message)
        try:
            button = driver.find_element_by_class_name('_3M-N-')
        except:
            return -1
        else:
            button.click()

        print ("{} >> {} << has been sent to {}\n".format(WhatsAppBot.get_current_time(), message, username))
        return 0

    @staticmethod
    def extract_time(st):
        s = re.search(r'(\d+):(\d+), (\d+)/(\d+)/(\d+)', st)
        if s:
            tm = datetime(int(s.group(5)), int(s.group(3)), int(s.group(4)), int(s.group(1)), int(s.group(2)), 0)
            return tm
        return datetime.now()

    @staticmethod
    def get_unread_messages(driver):
        unread_messages = []
        unread_messages = driver.find_elements_by_class_name("X7YrQ")
        unread_messages_dict = {}
        for unread_user in unread_messages:
            try:
                contacttype = unread_user.find_element_by_class_name("B9BIa")
            except:
                continue
            else:
                ty = contacttype.find_element_by_css_selector("span")
                if not "default-user" in ty.get_attribute("data-icon"):
                    continue
            try:

                user = unread_user.text.split('\n')[0]
                if re.search(r'(\d+):(\d+)', user):
                    continue
            except:
                continue
            try:
                unread_msg_count= int(unread_user.find_element_by_class_name("P6z4j").text)
            except:
                continue
            else:
                lastmsg = unread_user.find_element_by_class_name("_0LqQ").text
                unread_messages_dict[user] = (unread_msg_count, lastmsg)
        return unread_messages_dict

    @staticmethod
    def scheduled_send(driver, message, schedtime, users=[]):
        print("Schduled message started executing....")
        while True:
            current_time = datetime.now()
            if (((current_time - schedtime).total_seconds()) >= 0):
                for user in users:
                    WhatsAppBot.send_message(driver, user, message)
                break
            time.sleep(10)

    @staticmethod
    def scheduled_message(driver):
        message = "Happy new year"
        users = ["Satish Davala"]
        sched_time = datetime(2019, 12, 31, 10, 41, 00)
        t = threading.Thread(target=scheduled_send, args=(driver, message, sched_time, users), daemon=True)
        t.start()

    @staticmethod
    def filter_messages(driver, unread_msgs):
        all_messages = []
        for msg in unread_msgs:
            try:
                m = msg.find_element_by_class_name("copyable-text")
            except:
                continue
            else:
                tm = WhatsAppBot.extract_time(m.get_attribute("data-pre-plain-text"))
                user = re.search(r'(\d+):(\d+), (\d+)/(\d+)/(\d+)]\s+(.*):', m.get_attribute("data-pre-plain-text")).group(6)
                mesg = m.text
                all_messages.append((mesg, tm, user.strip()))
        return all_messages

    @staticmethod
    def respond_to_messages(driver, mesgs):
        print("respond_to_messages")
        chatbot = ChatBot()

        for msgt in mesgs:
            msg = msgt[0]
            username = msgt[2]
            answer = chatbot.estimate_answer(msg.lower())
            print(msg, "---->", answer, " :::::: ", username)
            WhatsAppBot.send_message(driver, username, answer)

    @staticmethod
    def frame_timestamp(msg):
        ss = re.search(r'(\d+):(\d+)', msg)
        ts = None
        if ss or lastmsg == "yesterday":
            tm = datetime.now()
            if ss:
                ts = datetime(tm.year, tm.month, tm.day, int(ss.group(1)), int(ss.group(2)), 0)
                return ts
            return datetime(tm.year, tm.month, tm.day-1, 0, 0, 0)
        return None

    @staticmethod
    def get_all_messages(driver, user):
        #user.click()
        driver.execute_script("arguments[0].click();", user)
        unread_msgs = driver.find_elements_by_class_name("FTBzM")
        return unread_msgs

    @staticmethod
    def get_last_message(messages):
        message = None
        last = len(messages)-1
        if ("message-in" in messages[last].get_attribute("class")):
            message = messages[last]
            return message
        else:
            return None

    @staticmethod
    def kill_autobot(messages):
        for msg in messages:
            quest = msg[0].strip()
            if quest.lower() == "kill chatbot":
                return True
        return False

    @staticmethod
    def trigger_user_autobot(driver, user):
        print("trigger_user_autobot:{}".format(user))
        WhatsAppBot.send_user_message(driver, user, "Chatbot started... How can I help here? note: type 'kill chatbot' if you want to kill chatbot")
        while True:
            user.click()
            all_messages = WhatsAppBot.get_all_messages(driver, user)
            for last in range(len(all_messages)-1, -1, -1):
                if ("message-out" in all_messages[last].get_attribute("class")):
                    unread_msg_act = all_messages[last+1:]
                    break
            all_unread_messages = WhatsAppBot.filter_messages(driver, unread_msg_act)
            if WhatsAppBot.kill_autobot(all_unread_messages):
                at = WhatsAppBot.users_action.get(user)
                if at:
                    WhatsAppBot.send_user_message(driver, user, "ChatBot is terminated...")
                    del WhatsAppBot.users_action[user]
                WhatsAppBot.onblur_action(driver)
                break
            if all_unread_messages:
                WhatsAppBot.respond_to_messages(driver, all_unread_messages)

            time.sleep(5)

    @staticmethod
    def take_action(driver, user):
        count =  0
        lastmsg = ""

        while True:
            lmsg = WhatsAppBot.get_last_message(WhatsAppBot.get_all_messages(driver, user))
            if lmsg:
                allmsgs = WhatsAppBot.filter_messages(driver, [lmsg])
                if allmsgs:
                    lastmsg = allmsgs[0][0]

            if lastmsg and "yes" in lastmsg.lower():
                break

            if count >= 30:
                break

            count += 1
            time.sleep(2)

        if lastmsg and "yes" in lastmsg.lower():
                WhatsAppBot.trigger_user_autobot(driver, user)
        else:
            del WhatsAppBot.users_action[user]

        print("Exiting as there is no repsonse from  {}".format(user))

    @staticmethod
    def handle_user_thread(driver, user):
        if not WhatsAppBot.users_action.get(user):
            t = threading.Thread(target=WhatsAppBot.take_action, args=(driver, user), daemon=True)
            WhatsAppBot.users_action[user] = t
            t.start()
            print("take_user_separate_action: {}".format(user))
        else:
            print("{} thread is already running....".format(user))

    @staticmethod
    def autobot_action(driver):
        print("Autobot Started")
        message_text = """[CHATBOT]: Hey, I think, you are waiting for the reply for the last 15mins. It seems owner is busy.  \nDo you want me to help you here, if yes, type 'yes' in 60seconds."""
        while True:
            unread_messages = WhatsAppBot.get_unread_messages(driver)
            unread_msg_act = []

            if unread_messages:
                usernames= unread_messages.keys()
                for username in usernames:
                    username = username.strip()
                    lastseenmsg_time = WhatsAppBot.frame_timestamp(unread_messages[username][1])
                    current_time = datetime.now()

                    if lastseenmsg_time and (current_time - lastseenmsg_time).total_seconds() >= WhatsAppBot.waiting_time:
                        user = WhatsAppBot.finduser(driver, username)
                        if not user:
                            continue

                        if not WhatsAppBot.users_action.get(user):
                            WhatsAppBot.send_message(driver, username, message_text)
                            WhatsAppBot.handle_user_thread(driver, user)
            time.sleep(10)

    @classmethod
    def run(cls, autobot = False):
        driver = webdriver.Chrome(executable_path=WhatsAppBot.chrome_driverpath)
        driver.get("https://web.whatsapp.com")
        input("After scan, Press key to start:")

        if autobot:
            cls.autobot_action(driver)


if __name__ == "__main__":
    WhatsAppBot.run(autobot=True)
