from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

import pymysql

connection123 = pymysql.connect(host="localhost",
                            user="roczi",
                            password="",
                            db=("moviesdb"))
                            
                            
import os
app = Flask(__name__)


@app.route("/movies")
def home():
    cursor = pymysql.cursors.DictCursor(connection123)
    cursor.execute("SELECT movie.id, movie.title, genre.id, genre.genre, movie.year, movie.reviewrating FROM movie JOIN genre ON movie.id = genre.id")
    # SELECT movie.id, movie.title, genre.genre FROM movie INNER JOIN genre ON movie.id=genre.id;
    # cursor.execute("SELECT * from movie")    
    movies_var = cursor.fetchall()
    print(movies_var)
    return render_template("all_movies.html", all_movies_jinja = movies_var)




@app.route('/', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'GET':
        cursor = pymysql.cursors.DictCursor(connection123)
        cursor.execute('SELECT * from language')
        language_var = cursor.fetchall()
        
        cursor.execute('SELECT * from genre')
        genre_var = cursor.fetchall()
        
        cursor.execute('SELECT * from genre')
        genre_var = cursor.fetchall()
        
        cursor.execute('SELECT * from censorrating')
        censorrating_var = cursor.fetchall()
        
        return render_template('index.html', 
        all_languages_jinja = language_var, 
        all_genres_jinja = genre_var,
        all_censorratings_jinja = censorrating_var,
        )
    

    else:
        print(request.form)
        title_var = request.form['input_name_title']
        runtime_var = request.form['input_name_runtime']
        info_var = request.form['input_name_info']
        year_var = request.form['input_name_year']
        reviewrating_var = request.form['input_name_reviewrating']
        censorrating_var = request.form['input_name_censorrating']
        
        genre_var = request.form['input_name_genre']
        language_var = request.form['input_name_language']
        actor_var = request.form['input_name_actor']
        character_var = request.form['input_name_character']
        productioncompany_var = request.form['input_name_productioncompany']


        # INSERT INTO `movie`(`id`, `title`, `runtime`, `info`, `year`, `reviewrating`, `censorrating`)
        # VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7])
        # `id`, id, NULL, genre_var, language_var, actor_var, character_var, productioncompany_var
        sql = """
            INSERT INTO movie (`title`, `runtime`, `info`, `year`, `reviewrating`, `censorrating`)
            VALUES ("{}", {}, "{}", {}, {}, "{}")
        """.format(title_var, runtime_var, info_var, year_var, reviewrating_var, censorrating_var)
        
        cursor = pymysql.cursors.DictCursor(connection123)
        cursor.execute(sql)
        connection123.commit()
        cursor.close();
        return redirect('/')



    
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            
            
            
            
