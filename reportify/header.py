from os.path import dirname, abspath, join
import re

import yaml
from nbconvert.preprocessors import Preprocessor
from jinja2 import Environment, FileSystemLoader, select_autoescape

THIS_FILE_DIR_PATH = dirname(abspath(__file__))
CONFIG_FILE_PATH = join(THIS_FILE_DIR_PATH, 'data')

env = Environment(
    loader=FileSystemLoader(CONFIG_FILE_PATH),
    autoescape=select_autoescape(['html', 'xml'])
)
header_template = env.get_template('header.md')
footer_template = env.get_template('footer.md')


def read_yaml_block(source):
    match = re.match('^---\n([\s\S]+?)\n---', source)
    yaml_source = match.group(1)
    contents = yaml.safe_load(yaml_source)
    return contents


class HeaderPreprocessor(Preprocessor):
    """
    Parses and renders the header of a report-style notebook.

    Replaces yaml-formatted header and/or footer cells with templates rendered
    based on their contents.
    """

    def preprocess(self, nb, resources):
        cells = nb['cells']
        if cells:
            first_cell = cells[0]
            if first_cell.cell_type == 'raw' and first_cell.source:
                first_cell.cell_type = 'markdown'
                headers = read_yaml_block(first_cell.source)
                first_cell.source = header_template.render(**headers)

            if (len(cells) > 1 and cells[-1].cell_type == 'raw'
                    and cells[-1].source):
                last_cell = cells[-1]
                last_cell.cell_type = 'markdown'
                footers = read_yaml_block(last_cell.source)
                last_cell.source = footer_template.render(**footers)
        return nb, resources
