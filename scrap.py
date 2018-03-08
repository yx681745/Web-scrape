from urllib.request import urlopen as uReq
import sqlite3
import sys
from bs4 import BeautifulSoup as soup

def new_egg_scrape(url,table_name,db_name):
    '''
    Input: url - url of newegg website
           table_name - name of table you want to name
           db_name    - name of sqlite3 database you want to name
    Output:
           a sqlite3 database of the products table
    print procuct information
    '''
    def urlsoup(url):
        url_client=uReq(my_url)
        my_html=url_client.read()     
        url_client.close()       
        my_soup=soup(my_html,"html.parser")
        return my_soup

    def scrape_soup(soup,table_name,db_name):
    
        containers=my_soup.findAll("div",{"class":"item-container"})

        conn=sqlite3.connect(db_name)
        cur=conn.cursor()
        print ("Opened database")

        conn.execute('''CREATE TABLE IF NOT EXISTS ? 
            (ID INT PRIMARY KEY    NOT NULL,
            NAME       TEXT       NOT NULL,
            RATE        TEXT     NOT NULL,
            PRICE        TEXT        NOT NULL,
            BRAND         TEXT      NOT NULL,
            SHIPPRICE    TEXT    NOT NULL);''',table_name)


        for container in containers:
            brandtag=container.findAll("a",{"class":"item-brand"})
            if brandtag!=[]:        
                ratetag=container.findAll("a",{"class":"item-rating"})
                if ratetag!=[]:
                    rate=ratetag[0]["title"]
                else:
                    rate="No rate"
                brand=brandtag[0].img["title"]
            else:
                brand='see in name'
            nametag=container.findAll("a",{"class":"item-title"})
            name=nametag[0].text
            pricetag=container.findAll("li",{"class":"price-current"})
            if pricetag!=[]:
                price=pricetag[0].strong.text
            else:
                price="See in cart"
            shiptag=container.findAll("li",{"class":"price-ship"})
            ship_price=shiptag[0].text.strip()
            if ship_price=='':
                ship_price='Unknown'
    
            print("brand :" + brand)
            print("rate : "+ rate)
            print("name : " + name)
            print("ship_price: " + ship_price)
    
            cur.execute("INSERT INTO PRODUCTS VALUES (?,?,?,?,?,?)",(str(containers.index(container)+1),(name.replace(",","|")),rate,str(price),brand,ship_price))
        conn.commit()
        conn.close()
    return  scrape_soup(urlsoup(url),table_name,db_name)




    
