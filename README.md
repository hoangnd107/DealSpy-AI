# DealSpy AI

An automated deal tracking system that scrapes e-commerce sites, analyzes prices, and sends Telegram notifications for the best deals

## Features

- Automated web scraping
- Price tracking and discount analysis 
- AI-powered deal recommendations
- CSV exports with timestamp tracking
- Real-time Telegram notifications
- Daily deal analysis reports

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
    BASE_DATA_DIR=path_to_data_folder
    BASE_ANALYSIS_DIR=path_to_analysis_folder
    BOT_TOKEN=telegram_bot_token
    USERNAME_WEB=website_username
    PASSWORD_WEB=website_password
    CHAT_ID=telegram_chat_id
    API_URL=ai_api_url
    API_KEY=ai_api_key
    ```

## Usage

Start data collection:
    ```
    python web_scraper.py
    ```

Run analysis:
    ```
    python product_analyzer.py
    ```

Launch web interface:
    ```
    python app.py
    ```

## Project Structure

```plaintext
DealSpy-AI/
├── src/
│   ├── app.py              # Flask web interface
│   ├── web_scraper.py      # Data collection
│   ├── product_analyzer.py # Deal analysis
│   └── telegram_sender.py  # Notifications
├── templates/
│   └── products.html       # Product display template
├── requirements.txt        # Dependencies
└── .env                    # Environment config
```