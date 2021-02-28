# Washington, D.C. Neighborhood Analysis
### DSCI 551 Semester Project, Spring 2021

## Team

Madeleine Thompson - B.S. Chemistry with Mathematics Minor, M.S. Applied Data Science. I have worked with Python in web scraping, API crawling, and general data analysis. I have also used SQL (SQLite), Stata, MATLAB, and some Java in the past. I chose to work on my own because the project that I want to work on is based on my specific interests and will help me make a very important personal decision (what neighborhood to move to).

## Project/ Problem

The problem that I want to tackle is to collect real estate, restaurant, and Google Maps data to better inform me of what neighborhood I want to live in when I move to Washington, D.C. for work in the next few months. I want to use this data to build a dashboard (like Google Maps) that breaks down each neighborhood in D.C. based on my preferences (e.g. affordable, access to close vegan restaurants, shorter commute to work, etc.).

## Data
* Yelp Fusion API: 
  * https://www.yelp.com/developers/documentation/v3/get_started
* Google Maps API:
  * https://developers.google.com/maps
* Redfin Data:
  * https://www.redfin.com/news/data-center/ 
* ZIP Codes for DC, Maryland, and Virginia: 
  * https://www.zip-codes.com/state/dc.asp
  * https://www.zip-codes.com/state/md.asp
  * https://www.zip-codes.com/state/va.asp

## Plan

First, I need to figure out what areas I want to collect data for. Do I want to limit my search to only the city of Washington, D.C. or do I also want to look at some cities in Maryland and Virginia (surrounding states). Then, I will scrape the data from Yelp, Google Maps, and Refin for the relevant cities. I will store this data in a NoSQL database (probably MongoDB, but I want to further research which option will be best for my data). After this, I will need to create a dashboard to upload my data to and visualize the data that I have collected.
