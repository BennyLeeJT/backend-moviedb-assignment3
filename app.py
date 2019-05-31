from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

from flask import flash

import numpy
from imdb import IMDb

import pymysql
import os
app = Flask(__name__)

connection123 = pymysql.connect(host="localhost",
                            user="roczi",
                            password="",
                            db=("moviesdb"))
                            
cursor = pymysql.cursors.DictCursor(connection123)

app.secret_key = 'some_secret'


sql_query_all_tables_joined = """
        SELECT * 
        FROM movie
        
        LEFT JOIN `movie_actor` ON `movie`.`id` = `movie_actor`.`movie_id`
        LEFT JOIN `actor` ON `actor`.`id` = `movie_actor`.`actor_id`
        
        LEFT JOIN `movie_character` ON `movie`.`id` = `movie_character`.`movie_id` 
        LEFT JOIN `character` ON `character`.`id` = `movie_character`.`character_id`
        
        LEFT JOIN `movie_genre` ON `movie`.`id` = `movie_genre`.`movie_id`
        LEFT JOIN `genre` ON `genre`.`id` = `movie_genre`.`genre_id`
        
        LEFT JOIN `movie_language` ON `movie`.`id` = `movie_language`.`movie_id`
        LEFT JOIN `language` ON `language`.`id` = `movie_language`.`language_id`
        
        LEFT JOIN `movie_productioncompany` ON `movie`.`id` = `movie_productioncompany`.`movie_id`
        LEFT JOIN `productioncompany` ON `productioncompany`.`id` = `movie_productioncompany`.`productioncompany_id`
        
        LEFT JOIN `censorrating` ON `movie`.`censorrating` = `censorrating`.`id`
        
        LEFT JOIN `reviewrating` ON `movie`.`reviewrating` = `reviewrating`.`id`
    
        LEFT JOIN `year` ON `movie`.`year` = `year`.`id`
    
        WHERE 
        `title` LIKE %s OR
        `year` LIKE %s OR
        `genre` LIKE %s OR
        `language` LIKE %s OR
        `actor`.`name` LIKE %s OR
        `character`.name LIKE %s OR
        `productioncompany`.`name` LIKE %s OR
        `censorrating`.`censorrating` LIKE %s OR
        `year`.`id` LIKE %s
        """
        
        
@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/')
def home():
    print("request.args = ", request.args)
    
    if 'search_input_name' not in request.args:
        print("IF CONDITION")
        return render_template("index.html")
    else:
        search_for = "%" + request.args['search_input_name'] + "%"
        print("ELSE CONDITION : search_for = ", search_for)
        
        
        
        # print("sql_query_all_tables_joined = ", sql_query_all_tables_joined)
        cursor.execute(sql_query_all_tables_joined, (search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for))
        # print("cursor_executed = ", cursor_executed)
        movies_var = cursor.fetchall()
        print("movies_var = ", movies_var)
        return render_template('search_results.html', 
        all_movies_jinja = movies_var)





@app.route('/add', methods=['GET', 'POST'])
def addpage_including_search():
    if request.method == 'GET':
        if 'search_input_name' not in request.args:
            print("IF CONDITION")
            
            cursor.execute('SELECT * from language')
            language_var = cursor.fetchall()
            print("language_var = ", language_var)
            
            cursor.execute('SELECT * from genre')
            genre_var = cursor.fetchall()
            print("genre_var = ", genre_var)
            # cursor.execute('SELECT * from genre')
            # genre_var = cursor.fetchall()
            
            cursor.execute('SELECT * from censorrating')
            censorrating_var = cursor.fetchall()
            print("censorrating_var = ", censorrating_var)
            
            return render_template('add_movie.html', 
            all_languages_jinja = language_var, 
            all_genres_jinja = genre_var,
            all_censorratings_jinja = censorrating_var,
            )
            
            # return render_template("add_movie.html")
        else:
            search_for = "%" + request.args['search_input_name'] + "%"
            print("ELSE CONDITION : search_for = ", search_for)
            
            # print("sql_query_all_tables_joined = ", sql_query_all_tables_joined)
            cursor.execute(sql_query_all_tables_joined, (search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for))
            # print("cursor_executed = ", cursor_executed)
            movies_var = cursor.fetchall()
            print("movies_var = ", movies_var)
            return render_template('search_results.html', 
            all_movies_jinja = movies_var)
            
        


    else:
        print("request.form = ", request.form)
        title_var = request.form['input_name_title']
        runtime_var = request.form['input_name_runtime']
        info_var = request.form['input_name_info']
        year_var = request.form['input_name_year']
        reviewrating_var = request.form['input_name_reviewrating']
        censorrating_var = request.form['input_name_censorrating']
        # print("censorrating_var = ", censorrating_var)
        genre_var = request.form['input_name_genre']
        language_var = request.form['input_name_language']
        actor_var = request.form['input_name_actor']
        character_var = request.form['input_name_character']
        productioncompany_var = request.form['input_name_productioncompany']
            
            
        sql_movie = """
            INSERT INTO movie (id, title, year, reviewrating, info, runtime, censorrating) 
            VALUES (%s,%s,%s,%s,%s,%s,%s);
        """
        sql_input_movie = (None, title_var, int(year_var), float(reviewrating_var), info_var, int(runtime_var), int(censorrating_var))

        try:
            cursor.execute(sql_movie, sql_input_movie)
        except:
            print (cursor._last_executed)
            raise
    
        connection123.commit()
        lastrowid_movie = cursor.lastrowid
        # print("lastrowid_movie = ", lastrowid_movie)
        

        
        
        
        # INSERTING FREE TEXT WITH MN RELATIONSHIP
        sql_actor = """
            INSERT INTO `actor`(id, name)
            VALUES (%s, %s);
        """
        sql_input_actor = (None, actor_var)

        try:
            cursor.execute(sql_actor, sql_input_actor)
        except:
            print (cursor._last_executed)
            raise

        connection123.commit()
        lastrowid_actor = cursor.lastrowid
        # print("lastrowid_actor = ", lastrowid_actor)
        
        
        # WEAK ENTITY OF MOVIE_ACTOR TABLE, LINKING HERE
        sql_movie_actor = """
            INSERT INTO `movie_actor`(`id`, `movie_id`, `actor_id`)
            VALUES (%s, %s, %s);
        """
        sql_input_movie_actor = (None, int(lastrowid_movie), int(lastrowid_actor))

        try:
            cursor.execute(sql_movie_actor, sql_input_movie_actor)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        
        
        # CENSORRATING. OPTION INPUT WITH 1-M RELATIONSHIP TO MOVIE.
        # NO NEED TO INSERT TO TABLE BECOZ TABLE IS FIXED
        # MOVIE TABLE UPDATED WITH INPUT FROM USER UNDER OPTION VALUE

        
        # GENRE. OPTION INPUT WITH MN RELATIONSHIP
        # NO NEED TO INSERT TO TABLE BECOZ TABLE IS FIXED
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_censorrating = """
            INSERT INTO `movie_genre`(`id`, `movie_id`, `genre_id`)
            VALUES (%s,%s,%s);
        """
        sql_input_censorrating = (None, int(lastrowid_movie), int(genre_var))

        try:
            cursor.execute(sql_censorrating, sql_input_censorrating)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        
        
        

        
        
        # LANGUAGE. OPTION INPUT WITH MN RELATIONSHIP
        # NO NEED TO INSERT TO TABLE BECOZ TABLE IS FIXED
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_censorrating = """
            INSERT INTO `movie_language`(`id`, `movie_id`, `language_id`)
            VALUES (%s,%s,%s);
        """
        sql_input_censorrating = (None, int(lastrowid_movie), int(language_var))

        try:
            cursor.execute(sql_censorrating, sql_input_censorrating)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        

        
        
        # CHARACTER. INSERTING FREE TEXT WITH MN RELATIONSHIP
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_character = """
            INSERT INTO `character`(id, name)
            VALUES (%s,%s);
        """
        sql_input_character = (None, character_var)

        try:
            cursor.execute(sql_character, sql_input_character)
        except:
            print (cursor._last_executed)
            raise

        connection123.commit()
        lastrowid_character = cursor.lastrowid
        # print("lastrowid_actor = ", lastrowid_actor)
        
        
        # WEAK ENTITY OF MOVIE_CHARACTER TABLE, LINKING HERE
        sql_movie_character = """
            INSERT INTO `movie_character`(`id`, `movie_id`, `character_id`)
            VALUES (%s, %s, %s);
        """
        sql_input_movie_character = (None, int(lastrowid_movie), int(lastrowid_character))

        try:
            cursor.execute(sql_movie_character, sql_input_movie_character)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        

        
        # PRODUCTIONCOMPANY. INSERTING FREE TEXT WITH MN RELATIONSHIP
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_productioncompany = """
            INSERT INTO `productioncompany`(`id`, `name`)
            VALUES (%s,%s);
        """
        sql_input_productioncompany = (None, productioncompany_var)

        try:
            cursor.execute(sql_productioncompany, sql_input_productioncompany)
        except:
            print (cursor._last_executed)
            raise

        connection123.commit()
        lastrowid_productioncompany = cursor.lastrowid
        # print("lastrowid_productioncompany = ", lastrowid_productioncompany)
        



        # WEAK ENTITY OF MOVIE_PRODUCTIONCOMPANY TABLE, LINKING HERE
        sql_movie_productioncompany = """
            INSERT INTO `movie_productioncompany`(`id`, `movie_id`, `productioncompany_id`)
            VALUES (%s, %s, %s);
        """
        sql_input_movie_productioncompany = (None, int(lastrowid_movie), int(lastrowid_productioncompany))

        try:
            cursor.execute(sql_movie_productioncompany, sql_input_movie_productioncompany)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        
        flash("Your Movie has been entered successfully! Thank you for populating CinemaTronix Database for the greater good! \U0001F44D ", "error")

        # THIS SHOULD NOT BE AT THE LAST PART OF THE FUNCTION else unreacheable code
        return redirect('/add')
        



@app.route('/database')
def database_including_search():
    if 'search_input_name' not in request.args:
        # print("request.args = ", request.args)
        # print("IF CONDITION")
        cursor.execute(sql_all_movies_data)
        movies_var = cursor.fetchall()
        # print("movies_var = ", movies_var)
        print("database function running")
        
        return render_template("all_movies.html", all_movies_jinja = movies_var)

    else:
        search_for = "%" + request.args['search_input_name'] + "%"
        print("ELSE CONDITION : search_for = ", search_for)

        # print("sql_query_all_tables_joined = ", sql_query_all_tables_joined)

        cursor.execute(sql_query_all_tables_joined, (search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for))
        # print("cursor_executed = ", cursor_executed)
        movies_var = cursor.fetchall()
        # print("movies_var = ", movies_var)
        return render_template('search_results.html', 
        all_movies_jinja = movies_var)
        
        

# @app.route('/edit/<todo_id>', methods=['GET', 'POST'])
# def edit_to_do(todo_id):
#     if request.method == 'GET':
        
#         cursor = pymysql.cursors.DictCursor(conn)
#         cursor.execute('SELECT * from categories')
#         categories = cursor.fetchall()
        
#         cursor.execute("SELECT * FROM todos WHERE todo_id = " + todo_id)
#         td = cursor.fetchone()
#         return render_template('edit.html', todo=td,
#                 id=todo_id,all_categories = categories)
#     else:
#         name = request.form['todo']
#         comments = request.form['comments']
#         category_id = request.form['category']
#         sql = """
#             UPDATE todos SET name = "{}", 
#                 comments = "{}",
#                 category_id = "{}"
#             WHERE todo_id = {}
#         """.format(name, comments, category_id, todo_id)
#         cursor = pymysql.cursors.DictCursor(conn)
#         cursor.execute(sql)
#         conn.commit()
#         cursor.close();
#         return redirect('/')
        



@app.route('/edit/<id>', methods=['GET', 'POST']) # id here same as table column name
def edit_movie_including_search(id): # id here pass in from route parameter as argument, same as table column name
    if request.method == 'GET':
        # if 'search_input_name' not in request.args:
            print("IF CONDITION")
            print("id from route = ", id)
            
            cursor.execute('SELECT * from language')
            language_var = cursor.fetchall()
            print("language_var = ", language_var)
            
            cursor.execute('SELECT * from genre')
            genre_var = cursor.fetchall()
            print("genre_var = ", genre_var)
            
            cursor.execute("SELECT * from censorrating")
            censorrating_var = cursor.fetchall()
            print("censorrating_var = ", censorrating_var)
            
            
            
            # movie_data_from_id = cursor.execute(sql_all_movies_data_withID + id) # test putting into variable. there is no need to put in varaible.
            # print("movie_data_from_id = ", movie_data_from_id) # returns 1
            # movietest = movie_data_from_id # returns 1
            # print("movietest = ", movietest) # returns 1
            # ans = 10 + movie_data_from_id 
            # print("ans = ", ans) # returns 11.
            
            
            
            
            # see below for sql_all_movies_data_withID sql statement. this is to execute the sql statement to join all tables using the id indirectly from route parameter which is pass into the sql statement using concatenation. + id here will be directly from function parameter.all tables because we need all info pertaining to this id to populate the edit fields.
            cursor.execute(sql_all_movies_data_withID + id) 
            # this 2nd step is needed to fetch just the movie data from the id
            movie_fetchone_sql = cursor.fetchone()
            print("movie_fetchone_sql = ", movie_fetchone_sql)
            
            # id here pass in from FUNCTION parameter as argument, same as table column name
            return render_template('edit_movie.html', 
            all_languages_jinja = language_var, 
            all_genres_jinja = genre_var,
            all_censorratings_jinja = censorrating_var,
            movie_id_jinja = id,
            movie_fetchone_jinja = movie_fetchone_sql,
            )
            
            
        # else:
        #     search_for = "%" + request.args['search_input_name'] + "%"
        #     print("ELSE CONDITION : search_for = ", search_for)
            
        #     # print("sql_query_all_tables_joined = ", sql_query_all_tables_joined)
        #     cursor.execute(sql_query_all_tables_joined, (search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for, search_for))
        #     # print("cursor_executed = ", cursor_executed)
        #     movies_var = cursor.fetchall()
        #     print("movies_var = ", movies_var)
        #     return render_template('search_results.html', 
        #     all_movies_jinja = movies_var)
            
        


    else:
        print("request.form = ", request.form)
        title_var = request.form['input_name_title']
        runtime_var = request.form['input_name_runtime']
        info_var = request.form['input_name_info']
        year_var = request.form['input_name_year']
        reviewrating_var = request.form['input_name_reviewrating']
        censorrating_var = request.form['input_name_censorrating']
        # print("censorrating_var = ", censorrating_var)
        genre_var = request.form['input_name_genre']
        language_var = request.form['input_name_language']
        actor_var = request.form['input_name_actor']
        character_var = request.form['input_name_character']
        productioncompany_var = request.form['input_name_productioncompany']
            
        
        sql_movie = """
            UPDATE movie
            
            SET 
            title = %s, 
            year = %s, 
            reviewrating = %s, 
            info = %s, 
            runtime = %s, 
            censorrating = %s
            
            WHERE `movie`.`id` = 
        """
        
        sql_input_movie = (title_var, int(year_var), float(reviewrating_var), info_var, int(runtime_var), int(censorrating_var))

        try:
            cursor.execute(sql_movie + id, sql_input_movie)
        except:
            print (cursor._last_executed)
            raise
    
        connection123.commit()
        lastrowid_movie = cursor.lastrowid
        # print("lastrowid_movie = ", lastrowid_movie)
        

        
        
        
        # INSERTING FREE TEXT WITH MN RELATIONSHIP
        sql_actor = """
            UPDATE `actor`
            
            SET 
            name = %s
            
            WHERE `movie`.`id` = 
        """
        sql_input_actor = (actor_var)

        try:
            cursor.execute(sql_actor + id, sql_input_actor)
        except:
            print (cursor._last_executed)
            raise

        connection123.commit()
        lastrowid_actor = cursor.lastrowid
        # print("lastrowid_actor = ", lastrowid_actor)
        
        
        # WEAK ENTITY OF MOVIE_ACTOR TABLE, LINKING HERE
        sql_movie_actor = """
            INSERT INTO `movie_actor`(`id`, `movie_id`, `actor_id`)
            VALUES (%s, %s, %s);
            INSERT INTO `actor`(id, name)
            VALUES (%s, %s);
            UPDATE `actor`
            
            SET 
            `movie_id` = %s,
            `actor_id` = %s
            
            WHERE `movie`.`id` = 
        """
        sql_input_movie_actor = (None, int(lastrowid_movie), int(lastrowid_actor))

        try:
            cursor.execute(sql_movie_actor + id, sql_input_movie_actor)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        
        
        # CENSORRATING. OPTION INPUT WITH 1-M RELATIONSHIP TO MOVIE.
        # NO NEED TO INSERT TO TABLE BECOZ TABLE IS FIXED
        # MOVIE TABLE UPDATED WITH INPUT FROM USER UNDER OPTION VALUE

        
        # GENRE. OPTION INPUT WITH MN RELATIONSHIP
        # NO NEED TO INSERT TO TABLE BECOZ TABLE IS FIXED
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_censorrating = """
            INSERT INTO `movie_genre`(`id`, `movie_id`, `genre_id`)
            VALUES (%s,%s,%s);
        """
        sql_input_censorrating = (None, int(lastrowid_movie), int(genre_var))

        try:
            cursor.execute(sql_censorrating + id, sql_input_censorrating)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        
        
        

        
        
        # LANGUAGE. OPTION INPUT WITH MN RELATIONSHIP
        # NO NEED TO INSERT TO TABLE BECOZ TABLE IS FIXED
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_censorrating = """
            INSERT INTO `movie_language`(`id`, `movie_id`, `language_id`)
            VALUES (%s,%s,%s);
        """
        sql_input_censorrating = (None, int(lastrowid_movie), int(language_var))

        try:
            cursor.execute(sql_censorrating + id, sql_input_censorrating)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        

        
        
        # CHARACTER. INSERTING FREE TEXT WITH MN RELATIONSHIP
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_character = """
            INSERT INTO `character`(id, name)
            VALUES (%s,%s);
        """
        sql_input_character = (None, character_var)

        try:
            cursor.execute(sql_character + id, sql_input_character)
        except:
            print (cursor._last_executed)
            raise

        connection123.commit()
        lastrowid_character = cursor.lastrowid
        # print("lastrowid_actor = ", lastrowid_actor)
        
        
        # WEAK ENTITY OF MOVIE_CHARACTER TABLE, LINKING HERE
        sql_movie_character = """
            INSERT INTO `movie_character`(`id`, `movie_id`, `character_id`)
            VALUES (%s, %s, %s);
        """
        sql_input_movie_character = (None, int(lastrowid_movie), int(lastrowid_character))

        try:
            cursor.execute(sql_movie_character + id, sql_input_movie_character)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        

        
        # PRODUCTIONCOMPANY. INSERTING FREE TEXT WITH MN RELATIONSHIP
        # NEED TO LINK TO WEAK ENTITY TABLE
        sql_productioncompany = """
            INSERT INTO `productioncompany`(`id`, `name`)
            VALUES (%s,%s);
        """
        sql_input_productioncompany = (None, productioncompany_var)

        try:
            cursor.execute(sql_productioncompany + id, sql_input_productioncompany)
        except:
            print (cursor._last_executed)
            raise

        connection123.commit()
        lastrowid_productioncompany = cursor.lastrowid
        # print("lastrowid_productioncompany = ", lastrowid_productioncompany)
        



        # WEAK ENTITY OF MOVIE_PRODUCTIONCOMPANY TABLE, LINKING HERE
        sql_movie_productioncompany = """
            INSERT INTO `movie_productioncompany`(`id`, `movie_id`, `productioncompany_id`)
            VALUES (%s, %s, %s);
        """
        sql_input_movie_productioncompany = (None, int(lastrowid_movie), int(lastrowid_productioncompany))

        try:
            cursor.execute(sql_movie_productioncompany + id, sql_input_movie_productioncompany)
        except:
            print (cursor._last_executed)
            raise
        
        connection123.commit()
        
        flash("Your Movie has been entered successfully! Thank you for populating CinemaTronix Database for the greater good! \U0001F44D ", "error")

        # THIS SHOULD NOT BE AT THE LAST PART OF THE FUNCTION else unreacheable code
        return redirect('/add')
        





sql_all_movies_data_withID = """
    SELECT * 
    FROM movie
    
    LEFT JOIN `movie_actor` ON `movie`.`id` = `movie_actor`.`movie_id`
    LEFT JOIN `actor` ON `actor`.`id` = `movie_actor`.`actor_id`
    
    LEFT JOIN `movie_character` ON `movie`.`id` = `movie_character`.`movie_id` 
    LEFT JOIN `character` ON `character`.`id` = `movie_character`.`character_id`
    
    LEFT JOIN `movie_genre` ON `movie`.`id` = `movie_genre`.`movie_id`
    LEFT JOIN `genre` ON `genre`.`id` = `movie_genre`.`genre_id`
    
    LEFT JOIN `movie_language` ON `movie`.`id` = `movie_language`.`movie_id`
    LEFT JOIN `language` ON `language`.`id` = `movie_language`.`language_id`
    
    LEFT JOIN `movie_productioncompany` ON `movie`.`id` = `movie_productioncompany`.`movie_id`
    LEFT JOIN `productioncompany` ON `productioncompany`.`id` = `movie_productioncompany`.`productioncompany_id`
    
    LEFT JOIN `censorrating` ON `movie`.`censorrating` = `censorrating`.`id`
    
    LEFT JOIN `reviewrating` ON `movie`.`reviewrating` = `reviewrating`.`id`

    LEFT JOIN `year` ON `movie`.`year` = `year`.`id`
    
    WHERE `movie`.`id` = 
    """
    # to concat id using python
    
    
    




        
sql_all_movies_data = """
    SELECT * 
    FROM movie
    
    LEFT JOIN `movie_actor` ON `movie`.`id` = `movie_actor`.`movie_id`
    LEFT JOIN `actor` ON `actor`.`id` = `movie_actor`.`actor_id`
    
    LEFT JOIN `movie_character` ON `movie`.`id` = `movie_character`.`movie_id` 
    LEFT JOIN `character` ON `character`.`id` = `movie_character`.`character_id`
    
    LEFT JOIN `movie_genre` ON `movie`.`id` = `movie_genre`.`movie_id`
    LEFT JOIN `genre` ON `genre`.`id` = `movie_genre`.`genre_id`
    
    LEFT JOIN `movie_language` ON `movie`.`id` = `movie_language`.`movie_id`
    LEFT JOIN `language` ON `language`.`id` = `movie_language`.`language_id`
    
    LEFT JOIN `movie_productioncompany` ON `movie`.`id` = `movie_productioncompany`.`movie_id`
    LEFT JOIN `productioncompany` ON `productioncompany`.`id` = `movie_productioncompany`.`productioncompany_id`
    
    LEFT JOIN `censorrating` ON `movie`.`censorrating` = `censorrating`.`id`
    
    LEFT JOIN `reviewrating` ON `movie`.`reviewrating` = `reviewrating`.`id`

    LEFT JOIN `year` ON `movie`.`year` = `year`.`id`

    """



@app.route("/movies_admin")
def movies_admin():
    cursor.execute(sql_all_movies_data)
    movies_var = cursor.fetchall()
    print("movies_var = ", movies_var)
    
    return render_template("all_movies.html", all_movies_jinja = movies_var)





if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
            

        # INSERT INTO `movie`(`id`, `title`, `runtime`, `info`, `year`, `reviewrating`, `censorrating`)
        # VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7])
        # `id`, id, NULL, genre_var, language_var, actor_var, character_var, productioncompany_var
        
        # sql = """
        #     INSERT INTO movie (`title`, `runtime`, `info`, `year`, `reviewrating`, `censorrating`)
        #     VALUES ("{}", {}, "{}", {}, {}, "{}");
            
        # """.format(title_var, runtime_var, info_var, year_var, reviewrating_var, censorrating_var)
        # SET @last_id_in_actor = LAST_INSERT_ID();
        # SET @last_id_in_movie = LAST_INSERT_ID();
        
        # INSERT INTO `movie_actor` (`movie_id`, `actor_id`)
        # VALUES (@last_id_in_movie, @last_id_in_actor)
            # SET @last_id_in_movie = LAST_INSERT_ID();
            # SET @last_id_in_actor = LAST_INSERT_ID();
            
            # INSERT INTO `movie_actor` (`movie_id`, `actor_id`)
            # VALUES (@last_id_in_movie, @last_id_in_actor)
            
            
            
# FOR POPULATING DB - YEAR TABLE
# @app.route("/add_years")
# def add_years():
#     years = range(,)
#     print(years)
#     for i in years:
#         cursor = pymysql.cursors.DictCursor(connection123)
#         # PREPARED STATEMENTS
        
#         sql = "INSERT INTO `year` (id) VALUES (%s)"
        
#         cursor.execute(sql, i)

#         connection123.commit()


# FOR POPULATING DB - REVIEWRATINGS TABLE
# @app.route("/add_ratings")
# def add_ratings():
#     list = [round(i*0.1, 2) for i in range(0,101)] 
#     print(list)
    
#     for i in list:
#         cursor = pymysql.cursors.DictCursor(connection123)
#         # PREPARED STATEMENTS
        
#         sql = "INSERT INTO `reviewrating` (id) VALUES (%s)"
        
#         cursor.execute(sql, i)
    
#         connection123.commit()

# TRIED THESE
    # list = numpy.linspace(0.0,7.5,76) # decimals problem
    # list = numpy.arange(0.0,7.5,0.1) # decimals problem
    # print(list)
    # for i in list:
    #     print(i)
        # return "nothing"
        
        # cursor.close(); # NO NEED, cursor auto close, just need 1 cursor for 1 app



    # # create an instance of the IMDb class
    # print("RUNNNNN???!!?!?!?!?!?")
    # ia = IMDb()
    # print("ia = ", ia)
    # # get all movie
    # movie = ia.get_movie("0133093")
    # print("movie = ", movie)
    # # print the genres of the movie
    # print('Genres:')
    # for genre in movie['genres']:
    #     print(genre)


# POPULATING ALL GENRES PURE AND SUB excluding horror and comedy that i created in DB
# Genres_nohororcomedy = ["Action", "Adventure", "Alien", "Alternative", "Animation", "Anime", "Avant-Garde", "B-Movie", "Biblical", "Biography", "Biopic", "British", "Chick Flick", "Children", "Comedy", "Coming of Age", "Courtroom", "Crime", "Cult", "Dance", "Disaster", "Documentary", "Drama", "Dystopia", "Epic", "Erotic", "Espionage", "Experimental", "Exploitation", "Family", "Family Movie", "Fantasy", "Femme Fatale", "Film Noir", "Game", "Gangster", "High School", "History", "Horror", "Kung Fu", "Martial Arts", "Medical", "Medieval", "Melodrama", "Military", "Mockumentary", "Monster", "Music", "Musical", "Mystery", "Neo Noir", "New Age", "Occult", "Outlaw", "Paranormal", "Post-Apocalypse", "Revenge", "Road", "Rom-Com", "Romance", "Sci-Fi", "Serial", "Short", "Silent", "Slasher", "Spaghetti Western", "Spoof", "Sport", "Spy Movies", "Superhero", "Supernatural", "Talk Show", "Tech Noir", "Thriller", "Time Travel", "Vampire", "War", "Western", "Zombie"]
# @app.route("/add_genre")
# def add_genres():
#     for i in Genres_nohororcomedy:
#         cursor = pymysql.cursors.DictCursor(connection123)
#         # PREPARED STATEMENTS
        
#         sql = "INSERT INTO `genre` (`genre`) VALUES (%s)"
        
#         cursor.execute(sql, i)

#         connection123.commit()

# POPULATING ALL languages  excluding english and chinese(mandarin) that i created in DB
# language_noenglishmandarin = ["Acholi", " Afrikaans", " Albanian", " Amharic", " Arabic", " Ashante", " Assyrian", " Azerbaijani", " Azeri", " Bajuni", " Basque", " Behdini", " Belorussian", " Bengali", " Berber", " Bosnian", " Bravanese", " Bulgarian", " Burmese", " Cakchiquel", " Cambodian", " Cantonese", " Catalan", " Chaldean", " Chamorro", " Chao-chow", " Chavacano", " Chuukese", " Croatian", " Czech", " Danish", " Dari", " Dinka", " Diula", " Dutch", " Estonian", " Espanol", " Fante", " Farsi", " Finnish", " Flemish", " French", " Fukienese", " Fula", " Fulani", " Fuzhou", " Gaddang", " Gaelic", " Gaelic-irish", " Gaelic-scottish", " Georgian", " German", " Gorani", " Greek", " Gujarati", " Haitian Creole", " Hakka", " Hakka-chinese", " Hausa", " Hebrew", " Hindi", " Hmong", " Hungarian", " Ibanag", " Icelandic", " Igbo", " Ilocano", " Indonesian", " Inuktitut", " Italian", " Jakartanese", " Japanese", " Javanese", " Kanjobal", " Karen", " Karenni", " Kashmiri", " Kazakh", " Kikuyu", " Kinyarwanda", " Kirundi", " Korean", " Kosovan", " Kotokoli", " Krio", " Kurdish", " Kurmanji", " Kyrgyz", " Lakota", " Laotian", " Latvian", " Lingala", " Lithuanian", " Luganda", " Maay", " Macedonian", " Malay", " Malayalam", " Maltese", " Mandingo", " Mandinka", " Marathi", " Marshallese", " Mirpuri", " Mixteco", " Moldavan", " Mongolian", " Montenegrin", " Navajo", " Neapolitan", " Nepali", " Nigerian Pidgin", " Norwegian", " Oromo", " Pahari", " Papago", " Papiamento", " Pashto", " Patois", " Pidgin English", " Polish", " Portug.creole", " Portuguese", " Pothwari", " Pulaar", " Punjabi", " Putian", " Quichua", " Romanian", " Russian", " Samoan", " Serbian", " Shanghainese", " Shona", " Sichuan", " Sicilian", " Sinhalese", " Slovak", " Somali", " Sorani", " Spanish", " Sudanese Arabic", " Sundanese", " Susu", " Swahili", " Swedish", " Sylhetti", " Tagalog", " Taiwanese", " Tajik", " Tamil", " Telugu", " Thai", " Tibetan", " Tigre", " Tigrinya", " Toishanese", " Tongan", " Toucouleur", " Trique", " Tshiluba", " Turkish", " Ukrainian", " Urdu", " Uyghur", " Uzbek", " Vietnamese", " Visayan", " Welsh", " Wolof", " Yiddish", " Yoruba", " Yupik"]
# @app.route("/add_language")
# def add_language():
#     for i in language_noenglishmandarin:
#         cursor = pymysql.cursors.DictCursor(connection123)
#         # PREPARED STATEMENTS
        
#         sql = "INSERT INTO `language` (`language`) VALUES (%s)"
        
#         cursor.execute(sql, i)

#         connection123.commit()


        # sql_search_movie = """
        # SELECT * from movie, genre
        # WHERE `title` LIKE %s OR 
        # `year` LIKE %s OR
        # """
        # # sql_search1 = """
        # # SELECT * from movie 
        # # WHERE year LIKE %s
        # # """
        
        # # sql_search_genre = """
        # # SELECT * from genre 
        # # WHERE `genre` LIKE %s
        # # """

        # sql_search_genre = """
        # WHERE `genre` LIKE %s
        # """
        
        # sql_search_language = """
        # SELECT * from language 
        # WHERE `language` LIKE %s
        # """
        
        # sql_search_actor = """
        # SELECT * from actor 
        # WHERE `name` LIKE %s
        # """
        
        # sql_search_character = """
        # SELECT * from character 
        # WHERE `name` LIKE %s
        # """
        
        # sql_search_productioncompany = """
        # SELECT * from productioncompany 
        # WHERE `name` LIKE %s
        # """
        
        # sql_combined = sql_search_movie + sql_search_genre
        # print("sql_combined = ", sql_combined)



# def search():
#     print("request.args1 = ", request.args)
#     if "search_input_name" in request.args:
#         #     print("request.form = ", request.form)
#         print("request.args2 = ", request.args)
#         sql_search1 = """
#         SELECT * from movie 
#         WHERE `movie.title` LIKE %s OR 
#         `movie.year` LIKE %s
#         """
#         # sql_search1 = """
#         # SELECT * from movie 
#         # WHERE year LIKE %s
#         # """
        
#         sql_search2 = """
#         SELECT * from genre 
#         WHERE `genre.genre` LIKE %s
#         """
        
#         sql_search3 = """
#         SELECT * from language 
#         WHERE `language.language` LIKE %s
#         """
        
#         sql_search4 = """
#         SELECT * from actor 
#         WHERE `actor.name` LIKE %s
#         """
        
#         sql_search5 = """
#         SELECT * from character 
#         WHERE `character.name` LIKE %s
#         """
        
#         sql_search6 = """
#         SELECT * from productioncompany 
#         WHERE `productioncompany.name` LIKE '%s
#         """