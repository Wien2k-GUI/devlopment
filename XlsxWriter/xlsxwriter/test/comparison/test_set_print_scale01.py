###############################################################################
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2014, John McNamara, jmcnamara@cpan.org
#

from ..excel_comparsion_test import ExcelComparisonTest
from ...workbook import Workbook


class TestCompareXLSXFiles(ExcelComparisonTest):
    """
    Test file created by XlsxWriter against a file created by Excel.

    """

    def setUp(self):
        self.maxDiff = None

        filename = 'set_print_scale01.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = ['xl/printerSettings/printerSettings1.bin',
                             'xl/worksheets/_rels/sheet1.xml.rels']
        self.ignore_elements = {'[Content_Types].xml': ['<Default Extension="bin"'],
                                'xl/worksheets/sheet1.xml': ['<pageMargins']}

    def test_create_file(self):
        """Test the creation of a simple XlsxWriter file with printer settings."""

        workbook = Workbook(self.got_filename)

        worksheet = workbook.add_worksheet()

        worksheet.set_print_scale(110)
        worksheet.set_paper(9)

        worksheet.write('A1', 'Foo')

        workbook.close()

        self.assertExcelEqual()
