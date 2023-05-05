import re

def MAMnet_convert_symbolic(invcf, outvcf):
    with open(invcf,'r') as vcfin:
        with open(outvcf,'w') as vcfout:
            for line in vcfin:
                if line[0]!='#':
                    line = line.split('\t')
                    svtype = re.findall("SVTYPE=(\w+)",line[7])[0]
                    line[3] = 'N'
                    line[4] = '<'+svtype+'>'
                    line = '\t'.join(line)
                vcfout.write(line)
                

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--input','-i',)
    parser.add_argument('--output','-o')

    args = parser.parse_args()

    MAMnet_convert_symbolic(args.input, args.output)