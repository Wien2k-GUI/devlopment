import xlsxwriter
import os


class Draw_Graph():
    def __init__(self,folder_name,folder_path):
	self.folder_name = folder_name
	self.folder_path = folder_path


	#next two lines will be deleted. It is just for test.
	self.folder_name="gui"
	self.folder_path="/home/wien2k/work/gui/"

    def draw_const_K(self, K, x_axis, y_axis):
	f = open("trans.trace","r")

	K_lines = []
	K_value = round(float(K), 5)
	f.readline()
	for line in f.readlines():
	    if round(float(line.strip().split()[1]),5)==K_value:
		K_lines.append(line)
		#print line
	f.close()
	y_attribute=['Ef','T','N','DOS','Seeback coefficient','sigma/tau','R_H','kappa0','c_e','chi']
	y_index = y_attribute.index(y_axis)
	x_data = []
	y_data = []
	volume_file = open("volume.temp","r")
	volume = round(float(volume_file.readline().strip().split()[1]),5)
	volume_file.close()
	print "volume = " + str(volume)
	workbook = xlsxwriter.Workbook(x_axis + '_' + y_axis + '.xlsx')
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold':1})

	headings=[]
	if x_axis=='1':
	    headings.append('carrier concentration')
	else
	    headings.append('Fermi level')
	headings.append(y_axis)
	for line in K_lines:
	    elem_line = line.strip().split()
	    if x_axis=="1":
		denom = volume*(0.529177^3)*10^-24
		x_value =  round(float(elem_line[2]),5) / denom
	    else:
		x_value = round(float(elem_line[0]),5)
	    x_data.append(x_value)
	    y_data.append(round(float(elem_line[y_index]),5))
	worksheet.write_row('A1',headings,bold)
	worksheet.write_column('A2',x_data)
	worksheet.write_column('B2',y_data)
	
	
	workbook.close()

    def export_trace(self):
	f = open("trans.trace","r")
	workbook = xlsxwriter.Workbook('trans_trace.xlsx')
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold':1})

	headings = ['Ef[RY]', 'T[K]', 'N','DOS(Ef)','seedback coefficient', 'sigma/tau','R_H','kappa0', 'c_e','chi']
	data_list=[]
	for i in range(len(headings)):
	    temp=[]
	    data_list.append(temp)
	data_flag = False #To avoid first line
	
	for line in f.readlines():
	    if data_flag:
		elem_line = line.strip().split()
		for i in range(len(elem_line)):
		    data_list[i].append(round(float(elem_line[i]),5))
	    if ' Ef[Ry] ' in line and not data_flag:
		data_flag = True
	worksheet.write_row('A1',headings,bold)
	alphabet_list = ['A','B','C','D','E','F','G','H','I','J']
	for i in range(len(headings)):
	    worksheet.write_column(alphabet_list[i]+'2',data_list[i])

	workbook.close()
	f.close()

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
	f.close()
	



def draw_test():
    draw_graph = Draw_Graph('gui','/home/wien2k/work/gui')
    #draw_graph.draw_dos1ev()
    draw_graph.export_trace()


if __name__== '__main__':
    draw_test()
