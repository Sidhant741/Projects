import tkinter as tk
import tkinter.font as font
import pyscreenshot
import cv2
import numpy as np
import tensorflow as tf


class App:
    def __init__(self, window_width, window_height):
        self.model = tf.keras.models.load_model("model.h5")
        self.last_x, self.last_y = None, None
        self.brush = 10
        self.window_width = window_width
        self.window_height = window_height
        self.window = tk.Tk()
        self.window.geometry("{}x{}+300+200".format(self.window_width, self.window_height))
        self.window.resizable(False, False)

        # ********************     Frame_1     ********************
        self.frame_1 = tk.Frame(self.window, bg='red', width=self.window_width, height=self.window_height-100)
        self.frame_1.pack(side="top")

        # Canvas window
        canvas_width = self.window_width
        canvas_height = self.window_height - 100
        self.canvas = tk.Canvas(self.frame_1, width=canvas_width, height=canvas_height)
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.release)

        # ********************     Frame_2     ********************
        self.frame_2 = tk.Frame(self.window, bg='yellow', width=self.window_width, height=100)
        self.frame_2.pack(side="bottom")

        # Predict Button
        self.predict_button = tk.Button(self.frame_2, text="Predict", command=self.predict)
        self.predict_button.place(relx=0.1, y=30, relwidth=0.3)
        self.predict_button['font'] = font.Font(size=12)

        # Clear Button
        self.clear_button = tk.Button(self.frame_2, text="Clear", command=self.clear)
        self.clear_button.place(relx=0.6, y=30, relwidth=0.3)
        self.clear_button['font'] = font.Font(size=12)

    def clear(self):
        self.canvas.delete("all")

    def paint(self, event):
        if self.last_x:
            self.canvas.create_line((self.last_x, self.last_y), (event.x, event.y),
                                    capstyle="round", width=self.brush, smooth=True)
        self.last_x = event.x
        self.last_y = event.y

    def release(self, event):
        self.last_x, self.last_y = None, None

    def predict(self):
        image_prediction = pyscreenshot.grab(bbox=(385, 289, 1134, 668))
        image_prediction = np.array(image_prediction)
        image_gray = cv2.cvtColor(image_prediction, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.bitwise_not(image_gray)
        edges = cv2.Canny(image_gray, 30, 240)
        _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        old_x, old_y, old_w, old_h = 0, 0, 0, 0

        for contour in contours:
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect

            if old_x <= x < old_x + old_w and old_y <= y < old_y + old_h:
                pass
            else:
                cv2.rectangle(image_prediction, (x, y), (x+w, y+h), (0, 0, 255), 3)

                number_image = image_gray[y:y+h, x:x+w]

                processed_image = self.image_preprocesser(number_image)
                result = self.model.predict(processed_image)

                number, percentage = np.argmax(result), round(max(result[0]) * 100, 2)

                text_ = "(" + str(number) + ", " + str(percentage) + ")"

                cv2.putText(image_prediction, text_, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                old_x, old_y, old_w, old_h = x, y, w, h

        cv2.imshow('Prediction Window', image_prediction)

    def image_preprocesser(self, image):
        new_image = np.array(image)

        y, x = new_image.shape
        avg = ((x + y) // 2)

        if x > avg:
            temp_add = (x - avg) // 2
            temp = np.zeros((temp_add, x))
            new_image = np.concatenate((temp, new_image, temp), axis=0)
        elif y > avg:
            temp_add = (y - avg) // 2
            temp = np.zeros((y, temp_add), dtype='uint8')
            new_image = np.concatenate((temp, new_image, temp), axis=1)

        new_image = cv2.resize(new_image, dsize=(28, 28))

        k = np.zeros((28, 5), dtype='uint8')
        k = np.concatenate((k, new_image, k), axis=1)
        z = np.zeros((5, 38), dtype='uint8')

        new_image = np.concatenate((z, k, z))

        new_image = cv2.resize(new_image, (28, 28))

        new_image = new_image / 255.
        new_image = new_image.reshape(1, 28, 28, 1)
        return new_image


app = App(600, 400)
app.window.mainloop()
