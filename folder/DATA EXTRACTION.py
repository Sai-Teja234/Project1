#!/usr/bin/env python
# coding: utf-8

# # Data Extraction from Website URLs through Web Scraping

# IMPORT LIBRARIES

# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup 


# EXTRACTING SINGLE URL 

# In[96]:


url="https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/"


# In[97]:


page=requests.get(url)


# In[98]:


page.content


# In[99]:


soup=BeautifulSoup(page.content, 'html.parser')
soup


# In[100]:


article_title=soup.find('h1',attrs={'class':'entry-title'}).text #mentioned html title class
article_title


# In[101]:


article_text=soup.find('div',attrs={"class":"td-post-content tagdiv-type"}).text.replace("\n","")
article_text                 # mentioned html text class 


# * Above from single url webpage, only the title & text are Extracted

# Extract multiple URLs (100) and save the article titles and texts into text files, associating each file with its corresponding URL ID

# In[52]:


data=pd.read_excel(r"C:\Users\hp\Downloads\Input.xlsx")
data


# In[53]:


urls=data.URL
urls


# In[76]:


import os

def extract_article(url):       #using function extract article
    try:
        page = requests.get(url)
        page.raise_for_status()  

        soup = BeautifulSoup(page.content, 'html.parser')
        article_title = soup.find('h1', attrs={'class': 'entry-title'}).text.strip()
        article_text = soup.find('div', attrs={"class": "td-post-content tagdiv-type"}).text.strip()
        
        return article_title, article_text
    except Exception as e:               # exception used to avoid the errors
        print(f"Error extracting article from {url}: {e}")
        return None, None

df = pd.read_excel(r"C:\Users\hp\Downloads\Input.xlsx")
output_directory = "extracted_articles"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for index, row in df.iterrows(): ##calling the iterations from dataframe row wise
    url_id = row['URL_ID']
    url = row['URL']
    
    article_title, article_text = extract_article(url)
    
    if article_title and article_text:
       
        output_filename = os.path.join(output_directory, f"{url_id}.txt")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(article_title + "\n\n")
            f.write(article_text)
        print(f"Article extracted and saved: {output_filename}")
    else:
        print(f"Failed to extract article from URL_ID {url_id}: {url}")
print("Extraction process completed.")


# In[3]:


import os

def extract_article(url): #given function called etract article
    try:
        page = requests.get(url)
        page.raise_for_status()  

        soup = BeautifulSoup(page.content, 'html.parser')
        article_title = soup.find('h1', attrs={'class': 'tdb-title-text'}).text.strip()
        #article_text = soup.find('div', attrs={"class": "tdb-block-inner td-fix-index"}).text.strip()
        article_text = soup.find('div',class_="tdb-block-inner td-fix-index")
        div_element=soup.select_one('.td-post-content') #by using select the wanted text is extraced
        article_text=div_element.text
        article_text=article_text.replace('\n','') #removing the unnecessary strings
        #article_text = soup.select('div.tdb-block-inner td-fix-index')
        return article_title, article_text
    except Exception as e:   # exception used to avoid the errors
        print(f"Error extracting article from {url}: {e}")
        return None, None


df = pd.read_excel(r"C:\Users\hp\OneDrive\Documents\fail urls.xlsx")
output_directory = "extracted_articles"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for index, row in df.iterrows(): #calling the iterations from dataframe row wise
    url_id = row['URL_ID']
    url = row['URL']
    
    article_title, article_text = extract_article(url)
    
    if article_title and article_text:
       
        output_filename = os.path.join(output_directory, f"{url_id}.txt")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(article_title + "\n\n")
            f.write(article_text)
        print(f"Article extracted and saved: {output_filename}")
    else:
        print(f"Failed to extract article from URL_ID {url_id}: {url}")

print("Extraction process completed.")


# The extraction process failed to two files,due to empty, resulting in a 404 error."

# Successfully The URLs have been efficiently extracted and saved as text files, containing only the web page titles and their corresponding text content.
