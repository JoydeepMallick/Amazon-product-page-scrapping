# Assignment: Amazon Product Web Scraping

## Overview
This assignment focuses on web scraping product information from Amazon, including product URLs, names, prices, ratings, and reviews. The scraped data will be stored in a CSV file. The assignment is divided into two parts:

**Part 1: Scraping Product Listings**
In this part, we scrape product listings from Amazon. The requirements include:
- Scraping at least 20 pages of product listings.
- Collecting the following information:
  - Product URL
  - Product Name
  - Product Price
  - Rating
  - Number of reviews

**Part 2: Scraping Individual Product Pages**
With the product URLs obtained in Part 1, we will visit each URL and collect additional information for around 200 products. The information to be scraped includes:
- Description
- ASIN
- Product Description
- Manufacturer

The entire dataset will be exported in CSV format.

## Requirements
To run the code, you'll need the following Python packages:
1. `requests` for making HTTP requests.
   ```bash
   pip install requests
    ```
2. `beautifulsoup4` for parsing HTML content.
   ```bash
   pip install beautifulsoup4
    ```
3. `pandas` for working with CSV files
    ```bash
    pip install pandas
    ```
4. `validators` for URL validation
    ```bash
    pip install validators
    ```
5.  `fake_useragent` for generating random user agents to prevent bot detection 
    ```bash
    pip install fake-useragent
    ```


## Code Structure

The code consists of several key components:

1. **Fetching Product URLs:** ```hit_all_pages()``` is responsible for scraping product URLs from Amazon's search pages and saving them in a CSV file.

2. **Cleaning Valid URLs:** ```valid_csv_generator()``` reads the CSV file generated in *ABOVE*, validates the URLs, and creates a new CSV file with only valid URLs.

3. **Scraping Product Information:** ```product_info_scraper()``` takes the valid product URLs and scrapes the required information from individual product pages, storing it in a CSV file.

4. **Scraping Functions:** These functions (```scrap_name()```, ```scrap_price()```, etc.) are used to scrape specific information from product pages.

5. **Main block:** The code in ```__main__``` is used to execute the entire workflow.


## Current Issue

During the web scraping process, it has been observed that Amazon occasionally returns a different response, such as a CAPTCHA HTML page, even when the HTTP request's status is reported as `200`. This issue occurs when attempting to retrieve details from individual product pages using BeautifulSoup.


It seems antiscraping measures of amazon product page.