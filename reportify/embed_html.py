"""Embed graphics into HTML Exporter class"""

import base64
import imghdr
import os
try:
    # Python 3.
    from urllib.request import urlopen
except ImportError:
    # Python 2.
    from urllib2 import urlopen

from nbconvert.exporters.html import HTMLExporter
from bs4 import BeautifulSoup


def data_ify_url(url):
    """Replace source URL or file link with base64-encoded blob."""
    if url.startswith('data'):
        return url
    elif url.startswith('http'):
        data = urlopen(url).read()
    else:
        with open(url, 'rb') as f:
            data = f.read()

    # Try to infer format from data itself.
    image_format = imghdr.what('', h=data)
    # If this fails, rely on the file extension.
    if image_format is None:
        image_format = os.path.splitext(url)[1]

    if image_format == 'svg':
        media_type = 'image/svg+xml'
    elif image_format == 'pdf':
        media_type = 'application/pdf'
    else:
        media_type = 'image/{}'.format(image_format)

    b64_data = base64.b64encode(data).decode('utf-8')
    data_uri = 'data:{};base64,{}'.format(media_type, b64_data)
    return data_uri


def embed_html(html):
    """Modify 'src' attribute in HTML's 'img' tags to embed data in the HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for img_tag in soup.findAll('img'):
        for attr, old_val in img_tag.attrs.items():
            if attr.lower() == 'src':
                img_tag.attrs[attr] = data_ify_url(old_val)
    embedded_html = str(soup)
    return embedded_html


class EmbedHTMLExporter(HTMLExporter):
    """
    :mod:`nbconvert` Exporter which embeds graphics as base64 into HTML.

    Convert to HTML and embed graphics (PDF, SVG and raster images) in the HTML
    file.

    Example usage::

        jupyter nbconvert --to html_embed my_notebook.ipynb
    """

    def from_notebook_node(self, nb, resources=None, **kw):
        output, resources = super(
            EmbedHTMLExporter, self).from_notebook_node(nb, resources)
        embedded_output = embed_html(output)
        return embedded_output, resources
