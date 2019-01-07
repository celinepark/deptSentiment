import argparse
import csv
import os
import string
import textstat

def main():
    parser = argparse.ArgumentParser(description="calculate some metrics for college cs department webpages")
    parser.add_argument("path", help="a directory containing text files of website contents")
    parser.add_argument("outfile", help="a path to which to write a csv file containing calculated metrics")
    args = parser.parse_args()

    files = os.listdir(args.path)

    with open(args.outfile, 'w', newline='') as outf:
        for filename in files:
            metrics = [filename]
            with open(args.path + filename, 'r') as f:
                text = f.read()
                metrics.append(textstat.text_standard(text, float_output=True))
            writer = csv.writer(outf)
            writer.writerow(metrics)
    
if __name__=='__main__':
    main()
