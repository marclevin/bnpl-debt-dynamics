import pandas as pd
# Convert input file from Stata to CSV for easier use in Python
# Usage: python convert.py input_file.dta output_file.csv

import sys
if len(sys.argv) != 3:
    print("Usage: python convert.py input_file.dta output_file.csv")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]
# Read the Stata file
df = pd.read_stata(input_file, iterator=True)

df.variable_labels()

# Save as CSV
df.to_csv(output_file, index=False)