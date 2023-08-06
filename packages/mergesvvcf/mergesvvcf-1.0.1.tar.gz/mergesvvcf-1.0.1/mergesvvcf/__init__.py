import mergesvvcf.mergedfile as mergedfile
import argparse
import os
import sys

def main():
    """Merge SV VCF files, output to stdout or file"""
    defsvwindow = 100

    parser = argparse.ArgumentParser(description='Merge calls in SV VCF files')
    parser.add_argument('input_files', nargs='+', help='Input VCF files')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout, help="Specify output file (default:stdout)")
    parser.add_argument('-v', '--verbose', action='store_true', help="Specify verbose output")
    parser.add_argument('-l', '--labels', type=str, help='Comma-separated labels for each input VCF file (default:basenames)')
    parser.add_argument('-n', '--ncallers', action='store_true', help='Annotate variant with number of callers')
    parser.add_argument('-m', '--mincallers', type=int, default=0, help='Minimum # of callers for variant to pass')
    parser.add_argument('-s', '--sv', action='store_true', help='Force interpretation as SV (default:false)')
    parser.add_argument('-f', '--filtered', action='store_true', help='Include records that have failed one or more filters (default:false)')
    parser.add_argument('-w', '--svwindow', default=defsvwindow, type=int,
                         help='Window for comparing breakpoint positions for SVs (default:'+str(defsvwindow)+')')
    parser.add_argument('-d', '--debug', action=('store_true'),
                         help='Include original reads and raise errors (default:false)')

    args = parser.parse_args()
    input_files = args.input_files
    if args.labels is None:
        labels = [os.path.splitext(os.path.basename(f))[0] for f in input_files]
    else:
        labels = [label.strip() for label in args.labels.split(',')]

    mergedfile.merge(input_files, labels, args.sv, args.output,
                     slop=args.svwindow, verbose=args.verbose,
                     output_ncallers=args.ncallers,
                     min_num_callers=args.mincallers,
                     filterByChromosome=True, noFilter=args.filtered,
                     debug=args.debug)
