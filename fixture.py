import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_values
from connection import dbConnection
from app.models import User


def create_db():
    try:
        conn = dbConnection.connect_postgredb()
        print(conn)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE webapp_db")

    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def create_tables():
    TABLES = {}
    TABLES["table_name"] = [
       """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(32) NOT NULL,
            password_hash VARCHAR(256) NOT NULL
            )
        """,
        """
        CREATE TABLE macbooks
        (
          id SERIAL PRIMARY KEY,
          serial_number VARCHAR(32) NOT NULL,
          cpu VARCHAR(32) NOT NULL,
          cpu_cores INTEGER NOT NULL,
          cpu_clock VARCHAR(16) NOT NULL,
          ram VARCHAR(16) NOT NULL,
          location VARCHAR(16) NOT NULL
        )
        """,
        """
        CREATE TABLE apps
        (
          id SERIAL PRIMARY KEY,
          application_name VARCHAR(255) NOT NULL,
          pkg_source VARCHAR(128) NOT NULL,
          last_modified TIMESTAMP,
          macbook_id INTEGER NOT NULL,
          FOREIGN KEY (macbook_id)
              REFERENCES macbooks (id)
              ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE app_versions
        (
          id SERIAL PRIMARY KEY,
          version VARCHAR(255) default NULL,
          date_stored TIMESTAMP default CURRENT_DATE NOT NULL,
          app_id INTEGER,
          FOREIGN KEY (app_id)
              REFERENCES apps (id)
              ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE system_info
        (
          id SERIAL PRIMARY KEY,
          os_version VARCHAR(255) NOT NULL,
          kernel_version VARCHAR(255) NOT NULL,
          hostname VARCHAR(255) NOT NULL,
          usernames VARCHAR(255) NOT NULL,
          date_stored TIMESTAMP default CURRENT_DATE NOT NULL,
          macbook_id integer NOT NULL,
          FOREIGN KEY (macbook_id)
              REFERENCES macbooks (id)
              ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    ]

    try:
        conn = dbConnection.connect_webappdb()
        cur = conn.cursor()
        for command in TABLES["table_name"]:
            cur.execute(command)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def insert_data():
    try:
        conn = dbConnection.connect_webappdb()
        cur = conn.cursor()

        data = [{
                    "user": "root8",
                    "pass": "Route_66"
                },
                {
                    "user": "admin",
                    "pass": "admin"
                }]

        for item in data:
            insert_query =  ("INSERT INTO users (username, password_hash) "
                             f"VALUES (\'{item['user']}\', \'{User.hash_password(item['pass'])}\')")
            cur.execute(insert_query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        print('insert error')
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    create_db()
    create_tables()
    insert_data()
