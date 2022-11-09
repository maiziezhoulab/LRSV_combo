if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--bed','-b', type=str,)
    parser.add_argument('--chrs', nargs='+')
    args = parser.parse_args()

    if args.chrs is None:
        chrs = ['chr'+str(i) for i in range(1,23)]
        print("Only count length of regions in chr1-22 by default")
    else:
        chrs = args.chrs

    with open(args.bed,"r") as bf:
        length=0
        for line in bf:
            line = line.rstrip("\n").split("\t")
            if line[0] in chrs:
                length = length + int(line[2]) - int(line[1])

    print(length)

