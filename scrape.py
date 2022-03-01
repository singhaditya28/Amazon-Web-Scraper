from bs4 import BeautifulSoup
import requests
import time
import csv
import json
import sqlite3

def main(URL):
    jsondict= {}
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                                'Accept-Language': 'en-US, en;q=0.5'})
 
    webpage = requests.get(URL, headers=HEADERS)
 
    soup = BeautifulSoup(webpage.content, "lxml")
    try:
        title = soup.select("#productTitle")[0].get_text().strip()
 
        title_value = title.string
 
        title_string = title_value.strip().replace(',', '')
 
    except :#AttributeError
        title_string = f"{URL} not available"
        print(title_string)
 
    jsondict["Product Title"]= title_string
 
    try:
        price = soup.find(
            "span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
    except AttributeError:
        price = f"{URL} not available"
        print(price)
    
    jsondict["Product Price"]= price


    try:
        image = soup.find(
            "span", attrs={'id': 'landingImage'}).string.strip().replace(',', '')
        
    except AttributeError:
        image = f"{URL} not available"
        print(image)
 
    jsondict["Product Image URL"]= image

  
    try:
        detail = soup.find(
            "span", attrs={'id': 'productDescription'}).string.strip().replace(',', '')
        
    except AttributeError:
        detail = f"{URL} not available"
        print(detail)
 
    jsondict["Product Description"]= detail

    json_object = json.dumps(jsondict, indent = 4)
  
    with open("out.json", "a") as outfile:
      outfile.write(json_object)
    
    c.execute('create table if not exists Details (title text,price text,image text, desc text)')
    cursor.execute("Insert into Details values (?, ?, ?, ?)",(jsondict['Product Title'], jsondict['Product Price'], jsondict['Product Image URL'], jsondict['Product Description']))
    connection.commit()
    

if __name__ == '__main__':
  connection = sqlite3.connect("Output.db")
  cursor = connection.cursor()
  c =cursor
  with open("address.csv", 'r') as file:
    file.seek(0)
    datareader = csv.reader(file)
    next(datareader)
    count = 0
    start = time.time()
    for row in datareader:
      if count == 100:
        end = time.time()
        count = 0
        print("Time taken for this batch of 100 URLS : " ,end - start)
        start = time.time()
      country = row[3]
      asin = row[2]
      mainlink = f"https://www.amazon.{country}/dp/{asin}"
      print(mainlink)
      main(mainlink)
      count+=1
      
        
