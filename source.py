import pandas as pd
import time
import requests
import os
from seleniumbase import BaseCase

class WebScraper(BaseCase):

    def login(self):
        self.open("https://dropbuy.vn/")
        self.click("a.ant-dropdown-trigger.flex.items-center.mb-1.space-x-1.text-black>svg.lucide-user")
        self.click('a[href*="dang-nhap"]')
        self.type('input[name="username"]', "matrix")
        self.click('button[type="submit"]')
        self.type('input[name="password"]', "tlu@2020")
        self.click('button[type="submit"]')
        time.sleep(1)

    def get_products(self):
        products = self.find_elements("css selector", "div.relative.rounded-b-md.border")
        page_data = []
        
        for product in products:
            try:
                name = product.find_element("css selector", "div.h-16.line-clamp-3").text.strip()
                curr_price = product.find_element("css selector", "div.font-semibold.text-red-500").text.strip()
                original_price = product.find_element("css selector", "div.text-xs.text-gray-500.line-through").text.strip()
                img = product.find_element("css selector", "img.object-cover.aspect-square").get_attribute("src")
                
                page_data.append({
                    "name": name,
                    "current_price": curr_price,
                    "original_price": original_price,
                    "image_url": img
                })
            except Exception as e:
                print(f"Error extracting product: {e}")
                continue
                
        return page_data

    def scrape_category(self, category_url):
        self.click(f'a[href*="{category_url}"]')
        time.sleep(1)
        
        all_products = []
        page = 1
        
        while True:
            print(f"Scraping page {page}")
            products = self.get_products()
            all_products.extend(products)
            
            next_button = self.find_elements("css selector", "li.ant-pagination-next:not(.ant-pagination-disabled)")
            if not next_button: break
            
            self.click("li.ant-pagination-next")
            time.sleep(1)
            page+=1
            
        return all_products

    def save_to_csv(self, data, filename):
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"Data saved to {filepath}")

    def test_scrape_dropbuy(self):
        self.login()
        
        categories = [
            "nha-cua-doi-song",
            "dien-thoai-phu-kien",
            "dich-vu-phan-mem",
            "me-va-be"
        ]

        bot_token = "7709742283:AAGNy54APBv0mjfu49rx6sYXmLrxfHdh-jM"
        chat_id = "6457280522"

        for category in categories:
            products = self.scrape_category(category)
            filename = f"{category}.csv"
            self.save_to_csv(products, filename)
            time.sleep(1)
            self.send_telegram(os.path.join('data', filename), bot_token, chat_id)
        
    def tearDown(self):
        pass

    def send_telegram(self, file_path, bot_token, chat_id):
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(file_path, "rb") as file:
            response = requests.post(url, data={"chat_id": chat_id}, files={"document": file})
            if response.status_code == 200:
                print(f"File {file_path} sent successfully.")
            else:
                print(f"Failed to send {file_path}. Response: {response.text}")

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.test_scrape_dropbuy()