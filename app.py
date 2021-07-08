import tkinter as tk
from tkinter import filedialog, Text, Listbox, filedialog
import os
import cv2


APP_TITLE = "Steganography Packer"
WINDOW_H = 500
WINDOW_W = 500

GREY_DARK   = "gray68"
GREY_LIGHT  = "gray88"

BUTTON_COL  = "gray55"

TEXT_COL    = "gray40"
TEXT_FONT   = "Helvatical bold"

root = tk.Tk()

payload = []
hosts   = []


def loadImages(img_array, image_list):
    img_array = getSelection()
    file_list = getFileNames(img_array)
    setListBox(image_list, file_list)

def getSelection():
    return filedialog.askopenfilenames(parent=root, title='Select Images')

def getFileNames(dirs):
    base_names = []
    for file in dirs:
        base_names.append(os.path.basename(file))
    return base_names

def setListBox(list_box, image_list):
    for i, img in enumerate(image_list):
        list_box.insert(i, img)

def clearInput(img_array, image_list):
    img_array.clear()
    image_list.delete(0, 'end')

def process():
    print("processed")

def launch():
    root.resizable(width=False, height=False)
    root.title(APP_TITLE)

    canvas = tk.Canvas(root, height=WINDOW_H, width=WINDOW_W, bg=GREY_DARK)
    canvas.pack()
    
    data_frame = tk.Frame(root, bg=GREY_LIGHT)
    data_frame.place(relwidth=0.95, relheight=0.4, relx=0.025, rely=0.025)
    host_frame = tk.Frame(root, bg=GREY_LIGHT)
    host_frame.place(relwidth=0.95, relheight=0.4, relx=0.025, rely=0.45)
    info_frame = tk.Frame(root, bg=GREY_LIGHT)
    info_frame.place(relwidth=0.95, relheight=0.1, relx=0.025, rely=0.875)

    
    create_lbl = tk.Label(data_frame, text="PAYLOAD", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=10)
    payload_list = Listbox(data_frame, height = 8, 
                  width = 49,
                  bg = GREY_DARK,
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = GREY_LIGHT)
    payload_list.place(x=15, y=40)
    addImages = tk.Button(data_frame, text="Import", padx=10, pady=2, fg="white", bg=BUTTON_COL, command= lambda: loadImages(payload, payload_list))
    addImages.place(x=320, y=5)
    clearImages = tk.Button(data_frame, text="Clear", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: clearInput(payload, payload_list))
    clearImages.place(x=392, y=5)


    create_lbl = tk.Label(host_frame, text="CONTAINERS", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=10)
    container_list = Listbox(host_frame, height = 8, 
                  width = 49, 
                  bg = GREY_DARK,
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = GREY_LIGHT)
    container_list.place(x=15, y=40)
    addImages = tk.Button(host_frame, text="Import", padx=10, pady=2, fg="white", bg=BUTTON_COL, command= lambda: loadImages(hosts, container_list))
    addImages.place(x=320, y=5)
    clearImages = tk.Button(host_frame, text="Clear", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: clearInput(hosts, container_list))
    clearImages.place(x=392, y=5)


    create_lbl = tk.Label(info_frame, text="INFO", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=5)
    #entrybox for prefix
    #dropdown for steg rounding (5, 10, 20) ?
    #entrybox for folder name to be made in container location
    
    clearImages = tk.Button(info_frame, text="PROCESS", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: process())
    clearImages.place(x=370, y=10)


#topleft pixel RGB is steg rounding, num containers for specific payload file, 

if __name__ == "__main__":
    launch()
