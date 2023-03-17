from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

driver.get("https://www.nycu.edu.tw")
driver.maximize_window()

