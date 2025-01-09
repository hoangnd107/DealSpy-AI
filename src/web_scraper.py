import pandas as pd
import os
import time
import datetime
import schedule
from seleniumbase import SB
from dotenv import load_dotenv
from telegram_sender import TelegramSender

load_dotenv()
USERNAME = os.getenv('USERNAME_WEB')
PASSWORD = os.getenv('PASSWORD_WEB')
BASE_DATA_DIR = os.getenv('BASE_DATA_DIR')

class WebScraper:
    def __init__(self, username=USERNAME, password=PASSWORD, base_data_dir=BASE_DATA_DIR):
        self.categories = [
            "nha-cua-doi-song",
            "dien-thoai-phu-kien", 
            "dich-vu-phan-mem",
            "me-va-be"
        ]
        self.base_data_dir = base_data_dir
        self.username = username
        self.password = password
        self.telegram = TelegramSender()

    def scrape_dropbuy(self):
        with SB(uc=True) as sb:
            sb.open('https://dropbuy.vn/dang-nhap')
            sb.type('input[name="username"]', self.username)
            sb.click('button[type="submit"]')
            sb.type('input[name="password"]', self.password)
            sb.click('button[type="submit"]')
            time.sleep(1)

            for category in self.categories:
                products = self.scrape_category(sb, category)
                file_path = self.save_to_csv(products, f"{category}.csv")
                self.telegram.send_message(f"Data for category: {category}")
                self.telegram.send_file(file_path)

    def get_products(self, sb):
        products = sb.find_elements("css selector", "a.rounded-b-md.bg-white.text-black")
        page_data = []
        
        for product in products:
            try: product_name = product.find_element("css selector", "div.h-16.line-clamp-3").text.strip()
            except: product_name = "N/A"

            try: current_price = product.find_element("css selector", "div.font-semibold.text-red-500").text.strip()
            except: current_price = "N/A"

            try: original_price = product.find_element("css selector", "div.text-xs.text-gray-500.line-through").text.strip()
            except: original_price = "N/A"

            try: product_image_url = product.find_element("css selector", "img.object-cover.aspect-square").get_attribute("src")
            except:product_image_url = "N/A"

            try: product_url = product.get_attribute("href")
            except: product_url = "N/A"
            
            page_data.append({
                "product_name": product_name,
                "current_price": current_price,
                "original_price": original_price,
                "product_image_url": product_image_url,
                "product_url": product_url
            })
            
        return page_data

    def scrape_category(self, sb, category_url):
        sb.click(f'a[href*="{category_url}"]')
        time.sleep(1)
        
        all_products = []
        page = 1
        
        while True:
            print(f"Scraping page {page}")
            products = self.get_products(sb)
            all_products.extend(products)
            
            next_button = sb.find_elements("css selector", "li.ant-pagination-next:not(.ant-pagination-disabled)")
            if not next_button: 
                break
            
            sb.click("li.ant-pagination-next")
            time.sleep(1)
            page += 1
            
        return all_products

    def save_to_csv(self, data, filename):
        os.makedirs(self.base_data_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename_without_ext = os.path.splitext(filename)[0]
        filename_with_timestamp = f"{filename_without_ext}_{timestamp}.csv"
        
        file_path = os.path.join(self.base_data_dir, filename_with_timestamp)
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"Data saved to {file_path}")
        return file_path

def run_scraper():
    scraper = WebScraper()
    try:
        scraper.scrape_dropbuy()
    except Exception as e:
        print(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
    run_scraper()
    schedule.every().day.at("00:00").do(run_scraper)
    schedule.every(6).hours.do(run_scraper)
    while True:
        schedule.run_pending()
        time.sleep(1)