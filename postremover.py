#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from datetime import datetime
import selenium.common.exceptions as exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions


class PostRemover:
    def __init__(self, username, mode, browser):
        self.username = str(username)
        self.url_posts = f'https://www.reddit.com/user/{self.username}'
        self.url_comments = self.url_posts + '/comments'
        self.driver_option = str(browser).upper()
        self.debug_port_chrome = 9222
        self.debug_port_firefox = 2828

        if mode == 'p':
            self.main_url = self.url_posts
        elif mode == 'c':
            self.main_url = self.url_comments

        if self.driver_option == 'C':
            self.__consoleLog(0, 'Using Chrome')
            chrome_options = ChromeOptions()
            chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.debug_port_chrome}")
            self.driver = webdriver.Chrome(options=chrome_options)
        elif self.driver_option == 'F':
            self.__consoleLog(0, 'Using Firefox')
            service_options = Service(service_args=[
                '--marionette-port',
                str(self.debug_port_firefox),
                '--connect-existing'
            ])
            self.driver = webdriver.Firefox(service=service_options)
        else:
            self.__consoleLog(3, 'Missing driver option')
            sys.exit(1)

    def deletePost(self):
        def nuke():
            """
            1. Find and click the delete button
            2. Find and click the confirmation button
            If you have a slower internet connection, I suggest to modify the sleep timers.
            :return: No return
            """
            time.sleep(0.2)
            button_delete = driver.find_element(By.XPATH, '//span[.="delete"] '
                                                          '| //i[contains(@class, "icon-delete")]')
            button_delete.click()
            button_confirm = driver.find_element(By.XPATH, '//button[.="Delete"] | //button[.="Delete post"]')
            button_confirm.click()
            time.sleep(0.8)

        error = False
        driver = self.driver
        driver.switch_to.new_window('tab')
        driver.get(self.main_url)

        # check routine
        self.__checkUsernameExist()
        self.__checkLogin()
        self.__checkCurrentUsername()

        # deleting all comments and posts
        while True:
            try:
                # looking for the button with the three dots (...)
                button_more = driver.find_element(By.XPATH, "//i[contains(@class,'icon-overflow_horizontal')]")
            except exceptions.NoSuchElementException:
                # if the button doesn't exist anymore, we're done
                self.__consoleLog(1, 'Done deleting all posts')
                break
            try:
                button_more.click()
                nuke()
            except (exceptions.NoSuchElementException,
                    exceptions.StaleElementReferenceException,
                    exceptions.ElementClickInterceptedException):
                if error:
                    # if the error appears more than once, we're reloading the page
                    error = False
                    self.__consoleLog(1, 'Reloading page')
                    driver.get(self.main_url)
                else:
                    # sometimes an element we want to access isn't available in the initial instance
                    # we just skip it for now
                    error = True
                    self.__consoleLog(2, 'Element not found or stale exception')
                    pass

    def __checkLogin(self):
        try:
            self.driver.find_element(By.XPATH, '//i[contains(@class, "icon-user")]')
            self.__consoleLog(3, "You're not logged in")
            sys.exit(2)
        except exceptions.NoSuchElementException:
            self.__consoleLog(1, "You're logged in")

    def __checkUsernameExist(self):
        try:
            self.driver.find_element(By.XPATH, '//img[contains(@src, "snoo_thoughtful.png")]')
            self.__consoleLog(3, "User doesn't exists")
            sys.exit(1)
        except exceptions.NoSuchElementException:
            self.__consoleLog(1, "User exists")

    def __checkCurrentUsername(self):
        try:
            found_username = self.driver.find_element(By.XPATH, '//*[@id="email-collection-tooltip-id"]/span/span[1]')
            found_username = found_username.get_attribute('innerHTML').lower()
            initial_username = self.username.lower()

            if initial_username == found_username:
                self.__consoleLog(1, "You're logged into the right account")
            else:
                self.__consoleLog(3, "You're not logged into the right account")
                sys.exit(3)
        except exceptions.NoSuchElementException:
            self.__consoleLog(3, "You're not logged in")
            sys.exit(3)

    @staticmethod
    def __consoleLog(level, msg):
        level_dict = {
            0: 'DEBUG',
            1: 'INFO',
            2: 'WARN',
            3: 'ERROR'
        }
        ts = datetime.now().strftime('%y-%m-%d %H:%M:%S.%f')
        out = f'{ts} [{level_dict[level]}]: {msg}'
        print(out)
