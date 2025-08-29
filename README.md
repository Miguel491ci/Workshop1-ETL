## 1. Project Architecture

This section will include a flow diagram explaining the technologies used in the project:

<img width="772" height="568" alt="image" src="https://github.com/user-attachments/assets/4456d2fb-533e-4608-aa2d-3539e9ec62a3" />


## 2. Dimensional Model

This section will include the star schema diagram with the fact and dimension tables used.

<img width="1095" height="622" alt="image" src="https://github.com/user-attachments/assets/b88ef68b-f861-4004-8137-1ae5cc9f4572" />

Justification of the Data Model

This data model follows a star schema design, which simplifies reporting, querying, and analysis. At the center of the model, the FactHiring table captures the measurable outcomes of the hiring process, while the surrounding dimension tables provide descriptive context.

Fact Table (FactHiring):
The fact table stores key metrics related to candidate hiring, such as the CodeChallengeScore, TechnicalInterviewScore, and the HiredFlag indicator. These measures enable the analysis of candidate performance and hiring decisions across multiple perspectives.

Dimension Tables:

DimCandidate: Contains descriptive attributes of candidates, such as name, email, and years of experience, providing a detailed view of each applicant.

DimCountry: Stores the country information, enabling geographical analysis of hiring trends.

DimDate: Facilitates time-based analysis at different granularities (day, month, year, quarter).

DimSeniority: Provides hierarchical levels of seniority, allowing evaluation of hiring decisions across different job levels.

DimTechnology: Represents the technologies related to the candidates’ profiles or roles, making it possible to analyze hiring trends by technical expertise.

This design ensures high query performance and data consistency by separating facts from dimensions. Analysts can easily slice and dice the data across multiple dimensions (time, technology, geography, seniority, and candidate profiles).

## 3. ETL Process

Files included in the project:

connect.py → Contains the logic and permissions for connecting to the database in mysql workbench. Make sure to change the permissions for it to work properly.

Data/candidates.csv → Csv file with the data used in this project

db.py → Has the script to create the database and its tables based on the dimensional model

DB.sql → Backup with the script for creating the database but in sql format 

etl.py → Main ETL script that connects to sources, transforms the data, and loads it into MySQL.

main.py → Contains the script that runs everything in the project, this is the file you will run.

KPIs_&_DAX_Statements.txt → Info about the different KPIs required for the visualization and the DAX statements for PowerBI

Dashboard.pbix → final file with the KPIs and visualization.


The ETL process was implemented in Python and consists of the following steps:

Extraction:
Data is collected from the original sources (input files).

Transformation:

Data cleaning.

Date format conversion and normalization of values.

Creation of surrogate keys for dimension tables.

Creating the attribute HiredFlag and the necessary logic for it to determine when a candidate is hired or not

Load:
The transformed data is inserted into the Data Warehouse in MySQL Workbench.


## 4. Data Warehouse in MySQL Workbench

A star schema dimensional model was designed, with a central fact table and multiple dimension tables:

Fact_Hires → Contains hiring records (facts).

Dim_Technology, Dim_Country, Dim_Time, Dim_Seniority, among others → Provide context for analysis.

These structures are uploaded and managed in a Data Warehouse implemented in MySQL Workbench.

inserts.sql → Initial test data population.

## 5. Visualization in Power BI

The final layer of the project was developed in Power BI, connecting directly to the Data Warehouse in MySQL.

Several KPIs and interactive graphs were created, including:

- Hires by Technology 

- Hires by Year

- Hires by Country (focused on USA, Brazil, Colombia, and Ecuador)

- Hires by Seniority

- Hire rate percentage

- Average code challenge score and average technical interview score

This are the necessary DAX sentences respectively to solve this KPIs:

- Total Hires = COUNTROWS( FILTER('hiring_excercise facthiring', 'hiring_excercise facthiring'[HiredFlag] = TRUE() ) )
- Hires Key Countries = 
CALCULATE(
    [Total Hires],
    KEEPFILTERS(
        'hiring_excercise dimcountry'[CountryName] IN { "United States of America", "Brazil", "Colombia", "Ecuador" }
    )
)
- Hire Rate (%) = 
DIVIDE(
    [Total Hires], 
    COUNTROWS('hiring_excercise facthiring'),
    0
)
- Avg Code Challenge Score = AVERAGE('hiring_excercise facthiring'[CodeChallengeScore])
- Avg Technical Interview Score = AVERAGE('hiring_excercise facthiring'[TechnicalInterviewScore])

(The first DAX sentence is required for the first 4 KPIs.)

This is how the Dashboard looks:

<img width="1158" height="654" alt="image" src="https://github.com/user-attachments/assets/83e2b83c-8548-4051-ad2b-b5c5c9aca5fb" />



## 6 How to Replicate the Project

Clone this repository.

Make sure to change the permissions in 'connect.py' to your own permissions allowing the project to connect to MySQL Workbench

Run the ETL process with main.py.

Open dashboard.pbix in Power BI and connect it to the Data Warehouse.
