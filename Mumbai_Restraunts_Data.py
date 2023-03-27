import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

dataframe_final = pd.DataFrame()
total_page=37
for page in range(1,total_page+1):  
    
    response=requests.get("https://www.yelu.in/category/restaurants/{}/city:mumbai".format(page))
    soup=BeautifulSoup(response.text,'html.parser')
    all_company=soup.find('div',id="listings").find_all(class_=["company with_img g_0","company g_0"])

    
    Comapny_Name = []  
    Address = []                                       
    Description =[]
    Rating =[]
    Varified_Tag = []
    Icon=[]
    Company_Page_link =[]

    for info in all_company:
        # Name
        if(info.find('h4')!=None):
            Comapny_Name.append(info.find('h4').text) 
        else:
            Comapny_Name.append("No Name")

        #company page link
        comp_link=(info.find('h4').find('a').get('href'))
        Company_Page_link.append(("https://www.yelu.in"+comp_link))   

        #address
        Address.append(info.find('div',class_="address").text) 

        #description
        if((info.find('div',class_="details"))!=None):
            Description.append(info.find('div',class_="details").text) 
        else:
            Description.append(None)

        #Tag
        if(info.find('u',class_='v')!=None):
            Varified_Tag.append(info.find('div',class_='cont').find('u',class_='v').text.strip()) 
        else:
            Varified_Tag.append("Not varified")

        #Rating
        if ((info.find('div',class_="rate"))!=None):
            Rating.append((info.find('div',class_="rate").text.strip()))
        else:
            Rating.append(('0.0'))
            
        #Icon
        try:
            icon=soup.find('div',id="listings").find('div',class_='details').find('span').find('img').get('data-src')
            Icon.append("https://www.yelu.in/"+icon)
        except:
            Icon.append(None)
    
        
    data={
        "Company_Name":Comapny_Name,
        "Company_Address":Address,
        "Descriptin": Description,
        "Varification":Varified_Tag,
        "Rating":Rating,
        "Company_Icon":Icon,
        "Company_Page":Company_Page_link
    }
    df=pd.DataFrame(data)
    dataframe_final = dataframe_final.append(df, ignore_index=True)
    dataframe_final.to_json("Mumbai_Restaurants.json",indent=6)
   

