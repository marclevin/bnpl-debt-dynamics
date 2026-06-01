import pandas as pd
import sys
if len(sys.argv) != 3:
    print("Usage: python quick.py input_file.dta labels.json")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
# Read the Stata file
df = pd.read_stata(input_file, iterator=True)

# Save the labels dict to a JSON file
labels_dict = df.variable_labels()
import json
with open(output_file, 'w') as f:
    json.dump(labels_dict, f, indent=4)
