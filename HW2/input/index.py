from lxml import etree
import sys
import os
import re

def format_text(text):
    # "You can assume values are tokenized by white spaces and punctuation characters."
    text = text.lower()
    text = re.split(r'[^\w\d]+|_',text) # RegEx to get rid of white space and punctuation
    
    text2=[]
    for i in text:
        if i == "": # Get rid of any empty string objects
            continue
        else:
            text2.append(i)
    
    # Ensure you save unique values only
    text = set(text2)
    return text

def parse_xml(in_dir):
    # Initialize empty dictionary
    dictionary = {}
    
    for filename in os.listdir(in_dir):
        # Open the file only if it is a valid xml file
        if os.path.isfile(filename) and filename.endswith('xml'):

            # Get the xml info as a root and a tree using lxml.etree
            root = etree.parse(filename).getroot()
            tree = etree.ElementTree(root)

            # Only get the elements, no comments, etc.
            for element in root.iter(tag=etree.Element):
                
                # Save the absolute path to the element and the element's attributes
                abspath = tree.getpath(element).replace('/','.')[1:]
                attribute = element.attrib

                if element.text is not None:
                    # If there is text in the element, format it to get rid of whitespace/ punctuation
                    token_set = format_text(element.text)
                    # Then save the value to the dictionary
                    for value in token_set:
                        if value not in dictionary:
                            # {value: [{which: ... , where: ... }]}
                            dictionary[value] = [{'which': filename, 'where': abspath}]
                        else:
                            # {value: [{which: ... , where: ... },{which: ... , where: ...}]}
                            dictionary[value].append({'which': filename, 'where': abspath})

                if attribute != {}: # Attribute not empty
                    # Save the attribute items into the dictionary
                    for key, attr in attribute.items():
                        token_set = format_text(attr)
                        for attr in token_set:
                            if attr not in dictionary:
                                # {attribute: [{which: ... , where: ... }]}
                                dictionary[attr] = [{'which': filename, 'where': abspath + ".@" + key}] # @ for attribute
                            else:
                                # {attribute: [{which: ... , where: ... },{which: ... , where: ...}]}
                                dictionary[attr].append({'which': filename, 'where': abspath + ".@" + key})
    return dictionary



if __name__ == '__main__':
    # Exit the code if the arguments passed in via the command line are inadequate
    if len(sys.argv) != 3:
        print("Enter command line arguments: python3.8 index.py path/to/directory index.xml")
        sys.exit(1)
    
    # Specify input directory from command line argument
    input_dir = sys.argv[1]
    # Specify output index xml file from command line argument
    output_file = sys.argv[2]

    tokens_dict = parse_xml(input_dir)
    
    # Set up XML format
    root = etree.Element('index')

    for key, value in tokens_dict.items():
        token = etree.SubElement(root, 'token')
        val = etree.SubElement(token, 'value')
        val.text = key
        for i in value:
            prov = etree.SubElement(token, 'provenance')
            which = etree.SubElement(prov, 'which')
            which.text = str(i['which'])
            where = etree.SubElement(prov, 'where')
            where.text = str(i['where'])
    
    with open(output_file, 'wb') as f:
        f.write(etree.tostring(root))
        f.close()