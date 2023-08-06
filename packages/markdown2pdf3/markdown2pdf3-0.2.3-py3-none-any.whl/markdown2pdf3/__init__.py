#!/usr/bin/env python
import argparse
from .main import convert_markdown_to_pdf


def execute():
    parser = argparse.ArgumentParser(description='Convert markdown file to pdf')
    parser.add_argument('markdown_path', help='Markdown file path')
    parser.add_argument('--pdf_path', help='The output file name.')
    args = parser.parse_args()
    convert_markdown_to_pdf(**dict(args._get_kwargs()))


if __name__ == '__main__':
    execute()
