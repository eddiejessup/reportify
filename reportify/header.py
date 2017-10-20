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


def read_header(source):
    match = re.match('^---\n([\s\S]+?)\n---', source)
    yaml_source = match.group(1)
    headers = yaml.safe_load(yaml_source)
    return headers


class HeaderPreprocessor(Preprocessor):
    """
    Parses and renders the header of a report-style notebook.

    Replaces a yaml-formatted header with a template rendered based on its
    contents.
    """

    def preprocess_cell(self, cell, resources, index):
        """
        Preprocess cell

        Parameters
        ----------
        cell : NotebookNode cell
            Notebook cell being processed
        resources : dictionary
            Additional resources used in the conversion process.  Allows
            preprocessors to pass variables into the Jinja engine.
        cell_index : int
            Index of the cell being processed (see base.py)
        """
        if index == 0 and cell.cell_type == 'raw' and cell.source:
            cell.cell_type = "markdown"
            headers = read_header(cell.source)
            cell.source = header_template.render(**headers)
        return cell, resources
