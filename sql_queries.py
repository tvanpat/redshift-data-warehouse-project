import configparser


# Load CONFIG File
config = configparser.ConfigParser()
try:
    config.read_file(open('vpaws.cfg'))
except:
    config.read_file(open('dwh.cfg'))

# Load Parameters
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_PATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")
IAM_ROLE = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay_fact"
user_table_drop = "DROP TABLE IF EXISTS user_dim"
song_table_drop = "DROP TABLE IF EXISTS song_dim"
artist_table_drop = "DROP TABLE IF EXISTS artist_dim"
time_table_drop = "DROP TABLE IF EXISTS time_dim"

# CREATE TABLES

staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events(
artist          VARCHAR,
auth            VARCHAR,
first_name       VARCHAR,
gender          VARCHAR,
item_in_session   INTEGER,
last_name        VARCHAR,
length          NUMERIC,
level           VARCHAR,
location        VARCHAR,
method          VARCHAR,
page            VARCHAR,
registration    BIGINT,
session_id       INTEGER,
song            VARCHAR,
status          INTEGER,
ts              TIMESTAMP,
user_agent       VARCHAR,
user_id          INTEGER
);
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
    artist_id VARCHAR,
    artist_latitude NUMERIC,
    artist_location VARCHAR,
    artist_longitude NUMERIC,
    artist_name VARCHAR,
    duration FLOAT,
    num_songs INTEGER,
    song_id VARCHAR,
    title VARCHAR,
    year INTEGER
);
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS user_dim(
user_id INTEGER DISTKEY,
first_name VARCHAR,
last_name VARCHAR,
gender VARCHAR,
level VARCHAR,
PRIMARY KEY(user_id)
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song_dim(
song_id VARCHAR,
title VARCHAR,
artist_id VARCHAR distkey,
year INTEGER,
duration NUMERIC,
PRIMARY KEY (song_id),
FOREIGN KEY(artist_id) REFERENCES artist_dim(artist_id)
);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artist_dim(
artist_id VARCHAR distkey,
name VARCHAR,
location VARCHAR,
latitude NUMERIC,
longitude NUMERIC,
PRIMARY KEY (artist_id)
);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time_dim(
start_time TIMESTAMP sortkey distkey,
hour INTEGER,
day INTEGER,
week INTEGER,
month INTEGER,
year INTEGER,
weekday INTEGER,
PRIMARY KEY(start_time)
);
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay_fact(
songplay_id          INTEGER IDENTITY(0,1)  sortkey,
start_time           TIMESTAMP,
user_id              INTEGER,
level                VARCHAR,
song_id              VARCHAR,
artist_id            VARCHAR,
session_id           INTEGER,
location             VARCHAR,
user_agent           VARCHAR,
PRIMARY KEY (songplay_id),
FOREIGN KEY(start_time) REFERENCES time_dim(start_time),
FOREIGN KEY(user_id) REFERENCES user_dim(user_id),
FOREIGN KEY(song_id) REFERENCES song_dim(song_id),
FOREIGN KEY(artist_id) REFERENCES artist_dim(artist_id)
);
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {}
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    TIMEFORMAT as 'epochmillisecs'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
    FORMAT AS JSON {};
""").format(LOG_DATA, IAM_ROLE, LOG_PATH)

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    CREDENTIALS 'aws_iam_role={}'
    COMPUPDATE OFF region 'us-west-2'
    FORMAT AS JSON 'auto'
    TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES

songplay_table_insert = (""" INSERT INTO songplay_fact
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT to_timestamp(to_char(se.ts, '9999-99-99 99:99:99'),'YYYY-MM-DD HH24:MI:SS'),
                se.user_id as user_id,
                se.level as level,
                ss.song_id as song_id,
                ss.artist_id as artist_id,
                se.session_id as session_id,
                se.location as location,
                se.user_agent as user_agent
    FROM staging_events se
    JOIN staging_songs ss ON se.song = ss.title AND se.artist = ss.artist_name;
""")

user_table_insert = ("""
INSERT INTO user_dim(user_id, first_name, last_name, gender, level)
SELECT DISTINCT user_id as user_id,
                first_name as first_name,
                last_name as last_name,
                gender as gender,
                level as level
FROM staging_events
where user_id IS NOT NULL;
""")

song_table_insert = ("""INSERT INTO song_dim(song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id as song_id,
                title as title,
                artist_id as artist_id,
                year as year,
                duration as duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""INSERT INTO artist_dim(artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id as artist_id,
                artist_name as name,
                artist_location as location,
                artist_latitude as latitude,
                artist_longitude as longitude
    FROM staging_songs
    where artist_id IS NOT NULL;
""")

time_table_insert = ("""INSERT INTO time_dim(start_time, hour, day, week, month, year, weekday)
    SELECT distinct ts,
                EXTRACT(hour from ts),
                EXTRACT(day from ts),
                EXTRACT(week from ts),
                EXTRACT(month from ts),
                EXTRACT(year from ts),
                EXTRACT(weekday from ts)
    FROM staging_events
    WHERE ts IS NOT NULL;
""")

# QUERY LISTS

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop,
                      songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [staging_events_table_create, staging_songs_table_create,
                        user_table_create, artist_table_create, song_table_create,  time_table_create, songplay_table_create]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [user_table_insert, artist_table_insert,
                        song_table_insert, time_table_insert, songplay_table_insert, ]
