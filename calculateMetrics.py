import argparse
import csv
import os
import string
import textstat
from textblob import TextBlob

def polarityMetric(blob):
    """ Takes in text as TextBlob object, returns 0 if polarity is positive for each sentence, 
        otherwise returns the average (negative) polarity
    """
    polarity = 0
    sentenceCount = 0
    ratio = 0

    for sentence in blob.sentences:
        value = sentence.sentiment.polarity 
        if value < 0:
            polarity += value
            sentenceCount += 1
    
    if sentenceCount != 0:
        ratio = polarity/sentenceCount
    
    return ratio

def genderMetric(blob):
    """
    takes a textblob object, returns a score representing how balanced gender pronoun usage is.

    score calculated by formula 1 - (|MP - FP|/(MP + FP)), where MP and FP stand for masculine and feminine pronouns, respectively.
    the score is designed to be high (up to 1) if pronoun usage is completely even, and low (down to 0) if pronoun usage is very skewed in either direction.
    """
    M_PRONOUNS = ["him", "himself", "his"]
    F_PRONOUNS = ["she", "herself", "her", "hers"]
    
    MP, FP = 0
    text = blob.words
    for pronoun in M_PRONOUNS:
        MP += text.count(pronoun)
    for pronoun in F_PRONOUNS:
        FP += text.count(pronoun)
    
    return 1 - (abs(MP - FP) / (MP + FP))

def punctuationMetric(blob):
    """ Takes in a TextBlob, returns the ratio of exclamation points to
        total end punctuation
    """
    punctCount = 0
    exclamationCount = 0
    punctList = ['.', '!', '?']
    ratio = 0

    for sentence in blob.sentences:
        # grab last character (should be punctuation)
        punct = sentence[-1]
        if punct in punctList:
            punctCount += 1
            if punct == '!':
                exclamationCount += 1
    
    if punctCount != 0:
        ratio = exclamationCount/punctCount
    
    return ratio

def readabilityMetric(blob):
    """
    takes a textblob object and returns the readability score concensus across several readability metrics

    removes proper nouns to control for the effect of long names on these metrics, which typically use word length (either by characters or syllables) as a factor, which we theorize could bias them against texts with unusually high density of names from certain cultures
    """
    text = "" # this will be built sentence by sentence
    sentences = blob.sentences
    for sentence in sentences:
        wordList = sentence.words
        for tag in sentence.tags:
            if tag[1] == "NNP": # NNP = proper noun
                wordList.remove(tag[0])
        text += " ".join(wordList) + sentence[-1] + " " # rejoin words, add on end punctuation, plus a space to separate from next sentence

    return textstat.text_standard(text, float_output=True)

        
def secondPersonMetric(blob):
    """
    takes a textblob object and returns the ratio of second person pronouns to all pronouns
    """
    SECOND_PRONOUNS = ["you", "yourself", "yourselves", "your", "yours"]
    secondCount = 0
    pronounCount = 0
    text = blob.words
    tags = blob.tags
    ratio = 0
    for i in range(len(text)):
        if text[i] in SECOND_PRONOUNS:
            secondCount += 1
            pronounCount += 1
        elif tags[i][1].startswith("PRP"):
            pronounCount += 1
    if pronounCount != 0:
        ratio = secondCount / pronounCount
    
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

                readingLevel = readabilityMetric(blob)
                metrics.append(readingLevel) # aggregated/concensus score from a variety of readability metrics, generally based on word & sentence length
                
                punctRatio = punctuationMetric(blob)
                metrics.append(punctRatio) # ratio of exclamation points to end punctuation

                secondPerRatio = secondPersonMetric(blob)
                metrics.append(secondPerRatio) # ratio of second person pronouns to pronouns in total

                polarityRatio = polarityMetric(blob)
                metrics.append(polarityRatio) # average NEGATIVE polarity
            writer = csv.writer(outf)
            writer.writerow(metrics)
    
if __name__=='__main__':
    main()
