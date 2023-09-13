from bs4 import BeautifulSoup as soup
import requests
import nltk
from newspaper import Article
import logging
import sys
import json
import pandas as pd
import numpy as np

logging.basicConfig(filename='scraper.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%m-%y %H:%M:%S')

def stocknews_get_link():
    url='https://vietstock.vn/'
    headers={"User-agent": 'Chrome/101.0.4951.54'}
    request =requests.get(url, headers=headers)
    html=request.content
    s=soup(html,'html.parser')  
    h4_tags = s.find_all("h4")
    urls = []
    a_list=[]
    for h4_tag in h4_tags:
        a_tag = h4_tag.find("a")
        if a_tag is not None:
            url=a_tag['href']
            urls.append(url)
    return urls
def setup_logger():
  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s %(levelname)8s %(message)s",
      handlers=[
          logging.FileHandler("crawl_data.log"),
          logging.StreamHandler(sys.stdout)
      ]
  )

  global logger
  logger = logging.getLogger("main")
  logger.setLevel(logging.INFO)

def main():
    setup_logger()
    links=stocknews_get_link()
    logger.info('Start collecting data for {} movies'.format(len(links)))
    df = pd.DataFrame(links)
    df.to_pickle("./raw/link")

if __name__== "__main__":
    main()