import numpy as np
import tkinter as tk
import tkinter.filedialog
import os
import cv2
from PIL import Image
from constants import *


class Application:
    def __init__(self, master):
        self.window = master
        master.title("Steganography Tool")
        master.geometry("500x500")
        master.resizable(width=False, height=False)
        
        tk.Canvas(self.window, height=500, width=500, bg=COLOUR_DARK).pack()
        self.payload = []
        self.hosts = []
        self.containers = []
        self.out_location = ""
        self.displayOperations()


    def displayOperations(self):
        operations_frame = self._placeFrame(root, COLOUR_LIGHT, 1, 0.07, 0, 0)        
        self._placeLabel(operations_frame, "OPERATION:", COLOUR_LIGHT, COLOUR_TEXT, (TEXT_FONT,11), 15, 7)
        self._placeLabel(operations_frame, "or", COLOUR_LIGHT, COLOUR_TEXT, (TEXT_FONT,11), 260, 7)
        self._placeButton(operations_frame, "Pack Data", 25, 2, COLOUR_BUTTON_TEXT, COLOUR_BUTTON, lambda: self._packInterface(), 130, 5)
        self._placeButton(operations_frame, "Extract Data", 25, 2, COLOUR_BUTTON_TEXT, COLOUR_BUTTON, lambda: self._extractInterface(), 300, 5)
        self._placeButton(operations_frame, "Quit", 2, 2, COLOUR_BUTTON_TEXT, COLOUR_BUTTON, quit, 460, 5)


    @staticmethod
    def _placeFrame(parent, bg, rw, rh, rx, ry):
        frame = tk.Frame(parent, bg=bg)
        frame.place(relwidth=rw, relheight=rh, relx=rx, rely=ry)
        return frame


    @staticmethod
    def _placeLabel(frame, text, bg, fg, font, x, y):
        label = tk.Label(frame, text=text, bg=bg, fg=fg, font=font)
        label.place(x=x, y=y)


    @staticmethod
    def _placeButton(frame, text, padx, pady, fg, bg, fun, x, y):
        button = tk.Button(frame, text=text, padx=padx, pady=pady, fg=fg, bg=bg, command= lambda: fun())
        button.place(x=x, y=y)


    @staticmethod
    def _placeEntry(frame, width, x, y):
        entry = tk.Entry(frame, width=width)
        entry.place(x=x, y=y)
        return entry


    @staticmethod
    def _placeListbox(frame, h, w, x, y):
        listbox = tk.Listbox(frame, height=h, width=w, bg=COLOUR_DARK, activestyle='dotbox', font="Helvetica", fg=COLOUR_LIGHT)
        listbox.place(x=x, y=y)
        return listbox


    def _loadImages(self, img_array, image_list):
        selections = self._getSelection()
        img_array.extend(selections)
        file_list = self._getFileNames(img_array)
        self._setListBox(image_list, file_list)


    def _importFolderSystem(self, img_array, image_list):
        folderSystem = self._getDirectory()
        if folderSystem != "":
            list_tag = os.path.basename(folderSystem)
            img_array.append("#FS" + folderSystem)
            print("FS" + folderSystem)
            self._setListBox(image_list, ["Folder System: " + folderSystem])


    def _setOutputLocation(self, image_list):
        self.output_location = self._getDirectory()
        image_list.delete(0,'end')
        self._setListBox(image_list, [self.output_location])


    @staticmethod
    def _getSelection():
        return tk.filedialog.askopenfilenames(parent=root, title='Select Images')


    @staticmethod
    def _getDirectory():
        return tk.filedialog.askdirectory(parent=root, title='Select Folder Location')


    @staticmethod
    def _getSubDirItems(start_location):
        all_images = []
        uncharted_subdirs = []
        uncharted_subdirs.append(start_location)
        #while there is still some folders to check
        while len(uncharted_subdirs) > 0:
            current_location = uncharted_subdirs[0]
            location_items = os.listdir(current_location)
            for item in location_items:
                if "." in item:
                    if item.lower().endswith(('png', 'jpg', 'jpeg')):
                        all_images.append(current_location + "/" + item)
                else:
                    uncharted_subdirs.append(current_location + "/" + item)
            del uncharted_subdirs[0]
        return all_images


    @staticmethod
    def _makeDirectory(full_dir):
        if os.path.exists(full_dir) is False:
             os.makedirs(full_dir)





            
        for pix_row in range(0, container.shape[0], 1):
            for pix_col in range(0, container.shape[1], 2):

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
            
        cv2.imwrite(out_loc + "/" + str(index) + "-" + str(out_name) + ".png", container)
def makeImportFrame(frame, frame_title, img_array, img_list):
    create_lbl = tk.Label(frame, text=frame_title, bg=SECOND_COL, fg=TEXT_COL, font=(TEXT_FONT,11))
    create_lbl.place(x=15, y=10)
    addDir = tk.Button(frame, text="Import Folder System", padx=5, pady=2, fg="white", bg=BUTTON_COL, command= lambda: loadFolderSystem(img_array, img_list))
    addDir.place(x=140, y=5)
    addImages = tk.Button(frame, text="Import Image", padx=5, pady=2, fg="white", bg=BUTTON_COL, command= lambda: loadImages(img_array, img_list))
    addImages.place(x=280, y=5)
    clearImages = tk.Button(frame, text="Clear", padx=15, pady=2, fg="white", bg=BUTTON_COL, command= lambda: clearInput(img_array, img_list))
    clearImages.place(x=395, y=5)


def makeOutputFrame(frame, frame_title, img_list, folder_name, operation):
    info_lbl = tk.Label(frame, text=frame_title, bg=SECOND_COL, fg=TEXT_COL, font=(TEXT_FONT,11))
    info_lbl.place(x=15, y=5)
    addDir = tk.Button(frame, text="Set Output Location", padx=5, pady=2, fg="white", bg=BUTTON_COL, command= lambda: setOutputLocation(img_list))
    addDir.place(x=100, y=5)
    prefix_lbl = tk.Label(frame, text="Folder:", bg=SECOND_COL, fg=TEXT_COL, font=(TEXT_FONT,9))
    prefix_lbl.place(x=235, y=7)
    clearImages = tk.Button(frame, text="PROCESS", padx=10, pady=2, fg="white", bg=BUTTON_COL, command= lambda: operation(folder_name))
    clearImages.place(x=380, y=6)


def makeListbox(frame, h, w):
    return Listbox(frame, height=h, width=w, bg=FIRST_COL, activestyle='dotbox', font="Helvetica", fg=SECOND_COL)


def packInterface():
    global data_frame, host_frame, info_frame
    try:
        container_frame.destroy()
        output_info_frame.destroy()
    except:
        pass
    
    data_frame = tk.Frame(root, bg=SECOND_COL)
    data_frame.place(relwidth=0.95, relheight=0.355, relx=0.025, rely=0.085)
    host_frame = tk.Frame(root, bg=SECOND_COL)
    host_frame.place(relwidth=0.95, relheight=0.355, relx=0.025, rely=0.46)
    info_frame = tk.Frame(root, bg=SECOND_COL)
    info_frame.place(relwidth=0.95, relheight=0.138, relx=0.025, rely=0.84)

    payload_list = makeListbox(data_frame, 5, 40)
    payload_list.place(x=15, y=40)
    makeImportFrame(data_frame, "PAYLOAD", payload, payload_list)

    host_list = makeListbox(host_frame, 5, 40)
    host_list.place(x=15, y=40)
    makeImportFrame(host_frame, "CONTAINERS", hosts, host_list)

    folder_name = tk.Entry(info_frame, width=12)
    folder_name.place(x=280, y=10)
    output_list = makeListbox(info_frame, 1, 40)
    output_list.place(x=15, y=40)
    makeOutputFrame(info_frame, "OUTPUT", output_list, folder_name, packData)


def extractInterface():
    global container_frame, output_info_frame
    try:
        data_frame.destroy()#place_forget()
        host_frame.destroy()#place_forget()
        info_frame.destroy()#place_forget()
    except:
        pass
    
    container_frame = tk.Frame(root, bg=SECOND_COL)
    container_frame.place(relwidth=0.95, relheight=0.355, relx=0.025, rely=0.085)
    output_frame = tk.Frame(root, bg=SECOND_COL)
    output_frame.place(relwidth=0.95, relheight=0.355, relx=0.025, rely=0.46)
    output_info_frame = tk.Frame(root, bg=SECOND_COL)
    output_info_frame.place(relwidth=0.95, relheight=0.138, relx=0.025, rely=0.84)

    container_list = makeListbox(container_frame, 5, 40)
    container_list.place(x=15, y=40)

    makeImportFrame(container_frame, "CONTAINERS", containers, container_list)

    folder_name = tk.Entry(output_info_frame, width=12)
    folder_name.place(x=280, y=10)
    output_list = makeListbox(output_info_frame, 1, 40)
    output_list.place(x=15, y=40)
    makeOutputFrame(output_info_frame, "OUTPUT", output_list, folder_name, extractData)


if __name__ == "__main__":
    root = tk.Tk()
    Application(root)

