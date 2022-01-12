import re


def extract_unique_annotation(input):

    ann_dict = dict()
    
    with open(input,'r') as infile:
        for line in infile:
            if line[0] != '#':
                try:
                    ann = re.findall("ANN=([^;\t]+)",line)[0].split('|')[1]
                    if ann not in ann_dict:
                        ann_dict[ann]=1
                    else:
                        ann_dict[ann]+=1
                except:
                    pass

    print('\n'.join(ann_dict.keys()))


if __name__ == '__main__':
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input', type=str,)
    args = parser.parse_args()

    input = args.input
    extract_unique_annotation(input)