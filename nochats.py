import argparse
import json
import pandas as pd

def main():
    # Parse argumnts passed in via command line
    parser = argparse.ArgumentParser(description="Specify input and output files for this program")
    parser.add_argument("infile", nargs = 2, type = argparse.FileType('r'), help = "Input file names")
    parser.add_argument("outfile", type = argparse.FileType('w'), help = "Output file name")
    args = parser.parse_args()
    
    chat_log_file = args.infile[0]
    roster_file = args.infile[1]
    outfile = args.outfile
    
    # Make sure you can open the infile
    try:
        df = pd.read_csv(chat_log_file, delimiter='\t',header=None, names=['Timestamp', 'Name', 'Message'])
    except:
        print("Error reading chat file")

    try:
        roster = pd.read_csv(roster_file, delimiter = ",", header = 0)
    except:
        print("Error reading roster file")

    # Switch the order of everyone's name in the roster dataframe
    roster.Name = roster.Name.str.split(', ').apply(lambda x: x[1] + " " + x[0])
    # Get rid of colon at the end of everyone's name in df
    df['Name'] = df['Name'].str.replace(':','')
    # Get rid of the names that did send a chat message
    data = roster[~roster.Name.isin(df.Name)]

    # Send results to JSON outfile
    result = data.to_json(orient='records')
    json.dump(result, outfile)

    # Uncomment the following lines to preview the json:

    # results = json.loads(result)
    # print(json.dumps(results, indent = 2))
##################################################

# Run main script
if __name__ == "__main__":
    main()