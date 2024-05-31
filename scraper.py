import requests
from bs4 import BeautifulSoup
import csv

def scrape_products(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Ensure correct encoding
            response.encoding = 'utf-8'
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract product information
            products = []
            for product in soup.find_all('article', class_='product_pod'):
                name = product.find('h3').find('a')['title']
                price_text = product.find('p', class_='price_color').text.strip()
                price = float(price_text.encode('ascii', 'ignore').decode().replace('£', ''))
                rating = product.find('p', class_='star-rating')['class'][1]

                products.append({'Name': name, 'Price': price, 'Rating': rating})

            return products
        elif response.status_code == 404:
            print("Page not found: 404")
        elif response.status_code == 503:
            print("Service unavailable: 503. Retrying after 5 seconds...")
            time.sleep(5)
            return scrape_products(url)
        else:
            print(f"Failed to fetch page: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return None

def write_to_csv(products):
    # Define CSV file name and headers
    filename = 'products.csv'
    headers = ['Name', 'Price', 'Rating']

    # Write product information to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(products)

if __name__ == "__main__":
    # URL of the e-commerce website to scrape
    url ='http://books.toscrape.com/'  # Replace with the actual URL


    # Scrape product information
    products = scrape_products(url)

    if products:
        # Write product information to CSV file
        write_to_csv(products)
        print("Data scraped successfully and stored in products.csv")
    else:
        print("Failed to scrape data from the website.")
