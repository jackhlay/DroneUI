from tkinter import *
import tkintermapview

root = Tk()
root.title('Codemy.com - Tkinter MapView')
root.iconbitmap('c:/gui/codemy.ico')
root.geometry("900x700")

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600, corner_radius=0)
# Set Coordinates
map_widget.set_position(38.54567651402582, -106.9184393841674)

# Set A Zoom Level
map_widget.set_zoom(20)


map_widget.pack()



root.mainloop()