import sys
import pandas as pd


def main(input_filename, output_filename):
    print("Reading data from {0} and generating chloropleth map in file {1}".format(input_filename, output_filename))
    df = pd.read_csv(input_filename)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python geohash_chloropleth.py input_filename.tsv output_filename.html")
    else:
        main(sys.argv[1], sys.argv[2])
