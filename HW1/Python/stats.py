import argparse
import pandas as pd
import json

def main():
    # Parse arguments passed in via command line
    parser = argparse.ArgumentParser(description="Specify input and output files for this program")
    parser.add_argument("infile", default = "551-0119.txt", type = argparse.FileType('r'), help = "Input file name")
    parser.add_argument("outfile", default = "stats.json", type = argparse.FileType('w'), help = "Output file name")
    args = parser.parse_args()
    
    infile = args.infile
    outfile = args.outfile
    
    # Make sure you can open the infile
    try:
        df = pd.read_csv(infile, delimiter='\t',header=None, names=['Timestamp', 'Name', 'Message'])
    except:
        print("Error reading input file")

    # Get rid of colon at the end of everyone's name in df
    df['Name'] = df['Name'].str.replace(':','')
    # Group by the number of messages each person has sent
    data = df.groupby('Name')['Message'].count()
    # Send results to JSON outfile
    result = data.to_json(orient='table')
    json.dump(result, outfile)

    # Uncomment the following lines to preview the json:

    results = json.loads(result)
    print(json.dumps(results, indent = 2))

##################################################

# Run main script
if __name__ == "__main__":
    main()