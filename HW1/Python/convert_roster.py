import argparse
import pandas as pd
import json

def main():
    # Parse argumnts passed in via command line
    parser = argparse.ArgumentParser(description="Specify input and output files for this program")
    parser.add_argument("infile", default = "551-tue-roster.csv", type = argparse.FileType('r'), help = "Input file name")
    parser.add_argument("outfile", default = "roster.json", type = argparse.FileType('w'), help = "Output file name")
    args = parser.parse_args()
    
    infile = args.infile
    outfile = args.outfile
    
    # Make sure you can open the infile
    try:
        df = pd.read_csv(infile, delimiter=',',header=0)
    except:
        print("Error reading input file")

    # Switch order of everyone's name in df
    df.Name = df.Name.str.split(', ').apply(lambda x: x[1] + " " + x[0])

    # Send results to JSON outfile
    result = df.to_json(orient='records')
    json.dump(result, outfile)

    # Uncomment the following lines to preview the json:

    # results = json.loads(result)
    # print(json.dumps(results, indent = 2))
##################################################

# Run main script
if __name__ == "__main__":
    main()