import json
with open('/Users/madeleine/Desktop/DSCI_551/Project/Data/restaurant_data.json', 'r') as f:
    data = json.load(f)
    f.close()

with open('new_restaurant_data.json', 'w') as g:
    json.dump(data, g, indent=4)
    g.close()