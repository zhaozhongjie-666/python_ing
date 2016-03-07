#coding:utf-8

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
driver = webdriver.Firefox()

driver.get('http://exmail.qq.com/login')

test_user = {
'username': 'XXX',
'password': 'XXX',
}
#模拟表单输入账号名密码
user = driver.find_element(By.XPATH, '//input[@id="inputuin"]')
user.send_keys(test_user['username'])
time.sleep(1)
password = driver.find_element(By.XPATH, '//input[@id="pp"]')
password.send_keys(test_user['password'])
time.sleep(1)
btnSubmit = driver.find_element(By.XPATH, '//input[@id="btlogin"]')
btnSubmit.click()
