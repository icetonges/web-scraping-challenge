from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_copy
import pymongo

app = Flask(__name__)

# use flask_pymongo to set up mongo connection

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_app
db.listings.drop()

@app.route("/")
def index():
    # listings_test = list(db.listings.find())
    # print(listings_test)
    listings_test =list(db.listings.find({"news": {"$exists": True}}))
    listings_test1 =list(db.listings.find({"text": {"$exists": True}}))
    listings_test2 =list(db.listings.find({"url": {"$exists": True}}))
    listings_test3 =list(db.listings.find({"weather": {"$exists": True}}))
    listings_test4 =list(db.listings.find({"description": {"$exists": True}}))
    listings_test5 =list(db.listings.find({"title": {"$exists": True}}))
    # print (listings_test)

    return render_template("index.html", listings=listings_test, listings1=listings_test1,listings2=listings_test2,
                            listings3=listings_test3,listings4=listings_test4,listings5=listings_test5)
    
@app.route("/scrape")
def scraper():
    db.listings.drop()
    listings = db.listings
    listings_data = scrape_mars_copy.scrape()
    listings.insert_many(listings_data)
    # listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)