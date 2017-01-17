#!/usr/bin/env python
# -*- coding: cp1252 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import time


def reserva(univ, data, hour, minuto, duracao, nodes):  # , reserve_nodes):

    #data = "2016-12-16"
    #hour = "22"
    #minuto = "30"
    #duracao = "1"
    #num = "8"
    driver = webdriver.PhantomJS(executable_path='/home/victor/phantomjs/bin/phantomjs')
    driver.get("https://portal." + univ + ".fibre.org.br/LS-WEB/index.php")
    print "Acessando a url: " + "https://portal." + univ + ".fibre.org.br/LS-WEB/index.php"
    time.sleep(3)
    driver.find_element_by_name("username").send_keys("victor")
    driver.find_element_by_name("password").send_keys("familia061293")
    driver.find_element_by_name("sbmt_login").click()
    print "Efetuando o login..."
    time.sleep(5)
    print "Acessando reservas pela url: " + driver.current_url + "acessada"
    # driver.find_element_by_name("start_date").send_keys("2016-12-04")
    # driver.find_element_by_name("shour").send_keys("22")
    # driver.find_element_by_name("smin").send_keys("00")
    # driver.find_element_by_name("duration").send_keys("1")
    driver.find_element_by_xpath(r"""//a[@onclick="document.f.start_date.value='""" + data + """';"]""").click()
    #selecionar hora e duração
    Select(driver.find_element_by_name("shour")).select_by_visible_text(hour)
    Select(driver.find_element_by_name("smin")).select_by_visible_text(minuto)
    Select(driver.find_element_by_name("duration")).select_by_visible_text(duracao)

    driver.find_element_by_xpath("//input[@value='Check Available Nodes']").click()
    time.sleep(5)

    #driver.find_element_by_xpath("//input[@name='book_resources[]']").click()
    #driver.find_element_by_xpath("(//input[@name='book_resources[]'])[2]").click()
    #driver.find_element_by_xpath("(//input[@name='book_resources[]'])[3]").click()

    #if encontra(driver, node1) == False:
        #raise ValueError

    for node in nodes:
        if encontra(driver, node) == False:
         raise ValueError

    print "Reservando nodes..."
    driver.find_element_by_xpath("//input[@value='Reserve']").click()
    print "Reservado"
    driver.close()

def encontra(driver, num):
    try:
        driver.find_element_by_xpath("""//input[@name='book_resources[]' and @value='""" + num + """']""")
    except NoSuchElementException:
        return False
    return driver.find_element_by_xpath("""//input[@name='book_resources[]' and @value='""" + num + """']""").click()