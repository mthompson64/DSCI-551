from lxml import etree
import sys
import os
import re

def search_index(keyword_input, index):
    keywords = keyword_input.lower()
    keywords = re.split(r'[^\w\d]+|_', keywords) # Format keyword input

    # Initialize empty dictionary to store provenance and keywords
    d = {}

    search_root = etree.parse(index)
    for word in keywords:
        # Use xpath to get the provenance of the keyword in the index.xml file
        which = search_root.xpath("/index/token[value='" + word + "']/provenance/which/text()")
        where = search_root.xpath("/index/token[value='" + word + "']/provenance/where/text()")

        # Double check that which is equal to where in length
        if len(which) == len(where):
            for i in range(len(which)):
                # Add the keyword and provenance to the empty dictionary
                if word not in d:
                    # {keyword: [{which: ... , where: ... }]}
                    d[word] = [{'which': which[i], 'where': '/' + where[i].replace('.','/')}]
                else:
                    # {keyword: [{which: ... , where: ... }, {which: ... , where: ... }]}
                    d[word].append({'which': which[i], 'where': '/' + where[i].replace('.','/')})
    
    # Return the dictionary and keywords
    return d, keywords

def check_files(dictionary):
    element_set = set()
    # If the dictionary is empty, there are no matches found for the keywords entered
    if dictionary == {}:
        print("No such tokens")
    else:
        for value in dictionary.values():
            for i in value:
                # Open the 'which' file and find the specific element specified in 'where'
                f = open(i['which'], 'r')
                root = etree.parse(f)
                loc = root.xpath(i['where'])

                # Add the element and the file to element_set as a tuple to avoid repetition
                for j in loc:
                    try:
                        element_set.add((etree.tostring(j, encoding='unicode').strip(), i['which']))
                    except:
                        # If it's an attribute or having trouble adding that part of the xml
                        element_set.add((etree.tostring(j.getparent(), encoding='unicode').strip(), i['which']))
                
                f.close() # Close the file

    # Print out elements of element_set
    for line in element_set:
        print('Element: ' + line[0])
        print('File: ' + line[1])

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Enter command line arguments: python3.8 search.py index.xml path/to/directory "list of keywords separated by spaces"')
        sys.exit(1)
    
    # Specify index xml file
    ind = sys.argv[1]
    try:
        index = open(ind, 'r')
    except:
        print("Please enter a valid index.xml file")

    # Specify input directory from command line argument
    input_dir = sys.argv[2]

    for filename in os.listdir(input_dir):
        # Open the file only if it is a valid xml file
        if os.path.isfile(filename) and filename.endswith('xml'):
            continue
            #print(filename)

    # Specify keywords list from command line argument
    keywords = sys.argv[3]

    # Search through the index file for the keywords and return a dictionary
    d, keywords = search_index(keywords, index)
    
    # Check all the files returned from the provenance and print out the element and file the keyword was contained in
    check_files(d)

    index.close()