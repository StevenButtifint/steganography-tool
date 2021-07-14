import tkinter as tk
from tkinter import filedialog, Text, Listbox, filedialog, Entry
import os
import cv2
from PIL import Image
import numpy as np

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
out_loc = [0]

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


def setOutputLocation(output_location):
    location = getDirectory()
    output_location.insert(0, location)
    out_loc[0] = location
    


def getDirectory():
    return filedialog.askdirectory(parent=root, title='Select Output Folder Location')

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


def extractData(out_folder_entry):
    print("extract images")
    #add check that output location is given and selections are images
    
    out_location = out_loc[0] + "/" + out_folder_entry.get()
    try:
        os.mkdir(out_location)
    except:
        pass
    for container in containers:

        container_name_segs = os.path.basename(container).split(".")[0].split("-")
        out_name = container_name_segs[2] + ".png"
        
        current_cont = cv2.imread(container)
        current_out = np.zeros(shape=(int(current_cont.shape[0]),int(current_cont.shape[1]//2),3))

        x_out = 0
        for pix_row in range(0, current_cont.shape[0], 1):
            for pix_col in range(0, current_cont.shape[1], 2):

                cont_pix_front = current_cont[pix_row][pix_col]
                cont_pix_back = current_cont[pix_row][pix_col+1]

                b_pix = "{0:08b}".format(cont_pix_front[0])[4:8] + "{0:08b}".format(cont_pix_back[0])[4:8]
                b_pix = int(b_pix, 2)
                g_pix = "{0:08b}".format(cont_pix_front[1])[4:8] + "{0:08b}".format(cont_pix_back[1])[4:8]
                g_pix = int(g_pix, 2)
                r_pix = "{0:08b}".format(cont_pix_front[2])[4:8] + "{0:08b}".format(cont_pix_back[2])[4:8]
                r_pix = int(r_pix, 2)
                
                current_out[pix_row][x_out][0] = r_pix
                current_out[pix_row][x_out][1] = g_pix
                current_out[pix_row][x_out][2] = b_pix
                x_out += 1
            x_out = 0
                
        cv2.imwrite(out_location + "/" + str(out_name), current_out)

def packData(prefix_entry):
    print("pack images")

    prefix = prefix_entry.get()
    
    for index, img in enumerate(payload):
        out_location = os.path.dirname(img) + "/" + prefix
        try:
            os.mkdir(out_location)
        except:
            pass

        data_name = os.path.basename(payload[index]).split(".")[0]
        
        host_index = index % len(hosts)
        host_dir = hosts[host_index]

        data = cv2.imread(img)
        container = cv2.imread(host_dir)

        #make host 2x
        data_h, data_w, _ = data.shape
        container = cv2.resize(container, dsize=(int(data_w*2), int(data_h)), interpolation=cv2.INTER_CUBIC)

        x_pix = 0
        
        for pix_row in range(0, container.shape[0], 1):
            for pix_col in range(0, container.shape[1], 2):

               # print(pix_row, pix_col, x_pix)
               # print(container.shape)

                data_pix = data[pix_row][x_pix]
                
                cont_pix_front = container[pix_row][pix_col]
                cont_pix_back = container[pix_row][pix_col+1]

                b_front = "{0:08b}".format(cont_pix_front[0])[0:4] + "{0:08b}".format(data_pix[0])[0:4]
                b_front = int(b_front, 2)
                b_back = "{0:08b}".format(cont_pix_back[0])[0:4] + "{0:08b}".format(data_pix[0])[4:8]
                b_back = int(b_back, 2)

                g_front = "{0:08b}".format(cont_pix_front[1])[0:4] + "{0:08b}".format(data_pix[1])[0:4]
                g_front = int(g_front, 2)
                g_back = "{0:08b}".format(cont_pix_back[1])[0:4] + "{0:08b}".format(data_pix[1])[4:8]
                g_back = int(g_back, 2)
                
                r_front = "{0:08b}".format(cont_pix_front[2])[0:4] + "{0:08b}".format(data_pix[2])[0:4]
                r_front = int(r_front, 2)
                r_back = "{0:08b}".format(cont_pix_back[2])[0:4] + "{0:08b}".format(data_pix[2])[4:8]
                r_back = int(r_back, 2)


                container[pix_row][pix_col][0] = r_front
                container[pix_row][pix_col+1][0] = r_back
                
                container[pix_row][pix_col][1] = g_front
                container[pix_row][pix_col+1][1] = g_back
                
                container[pix_row][pix_col][2] = b_front
                container[pix_row][pix_col+1][2] = b_back

                x_pix += 1
            x_pix = 0
        
        cv2.imwrite(out_location + "/" + str(index) + "-" + str(prefix) + "-" + str(data_name) + ".png", container)
        


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


def makeListbox(frame):
    return Listbox(frame, height=6, width=40, bg=GREY_DARK, activestyle='dotbox', font="Helvetica", fg=GREY_LIGHT)


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

    payload_list = makeListbox(data_frame)
    payload_list.place(x=15, y=40)
    makeImportFrame(data_frame, "PAYLOAD", payload, payload_list)

    host_list = makeListbox(host_frame)
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
    output_frame = tk.Frame(root, bg=GREY_LIGHT)
    output_frame.place(relwidth=0.95, relheight=0.385, relx=0.025, rely=0.5)
    output_info_frame = tk.Frame(root, bg=GREY_LIGHT)
    output_info_frame.place(relwidth=0.95, relheight=0.078, relx=0.025, rely=0.9)

    container_list = Listbox(container_frame, height = 6, width = 40, bg = GREY_DARK, activestyle = 'dotbox', font = "Helvetica", fg = GREY_LIGHT)
    container_list.place(x=15, y=40)

    makeImportFrame(container_frame, "CONTAINERS", containers, container_list)

    create_lbl = tk.Label(output_frame, text="OUTPUT OPTIONS", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=10)
    #addImages = tk.Button(output_frame, text="Import", padx=10, pady=2, fg="white", bg=BUTTON_COL, command= lambda: loadImages(img_array, img_list))
    #addImages.place(x=320, y=5)

    output_location = Listbox(output_frame, height = 1, width = 40, bg = GREY_DARK, activestyle = 'dotbox', font = "Helvetica", fg = GREY_LIGHT)
    output_location.place(x=15, y=40)
    
    clearImages = tk.Button(output_frame, text="Set Output Location", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: setOutputLocation(output_location))
    clearImages.place(x=310, y=5)

    info_lbl = tk.Label(output_info_frame, text="INFO", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,11))
    info_lbl.place(x=15, y=5)
    prefix_lbl = tk.Label(output_info_frame, text="Output Folder:", bg=GREY_LIGHT, fg=TEXT_COL, font=(TEXT_FONT,9))
    prefix_lbl.place(x=70, y=7)
    out_folder_entry = tk.Entry(output_info_frame, width=12)
    out_folder_entry.place(x=150, y=7)
    clearImages = tk.Button(output_info_frame, text="PROCESS", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: extractData(out_folder_entry))
    clearImages.place(x=370, y=6)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.title(APP_TITLE)
    canvas = tk.Canvas(root, height=WINDOW_H, width=WINDOW_W, bg=GREY_DARK).pack()
    startMenu()

