from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_experimental_option("detach", True)
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install(), options=options))

driver.get("https://docs.python.org/3/tutorial/index.html")

select =  WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, 'language_select'))
lang_sel = Select(select)
lang_sel.select_by_value('zh-tw')
title = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.TAG_NAME, 'h1'))
print(title.text)

first_paragraph = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.TAG_NAME, 'p'))
print(first_paragraph.text)


