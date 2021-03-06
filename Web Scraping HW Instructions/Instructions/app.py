from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)


conn = 'mongodb://localhost:27017'


client = pymongo.MongoClient(conn)

@app.route("/")
def index():
    
    mars = client.db.mission_to_mars.find_one()
    return render_template("webscrape.html", mission_to_mars = mars)

@app.route("/scrape")
def scrape():
    
    mars = client.db.mission_to_mars 
    mars_data = scrape_mars.scrape()
    
    mars.insert_one(mars_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)