import base64
import pychrome
import sys
import tempfile
from django.conf import settings
from django.core.files.base import ContentFile
from pypandoc import convert_text
from socket import gethostbyname

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

if is_py2:
    from urlparse import urlparse
elif is_py3:
    from urllib.parse import urlparse


class BaseReport(object):
    id = ''
    name = ''

    def get_report_name(self, **kwargs):
        return ' '.join([kwargs['organization'].name, self.id.capitalize(),
                         'Report'])

    def get_report_filename(self, **kwargs):
        return '{0} {1} to {2}.{3}'.format(self.get_report_name(**kwargs),
                                           kwargs['start_datetime'].date(),
                                           kwargs['end_datetime'].date(),
                                           kwargs['typ'])

    def markdown_to_doc(self, markdown, typ, reference=None):
        """
        :param markdown: markdown document as a string
        :param typ: document conversion output extension
        :param reference: path to the reference docx, if different from default
        :return: path to a temporary file
        """

        with tempfile.NamedTemporaryFile(suffix='.{0}'.format(typ)) as temp:
            extra_args = ['--dpi=180']
            if typ == 'docx':
                if reference:
                    extra_args.append('--reference-docx={}'.format(reference))
                extra_args.append('--toc')
            convert_text(markdown, typ, 'markdown_phpextra',
                         outputfile=temp.name, extra_args=extra_args)
            with open(temp.name, 'r') as document:
                return ContentFile(document.read())

    def html_to_pdf(self, html, delay=5):
        """
        :param html: html document as a bytestring
        :param delay: time to wait for javascript loading in seconds
        :return: path to a temporary file
        """
        split = urlparse(settings.CHROME_URL)
        ipaddr = gethostbyname(split.hostname)
        # related to https://github.com/GoogleChrome/puppeteer/issues/2242
        url = settings.CHROME_URL.replace(split.hostname, ipaddr)

        browser = pychrome.Browser(url=url)
        encoded_html = base64.b64encode(html)

        data_url = "data:text/html;base64,{}".format(encoded_html)
        tab = browser.new_tab(data_url)
        tab.start()

        tab.wait(delay)
        try:
            data = tab.Page.printToPDF()
            data = base64.b64decode(data['data'])
            return ContentFile(data)
        finally:
            tab.stop()
            browser.close_tab(tab)
