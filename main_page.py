import csv
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ExifTags
import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("runs/detect/train16/weights/best.pt")

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.model = YOLO("runs/detect/train16/weights/best.pt")
        self.names = ['coca-cola zero (can)', 'coca-cola zero (bottle)', 'cactus mineral water', '100 plus', 'sprite',
                      'pepsi']
        self.create_widgets()

    def create_widgets(self):
        # Image frame
        self.image_frame = tk.Frame(self, width=450, height=600)
        self.image_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.image_frame.grid_propagate(False)  # Prevent the frame from resizing

        # Menu frame
        self.menu_frame = tk.Frame(self, width=450, height=600)
        self.menu_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.menu_frame.grid_propagate(False)  # Prevent the frame from resizing

        # Title label in menu frame
        self.label = tk.Label(self.menu_frame, text="Upload an image and detect objects", font=20)
        self.label.grid(row=0, column=0, pady=(0, 25))

        # Upload button
        self.upload_btn = ttk.Button(self.menu_frame, text="Upload Image", command=self.upload_image)
        self.upload_btn.grid(row=1, column=0, pady=(0, 10))

        # Slider for confidence score threshold
        self.slider = tk.Scale(
            self.menu_frame, from_=0, to=100, orient="horizontal", length=300,
            command=self.on_slider_change
        )
        self.slider.set(75)  # Set initial value
        self.slider.grid(row=2, column=0, pady=10)

        # Label to display slider value
        self.value_label = tk.Label(self.menu_frame, text="Current confidence score threshold: 0.75", font=18)
        self.value_label.grid(row=3, column=0, pady=10)

        # Detect button
        self.detect_btn = ttk.Button(self.menu_frame, text="Detect", command=self.detect_objects)
        self.detect_btn.grid(row=4, column=0, pady=(0, 25))

        # Labels for counts
        self.count_labels = []
        for i in range(6):
            lbl = tk.Label(self.menu_frame, text=f"{self.names[i]} Count: 0", font=20)
            lbl.grid(row=5 + i, column=0, pady=(5, 0), sticky="w")
            self.count_labels.append(lbl)

        # Canvas for displaying image
        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Button to switch pages
        self.switch_page_btn = ttk.Button(self.menu_frame, text="Go to Second Page",
                                          command=lambda: self.controller.show_frame("second"))
        self.switch_page_btn.grid(row=11, column=0, pady=(10, 0))

        # Set weights for grid cells
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_frame.grid_columnconfigure(0, weight=1)
        for i in range(12):
            self.menu_frame.grid_rowconfigure(i, weight=1)

        # Variables to hold image paths and processed images
        self.image_path = None
        self.result_image = None

    def on_slider_change(self, value):
        self.value_label.config(text=f"Current confidence score threshold: {float(value)/100}")

    def upload_image(self):
        # Open a file dialog to select an image
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            # Display the uploaded image on the canvas
            image = Image.open(self.image_path)

            # Correct orientation based on EXIF data
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):  # In case there is no EXIF data
                pass

            image = self.resize_image(image, 640, 480)
            self.result_image = ImageTk.PhotoImage(image)

            # Update the canvas size and clear it
            self.canvas.config(width=image.width, height=image.height)
            self.canvas.delete("all")

            # Draw the image on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.result_image)

    def detect_objects(self):
        self.can_list = self.read_threshold('can_threshold.csv')
        self.smallBott_list = self.read_threshold('small_bottle_threshold.csv')
        self.bott_list = self.read_threshold('bottle_threshold.csv')
        confidenceScore = self.slider.get()/100

        if not self.image_path:
            return

        # make predictions on the image
        results = model.predict(self.image_path, verbose=False, conf=confidenceScore)

        # draw bounding box
        image = cv2.imread(self.image_path)
        for r in results:
            image = r.plot()

        self.count_product(results)

        # convert the image to PIL format to resize
        image = Image.fromarray(image[..., ::-1])

        # resize to fit into the window
        max_width, max_height = 640, 480
        image = self.resize_image(image, max_width, max_height)

        # update canva size
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.delete("all")

        # draw the result image on canva
        self.result_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.result_image)

    def count_product(self, results):
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        countList = [0, 0, 0, 0, 0, 0]
        for i in range(len(boxes)):
            x1, y1, x2, y2 = boxes[i]
            width = x2 - x1
            height = y2 - y1
            class_index = int(classes[i])
            class_name = names[class_index]
            confidence = confidences[i]
            # When the detected is under can category
            if class_index in [0, 3, 4, 5]:
                if height > self.can_list[0]:
                    countList[class_index] += 6
                elif height > self.can_list[1]:
                    countList[class_index] += 5
                elif height > self.can_list[2]:
                    countList[class_index] += 4
                elif height > self.can_list[3]:
                    countList[class_index] += 3
                elif height > self.can_list[4]:
                    countList[class_index] += 2
                else:
                    countList[class_index] += 1
            # When under bottle category
            elif class_index == 2:
                if height > self.bott_list[0]:
                    countList[class_index] += 5
                elif height > self.bott_list[1]:
                    countList[class_index] += 4
                elif height > self.bott_list[2]:
                    countList[class_index] += 3
                elif height > self.bott_list[3]:
                    countList[class_index] += 2
                else:
                    countList[class_index] += 1
            # When under small bottle category
            elif class_index == 1:
                if height > self.smallBott_list[0]:
                    countList[class_index] += 6
                elif height > self.smallBott_list[1]:
                    countList[class_index] += 5
                elif height > self.smallBott_list[2]:
                    countList[class_index] += 4
                elif height > self.smallBott_list[3]:
                    countList[class_index] += 3
                elif height > self.smallBott_list[2]:
                    countList[class_index] += 2
                else:
                    countList[class_index] += 1

        # Update the count labels
        for i, count in enumerate(countList):
            self.count_labels[i].config(text=f" {self.names[i]} Count: {count}")

    def resize_image(self, image, max_width, max_height):
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        new_ratio = min(width_ratio, height_ratio)
        new_width = int(image.width * new_ratio)
        new_height = int(image.height * new_ratio)
        return image.resize((new_width, new_height))

    def read_threshold(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            float_values = [float(value) for row in reader for value in row]
            return float_values