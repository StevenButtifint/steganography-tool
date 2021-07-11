import tkinter as tk
from tkinter import filedialog, Text, Listbox, filedialog, Entry
import os
import cv2
from PIL import Image


APP_TITLE = "Steganography Packer"
WINDOW_H = 500
WINDOW_W = 500

GREY_DARK   = "gray68"
GREY_LIGHT  = "gray88"

BUTTON_COL  = "gray55"

TEXT_COL    = "gray40"
TEXT_FONT   = "Helvatical bold"

#input
payload     = []
hosts       = []

#output
containers  = []


def loadImages(img_array, image_list):
    selections = getSelection()    
    setArrayItems(img_array, selections)
    file_list = getFileNames(img_array)
    setListBox(image_list, file_list)


def setArrayItems(img_array, items):
    for item in items:
        img_array.append(item)


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


def extractData():
    print("extract images")


def packData(prefix_entry):
    print("pack images")

    prefix = prefix_entry.get()
    
    for index, img in enumerate(payload):
        out_location = os.path.dirname(img) + "/" + prefix
        try:
            os.mkdir(out_location)
        except:
            pass
        
        host_index = index % len(hosts)
        host_dir = hosts[host_index]
        container = cv2.imread(host_dir)

        #put host in container
        
        cv2.imwrite(out_location + "/" + "test.jpg", container)
        


def startMenu():
    menu_frame = tk.Frame(root, bg=GREY_LIGHT)
    menu_frame.place(relwidth=1, relheight=0.07, relx=0, rely=0)
    create_lbl = tk.Label(menu_frame, text="OPERATION:", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=7)
    create_lbl = tk.Label(menu_frame, text="or", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=260, y=7)
    packImages = tk.Button(menu_frame, text="Pack Data", padx=25, pady=2, fg="white", bg=BUTTON_COL, command= lambda: packInterface())
    packImages.place(x=130, y=5)
    openImages = tk.Button(menu_frame, text="Extract Data", padx=25, pady=2, fg="white", bg=BUTTON_COL, command= lambda: extractInterface())
    openImages.place(x=300, y=5)
    closeBtn = tk.Button(menu_frame, text="Quit", padx=2, pady=2, fg="white", bg=BUTTON_COL, command= lambda: quit())
    closeBtn.place(x=460, y=5)


def makeImportFrame(frame, frame_title, img_array, img_list):
    create_lbl = tk.Label(frame, text=frame_title, bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=10)

    addImages = tk.Button(frame, text="Import", padx=10, pady=2, fg="white", bg=BUTTON_COL, command= lambda: loadImages(img_array, img_list))
    addImages.place(x=320, y=5)
    clearImages = tk.Button(frame, text="Clear", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: clearInput(img_array, img_list))
    clearImages.place(x=392, y=5)


def packInterface():
    global data_frame, host_frame, info_frame
    try:
        container_frame.destroy()
        output_info_frame.destroy()
    except:
        pass
    
    data_frame = tk.Frame(root, bg=GREY_LIGHT)
    data_frame.place(relwidth=0.95, relheight=0.385, relx=0.025, rely=0.085)
    host_frame = tk.Frame(root, bg=GREY_LIGHT)
    host_frame.place(relwidth=0.95, relheight=0.385, relx=0.025, rely=0.5)
    info_frame = tk.Frame(root, bg=GREY_LIGHT)
    info_frame.place(relwidth=0.95, relheight=0.078, relx=0.025, rely=0.9)

    payload_list = Listbox(data_frame, height = 6, 
                  width = 40,
                  bg = GREY_DARK,
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = GREY_LIGHT)
    payload_list.place(x=15, y=40)
    makeImportFrame(data_frame, "PAYLOAD", payload, payload_list)

    host_list = Listbox(host_frame, height = 6, 
                  width = 40, 
                  bg = GREY_DARK,
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = GREY_LIGHT)
    host_list.place(x=15, y=40)
    makeImportFrame(host_frame, "CONTAINERS", hosts, host_list)

    info_lbl = tk.Label(info_frame, text="INFO", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    info_lbl.place(x=15, y=5)
    prefix_lbl = tk.Label(info_frame, text="Output Prefix:", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,9))
    prefix_lbl.place(x=70, y=7)
    prefix_entry = tk.Entry(info_frame, width=12)
    prefix_entry.place(x=150, y=7)
    clearImages = tk.Button(info_frame, text="PROCESS", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: packData(prefix_entry))
    clearImages.place(x=370, y=6)

    
    #increase host file by ~10% inc untill double size of payload dims
    #read bytes, split into front and end halfs and place into two least sig bits for two values at a time


def extractInterface():
    global container_frame, output_info_frame
    try:
        data_frame.destroy()#place_forget()
        host_frame.destroy()#place_forget()
        info_frame.destroy()#place_forget()
    except:
        pass
    
    container_frame = tk.Frame(root, bg=GREY_LIGHT)
    container_frame.place(relwidth=0.95, relheight=0.385, relx=0.025, rely=0.085)
    #output_frame = tk.Frame(root, bg=GREY_LIGHT)
    #output_frame.place(relwidth=0.95, relheight=0.385, relx=0.025, rely=0.5)
    output_info_frame = tk.Frame(root, bg=GREY_LIGHT)
    output_info_frame.place(relwidth=0.95, relheight=0.078, relx=0.025, rely=0.9)

    container_list = Listbox(container_frame, height = 6, width = 40, bg = GREY_DARK, activestyle = 'dotbox', font = "Helvetica", fg = GREY_LIGHT)
    container_list.place(x=15, y=40)

    makeImportFrame(container_frame, "CONTAINERS", containers, container_list)


    clearImages = tk.Button(output_info_frame, text="PROCESS", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: extractData())
    clearImages.place(x=370, y=6)
    


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title(APP_TITLE)
    canvas = tk.Canvas(root, height=WINDOW_H, width=WINDOW_W, bg=GREY_DARK).pack()
    startMenu()

