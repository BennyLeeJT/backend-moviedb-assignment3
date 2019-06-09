# Project's Name : CinemaTronix

>> Assignment3-Data Centric Development Milestone Project
My project is called "CinemaTronix". It is a Movie Database that is able to provide essential information for anyone wanting to know enough information quickly to make a decision in watching or recommending a good movie.

All that a user has to do is to search for a movie title. If they wish, they can also search or filter based on the options available for them, so that they can see what other movies there are, that they might be interested in based on their filter criteria selection. The website also allow users to populate the database by creating new movie title and its details, to edit existing movie and to delete as well.


## UX
 
This website is for movie lovers and those wanting to quickly find some information to decide whether they would like to watch a particular movie or not.

As a user who wants to watch movies with good ratings only, I will be visiting the website for my search. If I have a movie title, I will search using the movie title to see its review rating, genre and runtime. Else, I will check out the database either via a detailed sortable table format or via the filter function so I can focus better to see what other movies there are for my liking.

As a film enthusiast, I will be searching for titles and reading any info there may be.

As a user who wants to help to populate the database with the mindset that with everyone's contribution, it will become useful for the benefit of everyone, I will use the "Add Movie" form to fill in the details. If I see any typo or errors or duplicate, I will use the edit and delete functions.

The schema diagram that I come up with filename "moviedb.svg" is stored in a separate folder name Database Schema.


## Features

In this section, you should go over the different parts of your project, and describe each in a sentence or so.


### Existing Features
- Feature 1 - allows user to add movie and its information into the database by filling out a form (add_movie.html, layout_index.html)

- Feature 2 - allows user to view all the movies that is currently in the database in a detailed table format (all_movies.html, layout_search_results.html)

- Feature 3 - allows user to sort the table by ascending or descending order (all_movies.html, layout_search_results.html, static/js/sorttable.js)

- Feature 4 - allows user to edit any movie while at the database table view (edit_movie.html, layout_index.html)

- Feature 5 - allows user to delete any movie while at the database table view (delete_movie.html, layout_index.html)

- Feature 6 - allows user to filter by 5 different movie attributes namely Genre, Language, Year of Release, Censor Rating and Review Rating. Each of these category provides their full list of options (layout_index.html, filter_genre.html, filter_language.html, filter_year.html, filter_censorrating.html, filter_reviewrating.html, filter_grid.html)

- Feature 7 - when the user chooses a filter and its options, there will be a filtered results count displayed to the user to show how many movies are avaiable in the database that fit the filter selections (layout_index.html, filter_grid.html)

- Feature 8 - user can click on each movie in the filtered result webpage to go in and show the full details of that movie (layout_index.html, single_movie.html)

- Feature 9 - there is a seach bar function on top of every webpage to allow keyword search at anytime (layout_index.html, layout_search_results.html)

(filter_results.html was initially used before replaced by filter_grid.html. Kept for checking data retrieval accuracy)
(all_movies_admin.html is used to check CRUD accuracy by displaying more ids of some of the columns)


### Features Left to Implement
Feature ideas would be :
- to display movie images / thumbnails
- allow user to upload movie images / thumbnails
- allow multiple words to be searchable
- allow multipe filters simultaneously in one html
- to display filter results instantaneously (seemingly) as user select the filter options, without reloading the webpage
- existing free text input of data, checkable to prevent data duplication

## Technologies Used
- Python : The programming language used for this backend project

- Flask : The Python microframework used to route urls

- Jinja2 : The Python Template Engine used to display data from gathered by python onto html

- MySQL / pymysql / phpPHPmyadmin : relational database used

- Bootstrap (getbootstrap.com) : Bootstrap is used to enable mobile responsive webpages

- jQuery (jquery.com) : This project uses **JQuery** to simplify DOM manipulation, which is also used by templates point and in bootstrap themselves

- sorttable.js (www.kryogenix.org/code/browser/sorttable/) : This js file is used to enable sorting of table headers quickly and easily

- Canva (www.canva.com) : Canva was used to design and create the website logo

- Templates Point (www.templatespoint.net) : The frontend HTML CSS JS is largely obtained from a free responsive sample movie template (FlixGo) provided by Templates Point, and modified for this project's use, in order to save time in designing the backbone of the look and feel.


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.


1. Add Movie:
    1. Go to the "Add Movie" page
    2. Try to submit the empty form or missing required fields and verified that an error message about the required fields appears
    3. Try to submit the form with alphabets keyed in for number or float fields and verified that a relevant error message appears
    4. Try to submit the form with all inputs valid and verified that a success message appears
    5. Go to "Full Database" page to check all details keyed in and verified that all details appears correct as keyed in the form

2. Filter By:
    1. Click on the "Filter By" link on nav bar and click on each of the 5 movie attribute and verified that the page reloads to the correct html
    2. In each of the 5 webpages, the full options are available to be selected as per the populated data in MySQL database
    3. Verified that each of the 5 options selected and clicked submit will load the filter results page with the correct retrieval of data
    4. Verified that the total no. of records retrieved from database based on filter selections, is shown as accurate as per the result count displayed for the choice made
    5. Verified that each movie shown in the filtered results can be clicked to load the single movie page with the data shown correctly
    6. Go to "Full Database" page to check all details retrieved and verified that filtered results shows the same information as per database

3. Edit Movie:
    1. Go to the "Full Database" page and click on Edit on a movie
    2. Verified that Edit form page loads correctly and all fields populated with current data as per database records
    3. Try to submit the form with alphabets keyed in for number or float fields and verified that a relevant error message appears
    4. Try to submit the form with all inputs valid and verified that a success message appears
    5. Go to "Full Database" page to check all details keyed in and verified that all details appears correct as keyed in the form

4. Delete Movie:
    1. Go to the "Full Database" page and click on Delete on a movie
    2. Verified that Delete form page loads correctly and all fields populated with current data as per database records
    3. Try to submit the form and verified that a success message appears
    4. Go to "Full Database" page to check that movie and its details is gone

5. Search Bar:
    1. Go to every html page to click the magnifying glass button and key in a keyword and press enter. Verified that search bar will slide down in every page and once enter key or search button is pressed, the search results page will load
    2. Verified that search results page show every movie display contains the keyword in one or more of its attributes
    3. Try to submit the form and verified that a success message appears
    4. Go to "Full Database" page to check that movie and its details is gone

6. Full Database:
    1. Click on each header of movie attribute and verified that each header allows sorting by ascending or descending
    2. Verified that the sorting of ascending or descending is correct and the column itself sorts text case-insensitvely
    
7. Different Browsers:
    1. Each web page looks equally good in desktop Chrome, Firefox, Internet Explorer and Edge
    2. Only internet explorer shows that the table header css position: sticky isn't working. This happened whn in Full Database webpage and the Search Results webpage
    3. Mobile browser chrome checked and working well
    4. Using Developer Tools in desktop chrome, the default variety of phone and tablets dimensions given are used to check on mobile browsers and all seems well

On my manual testing :
One way to see my testing logs is based on the current data in the database. If you go to http://backend-assignment3-roczi.c9users.io:8080/movies_admin (I am using Desktop Chrome) and press Ctrl+F and type in "None", all the "None" will be highlighted and as you scroll down, you would see that the amount of "None" per record reduces as I code the relations correctly and retrieve and display the data correctly, as per their increasing ids for each columns.

However, Bugs:
- Was told switching from cloud9 phpmyadmin to removesql is necessary for heroku deployment. Filter By function does not work using remotesql
- got the error pymysql.err.InternalError: (1055
- if i change my code not to use GROUP BY, i get error pymysql.err.InternalError: (1140
- after trying a few online solutions to disable sql_mode=only_full_group_by, it is still not working
- sample filter including count that is success using cloud9 phpmyadmin : https://ibb.co/X3RZPnt
- can swith the connection back to cloud9 localhost, restart the app, to use the filter by function.


## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- text content are all self created

### Media
- background image is by Templates Point FlixGo template.

### Acknowledgements

- I received inspiration for this project from regular visits to www.IMDB.com
