# Web Scraper Bot

An automated web scraper that collects product data by category and sends results through Telegram at regular intervals.

## Features

- Collect product data from configured categories
- Save results to CSV files (one per category)
- Send the CSV files via Telegram
- Automatically run every 3 hours

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
    BOT_TOKEN=your_telegram_bot_token
    CHAT_ID=your_telegram_chat_id
    USERNAME_WEB=your_website_username
    PASSWORD_WEB=your_website_password
    BASE_DATA_DIR=your_base_data_directory
    ```

## Usage

Run the main script:
    ```
    python source.py
    ```