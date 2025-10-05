#!/usr/bin/env python3

import csv
import sys

def fix_hgnc_csv_proper(input_file, output_file):
    """Properly fix HGNC CSV by handling embedded newlines correctly."""
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        # Read the header to get expected field count
        header_line = infile.readline().strip()
        expected_fields = len(header_line.split('\t'))
        print(f"Expected fields: {expected_fields}")
        
        # Reset to beginning
        infile.seek(0)
        
        # Use csv.reader with tab delimiter to properly handle quoted fields
        reader = csv.reader(infile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            rows_written = 0
            for row_num, row in enumerate(reader, 1):
                if len(row) == expected_fields:
                    # Clean any embedded newlines within fields
                    cleaned_row = [field.replace('\n', ' ').replace('\r', ' ') for field in row]
                    writer.writerow(cleaned_row)
                    rows_written += 1
                else:
                    print(f"Skipping row {row_num}: has {len(row)} fields, expected {expected_fields}")
                    if row_num <= 10:  # Show first few problematic rows
                        print(f"  Row content: {row[:3]}...")
    
    print(f"Wrote {rows_written} rows to {output_file}")

if __name__ == "__main__":
    input_file = "data/hgnc/hgnc_complete_set.txt"
    output_file = "data/hgnc/hgnc_complete_set_clean.txt"
    fix_hgnc_csv_proper(input_file, output_file)