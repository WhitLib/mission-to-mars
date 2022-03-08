# Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
# PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
# To use the scraping code, convert from Jupyter notebook to Python
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define route for HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Create another function to set up scraping route
@app.route("/scrape")
def scrape():
    # Assign a new variable that points to Mongo database
    mars = mongo.db.mars
    # Create a new variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    # Insert data, but not if an identical record already exists; find the first matching document {}, then use the data
    # stored in mars_data and create a new document if one doesn't already exist
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    # Add a redirect after successfully scraping the data
    return redirect('/', code=302)

# Run Flask
if __name__ == "__main__":
   app.run()


