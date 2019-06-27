import os
import psycopg2


class dbConnection():

    def connect_postgredb():
        return psycopg2.connect(host = 'postgres',
                                user = 'postgres',
                                password = 'password',
                                database = 'postgres')

    def connect_webappdb():
        return psycopg2.connect(host = 'postgres',
                                user = 'postgres',
                                password = 'password',
                                database = 'webapp_db')
