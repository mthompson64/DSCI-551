import requests
import argparse
import json

def main():
    # Parse arguments passed in via command line
    parser = argparse.ArgumentParser(description="Specify input terms for this program")
    parser.add_argument("text", action = "store", help = "Input terms")
    args = parser.parse_args()

    # Change so keywords can be input case insensitive
    words = args.text
    keywords = words.split(" ")
    list_keywords = []
    for i in keywords:
        list_keywords.append(i.lower().capitalize())
    query_keyword = " ".join(list_keywords)

    firebase_url = 'https://dsci-551-hw-1-d41f5-default-rtdb.firebaseio.com/'
    target_db = "chat_log"
    json_suffix = ".json"
    try:
        # Get all of the messages for that person
        response = requests.get(firebase_url + target_db + json_suffix + '?orderBy="Name"&equalTo="' + query_keyword + '"')
    except:
        print("Error processing keywords")
    if response.json() != {}:
        # If the person sent a message, print out all their messages in order by timestamp
        chat_list = []
        for value in response.json().values():
            chat_list.append(value['Timestamp'] + '\t' + value['Message'])
        chat_list.sort()
        for i in chat_list:
            print(i)
    else:
        # If there aren't any chats for that person
        print("No messages by " + query_keyword)

##################################################

# Run main script
if __name__ == "__main__":
    main()