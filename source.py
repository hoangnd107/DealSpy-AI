import pandas as pd
import os
import time
import requests
import schedule
from seleniumbase import SB
from dotenv import load_dotenv
import datetime

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
USERNAME = os.getenv('USERNAME_WEB')
PASSWORD = os.getenv('PASSWORD_WEB')
BASE_DATA_DIR = os.getenv(r'BASE_DATA_DIR')

class WebScraper:
    def __init__(self):
        self.categories = [
                "nha-cua-doi-song",
                "dien-thoai-phu-kien",
                "dich-vu-phan-mem",
                "me-va-be"
            ]
        self.bot_token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.username = USERNAME 
        self.password = PASSWORD

    def scrape_dropbuy(self):
        with SB(uc=True) as sb:
            sb.open("https://dropbuy.vn/dang-nhap?")
            sb.type('input[name="username"]', self.username)
            sb.click('button[type="submit"]')
            sb.type('input[name="password"]', self.password)
            sb.click('button[type="submit"]')
            time.sleep(1)

            def get_products():
                products = sb.find_elements("css selector", "div.relative.rounded-b-md.border")
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

            def scrape_category(category_url):
                sb.click(f'a[href*="{category_url}"]')
                time.sleep(1)
                
                all_products = []
                page = 1
                
                while True:
                    print(f"Scraping page {page}")
                    products = get_products()
                    all_products.extend(products)
                    
                    next_button = sb.find_elements("css selector", "li.ant-pagination-next:not(.ant-pagination-disabled)")
                    if not next_button: break
                    
                    sb.click("li.ant-pagination-next")
                    time.sleep(1)
                    page+=1
                    
                return all_products

            def save_to_csv(data, filename):
                data_dir = BASE_DATA_DIR
                os.makedirs(data_dir, exist_ok=True)
                
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                filename_without_ext = os.path.splitext(filename)[0]
                filename_with_timestamp = f"{filename_without_ext}_{timestamp}.csv"
                
                file_path = os.path.join(data_dir, filename_with_timestamp)
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"Data saved to {file_path}")
                return file_path

            def send_telegram(file_path):
                msg_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                category_name = os.path.basename(file_path).replace('.csv', '')
                msg = f"Data for category: {category_name}"
                requests.post(msg_url, data={"chat_id": self.chat_id, "text": msg})
                
                with open(file_path, "rb") as file:
                    url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
                    response = requests.post(url, data={"chat_id": self.chat_id}, files={"document": file})
                    if response.status_code == 200:
                        print(f"File {file_path} sent successfully.")
                    else:
                        print(f"Failed to send {file_path}. Response: {response.text}")

            for category in self.categories:
                products = scrape_category(category)
                file_path = save_to_csv(products, f"{category}.csv")
                send_telegram(file_path)

def run_scraper():
    scraper = WebScraper()
    try:
        scraper.scrape_dropbuy()
    except Exception as e:
        print(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
    run_scraper()
    schedule.every(3).hours.do(run_scraper)
    while True:
        schedule.run_pending()
        time.sleep(1)