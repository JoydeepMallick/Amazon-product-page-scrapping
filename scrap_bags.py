import os
import requests
from bs4 import BeautifulSoup 
import pandas as pd
import validators
import csv
from fake_useragent import UserAgent

# Define the URL
BASE_URL = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'

# ________________________Define headers for the request__________________________

# generate a ramdom UserAgent object
user_agent = UserAgent().random

HEADERS = {
    'User-Agent': user_agent,
    'Accept-Language': 'en-US'
}

#empty list storing all product URLs
links_to_products = [];

# ___________________hit 20 pages of bag product from amazon____________________
def hit_all_pages():
    for pagenumber in range(1, 21):
        #building complete url for current page
        curpageurl = f'{BASE_URL}{pagenumber}'
        
        print("\nFetching data from page ", pagenumber, "...");
        while(True):
            # Make a GET request to current page
            response = requests.get(curpageurl, headers=HEADERS)
        
            if(response.status_code == 200):
                print("Fetch successful!")
                break

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        all_links_of_this_page = soup.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        print(len(all_links_of_this_page), "product links fetched from current page.")

        for atag in all_links_of_this_page:
            bag_link = 'https://www.amazon.in' + atag.get('href')
            #inserting the urls in a csv file
            links_to_products.append(bag_link)
     
    # after link_to_products complete convert it to csv for further use
    pd.DataFrame({"URL" : links_to_products}).to_csv('url_info.csv')



# _______________________checking valid urls in csv file___________________________
def valid_csv_generator():
    input_file = './url_info.csv'
    output_file = './valid_url_info.csv'
    cnt = 0
    # Read the data from the input file and write valid rows to the output file
    with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
        reader = csv.DictReader(input_csv)
        fieldnames = reader.fieldnames

        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if validators.url(row['URL']):
                writer.writerow(row)
            else:
                cnt+=1
    
    os.system('cls')
    print("\nCSV cleaned\nInvalid URLs removed :", cnt)
    os.remove(input_file)
    os.rename(output_file, input_file)


# ________________________Scrap all info about products from url_info.csv_________________________
def product_info_scraper():
    input_file = './url_info.csv'
    output_file = './product_desc.csv'
    with open(input_file, 'r') as input_csv, open(output_file, 'w',  encoding='utf-8', newline='') as output_csv:
        reader = csv.DictReader(input_csv)
        fieldnames = reader.fieldnames + ["Name", "Price", "Rating", "Number_of_reviews","Description", "ASIN", "Product_information", "Manufacturer"]

        # preparing writer
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        cnt = 0

        for row in reader:
            cur_bag_link = row['URL']
            while(True):
                cur_bag_page = requests.get(cur_bag_link, headers=HEADERS)
                if(cur_bag_page.status_code == 200):
                    cnt +=1
                    break
            
            # scrap all neccessary details from current page
            new_soup = BeautifulSoup(cur_bag_page.content, "html.parser")
            print("Fetched Bag from link ", cnt)
            '''
            From the output it seems the captcha page and amazon seems to be blocking it.
            '''
            # print(new_soup)
            product_name = scrap_name(new_soup)
            product_price = scrap_price(new_soup)
            product_rating = scrap_rating(new_soup)
            product_reviews = scrap_numofreviews(new_soup);
            product_desc = scrap_description(new_soup)
            product_asin = scrap_ASIN(new_soup)
            product_manu = scrap_manufacturer(new_soup)
            
            # Create a dictionary to hold the row data
            row_data = {
                "URL": row['URL'],
                "Name": product_name,
                "Price": product_price,
                "Rating": product_rating,
                "Number_of_reviews": product_reviews,
                "Description": product_desc,
                "ASIN": product_asin,
                "Product_information": "",
                "Manufacturer": product_manu
            }
            writer.writerow(row_data)

            if(cnt == 200):
                break #just fetching 200 products as mentioned

#_________________________ALL details scraped______________________
def scrap_name(new_soup):
    try:
        name = new_soup.find("span", attrs={"id": "productTitle"}).text.strip()
    except AttributeError:
        name = "N/A"
    return name

def scrap_price(new_soup):
    try:
        price = new_soup.find("span", attrs={"class": "a-price aok-align-center"}).find("span", attrs={"class": "a-offscreen"}).text
    except AttributeError:
        price = "N/A"
    return price

def scrap_rating(new_soup):
    try:
        rating = new_soup.find("span", attrs={"class": "a-icon-alt"}).text
    except AttributeError:
        rating = "N/A"
    return rating

def scrap_numofreviews(new_soup):
    try:
        num_of_reviews = new_soup.find("span", attrs={"id": "acrCustomerReviewText"}).text
    except AttributeError:
        num_of_reviews = "N/A"
    return num_of_reviews

def scrap_description(new_soup):
    try:
        desc = new_soup.find("div", attrs={"id": "featurebullets_feature_div"}).find_all("span", attrs={"class": "a-list-item"})[0].text
    except AttributeError:
        desc = "N/A"
    return desc

def scrap_ASIN(new_soup):
    try:
        asin = new_soup.find("td", attrs={"class": "a-size-base prodDetAttrValue"}).text.strip()
    except AttributeError:
        asin = "N/A"
    return asin

def scrap_manufacturer(new_soup):
    try:
        manufacturer = new_soup.find("td", attrs={"class": "a-size-base prodDetAttrValue"}).text.strip()
    except AttributeError:
        manufacturer = "N/A"
    return manufacturer


# _____________________main function calls_________________________ 
if __name__ == "__main__":
    # hit_all_pages()
    # valid_csv_generator()

    # now visit each valid url from url_info.csv and then update all needed data into product_desc.csv
    product_info_scraper()
    # view the csv file named product_desc.csv.
    ###THE END### 