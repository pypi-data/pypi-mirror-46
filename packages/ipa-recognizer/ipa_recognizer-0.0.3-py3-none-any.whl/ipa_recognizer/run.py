#!/usr/bin/env python

import argparse
from ipa_recognizer.recognizer import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="run the model to generate phones")
    parser.add_argument("-i", "--input", required=True,  help="input audio file or input directory containing multiple audio files")
    #parser.add_argument("-o", "--output",required=True,  help="output directory. phones.txt will be generated under this directory")
    # parser.add_argument("-s", "--segment", type=float, default=1.0, help="weight")
    parser.add_argument("-m", "--model", type=float, default='english', help='pretrained acoustic model')
    parser.add_argument("--b", "--blank", type=float, default=0.8, help="change the blank factor (default: 0.8). Smaller blank factor means it will generate more phones")

    args = parser.parse_args()

    recognizer = Recognizer(args.model)
