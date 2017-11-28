# Naviance II
MaKERs<br>
Ryan Siu, Michela Marchini, Kerry Chen, Edmond Wong<br>
Software Development<br>
Project 01<br>
Period 9<br>

## Overview
Welcome to Naviance II!  The goal of our app is to provide a comprehensive overview of any college you may want.  Users simply search the name of a college and are presented with data about the school, ranging from their acceptance rate, to the ehtnic breakdown of the school, and even a map of the surrounding area.  Those users who decide to create accounts can save colleges in their favorites for easy access.  We used the College Scorecard API to access colleges' data and the Google Maps Embed API to embed a map of the colleges' surroundings.

## Installation and Setup
Installing and setting up our app should be simple.

### Downloading the Application
1. Clone this repository with `git clone https://github.com/siuryan-cs-stuy/naviance2.0.git`.

### Getting API Keys
2. Go to the [College Scorecard website](https://api.data.gov/signup) and fill out the form to get an API key.  The API key will be emailed to you.  
3. Get the [Google Maps API key](https://developers.google.com/maps/documentation/embed/).  Click the "Get A Key" button in the top right corner and follow the steps to get an API key.

### Using the API Keys
4. Create a file called `config.py` in the root directory of the application. Paste the following inside, replacing the angle brackets and the text inside with the respective API key you created.
```
COLLEGE_API_KEY = <API_KEY_FROM_STEP_1>
GOOGLE_API_KEY = <API_KEY_FROM_STEP_2>
```

### Running the Application
5. In order to run this app, your computer will need to have Python 2.7 and the Flask module.  To install Flask, use `pip install Flask` in the terminal.
6. In the root directory of the application, run `python main.py`.
5. Open a web browser and go to `localhost:5000`. Congratulations, you should be running Naviance II!
