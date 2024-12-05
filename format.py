
# Specify file paths
input_file = '/Users/quynhnguyen/Documents/Documents/Project Data/INSAnonym-master 2/test/original_file.csv'  # Replace with the path to your input file
output_file = '/Users/quynhnguyen/Documents/Documents/Project Data/INSAnonym-master 2/test/result.csv'  # Replace with the desired output file path


# Open the input file and create the output file
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # Replace commas with tabs and write to the output file
        outfile.write(line.replace(',', '\t'))

print(f"File with commas replaced by tabs has been saved to: {output_file}")