import os
import datetime
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():

        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date =  datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            return redirect(url_for('home'))
        
        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.datetime.strptime(entry['date'], "%Y-%m-%d").strftime("%b %d")
                
            )
            for entry in app.db.entries.find().sort("_id", -1)
        ]
        return render_template("home.html", entries=entries_with_date)
    return app
    