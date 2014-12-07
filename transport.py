import os
import start
import run_calculation
import tkMessageBox
import draw_graph
import text_editor
import time
import subprocess
from Tkinter import *

class Transport():
    def __init__(self,root, right_frame):
	self.root = root
	self.right_frame = right_frame
	self.case = "gui"
	self.so_executed=False
	self.transport_execute=False
	self.boltz_execute = False
	self.boltztrap_folder = "./boltztrap_folder/"
    def draw_graph1(self):
	self.draw_graph = draw_graph.Draw_Graph('','')
	self.draw_graph.draw_const_K(self.temperature_value.get(), 
					self.x_axis_value.get(),
					self.y_axis_value.get())
    def execute_boltz(self):

	self.boltz_execute = True
	self.fermi_ne()
	os.system("cp " + self.boltztrap_folder + "/BoltzTraP.def ./")
	os.system("cp " + self.case + ".energy trans.energy")
	os.system("cp " + self.case + ".struct trans.struct")
	os.system(self.boltztrap_folder+"/src/BoltzTraP BoltzTraP.def")

	os.system("grep VOLUME trans.outputtrans >> volume.temp")

	self.temperature_label = Label(self.right_frame, text="Temperature(K)",padx=0,pady=0,borderwidth=0,bd=0)
	self.x_axis_label = Label(self.right_frame, text="X-axis",padx=0,pady=0,borderwidth=0,bd=0)
	self.y_axis_label = Label(self.right_frame, text="Y-axis",padx=0,pady=0,borderwidth=0,bd=0)
	self.temperature_value = StringVar()
	self.temperature_entry = Entry(self.right_frame, textvariable = self.temperature_value)
	x_axis_list = [("Carrier concentration","1"),("Fermi level","2")]
	
	self.x_axis_value = StringVar()
	self.x_axis_value.set("1")
	self.x_axis_buttons=[]
	self.y_axis_value = StringVar()
	self.y_axis_value.set("DOS")
	self.y_axis_option = OptionMenu(self.right_frame, self.y_axis_value,
			"DOS","Seeback coefficient","sigma/tau","R_H","kappa0","c_e","chi")
	self.draw_graph1_button = Button(self.right_frame, text="Execute",
					command=lambda n=1 : self.draw_graph1())
	
	i=0

	
	self.temperature_label.grid(row=5,column=0,columnspan=2,sticky=W)
	self.x_axis_label.grid(row=6,column=0,columnspan=2,sticky=W)
	self.temperature_entry.grid(row=5,column=2,sticky=W)
	
	for text, val in x_axis_list:
	    b = Radiobutton(self.right_frame,text=text, 
				variable = self.x_axis_value, value=val)
	    self.x_axis_buttons.append(b)
	    b.grid(row=6+i,column=2,sticky=E)
	    i=i+1
	self.y_axis_label.grid(row=6+i,column=0,columnspan=2,sticky=W)
	self.y_axis_option.grid(row=6+i,column=2,sticky=E)
	self.draw_graph1_button.grid(row=7+i,column=0,columnspan=5,sticky=W)
	

	
	

    def fermi_ne(self):
	ne_file = open("ne.temp","r")
	ne_l = ne_file.readline().strip()
	ne_list = ne_l.split()
	print ne_list
	ne_value = ne_list[1]
	ne_file.close()
	fermi_file = open("fermi.temp","r")
	fermi_l = fermi_file.readline()
	fermi_list = fermi_l.split("=")
	fermi_value=fermi_list[1].strip()
	#print ne_value, fermi_value
	fermi_file.close()
	
	intrans_file = open("trans.intrans","r")
	copy_original = intrans_file.readlines()
	
	intrans_file.close()
	print copy_original[2].split()
	modify_line = copy_original[2].split()
	modify_line[3] = ne_value
	modify_line[0] = fermi_value[0:7]
	
	intrans_file = open("trans.intrans","w")
	intrans_file.write(copy_original[0])
	intrans_file.write(copy_original[1])
	intrans_file.write(' '.join(modify_line) + "\n")
	
	for i in range(len(copy_original)-3):
	    intrans_file.write(copy_original[3+i])
	intrans_file.close()

    def show_entry(self,op):
        if op==2:#When Excute button is toggled
	    self.transport_execute=True
           
	    os.system("rm -rf ./trans/")
	    os.system("mkdir trans")
	    os.system("cp " + self.case + ".struct ./trans/")
	    if self.so_executed:
		print "cp " + self.case + ".energyso* ./trans/"
		os.system("cp " + self.case + ".energyso* ./trans/")
	    print "cp " + self.case + ".energy* ./trans/"
	    os.system("cp " + self.case + ".energy* ./trans/")
	    if os.path.exists("/home/wien2k/work/" + self.case + "/"+self.case+".inso"):
		self.boltztrap_folder = "/home/wien2k/boltz/comiled/"
	    os.system("cp " + self.boltztrap_folder + "trans.intrans ./trans")
	    os.system("cp " + self.case + ".inso ./trans")
	    os.system("cp " + self.boltztrap_folder + "util/gather_energy.pl ./trans/")
	    os.chdir("./trans/")
	    os.system("chmod +x gather_energy.pl")
	    os.system("./gather_energy.pl " + self.case)

	    os.system("grep :FER ../test/"+self.case+".scf >> fermi.temp")
	    if os.path.exists("/home/wien2k/work/" + self.case + "/" + "scf/" + self.case + ".in2"):
		os.system("grep NE ../test/" + self.case+".in2 >> ne.temp")
	    else:
		os.system("grep NE ../test/" + self.case+".in2c >> ne.temp")
	    

	    self.boltz_execute_image = PhotoImage(file="../template/inner_button_1_boltztrap_execute.gif")
	    self.boltz_execute_bt = Button(self.right_frame, text="Execute",
					image = self.boltz_execute_image,
					command=lambda n=1:self.execute_boltz())
	    self.boltz_execute_bt.grid(row=4, column=0, columnspan=5, sticky=W,padx=0,pady=0)

		
	 
        '''if not self.init_toggles[op]:
            self.init_toggles[op]=True
            self.init_buttons[op].config(image = self.inner_button_2[op])
            if op==0:
                self.so_button.grid(row=1,column=2,padx=0)
            elif op==1:
		self.p_value.grid(row=2,column=2,padx=0)
        else:
            self.init_toggles[op]=False
            self.init_buttons[op].config(image = self.inner_button_1[op])
	    if op==0:
		self.so_button.grid_forget()
		print "So Value was + " + str(self.so_value.get())
	    elif op==1:
		self.p_value.grid_forget()
		print "P Value was " + self.p_value.get()'''
		




    def destroy_menu(self):
        #for i in range(3):
        self.init_buttons[2].grid_forget()
        if self.init_toggles[0]:
            self.so_button.grid_forget()
        if self.init_toggles[1]:
            self.p_value.grid_forget()
	os.chdir("/home/wien2k/work/gui")
	if self.transport_execute:
	    self.boltz_execute_bt.grid_forget()
	if self.boltz_execute:
	    self.temperature_label.grid_forget()
	    self.x_axis_label.grid_forget()
	    self.y_axis_label.grid_forget()
	    self.y_axis_option.grid_forget()
	    self.temperature_entry.grid_forget()
	    self.draw_graph1_button.grid_forget()
	    for bts in self.x_axis_buttons:
		bts.grid_forget()
    def create_menu(self):
	button_name = ['So','P','Transport_Execute']
	self.init_toggles=[]
	self.init_buttons=[]
	self.inner_button_1=[]
	self.inner_button_2=[]
	self.name_image = PhotoImage(file = "template/name_transport.gif")
	
	for i in range(len(button_name)):
	    tmp = PhotoImage(file = "template/inner_button_1_" + button_name[i].lower() + ".gif")
	    self.inner_button_1.append(tmp)
	    tmp = PhotoImage(file = "template/inner_button_2_" + button_name[i].lower() + ".gif")
            self.inner_button_2.append(tmp)
            temp = Button(self.right_frame, text = button_name[i],
                            image = self.inner_button_1[i],
                            command=lambda i=i : self.show_entry(i))

            self.init_buttons.append(temp)
            self.init_toggles.append(False)
	self.so_value = IntVar()
	self.so_button = Checkbutton(self.right_frame, text="So option",variable=self.so_value)

	self.p_value = Spinbox(self.right_frame, from_=1, to=4)
	init_buttons_padx=5
	init_buttons_pady=3
	
	self.name_label = Label(self.right_frame, image = self.name_image,
                                        padx=0,pady=0,borderwidth=0,bd=0)
        self.name_label.grid(row=0,column=0,sticky=W,padx=2,
                                columnspan=5,pady=10)

        '''for i in range(2):
            self.init_buttons[i].grid(row=i+1,column=0,sticky=W,
                                            padx=init_buttons_padx,
                                            pady=init_buttons_pady)'''
	self.init_buttons[2].grid(row=3,column=0,columnspan=5, sticky=W,
				padx=0,pady=0)

    def write_machines(self,p):
        f = open("gui.machines","w")
        if p=='2':
            print p
            f.write("1:localhost\n1:localhost\ngranularity:1\nextrafine:1")
        elif p=='4':
            f.write("1:localhost\n1:localhost\n1:localhost\n1:localhost\ngranularity:1\nextrafine:1")
        f.close()
