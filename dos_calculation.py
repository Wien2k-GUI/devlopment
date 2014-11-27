import os
import start
import run_calculation
import tkMessageBox
import draw_graph
import text_editor
import time
import subprocess
from Tkinter import *

class Dos_Calculation():
    def __init__(self,root, right_frame):
	self.root = root
	self.right_frame = right_frame
	self.so_execute = False
	self.number_of_atoms=0
	self.dos_graph_execute=False
    def execute_dos_cal(self, atom_num):
	int_file = open("/home/wien2k/work/gui/gui.int","w")
	int_file.write(self.line_one)
	int_file.write(self.line_two)
	int_file.write("  " + self.tot_of_dos.get() + "     " + self.tot_of_atoms.get() + "    0.000\n")
	if self.total_check_var.get():
	    int_file.write("    0     1    total\n")
	for i in range(atom_num):
	    for j in range(4):
		if self.atoms[i][j].get():
		    int_file.write("    " + str(i+1)+"     " + str(j+1)+"    "+
				"Atom" + str(i+1) + " ")
		    if j==0:
			int_file.write("tot\n")
		    elif j==1:
			int_file.write("s\n")
		    elif j==2:
			int_file.write("p\n")
		    elif j==3:
			int_file.write("d\n")
	
	instruction = "x tetra "
	if self.so_value.get() and self.so_execute:
	    instruction+="-so"
	self.draw_graph = draw_graph.Draw_Graph('gui','/home/wien2k/work/gui')
	int_file.close()
	os.system(instruction)
	self.draw_graph.draw_dos1ev()
	print "Drawing dos1ev is completed!"


    def make_dos_option(self, atom_num):
	atom_num = int(self.tot_of_atoms.get())
	self.number_of_atoms=atom_num
	self.dos_graph_execute=True
	self.atoms=[]
	self.atoms_checkbuttons=[]
	self.atoms_image = PhotoImage(file="template/inner_button_1_atoms.gif")
	self.total_check_var = IntVar()
	self.total_check = Checkbutton(self.right_frame, text="total", variable=self.total_check_var)
	
	self.atoms_image_label = Label(self.right_frame, image = self.atoms_image, padx=0, pady=0, borderwidth=0,bd=0)
	self.atoms_image_label.grid(row=7,column=0, padx=0,columnspan=2,pady=0,sticky=W)
	self.total_check.grid(row=7, column=2, padx=5, pady=3)
	for i in range(atom_num):
	    atoms_tot=IntVar()
	    atoms_s=IntVar()
	    atoms_p=IntVar()
	    atoms_d=IntVar()
	    atoms_tot_check = Checkbutton(self.right_frame, text="tot",variable=atoms_tot)
	    atoms_s_check = Checkbutton(self.right_frame, text="s",variable=atoms_s)
	    atoms_p_check = Checkbutton(self.right_frame, text="p",variable=atoms_p)
	    atoms_d_check = Checkbutton(self.right_frame, text="d",variable=atoms_d)
	    temp_list = [atoms_tot, atoms_s, atoms_p, atoms_d]
	    self.atoms.append(temp_list)
	    temp_label = Label(self.right_frame, text=str(i+1), padx=0, pady=0, borderwidth=0, bd=0,width=3)
	    temp_label.grid(row=8+i, column=0,sticky=W+E)
	    self.atoms_checkbuttons.append([temp_label,atoms_tot_check,atoms_s_check,atoms_p_check,atoms_d_check])
	    atoms_tot_check.grid(row=8+i,column=1)
	    atoms_s_check.grid(row=8+i,column=2)
	    atoms_p_check.grid(row=8+i,column=3)
	    atoms_d_check.grid(row=8+i,column=4)
	self.draw_graph_image = PhotoImage(file="template/inner_button_1_execute.gif")
	self.draw_graph_button = Button(self.right_frame,image=self.draw_graph_image, command=lambda a=atom_num: self.execute_dos_cal(a))
	self.draw_graph_button.grid(row=8+i+1,column=0,columnspan=5)


    def show_entry(self,op):
        if op==2:#When Excute button is toggled
            instruction = "/home/wien2k/wien2k/x lapw2 -qtl "
	    
            if self.init_toggles[0]:
		if self.so_value.get():
		    if self.so_execute:
			instruction +="-so "
		    else:
			tkMessageBox.showwarning("Warning","so option is not yet executed.")
			return

            if self.init_toggles[1]:
		instruction +="-p "
		#self.write_machines(self.p_value.get())

	    f = open("/home/wien2k/work/gui/qsub.sh","w")
	    r = open("/home/wien2k/work/gui/qsub_bone.txt","r")
	
	    f.write("#!/bin/tcsh -f\n")
            f.write("#PBS -l nodes=1:ppn=4\n")
            f.write("##PBS -l nodes=x028:ppn=4\n")
            f.write("#PBS -N BT-K56000\n")


            for line in r.readlines():
                f.write(line)
            f.write(instruction)
	    f.close()
	    
	    self.execute_button_toggle=True
	    self.tot_of_dos = Spinbox(self.right_frame, from_=1, to=10,width=3)
	    self.tot_of_atoms=Spinbox(self.right_frame, from_=1, to=10,width=3)
	    int_file = open("/home/wien2k/work/gui/gui.int","r")
	    self.line_one = int_file.readline()
	    self.line_two = int_file.readline()
	    #l = int_file.readline()
	    #temp_input = l.split()
	    #print temp_input
	    int_file.close()
	    
	    #self.num_of_atom = int(temp_input[1])
	    #print "num of atom = " + str(self.num_of_atom)
	    #self.make_dos_option(self.num_of_atom)
	    self.total_number_of_dos = Label(self.right_frame, text="total number of dos", padx=0, pady=0, borderwidth=0,bd=0)
	    self.total_number_of_dos.grid(row=4,column=0, columnspan=2,sticky=W)
	    self.tot_of_dos.grid(row=4, column=2,columnspan=1)
	    self.tot_of_atoms.grid(row=5, column=2,columnspan=1)
	    self.dos_graph_execute_image= PhotoImage(file="template/graph_option_1.gif")
	    self.dos_graph_execute_bt = Button(self.right_frame, text="Execute",
					image=self.dos_graph_execute_image,
					command=lambda n=self.tot_of_dos.get() : self.make_dos_option(int(n)))
	    self.dos_graph_execute_bt.grid(row=6,column=0,columnspan=5,sticky=W, padx=0, pady=0)




	    #self.text_editor = text_editor.Text_Editor(self.root,self.right_frame)
	    #self.text_editor.show_entry()
            return

	
	
        if not self.init_toggles[op]:
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
		print "P Value was " + self.p_value.get()
		




    def destroy_menu(self):
        for i in range(3):
            self.init_buttons[i].grid_forget()
        if self.init_toggles[0]:
            self.so_button.grid_forget()
        if self.init_toggles[1]:
            self.p_value.grid_forget()
	if self.dos_graph_execute:
	    self.draw_graph_button.grid_forget()
	    self.atoms_image_label.grid_forget()
	    self.total_check.grid_forget()
	    for i in range(self.number_of_atoms):
		for j in range(5):
		    self.atoms_checkbuttons[i][j].grid_forget()
	if self.execute_button_toggle:
	    self.tot_of_dos.grid_forget()
	    self.tot_of_atoms.grid_forget()
	    self.dos_graph_execute_bt.grid_forget()
	    self.total_number_of_dos.grid_forget()
    def create_menu(self):
	button_name = ['So','P','x_lapw2_Execute']
	self.init_toggles=[]
	self.init_buttons=[]
	self.inner_button_1=[]
	self.inner_button_2=[]
	self.execute_button_toggle=False
	self.dos_graph_execute_toggle=False
	self.name_image = PhotoImage(file = "template/name_dos_calculation.gif")
	
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
        self.name_label.grid(row=0,column=0,padx=2,sticky=W,
                                columnspan=5,pady=10)

        for i in range(2):
            self.init_buttons[i].grid(row=i+1,column=0,sticky=W,
                                            padx=init_buttons_padx,
                                            pady=init_buttons_pady)
	self.init_buttons[2].grid(row=3,column=0,columnspan=5,sticky=W,
				padx=0,pady=0)

    def write_machines(self,p):
        f = open("gui.machines","w")
        if p=='2':
            print p
            f.write("1:localhost\n1:localhost\ngranularity:1\nextrafine:1")
        elif p=='4':
            f.write("1:localhost\n1:localhost\n1:localhost\n1:localhost\ngranularity:1\nextrafine:1")
        f.close()
