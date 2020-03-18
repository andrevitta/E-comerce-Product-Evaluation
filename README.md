![IronHack Logo](https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/upload_d5c5793015fec3be28a63c4fa3dd4d55.png)

# E-comerce Product Evaluation

# Overview

I worked on building a pipeline to automate all processes from data acquisition to the final visualization.

Evaluate Garnier’s product   customers evaluation over e-commerce

* Identify better evaluated products
* Classify commentaries over good and bad
* Product most bought together
* Identify most used words over good and bad evaluations

# Data Acquisition

Data was collected from a major e-commerce platform using web scraping techniques and  python requests library. I've narrowed down to a specific brand of products so I could have a more reduced scope of products. Acquisition consists of accessing the main webpage using a specific query. Each product name and link was read and their specific page accessed. I was able to gather 255 products with over 5000 comments and evaluations.

<img src="./image/Data_scrapping_flow.PNG" alt="Data flow" width="500"/>

The website wacs mapped and scraped for each product found and them their link was collected and stored


<img src="./image/articles_amazon.PNG" alt="Data flow" width="700"/>

With the the link for each of the 255 products a loop was used to access all of them to retrieve the ratings for the specific product

<img src="./image/rating.PNG" alt="Data flow" width="700"/>

Finally all comments for each product were also retrieved and stored together with their info, overall 5000 comments were stored.


<img src="./image/comments.PNG" alt="Data flow" width="700"/>

# Results

Below are the top 5 product according to their evaluation to present the final results.

<img src="./image/results.PNG" alt="Data flow" width="500"/>
