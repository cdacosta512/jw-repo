#!/usr/bin/env python3
"""
update_local_tax.py
-------------------
Usage:
    python update_local_tax.py input.csv input.xml

Description:
    Reads a CSV file and an XML file, matches LocalJurisdiction values,
    and updates column C (LocalTaxAmount) if it is blank in the CSV.
    The XML must include <LocalJurisdiction> and <LocalTaxAmount> elements
    under <LocalTaxWithheld> blocks.

Notes:
    - The output file is automatically created using the input CSV name,
      with "-UPDATED.csv" appended (e.g., input.csv → input-UPDATED.csv).
"""

import sys
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import time


def load_xml_data(xml_path):
    """Parse the XML and return a dictionary of {LocalJurisdiction: LocalTaxAmount}."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Detect XML namespace from the root tag
    ns = {"ns": root.tag.split("}")[0].strip("{")}
    xml_map = {}

    # Extract LocalJurisdiction and LocalTaxAmount pairs
    for node in root.findall(".//ns:LocalTaxWithheld", ns):
        lj = node.find("ns:LocalJurisdiction", ns)
        amt = node.find("ns:LocalTaxAmount", ns)
        if lj is not None and amt is not None and lj.text and amt.text:
            try:
                lj_val = int(lj.text.strip())
                amt_val = float(amt.text.strip())
                xml_map[lj_val] = amt_val
            except ValueError:
                continue

    print(f"Found {len(xml_map)} LocalJurisdiction entries in XML.")
    return xml_map


def update_csv(csv_path, xml_map, output_path):
    """Update column C in the CSV using data from the XML map."""
    updated_count = 0
    total_rows = 0

    with open(csv_path, newline="", encoding="utf-8-sig") as f_in, \
         open(output_path, "w", newline="", encoding="utf-8-sig") as f_out:

        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        for row in reader:
            if not row or not row[0].strip():
                continue
            total_rows += 1

            try:
                jurisdiction = int(row[0].strip())
            except ValueError:
                writer.writerow(row)
                continue

            # Ensure at least 3 columns exist
            while len(row) < 3:
                row.append("")

            # Update column C if blank and jurisdiction exists in XML map
            if not row[2].strip() and jurisdiction in xml_map:
                row[2] = str(xml_map[jurisdiction])
                updated_count += 1
                print(f"Updated {jurisdiction}: {row[2]}")
            else:
                print(f"Skipped {jurisdiction}")

            writer.writerow(row)

    print("\nProcessing complete.")
    print(f"Total rows processed: {total_rows}")
    print(f"Rows updated: {updated_count}")
    print(f"Output file: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python update_local_tax.py input.csv input.xml")
        sys.exit(1)

    start_time = time.perf_counter()

    csv_path = Path(sys.argv[1])
    xml_path = Path(sys.argv[2])

    # Automatically create an output filename
    output_path = csv_path.with_name(f"{csv_path.stem}-UPDATED.csv")

    xml_map = load_xml_data(xml_path)
    update_csv(csv_path, xml_map, output_path)

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"\nExecution time: {elapsed:.4f} seconds")


if __name__ == "__main__":
    main()
