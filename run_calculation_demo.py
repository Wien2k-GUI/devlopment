import os
import start_demo
import tkMessageBox
import time
import subprocess
from Tkinter import *


class Run_Calculation():
    def __init__(self, root, right_frame):
	self.root = root
	self.right_frame=right_frame 
	self.exist = False
    def show_entry(self,op):
	if op==4:
	    instruction = "/home/wien2k/wien2k/run_lapw "
	    if self.init_toggles[0]:
		instruction += "-ec " + self.ec_value.get() + " "
	    if self.init_toggles[1]:
		instruction +="-so "
	    if self.init_toggles[2]:
		instruction +="-p "
		self.write_machines(self.p_value.get())
	    if self.init_toggles[3]:

		'''if os.path.exists("/home/wien2k/work/gui/gui.dayfile"):
			f = open("/home/wien2k/work/gui/gui.dayfile","r")
			for line in f.readlines():
			    if "ec cc and fc_conv 1 1 1" in line:
				self.result=0
				break'''
			




		instruction = "qsub ../test/qsub.sh"
	    '''else:
		instruction+=">>std.out"'''
	
	    print instruction
	    #os.system(instruction)
	    if not self.init_toggles[3]:
		p = subprocess.Popen(instruction,shell=True, stdout=subprocess.PIPE)
		stdout = []
		while True:
		    line = p.stdout.readline()
		    stdout.append(line)	
		    print "run_lapw = " + line
		    if "ec cc and fc_conv 1 1 1" in line:
			print "Run Lapw is finished!"
			os.system("/home/wien2k/wien2k/save_lapw -a -d test")
			break
		    if line == '' and p.poll() != None:
			break
	    


	    return

	if not self.init_toggles[op]:
	    self.init_toggles[op] = True
	    self.init_buttons[op].config(image =self.inner_button_2[op])
	    if op==0:
		self.ec_entry.grid(row=1,column=2,padx=0)
	    elif op==1:
		self.so_button.grid(row=2,column=2,padx=0)
	    elif op==2:
		self.p_value.grid(row=3,column=2,padx=0)
	    elif op==3:
		self.qsub_button.grid(row=4,column=2,padx=0)
	else:
	    self.init_toggles[op]=False
	    self.init_buttons[op].config(image = self.inner_button_1[op])
	    if op==0:
		self.ec_entry.grid_forget()
		print "Ec Value was "  + self.ec_value.get()
	    elif op==1:
		self.so_button.grid_forget()
		print "So Value was " + str(self.so_value.get())
	    elif op==2:
		print "P Value was " + self.p_value.get()
		self.p_value.grid_forget()
	    elif op==3:
		self.qsub_button.grid_forget()
		print "Qsub Value was" + str(self.qsub_value.get())
    def destroy_menu(self):
	for i in range(5):
	    self.init_buttons[i].grid_forget()
	if self.init_toggles[0]:
	    self.ec_entry.grid_forget()
	if self.init_toggles[1]:
	    self.so_button.grid_forget()
	if self.init_toggles[2]:
	    self.p_value.grid_forget()
	if self.init_toggles[3]:
	    self.qsub_button.grid_forget()
	    
    def create_menu(self):
	if os.path.exists("/home/wien2k/work/gui/gui.outputd"):
	    print "True"
	    self.exist = True
	    print type(self.root)
    	    button_name = ['Ec','So','P','Qsub','Execute']
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
	    self.ec_value = StringVar()
		
	    self.ec_entry = Entry(self.right_frame, textvariable=self.ec_value)
	    self.so_value = IntVar()
	    self.qsub_value = IntVar()


	    self.so_button = Checkbutton(self.right_frame, text="So option",variable=self.so_value)
	    self.qsub_button = Checkbutton(self.right_frame, text="Qsub option",variable=self.qsub_value)

	    self.p_value = Spinbox(self.right_frame, from_=1, to=4)
	    init_buttons_padx = 5
	    init_buttons_pady = 3
	
	    self.name_label = Label(self.right_frame, image = self.name_image,
					padx=0,pady=0,borderwidth=0,bd=0)
	    self.name_label.grid(row=0,column=0,sticky=W,padx=2,
				columnspan=5,pady=10)	

	    for i in range(4):
		self.init_buttons[i].grid(row=i+1,column=0,sticky=W,
						padx=init_buttons_padx,
						pady=init_buttons_pady)
	    self.init_buttons[4].grid(row=5,column=0,columnspan=5,
					sticky=W,padx=0,pady=5)
	
	else:
	    tkMessageBox.showwarning("Warning","initialization is not yet finished.")
	    self.exist = False
	    print "False"

    def write_machines(self,p):
	f = open("gui.machines","w")
	if p=='2':
	    print p
	    f.write("1:localhost\n1:localhost\ngranularity:1\nextrafine:1")
	elif p=='4':
	    f.write("1:localhost\n1:localhost\n1:localhost\n1:localhost\ngranularity:1\nextrafine:1")
	f.close()
