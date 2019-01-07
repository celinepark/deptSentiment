import argparse
import csv
import os
import string
import textstat
from textblob import TextBlob

def punctuationMetric(sentenceList):
    """ Takes in a TextBlob sentence list, returns the ratio of exclamation points to
        total end punctuation
    """
    punctCount = 0
    exclamationCount = 0
    punctList = ['.', '!', '?']
    ratio = 0

    for sentence in sentenceList:
        # grab last character (should be punctuation)
        punct = sentence[-1]
        if punct in punctList:
            punctCount += 1
            if punct == '!':
                exclamationCount += 1
    
    if punctCount != 0:
        ratio = exclamationCount/punctCount
    
    return ratio
        


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
                blob = TextBlob(text) # blob.words and blob.sentences gives an iterable
                metrics.append(textstat.text_standard(text, float_output=True)) # aggregated/concensus score from a variety of readability metrics, generally based on word & sentence length
                
                punctRatio = punctuationMetric(blob.sentences)
                metrics.append(punctRatio) # ratio of exclamation points to end punctuation
            writer = csv.writer(outf)
            writer.writerow(metrics)
    
if __name__=='__main__':
    main()
