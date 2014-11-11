import os
#os.system("/home/wien2k/wien2k/init_lapw -b -red 0 -vxc 13 -ecut -6.0 -rkmax 7.0 -mix 0.2 -numk 1000")

from Tkinter import *
#from gui import run_cal as run_cal
import run_calculation as run_cal
import dos_calculation as dos_cal

tab_mode=0
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
	self.root = master
        self.pack()
        #self.createWidgets()
	self.initial_cal = 0
	self.run_cal_menu = 0
	self.dos_cal_menu = 0
	self.create_frames()
    def create_frames(self):
	self.left_frame = Frame(self.master, background="white",borderwidth=2,
				relief=RIDGE, height=640, width=164)
	self.left_frame.pack_propagate(False)
	self.right_frame = Frame(self.master, background="gray90",borderwidth=2,
			relief=RIDGE, width=263,height=640)
	self.right_frame.grid_propagate(False)
	self.right_frame.pack(side=RIGHT,fill=BOTH)
	self.left_frame.pack(side=LEFT,fill=BOTH)
	
	self.run_cal = run_cal.Run_Calculation(self.root, self.right_frame)
	self.dos_cal = dos_cal.Dos_Calculation(self.root, self.right_frame)

	self.tab_menu = IntVar()
	self.radio_buttons =[]
	self.left_button_1=[]
	self.left_button_2=[]

	#left buttons
	self.left_button_1.append(PhotoImage(file="template/left_button_1_initial_calculation.gif"))
	self.left_button_2.append(PhotoImage(file="template/left_button_2_initial_calculation.gif"))
	self.left_button_1.append(PhotoImage(file="template/left_button_1_run_calculation.gif"))
	self.left_button_2.append(PhotoImage(file="template/left_button_2_run_calculation.gif"))
	self.left_button_1.append(PhotoImage(file="template/left_button_1_dos_calculation.gif"))
	self.left_button_2.append(PhotoImage(file="template/left_button_2_dos_calculation.gif"))
	self.left_button_1.append(PhotoImage(file="template/left_button_1_transport.gif"))
	self.left_button_2.append(PhotoImage(file="template/left_button_2_transport.gif"))
	#

	self.left_up = PhotoImage(file = "template/left_up.gif")
	self.empty_label = Label(self.left_frame, background="white",image = self.left_up)
	self.empty_label.grid(row=0,column=0)

	for text, var in [('Initial Calculation',1), ('Run Calculation',2),('Dos Calculation',3)]:
		
		temp = Radiobutton(self.left_frame, text=text, value=var,indicatoron=0,
				variable = self.tab_menu,command=self.verify,
				image = self.left_button_1[var-1],
				bd=0,borderwidth=0)
		self.radio_buttons.append(temp)
   		temp.grid(row=len(self.radio_buttons),column=0,sticky=W)

    def destroy_initial(self):
	self.initial_cal = 0
	self.name_label.grid_forget()
	for i in range(7):
	    self.init_buttons[i].grid_forget()
	    if self.init_toggles[i]:
		self.init_input[i].grid_forget()
	
    def verify(self):
	if self.tab_menu.get()==1:
	    self.radio_buttons[0].config(image = self.left_button_2[0])
	    if self.initial_cal:
		self.destroy_initial()
	    elif self.run_cal_menu and self.run_cal.exist:
		self.radio_buttons[1].config(image = self.left_button_1[1])
		self.run_cal.destroy_menu()
		self.run_cal_menu=0
		#clean right frame and change run_cal button image
	    elif self.dos_cal_menu:
		self.radio_buttons[2].config(image = self.left_button_1[2])
		self.dos_cal.destroy_menu()
		self.dos_cal_menu=0
	    self.initial_cal = 1
	    self.initial_calculation()
	elif self.tab_menu.get()==2:
	    #self.run_calculation()
	    if self.initial_cal:
		self.destroy_initial()
		self.radio_buttons[0].config(image = self.left_button_1[0])
		self.initial_cal=0
		#change initial_cal button image
	    elif self.run_cal_menu and self.run_cal.exist:
		self.run_cal.destroy_menu()
	    elif self.dos_cal_menu:
                self.radio_buttons[2].config(image = self.left_button_1[2])
                self.dos_cal.destroy_menu()
                self.dos_cal_menu=0

	    self.run_cal.create_menu()
	    self.run_cal_menu = 1
	    self.radio_buttons[1].config(image = self.left_button_2[1])
	elif self.tab_menu.get()==3:
	    self.radio_buttons[2].config(image = self.left_button_2[2])
	    if self.initial_cal:
		self.destroy_initial()
		self.radio_buttons[0].config(image = self.left_button_1[0])
		self.initial_cal = 0
	    elif self.run_cal_menu and self.run_cal.exist:
		self.run_cal.destroy_menu()
		self.radio_buttons[1].config(image = self.left_button_1[1])
		self.run_cal_menu=0
		self.dos_cal.so_execute = self.run_cal.so_execute
	    print 3
	    self.dos_cal.create_menu()
	    self.dos_cal_menu = 1
    def show_entry(self,op):
	if op==6:#When Excute button is toggled
	    instruction = "/home/wien2k/wien2k/init_lapw -b "
	    if self.init_toggles[0]:
		instruction +="-red " + self.init_input_values[0].get() + " "
		    
	    if self.init_toggles[1]:
		instruction +="-vxc " + self.init_input_values[1].get() + " "


	    if self.init_toggles[2]:
		instruction +="-ecut " + self.init_input_values[2].get() + " "
	    if self.init_toggles[3]:
		instruction +="-rkmax " + self.init_input_values[3].get() + " "
	    if self.init_toggles[4]:
		instruction +="-mix " + self.init_input_values[4].get() + " "
	    if self.init_toggles[5]:
		instruction +="-numk " + self.init_input_values[5].get() + " "
	    os.system(instruction)
	    return


	if not self.init_toggles[op]:
	    self.init_toggles[op]=True
	    self.init_buttons[op].config(image = self.inner_button_2[op])
	    if op==0:
		row=1
		column=4
	    elif op==1:
		row=2
		column=4
	    elif op==2:
		row=3
		column=4
	    elif op==3:
		row=4
		column=4
	    elif op==4:
		row=5
		column=4
	    elif op==5:
		row=6
		column=4
	    self.init_input[op].grid(row=row,column=column-2,padx=0)
	else:
	    self.init_toggles[op]=False
	    self.init_buttons[op].config(image = self.inner_button_1[op])
	    self.init_input[op].grid_forget()
	    print "Value was " + self.init_input_values[op].get()
    def initial_calculation(self):
	global tab_mode
	if tab_mode!=1:
	
	    print "Tab mode = " + str(tab_mode)
	button_name=["Red","Vxc","Ecut","Rkmax","Mix","Numk","Execute"]
	self.init_buttons=[]
	self.init_input=[]
	self.init_input_values=[]
	self.init_toggles=[]
	tab_mode=1
	self.inner_button_1=[]
	self.inner_button_2=[]
	self.name_image = PhotoImage(file = "template/name_initial_calculation.gif")

	for i in range(len(button_name)):
		tmp = PhotoImage(file="template/inner_button_1_" + button_name[i].lower() + ".gif")
		self.inner_button_1.append(tmp)
		tmp = PhotoImage(file="template/inner_button_2_" + button_name[i].lower() + ".gif")
		self.inner_button_2.append(tmp)
		temp = Button(self.right_frame,text=button_name[i],
				padx=0,pady=0,borderwidth=0,bd=0,
				image = self.inner_button_1[i],
				command=lambda i=i : self.show_entry(i))
		self.init_buttons.append(temp)
		e = StringVar()
		temp = Entry(self.right_frame,textvariable=e)
		self.init_input.append(temp)
		self.init_toggles.append(False)
		self.init_input_values.append(e)

	init_buttons_padx=5
	init_buttons_pady=3
	self.name_label = Label(self.right_frame, image = self.name_image,
				padx=0,pady=0,borderwidth=0,bd=0)
	self.name_label.grid(row=0,column=0,sticky=W, padx=2, 
				columnspan=5,pady=10)
	for i in range(6):
	    self.init_buttons[i].grid(row=i+1,column=0,sticky=W,
					padx=init_buttons_padx,
					pady=init_buttons_pady)
	self.init_buttons[6].grid(row=7,column=0,columnspan=5,sticky=W,padx=0,pady=5)
	


    def createWidgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=root.destroy)
        self.QUIT.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


def main():
    root = Tk()
    app = Application(master=root)


    app_width = 690
    app_height=640
    app.master.title("Wien2k_GUI")
    app.master.configure(width=app_width,height=app_height)
    app.master.minsize(app_width,app_height)
    app.master.maxsize(app_width,app_height)
    app.mainloop()

if __name__=='__main__':
    main()
