#! /usr/bin/env python

from os.path import splitext, extsep, dirname, abspath, basename, join
import argparse

from traitlets.config import Config
import nbformat
from nbconvert import HTMLExporter
from jupyter_contrib_nbextensions.nbconvert_support import pre_pymarkdown

from .embed_html import EmbedHTMLExporter

THIS_FILE_DIR_PATH = dirname(abspath(__file__))
CONFIG_FILE_PATH = join(THIS_FILE_DIR_PATH, 'data')
DEFAULT_TEMPLATE = 'no_code'


def run(in_file_path,
        process_pymarkdown, embed_images,
        config_dir_path, template_file):
    print('Reading notebook at {}...'.format(in_file_path))
    nb = nbformat.read(in_file_path, as_version=nbformat.NO_CONVERT)
    print('Read notebook.')

    print('Configuring exporter...')
    c = Config()
    if process_pymarkdown:
        print('Using PyMarkdown.')
        # Add preprocessor to do markdown-python rendering.
        preprocessor = pre_pymarkdown.PyMarkdownPreprocessor
        c.HTMLExporter.preprocessors.append(preprocessor)
    else:
        print('Not using PyMarkdown.')
    if embed_images:
        print('Embedding images.')
        Exporter = EmbedHTMLExporter
    else:
        print('Not embedding images.')
        Exporter = HTMLExporter
    # Template lives next to this build file, so add that to search path.
    c.HTMLExporter.template_path.append(config_dir_path)
    # Tell it to use our custom HTML template.
    print("Using template '{}'.".format(template_file))
    c.HTMLExporter.template_file = template_file
    exporter = Exporter(config=c)
    print('Configured exporter.')

    print('Rendering exported notebook...')
    # The exporter will look in config_dir for a directory called 'custom',
    # containing custom CSS.
    resources = {'config_dir': config_dir_path}
    # Render the notebook. We will not use the second argument, the returned
    # resources.
    body, _ = exporter.from_notebook_node(nb, resources=resources)
    print('Rendered exported notebook.')

    # Make output file name.
    in_file_name = basename(in_file_path)
    out_file_name = '{}{}html'.format(splitext(in_file_name)[0], extsep)
    print("Writing exported notebook to '{}'...".format(out_file_name))
    with open(out_file_name, mode='w') as out_file:
        out_file.write(body)
    print("Wrote exported notebook.".format(out_file_name))


def main():
    parser = argparse.ArgumentParser(
        description='Reportify: Jupyter notebook to report-formatted HTML. '
                    'Optimized for pasting into a Google doc')
    parser.add_argument('in_file_path', metavar='in-file-path',
                        help='Path to Jupyter notebook')
    parser.add_argument('--no-pymarkdown', default=False,
                        action='store_true',
                        help='Disable PyMarkdown processing')
    parser.add_argument('--no-embed-images', default=False,
                        action='store_true',
                        help='Disable HTML image embedding')
    args = parser.parse_args()
    run(
        in_file_path=args.in_file_path,
        process_pymarkdown=not args.no_pymarkdown,
        embed_images=not args.no_embed_images,
        config_dir_path=CONFIG_FILE_PATH,
        template_file=DEFAULT_TEMPLATE,
    )
