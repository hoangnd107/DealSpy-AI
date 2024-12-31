# web-scraping

A Python project for web scraping using SeleniumBase to extract data from dynamic websites efficiently.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/hoangnd107/web-scraping.git
    cd web-scraping
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the `test_scrape_dropbuy` method in `source.py` with your Telegram bot token and chat ID.

2. Run the scraper:
    ```sh
    pytest source.py
    ```

3. The scraped data will be saved as CSV files in the project directory and sent to the specified Telegram chat.
