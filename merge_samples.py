#!/usr/bin/python3.8
import sys
import os
from typing import List, Optional

from PyPDF2 import PdfFileMerger

def print_usage():
    print(f'Usage : {sys.argv[0]} <list of folders or files> -o <output_file>')


def get_pdf_or_none(f: str) -> Optional[str]:
    if f[-4:] == '.pdf':
        return f
    else:
        return None


def get_files(lst: List[str]) -> List[str]:
    all_pdfs = []
    for itm in lst:
        if os.path.isdir(itm):
            for prefix, _, files in os.walk(itm):
                pdfs = [get_pdf_or_none(f) for f in files]
                all_pdfs += [ f'{prefix}/{f}' for f in pdfs if f is not None]
        else:
            pdf = get_pdf_or_none(itm)
            if pdf is not None:
                all_pdfs.append(pdf)
    return all_pdfs

def merge_pdfs(pdfs: List[str], output: str):
    pdfs_sorted = sorted(pdfs)
    merger = PdfFileMerger()
    for pdf in pdfs_sorted:
        merger.append(pdf)
    merger.write(output)
    merger.close()


def main() -> int:
    if '-h' in sys.argv or '--help' in sys.argv:
        print_usage()
        return 0

    args = sys.argv[:]
    output = 'output.pdf'
    for i, elm in enumerate(sys.argv):
        if elm == '-o':
            if i == len(sys.argv) - 1:
                print(f'Need to specify an output path with the -o flag.')
                return 1
            output = sys.argv[i+1]
            args = args[:i] + args[i+2:]

    if len(args) < 2:
        print_usage()
        return 1


    pdfs = get_files(args[1:])
    merge_pdfs(pdfs, output)

if __name__ == '__main__':
    sys.exit(main())
