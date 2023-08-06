import os
import sys
import pypandoc
from . import utils


@utils.save_cwd
def convert_markdown_to_pdf(
        markdown_path,
        pdf_path=None,
        pdf_engine=None,
):
    markdown_dir, _ = os.path.split(markdown_path)
    os.chdir(markdown_dir)

    if not pdf_engine:
        pdf_engine = {
            'win32': 'latex',
        }[sys.platform]

    if not pdf_path:
        pdf_path = os.path.splitext(markdown_path)[0] + '.pdf'

    pypandoc.convert_file(
        source_file=markdown_path,
        outputfile=pdf_path,
        to='pdf',
        format='md',
        extra_args=[
            f'--pdf-engine={pdf_engine}'
        ]
    )
