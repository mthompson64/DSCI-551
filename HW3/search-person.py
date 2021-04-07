import sys
import pymysql

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Enter command line arguments: python3.8 nochats.py 'keywords'")
        sys.exit(1)
    
    host="localhost"
    user="dsci551"
    password="Dsci-551"
    database="dsci551"

    # Connect to MySQL
    conn = pymysql.connect(host=host, user=user, passwd=password, db=database)

    # Create cursor
    cur = conn.cursor()

    keywords = sys.argv[1].split()

    if len(keywords) == 1:
        sql = f"SELECT `Name` FROM `roster` WHERE MATCH (`Name`) AGAINST ('{keywords[0]}' IN NATURAL LANGUAGE MODE);"
    elif len(keywords) > 1:
        sql = f"SELECT `Name` FROM `roster` WHERE MATCH (`Name`) AGAINST ('{keywords[0]}' IN NATURAL LANGUAGE MODE)"
        for keyword in keywords[1:]:
            sql = sql + f" OR MATCH (`Name`) AGAINST ('{keyword}' IN NATURAL LANGUAGE MODE)"
    
    cur.execute(sql)

    records = cur.fetchall()
    for record in records:
        print(record[0])