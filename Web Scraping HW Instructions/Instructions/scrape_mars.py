from splinter import Browser
from bs4 import BeautifulSoup 
import pandas as pd
import requests
import time


def browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_news():
    scrape_browser = browser()

    browser.visit('https://mars.nasa.gov/news/')

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    title_results = soup.find_all('div', class_='content_title')
    news_title = title_results[0].text

    p_results = soup.find_all('div', class_='article_teaser_body')
    news_p = p_results[0].text
    browser = init_browser()
    mars_data = {}
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response = requests.get(url)
    
    time.sleep(1)
    
    mars_weather_tweet = []
    soup = BeautifulSoup(response.text, "html.parser")    
    
    tweets = soup.find_all('div', class_='js-tweet-text-container')
     
    for data in tweets:
        twitter = data.find('p').text
        
        if 'sol' and 'pressure' in twitter:
            mars_weather = twitter
            new_twitter = twitter.split('pic')
            cleaned_tweet = new_twitter[0].replace('\n', '')            
            break
        else:
            pass
    
    mars_weather_tweet.append(cleaned_tweet)
    
    url = 'https://space-facts.com/mars'
    browser.visit(url)
    response = requests.get(url)
    
    time.sleep(1)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    mars_facts = soup.find('table')
    
    table_rows = mars_facts.find_all('tr')
    
    df_data = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        df_data.append(row)
        scrape_table = pd.DataFrame(df_data, columns=['Description', 'Value'])    
    
        scrape_table.reset_index()
        new_scraped = scrape_table.set_index('Description')
        
        final_table = new_scraped.to_html(index=True)
        
        url = 'https://www.jpl.nasa.gov/spaceimages'
        browser.visit(url)
        html = browser.html
        
        
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, 'html.parser')
    
    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img = 'https://www.jpl.nasa.gov' + relative_img_path

        
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        time.sleep(1)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        hemisphere_image_urls = []
        hem_url = []
        main_url = 'https://astrogeology.usgs.gov'
        links = soup.find_all('div', class_='item')
        
        for link in links:
            img_url = link.find('a', class_='itemLink product-item')['href']
            title = link.find('h3').text
            final_url = main_url + img_url
            browser.visit(final_url)
            
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            img_wd = soup.find('div', class_='downloads')
            img_link = img_wd.find('a')['href']
            hemisphere_image_urls.append({'title':title, 'image_url':img_link})
            hem_url.append(img_link)
            
    mars_data = {
        "headline": news_title,
        "paragraph": news_p,
        "weather": mars_weather_tweet,
        "facts": final_table,
        "image": featured_image_url,
        "hemispheres": hemisphere_image_urls
    }    
        
    browser.quit()
    
    return mars_data