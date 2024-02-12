from os import close
import cv2 as cv
import PySimpleGUI as sg
import os.path
import csv

selected_image = False
selecting_mode = False
selected_object=False
ix, iy = -1, -1
ref_point = (0,0)
img_name = "0"
selected_video = False
frame_class_selection = False
i = 0

def select(event, x, y, flags, param):
    global ix, iy, selecting_mode, ref_point, selected_object

    if event == cv.EVENT_LBUTTONDOWN:
        selecting_mode = True
        ix, iy = x, y
        cv.circle(resized_img, (ix,iy), 10, (0,0,255),-1)
    elif event == cv.EVENT_LBUTTONUP:
        selecting_mode = False
        cv.circle(resized_img, (x,y), 10, (0,0,255),-1)
        cv.rectangle(resized_img, (ix, iy), (x,y), (0,0,255),2)
        ref_point = (x,y)
        selected_object=True
        cv.imshow('Select an object', resized_img)

def rescaleFrame(frame, scale=0.75):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

def make_win1():
    layout = [
        [sg.Button("Labeling", size=(100,5), enable_events=True)],
        [sg.Button("Object Detection", size=(100,5), enable_events=True)],
        [sg.Button("Exit", size=(100,5))],
    ]
    return sg.Window("Labeling Program", layout, size=(800,300), finalize=True)

def make_win2():
    layout = [
        [
            sg.Text("Image Folder"),
            sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
        [sg.Text("Name:", size=(40,1))],
        [sg.Text(size=(40,1), key="-TOUT-")],
        [sg.Button("Select",size=(10,1), enable_events=True), sg.Button("Back",size=(10,1), enable_events=True)],
    ]
    return sg.Window("Choose Image", layout, finalize=True)

def make_win3():
    layout =[
        [sg.Text("Choose object class:", size=(40,1))],
        [sg.Button("Object Class 1", size=(30,1), enable_events=True)],
        [sg.Button("Object Class 2", size=(30,1), enable_events=True)],
        [sg.Button("Object Class 3", size=(30,1), enable_events=True)],
        [sg.Text("Selected Object Class:", size=(40,1))],
        [sg.Text(size=(40,1), key = "-CLASS-")],
        [sg.Button("Save", size=(10,1), enable_events=True), sg.Button("Back", size=(10,1), enable_events=True)],
    ]
    return sg.Window("Selecting Class Object", layout, location=(1000,500), finalize=True)

s1, d1, j1, s2, d2, j2, s3, d3, j3 = 0, 0, 0, 0, 0, 0, 0, 0, 0
window1, window2, window3 = make_win1(), None, None

while True:
    window, event, values = sg.read_all_windows()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Back":
        window.close()
        if window == window2:
            window2 = None
        elif window == window3:
            window3 = None
            selected_image = False
            cv.destroyWindow("Cropped Object")
    elif event == "Labeling":
        window2 = make_win2()
    elif event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder,f))
            and f.lower().endswith((".jpg", ".png", ".mp4"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(values["-FILE LIST-"][0])
            window["-TOUT-"].update(filename)
        except:
            pass
    elif event == "Select":
        if filename.endswith(".mp4") == True:
            selected_video = True
            capture = cv.VideoCapture("Videos/" + filename)
        else:
            img = cv.imread("Photos/" + filename)
            selected_image=True       
    elif event == "Object Class 1":
        selected_image = False
        img_name = "1"
        window["-CLASS-"].update("Object Class 1")
    elif event == "Object Class 2":
        selected_image = False
        img_name = "2"
        window["-CLASS-"].update("Object Class 2")
    elif event == "Object Class 3":
        selected_image = False
        img_name = "3"
        window["-CLASS-"].update("Object Class 3")
    elif event == "Save":
        if img_name == "0":
            window["-CLASS-"].update("CLASS NOT SELECTED!!!")
        else:
            selected_image = False 
            if img_name == "1":
                with open('Database/object_class_1.csv', mode='a') as annotations:
                    annotation_writer = csv.writer(annotations, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    annotation_writer.writerow([filename, ix, iy, ref_point[0], ref_point[1], 'airplane'])
                if j1<9:
                    j1 = j1 + 1
                    counter = "00" + str(j1)
                elif j1 == 9:
                    j1 = 0
                    d1 = d1 + 1
                    counter = "0" + str(d1) + str(j1)
                if d1 == 9:
                    d1 = 0
                    s1 = s1 + 1
                    counter = str(s1) + str(d1) + str(j1)
            elif img_name == "2":
                with open('Database/object_class_2.csv', mode='a') as annotations:
                    annotation_writer = csv.writer(annotations, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    annotation_writer.writerow([filename, ix, iy, ref_point[0], ref_point[1], 'helicopter'])
                if j2<9:
                    j2 = j2 + 1
                    counter = "00" + str(j2)
                elif j2 == 9:
                    j2 = 0
                    d2 = d2 + 1
                    counter = "0" + str(d2) + str(j2)
                if d2 == 9:
                    d2 = 0
                    s2 = s2 + 1
                    counter = str(s2) + str(d2) + str(j2)
            elif img_name == "3":
                with open('Database/object_class_3.csv', mode='a') as annotations:
                    annotation_writer = csv.writer(annotations, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    annotation_writer.writerow([filename, ix, iy, ref_point[0], ref_point[1], 'kangaroo'])                
                if j3<9:
                    j3 = j3 + 1
                    counter = "00" + str(j3)
                elif j3 == 9:
                    j3 = 0
                    d3 = d3 + 1
                    counter = "0" + str(d3) + str(j3)
                if d3 == 9:
                    d3 = 0
                    s3 = s3 + 1
                    counter = str(s3) + str(d3) + str(j3)
            cv.imwrite("Database/object_class_" + img_name + "_" + counter + ".jpg", cropped_image)
            close_cropped_image = True
            window.close()
            frame_class_selection = False
            if window == window3:
                window3 = None
                cv.destroyWindow('Cropped Object')
    if selected_video == True:
        frame_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
        while i <= frame_count:
            if frame_class_selection == False:
                print ('Frame count:', frame_count)
                print('Position:', int(capture.get(cv.CAP_PROP_POS_FRAMES)))
                _, frame = capture.read()
                resized_img = rescaleFrame(frame, scale=.5)
                cv.imshow('Select an object', resized_img)
                cv.setMouseCallback('Select an object', select)
                cv.waitKey(0)
                cropped_image = resized_img[iy:ref_point[1], ix:ref_point[0]]
                cv.imshow('Cropped Object', cropped_image)
                window3 = make_win3()
                frame_class_selection = True 
            if event == sg.WIN_CLOSED:
                i = frame_count + 1
            i = i + 1
        capture.release()
    if selected_image == True:
        resized_img = rescaleFrame(img, scale=1)
        cv.imshow('Select an object', resized_img)
        cv.setMouseCallback('Select an object', select)
        cv.waitKey(0)
        cv.destroyWindow('Select an object')
        cropped_image = resized_img[iy:ref_point[1], ix:ref_point[0]]
        cv.imshow('Cropped Object', cropped_image)
        window3 = make_win3()
window.close()