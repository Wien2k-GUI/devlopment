import os
import start
import run_calculation
import tkMessageBox
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
	self.boltztrap_folder = "./boltztrap_folder/"


    def show_entry(self,op):
        if op==2:#When Excute button is toggled
	    
           
	    os.system("rm -rf ./trans/")
	    os.system("mkdir trans")
	    os.system("cp " + self.case + ".struct ./trans/")
	    os.system("cp " + self.case + ".energy* ./trans/")
	    if self.so_executed:
		os.system("cp " + self.case + ".energyso* ./trans/")
	    if os.path.exists("/home/wien2k/work/" + self.case + "/"+self.case+".inso"):
		self.boltztrap_folder = "/home/wien2k/boltz/comiled/"
	    os.system("cp " + self.boltztrap_folder + "trans.intrans ./trans")
	    os.system("cp " + self.case + ".inso ./trans")
	    os.system("cp " + self.boltztrap_folder + "util/gather_energy.pl ./trans/")
	    os.chdir("./trans/")
	    os.system("chmod +x gather_energy.pl")
	    os.system("./gather_energy.pl " + self.case)
		
	 
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
    def create_menu(self):
	button_name = ['So','P','Execute']
	self.init_toggles=[]
	self.init_buttons=[]
	self.inner_button_1=[]
	self.inner_button_2=[]
	self.name_image = PhotoImage(file = "template/name_run_calculation.gif")
	
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
