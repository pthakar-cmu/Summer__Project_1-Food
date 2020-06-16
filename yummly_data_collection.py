from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time

chrome_driver = r"P:\CMU\Nelson_Project\chromedriver.exe" 
chrome_options = webdriver.ChromeOptions()
browser = webdriver.Chrome(chrome_driver)
current_tab = browser.current_window_handle

def check_element(element):
    global browser
    try:
        browser.find_element_by_xpath(element)
    except NoSuchElementException or StaleElementReferenceException:
        return False
    return True


def check_element_by_class(element):
    global browser
    try:
        browser.find_element_by_class_name(element)
    except NoSuchElementException or StaleElementReferenceException:
        return False
    return True

def add_to_table(df, column_names, input_array):
    df = df.append({column:value for column, value in zip(column_names, input_array)}, ignore_index=True)
    return df

Countries = ['American', 'Kid-Friendly', 'Italian', 'Asian', 'Mexican', 'Southern', 'French', 'Southwestern', 'Barbecue', 'Indian',\
             'Chinese', 'Cajun', 'Mediterranean', 'Greek', 'English', 'Spanish', 'Thai', 'German', 'Moroccan', 'Irish', 'Japanese', \
             'Cuban', 'Hawaiian', 'Swedish', 'Hungarian', 'Portuguese']

search_space = ['American', 'Kid-Friendly', 'Italian', 'Asian', 'Mexican', 'Southern', 'French', 'Southwestern', 'Barbecue', 'Indian',\
                'Chinese', 'Cajun', 'Mediterranean', 'Greek', 'English', 'Spanish', 'Thai', 'German', 'Moroccan', 'Irish', 'Japanese', 'Cuban', \
                'Hawaiian', 'Swedish', 'Hungarian', 'Portuguese', 'Gluten-Free', 'Peanut-Free', 'Seafood-Free', 'Sesame-Free', 'Soy-Free', \
                'Dairy-Free', 'Egg-Free', 'Sulfite-Free', 'Tree', 'Wheat-Free', 'Ketogenic', 'Vegetarian', 'Vegetarian', 'Pescetarian', \
                'Vegan', 'Low', 'Vegetarian', 'Paleo', 'Alcohol', 'Avocado', 'Bacon', 'Bananas', 'Beef', 'Brussels', 'Cilantro', 'Coconut',\
                'Eggplant', 'Fish', 'Mayonnaise', 'Mushrooms', 'Olives', 'Onions', 'Pork', 'Potatoes', 'Seafood', 'Shrimp', 'Sugar', 'Tomatoes']

column_names = ["Type", "Name", "Number of Ingredients", "Time to Make", "Calories", "Ingredients", "Nutrition", "Tags", "Number of Ratings", "URL"]
df = pd.DataFrame(columns = column_names)

Countries_Food = [[] for _ in range(len(Countries))]
for i in range(len(Countries)):
    url = 'https://www.yummly.com/recipes?q=' + Countries[i].lower() + '&taste-pref-appended=true'
    browser.get(url)

    time.sleep(1)
    if check_element('//*[@id="mainApp"]/div[2]/div/div/span'):
        browser.find_element_by_xpath('//*[@id="mainApp"]/div[2]/div/div/span').click()

    start = time.time()
    seconds = 0
    while seconds<90:
        if check_element_by_class('structured-data-info'):
            target = browser.find_element_by_class_name('structured-data-info')
            browser.execute_script('arguments[0].scrollIntoView(true);', target)
        time.sleep(0.5)
        now = time.time()
        seconds = now - start

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    Food_Titles = soup.find_all("a",{'class':'card-title p2-text font-normal'}, href=True)
    links = []
    for x in Food_Titles:
        Countries_Food[i].append(x.get_text()) 
        links.append(x['href'])

    for link in links:
        url_food = 'https://www.yummly.com' + link
        no_ingredients, time_to_make, calories, no_ratings, ingredients, nutrition, tags = 'N/A', 'N/A', 'N/A', 'N/A', [], [], []
        script = 'window.open("{}");'.format(url_food)
        browser.execute_script(script)
        new_tab = [tab for tab in browser.window_handles if tab != current_tab][0]
        browser.switch_to.window(new_tab)

        browser.get(url_food) 
        time.sleep(0.5)

        if check_element('//*[@id="mainApp"]/div[2]/div/div/span'):
            browser.find_element_by_xpath('//*[@id="mainApp"]/div[2]/div/div/span').click()
        
        if check_element(".//div[contains(@class,'recipe-summary-item  h2-text')]"):
            try:
                no_ingredients = browser.find_element_by_xpath(".//div[contains(@class,'recipe-summary-item  h2-text')]").text.split('\n')[0]
            except StaleElementReferenceException:
                pass

        if check_element(".//div[contains(@class,'recipe-summary-item unit h2-text')]"):
            try:
                time_to_make = browser.find_element_by_xpath(".//div[contains(@class,'recipe-summary-item unit h2-text')]").text.split('\n')[0]
            except StaleElementReferenceException:
                pass

        if check_element(".//div[contains(@class,'recipe-summary-item nutrition h2-text')]"):
            try:
                calories = browser.find_element_by_xpath(".//div[contains(@class,'recipe-summary-item nutrition h2-text')]").text.split('\n')[0]
            except StaleElementReferenceException:
                pass

        if check_element(".//div[contains(@class,'shopping-list-ingredients')]"):
            ingredients_class =  browser.find_element_by_xpath(".//div[contains(@class,'shopping-list-ingredients')]")
            if ingredients_class:
                try:
                    ingredients_tags = ingredients_class.find_elements_by_tag_name('li')
                except StaleElementReferenceException:
                    pass
                if ingredients_tags:
                    try:
                        ingredients = [i.text for i in ingredients_tags]
                    except StaleElementReferenceException:
                        pass

        if check_element(".//div[contains(@class,'recipe-nutrition')]"):
            nutrition =  browser.find_elements_by_xpath(".//div[contains(@class,'recipe-nutrition')]")
            if nutrition:
                try:
                    nutrition = [i.text.split('\n') for i in nutrition][0]
                except StaleElementReferenceException:
                    pass
                 
        if check_element(".//ul[contains(@class,'recipe-tags')]"):
            tags =  browser.find_elements_by_xpath(".//ul[contains(@class,'recipe-tags')]")
            if tags:
                try:
                    tags = [i.text.split('\n') for i in tags][0]
                except StaleElementReferenceException:
                    pass
        
        if check_element(".//span[contains(@class,'font-number font-normal p3-text')]"):
            no_ratings = browser.find_element_by_xpath(".//span[contains(@class,'font-number font-normal p3-text')]").text
  

        input_values = [Countries[i], Countries_Food[i][links.index(link)], no_ingredients, time_to_make, calories, ingredients, nutrition, tags, no_ratings, url_food]
        df = add_to_table(df, column_names, input_values)
        browser.close()
        browser.switch_to_window(current_tab)

df.to_csv('full_data_countries_2.csv')
browser.quit()


