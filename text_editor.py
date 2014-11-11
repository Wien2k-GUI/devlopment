import os
import dos_calculation
import time
import subprocess
import ScrolledText
import tkFileDialog
import tkMessageBox
from Tkinter import *

class Text_Editor():
    def open_command(self):
	f = open("/home/wien2k/work/test/test.int","r")
	lines = f.readlines()
	for i in range(len(lines)):
	    self.textPad.insert('1.0',lines[len(lines)-i-1])
	
 
    def save_command(self):
        #file = tkFileDialog.asksaveasfile(mode='w')
	file = open("/home/wien2k/work/test/test.int","w")
        if file != None:
        # slice off the last character from get, as an extra return is added
            data = self.textPad.get('1.0', END+'-1c')
            file.write(data)
            file.close()
         
    def exit_command(self):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.text_editor.destroy()
	    os.system("python draw_graph.py")

    def __init__(self,root, right_frame):
        self.root = root
        self.right_frame = right_frame


    def show_entry(self):
        self.text_editor = Toplevel(self.root)
        self.text_edit = Label(self.text_editor, text="just for test")
        #self.text_edit.pack(side="top",fill="both",padx=10,pady=10)

        self.textPad = ScrolledText.ScrolledText(self.text_editor, width=100, height=80)
	menu = Menu(self.text_editor)
	self.text_editor.config(menu = menu)
	filemenu = Menu(menu)
	menu.add_cascade(label="File",menu = filemenu)
	filemenu.add_command(label="Save",command = self.save_command)
	filemenu.add_separator()
	filemenu.add_command(label="Exit",command = self.exit_command)

        self.textPad.pack(side="top",fill="both",padx=10,pady=10)
	self.open_command()

	self.text_editor.mainloop()
