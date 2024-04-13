from poem_to_VA import*
import sys
import csv


def main():
    if len(sys.argv) > 1:
        #print("sys: ", sys.argv)
        paragraph = sys.argv[1]
        progressive = sys.argv[2] == 'True'
        my_poem = poem_to_VA(paragraph)
        my_poem.wrapper(progressive)
    else:
        print("Please provide a paragraph as a command line argument.")

if __name__ == "__main__":
    main()