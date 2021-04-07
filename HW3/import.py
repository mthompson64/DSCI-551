import pymysql
import pandas as pd
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:    # There should only be three command line inputs
        print('Enter command line arguments: python3.8 import.py <chat-log-file> <roster-file>')
        sys.exit(1)
    
    # Connect to the database
    host="localhost"
    user="dsci551"
    password="Dsci-551"
    database="dsci551"

    conn = pymysql.connect(host=host, user=user, passwd=password)

    # Create cursor
    cur = conn.cursor()

    sql = "CREATE DATABASE IF NOT EXISTS `dsci551`;"
    cur.execute(sql)

    sql = "USE `dsci551`;"
    cur.execute(sql)

    # Read in chat log file
    chats = sys.argv[1]
    try:
        df = pd.read_csv(chats, delimiter='\t',header=None, names=['Timestamp', 'Name', 'Message'])
        df['Name'] = df['Name'].str.replace(':','')
    except:
        print("Error reading in chat log file")

    # Drop chats table if it already exists
    sql = "DROP TABLE IF EXISTS `chats`;"
    cur.execute(sql)
    # Create chats table
    sql = "CREATE TABLE `chats` (`Timestamp` varchar(20) NOT NULL,`Name` tinytext NOT NULL,\
        `Message` mediumtext, FULLTEXT(`Name`, `Message`));"
    cur.execute(sql)

    # Insert the values from the chats dataframe into the chats table
    for index, row in df.iterrows():
        sql = "INSERT INTO `chats` VALUES (%s, %s, %s);"
        cur.execute(sql, (row['Timestamp'], row['Name'], row['Message']))
    conn.commit()

    # Read in roster file
    roster = sys.argv[2]
    try:
        df1 = pd.read_csv(roster, delimiter=',',header=0)
        df1['Name'] = df1['Name'].str.split(', ').apply(lambda x: x[1] + " " + x[0])
    except:
        print("Error reading in roster file")
    
    # Drop roster table if it already exists
    sql = "DROP TABLE IF EXISTS `roster`;"
    cur.execute(sql)
    # Create roster table
    sql = "CREATE TABLE `roster` (`Name` tinytext NOT NULL, `Participating_from` tinytext,\
        FULLTEXT(`Name`));"
    cur.execute(sql)

    # Insert the values from the roster dataframe into the roster table
    for index, row in df1.iterrows():
        sql = "INSERT INTO `roster` VALUES (%s, %s);"
        cur.execute(sql, (row['Name'], row['Participating from']))
    conn.commit()

    # Close the connection
    conn.close()