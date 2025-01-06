# DealSpy AI

An automated system that scrapes product data from e-commerce sites, analyzes deals, and sends notifications through Telegram.

## Features

- Automated web scraping every 6 hours
- Price tracking and discount analysis 
- AI-powered deal recommendations
- CSV exports with timestamp tracking
- Real-time Telegram notifications
- Daily deal analysis reports at 5:00 AM

## Setup

1. Clone the repository

2. Create a virtual environment and activate it (optional):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure environment variables: Create a .env file with the following:
    ```sh
    BASE_DATA_DIR=your_base_data_directory
    BASE_ANALYSIS_DIR=your_base_analysis_directory
    BOT_TOKEN=your_telegram_bot_token
    USERNAME_WEB=your_website_username
    PASSWORD_WEB=your_website_password
    CHAT_ID=your_telegram_chat_id
    API_URL=your_api_url
    API_KEY=your_api_key
    ```

## Usage

Run the scraper:
    ```
    python web_scraper.py
    ```

Run the analysis:
    ```
    python analysis.py
    ```