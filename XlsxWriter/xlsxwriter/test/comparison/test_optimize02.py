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

        filename = 'optimize02.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = []
        self.ignore_elements = {}

    def test_create_file(self):
        """Test the creation of a simple XlsxWriter file."""

        workbook = Workbook(self.got_filename, {'constant_memory': True, 'in_memory': False})
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Hello')
        worksheet.write('A2', 123)

        worksheet.write('G1', 'Foo')

        workbook.close()

        self.assertExcelEqual()
