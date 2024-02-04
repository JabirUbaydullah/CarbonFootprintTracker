# CarbonFootprint

## Inspiration

The topic I wanted to address was promoting sustainability by encouraging decreasing the carbon footprint of the food we eat.

## What it does

The web application allows the user to enter in specific amounts of ingredients that they are consuming and will show the total carbon footprint of the complete recipe with all the ingredients together. This application also allows users to see the number of miles of driving that would produce an equivalent amount of carbon as the amount of food they are eating.

## How we built it

Carbon Footprint Tracker was built in Python and using the following libraries and services:

* [streamlit](https://streamlit.io) for the web user interface and web application hosting
* [pandas](https://pandas.pydata.org) for all data transformation and aggregation
* [plost](https://github.com/tvst/plost) for the carbon footprint contribution donut chart

## Challenges we ran into

The most significant challenge I ran into was finding carbon footprint data as I could not find any comprehensive lists of carbon footprints of food items and instead had to manually collect values from a variety of websites. 

## Accomplishments that we're proud of

I am very happy that I managed to create the web application I had envisioned with a fairly comprehensive list of ingredients and the dynamic total carbon footprint calculation and individual ingredient carbon footprint contributions working correctly all of which felt a bit daunting when I began the project. 

## What we learned

This project allowed me to gain more experience creating stateful UI’s using streamlit. I also gained more experience using pandas both for extracting and transforming data.

## What's next for Carbon Footprint Tracker

In the future I plan to improve Carbon Footprint Tracker by increasing the number of ingredients even further as well as adding a feature to suggest recipes that have a low carbon footprint.
