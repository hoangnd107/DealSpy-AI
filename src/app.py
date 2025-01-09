from flask import Flask, render_template, request
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
BASE_ANALYSIS_DIR = os.getenv(r'BASE_ANALYSIS_DIR')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Route for uploading and displaying products
@app.route("/", methods=["GET", "POST"])
def display_products():
    products = []
    try:
        # Read analysis CSV file from the base directory
        data = pd.read_csv(os.path.join(BASE_ANALYSIS_DIR, 'analysis.csv'))
        
        # Check if required columns exist
        if not {'product_name', 'discount_percentage', 'current_price', 'original_price', 'product_image_url', 'product_url'}.issubset(data.columns):
            return "The CSV file must contain 'product_name', 'discount_percentage', 'current_price', 'original_price', 'product_image_url', and 'product_url' columns.", 400
        
        # Convert data into a list of dictionaries
        products = data.to_dict(orient="records")
    except Exception as e:
        return f"An error occurred while processing the file: {e}", 500
    
    return render_template("products.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
