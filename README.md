# Naviance 2.0
MaKERs<br>
Ryan Siu, Michela Marchini, Kerry Chen, Edmond Wong<br>
Software Development<br>
Project 01<br>
Period 9<br>

## Overview
Welcome to Naviance II!  The goal of our app is to provide a comprehensive overview of any college you may want.  Users simply search the name of a college and are presented with data about the school, ranging from their acceptance rate, to the ehtnic breakdown of the school, and even a map of the surrounding area.  Those users who decide to create accounts can save colleges in their favorites for easy access.  We used the College Scorecard API to access colleges' data and the Google Maps Embed API to embed a map of the colleges' surroundings.

## Installation and Setup
Installing and setting up our app should be simple.

### Getting API Keys
1. Go to https://api.data.gov/signup and fill out the form to get an API key.  The API key will be emailed to you.  
2. To get the Google Maps API key, go to https://developers.google.com/maps/documentation/embed/.  Click the "Get A Key" button in the top right corner and follow the steps to get an API key.

### Using the API Keys
3. Create a file called ```config.py```. Paste the following inside, replacing the angle brackets...

### Installing and Running the Application

When you get it, copy and paste it into the file called config.py inside the quotation marks next to COLLEGE_API_KEY.    Once you have your API key, copy and paste it into config.py inside the quotation marks next to GOOGLE_API_KEY. <br>
In order to run this app, your computer will need to be running python.  If it is not already on your computer (it comes preinstalled on Macs), you can download it here: https://www.python.org/downloads/.  In addition, you will need to install Flask.  You can do this by going to your terminal and typing "pip install Flask". <br>
Congratulations, you are now ready to run Naviance II!
