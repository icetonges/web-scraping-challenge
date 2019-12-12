# Import necessary libraries

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests

import pandas as pd

    # @NOTE: Replace the path with your actual path to the chromedriver
executable_path = {"executable_path": "chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)
    
# NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.
# Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, 
# has ramped up this summer, on course for launch next May from Vandenberg 
# Air Force Base in central California -- 
# the first interplanetary launch in history from America's West Coast."

def scrape():

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_="content_title").text
    news_text = soup.find('div', class_="article_teaser_body").text
    print(news_title, "********", news_text)

    # 2. JPL Mars Space Images - Featured Image

    # https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars

    # Visit  the url for JPL Featured Space Image here.
    # Use splinter to navigate the site and find the image url 
    # for the current Featured Mars Image and assign the url string to 
    # a variable called featured_image_url.

    # Make sure to find the image url to the full size .jpg image.

    # Make sure to save a complete url string for this image.

    # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    imgbody = soup.find("a", class_="fancybox").get('data-fancybox-href').strip()
    imgurl = 'https://www.jpl.nasa.gov'+imgbody
    print(imgurl)

    # 3. Mars Weather

    # https://twitter.com/marswxreport?lang=en

    # Visit the Mars Weather twitter account
    # and scrape the latest Mars weather tweet from the page. Save the tweet text
    # for the weather report as a variable called mars_weather.
    # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    tweet = soup.find(class_="js-tweet-text").text
    weather = tweet.split('pic')[0] 
    print(weather)

    # 4. Mars Facts

    # https://space-facts.com/mars/

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing
    # facts about the planet including Diameter, Mass, etc.

    # Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    tables

    df = tables[0]
    df.columns = ['description','Value']
    df.set_index('description', inplace=True)
    df

    # 5. Mars Hemispheres
    # https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

    # Visit the USGS Astrogeology site here to obtain high resolution images 
    # for each of Mar's hemispheres.

    # You will need to click each of the links to the hemispheres in order to 
    # find the image url to the full resolution image.

    # Save both the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name. Use a Python dictionary
    # to store the data using the keys img_url and title.

    # Append the dictionary with the image url string and the hemisphere title to 
    # a list. This list will contain one dictionary for each hemisphere.

    # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    url_list = []
    itemlinks = soup.find_all(class_="description")

    for itemlink in itemlinks:
        item = itemlink.find('a', class_="itemLink product-item").get('href')
        url_list.append(item)
    item_url_list = ['https://astrogeology.usgs.gov/' + item_url for item_url in url_list]

    print(item_url_list[0],item_url_list[1], item_url_list[2], item_url_list[3] )

    title_list = []
    image_urls_list = []
    for x in range (0,4):
        
        item_url = item_url_list[x]
        browser.visit(item_url)
        html = browser.html
        soup = bs(html, 'html.parser')
    #     print(item_url)
        image_urls = soup.find("li").find('a')['href']
        title = soup.find('h2', class_="title").text
        title_list.append(title)
        image_urls_list.append(image_urls)
    print(title_list)
    print(image_urls_list)
    # hemisphere_image_urls = zip(title_list,imgurl_list )
    hemisphere_image_urls = [{"title": title_list, "img_url": image_urls_list}]
    print(hemisphere_image_urls)


