# sqlalchemy-challenge

## Instructions
* The focus of the assignment is to analyze climate data in advance of taking a trip to hawaii 
* There are 2 main parts to the activity
    * part 1: Analyze and Explore the Climate Data in Jupyter Notebook
    * part 2: Design a climate app (Flask API) using the queries from the jupyter notebook

## Part 1: Climate Analysis
* Use Python and SQLAlchemy to do a basic climate analysis and data exploration
* Use SQLAlchemy ORM queries along with Pandas and Matplot to
    * connect to SQLLite database, reflect tables into classes and link Python to the database using SQLAlchemy session
    * conduct a PRECIPITATION ANALYSIS: 
        * query precipitation over last 12 months from latest date. 
        * read query results into DataFrame and generate a line plot -- which should replicate sample image provided in homework.
    * conduct a STATION ANALYSIS:
        * design a query to calculate number of stations in the dataset
        * determine the most active station
        * design a query to return min, max, and average temperature for the most active station for the last year of data
        * plot a histogram with the temperature observations. the histogram should have 12 bins
* Close session.
