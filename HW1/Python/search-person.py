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
    target_db = "roster"
    json_suffix = ".json"
    try:
        # Get the json if the keywords are that person's full name ("equalTo")
        response = requests.get(firebase_url + target_db + json_suffix + '?orderBy="Name"&equalTo="' + query_keyword + '"')
        if response.json() == {}:
            # Get the json if the keyword is the person's (full) first name
            response = requests.get(firebase_url + target_db + json_suffix + '?orderBy="Name"&startAt="' + query_keyword + '"&endAt="' + query_keyword + ' "')
            if response.json() == {}:
                # Get the json if the keyword is the person's last name
                response = requests.get(firebase_url + target_db + json_suffix + '?orderBy="Name"&startAt="' + query_keyword + '"&endAt="' + query_keyword + '"')
                # This doesn't quite work...
    except:
        print("Error processing keywords")
    if response.json() != {}:
        # Print person's name
        for value in response.json().values():
            print(value['Name'])
    else:
        print(" ")

##################################################

# Run main script
if __name__ == "__main__":
    main()