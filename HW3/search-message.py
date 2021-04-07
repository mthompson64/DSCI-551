import sys
import pymysql

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Enter command line arguments: python3.8 nochats.py 'Name'")
        sys.exit(1)
    
    host="localhost"
    user="dsci551"
    password="Dsci-551"
    database="dsci551"

    # Connect to MySQL
    conn = pymysql.connect(host=host, user=user, passwd=password, db=database)

    # Create cursor
    cur = conn.cursor()

    name = sys.argv[1]

    sql = f"SELECT Timestamp, Message FROM chats JOIN roster ON chats.Name = roster.Name WHERE MATCH (roster.Name) AGAINST ('{name}' IN NATURAL LANGUAGE MODE);"
    
    cur.execute(sql)

    records = cur.fetchall()
    for record in records:
        print(f"{record[0]}\t{record[1]}")