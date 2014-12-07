import os
import matplotlib.pyplot as mp
import transport
import time
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from Tkinter import *

class Show_Graph():
    def __init__(self, root, right_frame,x_data, y_data):
	matplotlib.use('TkAgg')
	self.root = root
	self.right_frame = right_frame
	self.x_data
	self.y_data

    def show_entry(self):
	self.show_graph = Toplevel(self.root)
	f = Figure(figsize(5,4),dpi=100)
	a = f.add_subplot(111)
	
	
	a.plot(self.x_data,self.y_data)
	a.set_title('Result Graph')
	a.set_xlabel('x_axis')
	a.set_ylabel('y_axis')
	#mp.draw()

	canvas = FigureCanvasTkAgg(f,master = self.show_graph)
	canvas.show()
	canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
	canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
	
	self.show_graph.mainloop()

