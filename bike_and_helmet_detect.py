import cv2
import tkinter as tk
from PIL import ImageTk, Image


# cascade_src = "haarcascade_helmet.xml"
cascade_src = (
    "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test6_helmet\\bike.xml"
)
helmet_src = (
    "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test6_helmet\\cascade.xml"
)
# cascade_src = "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test6_helmet\\haarcascade_helmet.xml"

# video_src = 'movie2.mp4'
# video_src = "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test6_helmet\\bikes.mp4"
video_src = (
    "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test9_all_required\\bikes.mp4"
)

# video_src = 'T2_Trim.mp4'
# video_src= 'highway.mp4'

cap = cv2.VideoCapture(video_src)
fgbg = cv2.createBackgroundSubtractorMOG2()
motorcycle_cascade = cv2.CascadeClassifier(cascade_src)
helmet_cascade = cv2.CascadeClassifier(helmet_src)

# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")

# Graphics window
imageFrame = tk.Frame(window, width=1024, height=576)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)


def helmet(img):
    helmet = helmet_cascade.detectMultiScale(img, 1.25, 1)  #######1.25
    return helmet


i = 1


def show_frame():
    _, frame = cap.read()
    # resizing frame to improve
    frame = cv2.resize(frame, (1024, 576))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    global i

    motorcycles = motorcycle_cascade.detectMultiScale(gray, 1.59, 1)

    for (x, y, w, h) in motorcycles:

        crop_img = gray[y : y + h, x : x + w]
        # i += 1
        # rand_name = str(i)
        # name = (
        #     "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test6_helmet\\pics\\"
        #     + str(rand_name)
        #     + ".jpg"
        # )
        # print("Creating..." + name)
        # cv2.imwrite(name, crop_img)
        ################before 22-05-2021
        # height = crop_img.shape[0]
        # width = crop_img.shape[1]

        # height = int(height * 0.5)
        # crop_img = crop_img[0:height, 0:width]
        ################################
        new_helmet = helmet(crop_img)
        if new_helmet is not None:
            # cv2.rectangle(
            # frame, (x + 10, y + 20), (x + w - 10, y + h - 50), (0, 255, 0), 2
            # )
            for (xx, yy, ww, hh) in new_helmet:
                cv2.rectangle(
                    frame, (x + xx, y + yy), (x + xx + ww, y + yy + hh), (0, 255, 0), 2
                )
                cv2.putText(
                    frame,
                    "Helmet",
                    (x + xx, y + yy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
        else:
            cv2.rectangle(
                frame, (x + 10, y + 10), (x + w - 10, y + w - 10), (0, 0, 255), 2
            )

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 215), 2)
        cv2.putText(
            frame, "bike", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
        )

    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(color)

    i += 1
    rand_name = str(i)
    name = (
        "C:\\Users\\Angkon\\personal_works\\THE_FINAL_WORK\\test9_all_required\\Total_detection2\\bikes\\"
        + str(rand_name)
        + ".jpg"
    )
    print("Creating..." + name)
    cv2.imwrite(
        name,
        frame,
    )

    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


# Slider window (slider controls stage position)
# sliderFrame = tk.Frame(window, width=600, height=100)
# sliderFrame.grid(row=600, column=0, padx=10, pady=2)


show_frame()  # Display 2
window.mainloop()  # Starts GUI

cv2.destroyAllWindows()
