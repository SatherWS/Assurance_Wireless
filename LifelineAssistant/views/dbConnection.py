"""
Below is an attempt at a MySQL connection pool, currently failing
"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import re
import mysql.connector
from mysql.connector import pooling


dbConfig = {
    "host": "localhost",
    "database": "awla_db",
    "user": "root",
    "password": ""
}
cnxpool = pooling.MySQLConnectionPool(
    pool_name = "mypool", pool_size = 3, **dbConfig
)
conn = cnxpool.get_connection()
curs = conn.cursor()
