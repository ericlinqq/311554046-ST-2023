from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

# install webdriver for edge and use it
options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_experimental_option("detach", True)
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

# navigate to NYCU home page
print("Navigating to NYCU home page...")
driver.get("https://www.nycu.edu.tw")

# maximize the window size
print("Maximizing window size...")
driver.maximize_window()

# find and press the "新聞" button
print("Finding \"新聞\" button...")
news_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "新聞")))
assert news_button.text == "新聞"
print("Click the button...")
news_button.click()

# find and press the first news
print("Finding the first news...")
first_news_column = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "su-post")))
first_news_button = first_news_column.find_element(By.TAG_NAME, 'a')
assert first_news_button.text == "伊利諾大學訪問陽明交大，關心醫師工程師與醫學電資組人才培育"
print("Click the first news...")
first_news_button.click()

# find and print the title of the news
print("Finding and printing the title...")
title = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.TAG_NAME, 'h1'))
# find the search button and click it
print("Title:")
print(title.text)
print()

# find and print the content of the news
print("Finding and print the content...")
content_div = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME, "entry-content.clr"))
content = content_div.find_elements(By.TAG_NAME, 'p')
print("Content:")
for paragraph in content:
    print(paragraph.text)
print()

# open a new tab and switch to it
print("Opening a new tab and switching to it...")
assert len(driver.window_handles) == 1
driver.switch_to.new_window('tab')

# navigate to google
print("Navigating to google...")
driver.get("https://www.google.com")

# find the search bar and search student ID
print("Finding the search bar and input student ID...")
search_bar = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CLASS_NAME, "gLFyf"))
search_bar.send_keys("311554046")
search_bar.send_keys(Keys.ENTER)

# find the second result and print its title
print("Finding the second search result and print its title...")
result = WebDriverWait(driver, 10).until(lambda d: d.find_elements(By.TAG_NAME, 'h3'))
print(result[1].text)

# close the browser
print("Closing the browser")
driver.quit()
