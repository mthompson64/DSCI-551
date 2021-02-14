import requests
import argparse
import json

def main():
    # Parse arguments passed in via command line
    parser = argparse.ArgumentParser(description="Specify input and output files for this program")
    parser.add_argument("infile", nargs = 2, help = "Input file names")
    args = parser.parse_args()

    with open(args.infile[0]) as f:
        chats = json.load(f)
        chats_data = json.loads(chats)
    with open(args.infile[1]) as g:
        roster = json.load(g)
        roster_data = json.loads(roster)
    
    # Put json to firebase under chat_log and roster
    firebase_url = 'https://dsci-551-hw-1-d41f5-default-rtdb.firebaseio.com/'
    requests.put(url = firebase_url + "/chat_log.json", json = chats_data)
    requests.put(url = firebase_url + "/roster.json", json = roster_data)

##################################################

# Run main script
if __name__ == "__main__":
    main()