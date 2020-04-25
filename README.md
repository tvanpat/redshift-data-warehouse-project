# Data Warehousing with Redshift
 A data warehouse project for the Udacity Data Engineer Nanodegree

 This README file includes a summary of the project, how to run the Python scripts, and an explanation of the files in the repository.

 ## Getting Started

 1.  You will need to first connect and build the Redshift Database.  First open the deh.cfg file and enter your aws key and secret.  YOU MUST ADD THIS FILE TO YOUR .gitignore if you are using github.  Failure to do so may expose your aws key and secret.  If you are using a custom configuration file, replace the vpaws.cfg file name thought-out all the scripts.

 2.  Next open the aws_setup.ipynb file.  Run each cell.  Stop after step 7.  Step 8 and 9 are to delete the Redshift database.  Only use those once your project is complete.

 3.  Run the create_table.py using the following command:
 > python create_tables.py

4.  You can check the table creation in the aws_data_test.ipynb file.  Open this file and run all cells through "Check Table Creation".

5.  Once the tables have been created use the command below to copy data from the S3 bucket to the staging tables and then to insert the data from the staging tables into the appropriate fact or dimension table.

 >python etl.py

 6.  Once you no longer need the database go to the aws.setup.ipynb file and run cells 8 and 9.  This will delete your Redshift cluster and all data stored on it.  This will also delete the endpoint, host, and the arn data from the configuration file.

 ## Prerequisites
 1.  **pandas**

 2.  **boto3**

 ## Purpose
 The purpose of this database is to conduct ETL operations and store data from user activity from the Sparkify app.  
 This data will be used by the Sparkify analytics team will use this data gain a greater understanding of user activity and songs being listened to.


 ## Database Schema
 There are 5 tables in the database.  This design focuses on the songplay table which houses the most important information for the analytics team.  The supporting tables of time, users, songs, and artists help to provide context and additional details for the songplay table.

 There are two staging tables **staging_events** and the **staging_songs** tables.  These tables are to temporally hold data from the S2 Bucket before being transformed and inserted into the primary use tables.

 The **staging_songs** table contains:

 | Field           | Data Type          |
  |-------------  | -------------         |
 | artist_id            | VARCHAR                    |
 | artist_latitude   | NUMERIC                   |
 | artist_location  | VARCHAR                 |
 | artist_longitude | NUMERIC                  |
 | artist_name        | VARCHAR                 |
 | duration              | FLOAT                  |
 | num_songs         | INTEGER                   |
 | song_id               | VARCHAR                |
 | title                     | VARCHAR                 |
 | year                    | INTEGER                 |

  The **staging_events** table contains:

  | Field           | Data Type          |
   |-------------  | -------------         |
  | artist             | VARCHAR                    |
  | auth     | VARCHAR                  |
  | first_name  | VARCHAR                 |
  | gender | VARCHAR                  |
  | item_in_session       | INTEGER                 |
  | last_name        | VARCHAR                 |
  | length            | NUMERIC                  |
  | level          | VARCHAR                |
  | location              | VARCHAR                |
  | method                    | VARCHAR                |
  | page                  | VARCHAR                 |
  | registration           | BIGINT                  |
  | session_id          | INTEGER                   |
  | song              | VARCHAR                |
  | status                     | INTEGER            |
  | ts                  | TIMESTAMP               |
  | user_agent                     | VARCHAR  |
  | user_id                 | INTEGER                 |

![Staging ERD Diagram](/images/stage_erd.png)


The use tables are the **songplay_fact**, **time_dim**, **user_dim**, **song_dim**, and **artist_dim** tables.  These tables are in the

 The **time table** which contains:

 | Field        | Data Type          | Key       | KEYDIST |
  |-------------  | ------------- | ------------- | ------------- |
 | start_time      | TIMESTAMP | Primary | SORTKEY/DISTKEY |
 | hour      | INTEGER     |    | |
 | day | INTEGER      |     | |
 | week | INTEGER      |     | |
 | month | INTEGER      |     | |
 | year | INTEGER     |     | |
 | weekday | INTEGER     |     | |

 The **users table** which contains:

 | Field        | Data Type          | Key  | KEYDIST |
 | ------------- | ------------- |  ------------- | ------------- |
 | user_id      | INTEGER | Primary | |
 | first_name      | VARCHAR      |    | |
 | last_name | VARCHAR      |     | |
 | gender | VARCHAR      |     | |
 | level | VARCHAR     |     | |

 The **songs table** which contains:

 | Field        | Data Type          | Key  | KEYDIST |
 | ------------- | ------------- |  ------------- | ------------- |
 | song_id      | VARCHAR | Primary | |
 | title      | VARCHAR      |    | |
 | artist_id | VARCHAR      |  Foreign Key   | |
 | year | INT      |     | |
 | duration | NUMERIC     |     | |

 The **artists table** which contains:

 | Field        | Data Type          | Key  | KEYDIST |
 | ------------- | ------------- |  ------------- | ------------- |
 | artist_id      | VARCHAR | Primary | DISTKEY |
 | name      | VARCHAR      |    | |
 | location | VARCHAR      |    | |
 | latitude | NUMERIC      |     | |
 | longitude | NUMERIC   |     | |

 The **songplay table** which contains:

 | Field        | Data Type          | Key  | KEYDIST |
 | ------------- | ------------- |  ------------- | ------------- |
 | songplay_id      | INT | Primary | SORTKEY |
 | start_time      | TIMESTAMP    |  Foreign Key  | |
 | user_id | INTEGER  |  Foreign Key   | |
 | song_id | VARCHAR      |  Foreign Key   | |
 | artist_id | VARCHAR     |  Foreign Key   | |
 | session_id | INT  |     | |
 | location | VARCHAR      |     | |
 | user_agent | VARCHAR     |     | |

 ![ERD Diagram](./images/snowflake_erd.png)

## File Description

- aws_data_test.ipynb
 - This file is used to check the if tables have been successfully created in Redshift and to check if data was properly loaded from S3 buckets to the staging tables and from staging tables to the use tables.

- aws_setup.ipynb
 - The file is used to set up the Redshift cluster.  Before connecting the aws key and secret must be added to the dwh.cfg file.  This file will also be used to delete the Redshift cluster to avoid excess charges.

- create_tables.py
 - This file is used to create the staging and use tables in Redshift.  It will import the create table queries from the sql_queries.py.  To execute this file use the following command:
 > python create_table.py

- dwh.cfg
 - This is the configuration file which stores aws key, aws secrets, and settings for the aws cluster.  ENSURE THIS FILE IS ADDED TO YOUR .gitignore FAILURE TO DUE SO MAY RESULT IN AWS KEY AND SECRETS BEING EXPOSED.

- etl.py
 - This file is used to transfer data from S3 Buckets to staging tables and then to insert data from the staging tables into the use tables.  This file will import the copy and insert commands from the sql_queries.py script.  To execute this file use the following command:
 > python etl.py

- sql_queries.py
 - This file contains the queries used to create tables in Redshift and ETL data from the S3 Bucket into the staging table and then insert data from the staging table into the use tables.

- log_data_file_tst
 - This file contains an example of the log data currently contained in the S3 Bucket.

- song_data_file.json
    - This file contains an example of the song data currently contained in the S3 Bucket.
