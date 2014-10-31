import xlsxwriter
import os


class Draw_Graph():
    def __init__(self,folder_name,folder_path):
	self.folder_name = folder_name
	self.folder_path = folder_path


	#next two line will be deleted. It is just for test.
	self.folder_name="gui"
	self.folder_path="/home/wien2k/work/gui/"

    def draw_dos1ev(self):
	f = open(self.folder_path+self.folder_name+".dos1ev","r")
	workbook = xlsxwriter.Workbook(self.folder_name+'dos1ev_graph.xlsx')
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': 1})import xlsxwriter

	workbook = xlsxwriter.Workbook('chart_line.xlsx')
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': 1})
	
	headings = ['Energy','Total-DOS']
	
