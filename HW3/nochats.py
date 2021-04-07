import json
import sys
import pymysql

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Enter command line arguments: python3.8 nochats.py <output-json-file>')
        sys.exit(1)
    
    host="localhost"
    user="dsci551"
    password="Dsci-551"
    database="dsci551"

    # Connect to MySQL
    conn = pymysql.connect(host=host, user=user, passwd=password, db=database)

    # Create cursor
    cur = conn.cursor()

    # Calculate how many messages each person sent
    sql = "SELECT roster.Name, roster.Participating_from FROM roster LEFT JOIN chats ON roster.Name = chats.Name WHERE chats.Message IS NULL;"
    cur.execute(sql)

    records_list = []

    # Save the data as a list of dicts to go into a json file
    records = cur.fetchall()
    for row in records:
        d = {}
        d['Name'] = row[0]
        d['Participating from'] = row[1]
        records_list.append(d)

    # Save the stats to the output file as specified in the command line argument
    json_file = sys.argv[1]
    with open(json_file, 'w') as outfile:
        json.dump(records_list, outfile, indent=2)

    # Close the connection
    conn.close()