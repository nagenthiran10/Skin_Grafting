#!/usr/bin/env python
"""
Script to create the MySQL database for the skin grafting project.
Run this script before running Django migrations.
"""

import mysql.connector
from mysql.connector import Error

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'skin grafting'

try:
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD if DB_PASSWORD else None,
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Create database
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
            print(f"✓ Database '{DB_NAME}' created successfully!")
        except Error as err:
            print(f"✗ Error creating database: {err}")
        
        # Show databases
        cursor.execute("SHOW DATABASES LIKE 'skin%'")
        print("\nAvailable databases:")
        for db in cursor.fetchall():
            print(f"  - {db[0]}")
        
        cursor.close()
        connection.close()
except Error as err:
    print(f"✗ Error connecting to MySQL: {err}")
    print("\nMake sure MySQL server is running and accessible at localhost:3306")
    print("If you need to set a password or change the host, edit the variables at the top of this script.")
