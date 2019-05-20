from flask import Flask
from flask import request
from flask import render_template

import pymysql

connection123 = pymysql.connect(host="localhost",
                            user="roczi",
                            password="",
                            db=("moviesdb"))
                            
                            
import os
app = Flask(__name__)


@app.route("/")
def home():
    cursor = pymysql.cursors.DictCursor(connection123)
    # cursor.execute("SELECT movies.title AS movie_title, genre.genre AS category_name FROM todos JOIN categories ON todos.category_id = categories.category_id")
    cursor.execute("SELECT * from movies")    
    movies = cursor.fetchall()
    print(movies)
    return render_template("index.html", all_movies = movies)
    # return render_template("index.html")


    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            
            
            
            
