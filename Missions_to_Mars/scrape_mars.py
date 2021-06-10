#!/usr/bin/env python
# coding: utf-8
#made some modifications after exported from notebook
# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Scrape [Mars News Site](https://redplanetscience.com) and collect the latest News Title and Paragraph Text
    url = 'https://redplanetscience.com'
    browser.visit(url)

    mars_data = {}

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_data['headline'] = soup.find('div', class_='content_title').text

    mars_data['news'] = soup.find('div', class_='article_teaser_body').text

    browser.quit()

    #Scrape [JPL Mars Space Images](https://spaceimages-mars.com/) and collect the latest Featured Image

    executable_path = {'executable_path': ChromeDriverManager().install()}
    jpl_browser = Browser('chrome', **executable_path, headless=False)
    jpl_url = 'https://spaceimages-mars.com/'
    jpl_browser.visit(jpl_url)
    jpl_html = jpl_browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')


    featured_image = jpl_soup.find('img', class_='headerimage')['src']

    featured_image_url = jpl_url + featured_image
    mars_data['featured_image']= featured_image_url

    jpl_browser.quit()

    #Scrape [Mars Facts](https://galaxyfacts-mars.com) and get facts about the planet including Diameter, Mass, etc.

    fact_url = 'https://galaxyfacts-mars.com'

    fact_table = pd.read_html(fact_url)[1]
    fact_table.columns = ['Facts','Values']
    fact_table = fact_table.set_index(['Facts'])
    mars_fact = fact_table.to_html()
    mars_fact = mars_fact.replace('\n', "")

    mars_data['mars_fact']= mars_fact

    #Scrape [Mars Hemisphere](https://marshemispheres.com) and obtain high res images
    marshem_img = []

    #creating a function so can be reused
    def get_images(hem_name):
        marshem_url = "https://marshemispheres.com/"
        scrape_url = marshem_url + hem_name + ".html"
        executable_path = {'executable_path': ChromeDriverManager().install()}
        img_browser = Browser('chrome', **executable_path, headless=False)
        img_browser.visit(scrape_url)
        img_html = img_browser.html
        soup = BeautifulSoup(img_html, 'html.parser')
        images = soup.find_all('div', class_="wide-image-wrapper")

        for img in images:
            hem_picture = img.find('li')
            hem_full_img = hem_picture.find('a')['href']
            hem_title = soup.find('h2', class_='title').get_text()
            hem_img_url =  marshem_url + hem_full_img
            hem_dict = {"Title": hem_title, "url": hem_img_url}

            marshem_img.append(hem_dict)
            
        img_browser.quit()

    #using the function to get all hemispheres on Mars
    get_images('cerberus')
    get_images('schiaparelli')
    get_images('syrtis')
    get_images('valles')
    mars_data['hemisphere_image']= marshem_img

    return mars_data
