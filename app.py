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


    @staticmethod
    def _getFileNames(dirs):
        base_names = []
        for file in dirs:
            base_names.append(os.path.basename(file))
        return base_names


    @staticmethod
    def _setListBox(list_box, image_list):
        list_box.delete(0, 'end')
        for i, img in enumerate(image_list):
            list_box.insert(i, img)


    @staticmethod
    def _clearInput(img_array, image_list):
        img_array.clear()
        image_list.delete(0, 'end')


    def _extractData(self, out_folder):
        print("extract images")
        #add check that output location is given and selections are images, only allow jpg, png, jpeg in window?? or ignore ones not ending in such
        
        out_loc = self.output_location + "/" + out_folder.get()
        self._makeDirectory(out_loc)

        for container in self.containers:
            #use PNG for lossless
            container_name_segs = os.path.basename(container).split(".")[0].split("-")

            out_name = ""
            sub_folders = ""
            if "#" in container_name_segs[1]:
                out_name = container_name_segs[1].split("#")[-1]
                sub_folders = container_name_segs[1].replace("#", "/").replace(out_name, "")[:-1]
                self._makeDirectory(out_loc + sub_folders)
        
            else:
                out_name = container_name_segs[1]
            
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
            cv2.imwrite(out_loc + sub_folders + "/" + str(out_name) + ".png", current_out)


    def _packData(self, out_folder):
        print("pack images")

        #make output location
        out_loc = self.output_location + "/" + out_folder.get()
        self._makeDirectory(out_loc)

        #extract all images from subfolders and all to payload array before main loop starts
        for index, img in enumerate(self.payload):
            if img.startswith("#FS"):
                subItems = self._getSubDirItems(img[3:])
                for item in subItems:
                    self.payload.append("#" + img[3:] + "#" + item)
                del self.payload[index]

        out_name = ""
        
        for index, img_loc in enumerate(self.payload):
            
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

    def _makeImportFrame(self, frame, frame_title, img_array, img_list):
        self._placeLabel(frame, frame_title, COLOUR_LIGHT, COLOUR_TEXT, (TEXT_FONT,11), 15, 10)
        self._placeButton(frame, "Import Folder System", 5, 2, COLOUR_BUTTON_TEXT, COLOUR_BUTTON, lambda: self._importFolderSystem(img_array, img_list), 140, 5)
        self._placeButton(frame, "Import Image", 5, 2, COLOUR_BUTTON_TEXT, COLOUR_BUTTON, lambda: self._loadImages(img_array, img_list), 280, 5)
        self._placeButton(frame, "Clear", 15, 2, COLOUR_BUTTON_TEXT, COLOUR_BUTTON, lambda: self._clearInput(img_array, img_list), 395, 5)




    def _extractInterface(self):
        try:
            self.data_frame.destroy()#place_forget()
            self.host_frame.destroy()#place_forget()
            self.info_frame.destroy()#place_forget()
        except:
            pass

        self.container_frame = self._placeFrame(root, COLOUR_LIGHT, 0.95, 0.355, 0.025, 0.085)
        #self.output_frame = self._placeFrame(root, COLOUR_LIGHT, 0.95, 0.355, 0.025, 0.46)
        self.output_info_frame = self._placeFrame(root, COLOUR_LIGHT, 0.95, 0.138, 0.025, 0.84)

        container_list = self._placeListbox(self.container_frame, 5, 40, 15, 40)
        output_list = self._placeListbox(self.output_info_frame, 1, 40, 15, 40)
        folder_name = self._placeEntry(self.output_info_frame, 12, 280, 10)

        self._makeImportFrame(self.container_frame, "CONTAINERS", self.containers, container_list)
        self._makeOutputFrame(self.output_info_frame, "OUTPUT", output_list, folder_name, self._extractData)


if __name__ == "__main__":
    root = tk.Tk()
    Application(root)

