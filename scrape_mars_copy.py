# Import necessary libraries

from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

def init_browser():
    
    executable_path ={'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # listings = {}
    # NASA Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_text = soup.find('div', class_="article_teaser_body").text
    
    # 2. JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    imgbody = soup.find("a", class_="fancybox").get('data-fancybox-href').strip()
    imgurl = 'https://www.jpl.nasa.gov'+imgbody
    
    # 3. Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    tweet = soup.find(class_="js-tweet-text").text
    weather = tweet.split('pic')[0] 
    
    # 4. Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    fact_list=df.values.tolist()
    
    # 5. Mars Hem
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

    listings = [{'news':news_title}, 
           {'text':news_text}, 
           {'url':imgurl}, 
           {'weather':weather},
           {'description':fact_list[0][0], 'value':fact_list[0][1]},
           {'description':fact_list[1][0], 'value':fact_list[1][1]},
           {'description':fact_list[2][0], 'value':fact_list[2][1]},
           {'description':fact_list[3][0], 'value':fact_list[3][1]},
           {'description':fact_list[4][0], 'value':fact_list[4][1]},
           {'description':fact_list[5][0], 'value':fact_list[5][1]},
           {'description':fact_list[6][0], 'value':fact_list[6][1]},
           {'description':fact_list[7][0], 'value':fact_list[7][1]},
           {'description':fact_list[8][0], 'value':fact_list[8][1]},
           {"title": title_list[0], "img_url": image_urls_list[0]},                       
           {"title": title_list[1], "img_url": image_urls_list[1]},
           {"title": title_list[2], "img_url": image_urls_list[2]},
           {"title": title_list[3], "img_url": image_urls_list[3]}
           ]
    browser.quit()
    return listings

