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
	bold = workbook.add_format({'bold': 1})

	
	headings = ['Energy','Total-DOS']
	energy_data=[]
	total_dos_data=[]
	total_cnt=0
	data_flag = False
	for line in f.readlines():

	    if data_flag:
	        energy_data.append(round(float(line.strip().split()[0]),5))
	        total_dos_data.append(round(float(line.strip().split()[1]),5))
	        total_cnt = total_cnt+1

	    if ' ENERGY  total-DOS' in line and not data_flag:
		data_flag = True

	worksheet.write_row('A1',headings,bold)
	worksheet.write_column('A2',energy_data)
	worksheet.write_column('B2',total_dos_data)

	chart1 = workbook.add_chart({'type':'line'})

	chart1.add_series({
		'name':		'=Sheet1!$B$1',
		'categories':	'=Sheet1!$A$2:$A$' + str(total_cnt+1),
		'values':	'=Sheet1!$B$2:$B$' + str(total_cnt+1),
		'line':		{'width' :1}
	})

	print 'total_cnt = ' + str(total_cnt)
	chart1.set_title({'name':'Results of dos1ev'})
	chart1.set_x_axis({'name' : 'Energy'})
	chart1.set_y_axis({'name' : 'Total-DOS'})

	chart1.set_style(10)
	chart1.set_size({'x_scale':2,'y_scale':2})
	worksheet.insert_chart('D2',chart1,{'x_offset' :25, 'y_offset':10})
	
	workbook.close()
	



def draw_test():
    draw_graph = Draw_Graph('gui','/home/wien2k/work/gui')
    draw_graph.draw_dos1ev()


if __name__== '__main__':
    draw_test()
