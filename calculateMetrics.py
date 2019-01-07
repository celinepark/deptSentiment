import argparse
import csv
import os
import string
import textstat

def main():
    parser = argparse.ArgumentParser(description="calculate some metrics for college cs department webpages")
    parser.add_arugment("path", help="a directory containing text files of website contents")
    parser.add_argument("outfile", help="a path to which to write a csv file containing calculated metrics")
    args = parser.parse_args()

    files = os.listdir(args.path)

    for filename in files:
        metrics = [f]
        with open(path + filename) as f:
            text = f.read()
            metrics += textstat.flesch_kincaid_grade(text) # basic word/sentence-length based readability metric
        writer = csv.writer(args.outfile)
        writer.writerow(metrics)
    
if __name__=='__main__':
    main()
