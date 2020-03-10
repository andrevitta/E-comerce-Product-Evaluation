![IronHack Logo](https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/upload_d5c5793015fec3be28a63c4fa3dd4d55.png)

# E-comerce Product Evaluation

# Overview

The goal of this project is for us to practice what we have learned in the Intermediate Python and Data Engineering chapter of the program. 

We worked on building a pipeline to automate all process from data aquisition to the final visualization.

Evaluate Garnier’s product   customers evaluation over e-commerce

* Identify better evaluated products
* Classify commentaries over good and bad
* Product most bought together
* Identify most used words over good and bad evaluations

# Data Aquisition

Data was colected from a major e-comerce plataform using web scraping technics and  python requests libary. I've narrow down to a specific brand of products so I could have a more reduced scope of products. Aquisition consist on acessing the main webpage using a specific query. Each product name and link was read and their specific page acessed. I was able to gather 255 product with over 5000 coments and evaluations.

<img src="./image/Data_scrapping_flow.PNG" alt="Data flow" width="500"/>

# Results

To simplify analisis, I've picked the top 5 best product according to their evaluation to represent the final results.

<img src="./image/results.PNG" alt="Data flow" width="500"/>
