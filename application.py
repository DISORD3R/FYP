import tkinter as tk
from tkinter import filedialog
import cv2
from ultralytics import YOLO
from PIL import Image, ImageTk, ExifTags
import tkinter.ttk as ttk
import csv

# Load the YOLO model
model = YOLO("runs/detect/train16/weights/best.pt")


class YOLOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Object Detection")
        self.root.geometry("900x600")
        self.names = ['coca-cola zero (can)', 'coca-cola zero (bottle)', 'cactus mineral water', '100 plus', 'sprite',
                      'pepsi']

        # Read threshold data
        def read_threshold(filename):
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                float_values = [float(value) for row in reader for value in row]
                return float_values

        self.can_list = read_threshold('can_threshold.csv')
        self.smallBott_list = read_threshold('small_bottle_threshold.csv')
        self.bott_list = read_threshold('bottle_threshold.csv')

        # Create frames for different pages
        self.pages = {}
        self.create_main_page()
        self.create_second_page()

        # Show the main page initially
        self.show_frame("main")

    def create_main_page(self):
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.pages["main"] = main_frame

        # Create a frame for the image display and center it in the left part
        self.image_frame = tk.Frame(main_frame, width=450, height=600)
        self.image_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        # Create a frame for the buttons (menu) and center it in the right part
        self.menu_frame = tk.Frame(main_frame, width=450, height=600)
        self.menu_frame.grid(row=0, column=1, sticky="nsew", padx=100, pady=50)

        self.label = tk.Label(self.menu_frame, text="Upload an image and detect objects")
        self.label.grid(row=0, column=0, pady=(0, 25))

        self.upload_btn = ttk.Button(self.menu_frame, text="Upload Image", command=self.upload_image)
        self.upload_btn.grid(row=1, column=0, pady=(0, 10))

        self.detect_btn = ttk.Button(self.menu_frame, text="Detect", command=self.detect_objects)
        self.detect_btn.grid(row=2, column=0, pady=(0, 25))

        # Display product counts
        self.count_labels = []
        for i in range(6):
            lbl = tk.Label(self.menu_frame, text=f"{self.names[i]} Count: 0")
            lbl.grid(row=3 + i, column=0, pady=(5, 0), sticky="w")
            self.count_labels.append(lbl)

        # Create a canvas with fixed size for the image
        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image_path = None
        self.result_image = None

        # Button to switch to second page
        self.switch_page_btn = ttk.Button(self.menu_frame, text="Go to Second Page",
                                          command=lambda: self.show_frame("second"))
        self.switch_page_btn.grid(row=10, column=0, pady=(10, 0))

    def create_second_page(self):
        second_frame = tk.Frame(self.root)
        second_frame.grid(row=0, column=0, sticky="nsew")
        self.pages["second"] = second_frame

        # Configure the grid to have 3 columns and 2 rows
        second_frame.grid_columnconfigure(0, weight=1)
        second_frame.grid_columnconfigure(1, weight=1)
        second_frame.grid_columnconfigure(2, weight=1)
        second_frame.grid_rowconfigure(0, weight=1)
        second_frame.grid_rowconfigure(1, weight=1)

        # Add widgets for the second page here
        label = tk.Label(second_frame, text="This is the second page")
        label.grid(row=0, column=0, columnspan=3, pady=20, padx=10, sticky="n")

        # Widgets in the first column
        widget1 = tk.Label(second_frame, text="Column 1 - Item")
        widget1.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        # Widgets in the second column
        widget2 = tk.Label(second_frame, text="Column 2 - Item")
        widget2.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # Widgets in the third column
        widget3 = tk.Label(second_frame, text="Column 3 - Item")
        widget3.grid(row=1, column=2, pady=10, padx=10, sticky="w")

        # Back button spanning across columns
        back_btn = ttk.Button(second_frame, text="Back to Main Page", command=lambda: self.show_frame("main"))
        back_btn.grid(row=2, column=0, columnspan=3, pady=20, padx=10, sticky="n")

        # Optionally, set minimum size for better initial display
        self.root.minsize(width=800, height=600)

    # used to switch pages
    def show_frame(self, page_name):
        for frame in self.pages.values():
            frame.grid_forget()  # Hide all frames
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")  # show seelected frame

    def resize_image(self, image, max_width, max_height):
        # Maintain the aspect ratio when resizing
        width_ratio = max_width / image.width
        height_ratio = max_height / image.height
        new_ratio = min(width_ratio, height_ratio)
        new_width = int(image.width * new_ratio)
        new_height = int(image.height * new_ratio)
        return image.resize((new_width, new_height))

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
        if not self.image_path:
            return

        # Make predictions on the image
        results = model.predict(self.image_path, verbose=False, conf=0.75)

        # Draw bounding boxes
        image = cv2.imread(self.image_path)
        for r in results:
            image = r.plot()

        self.count_product(results)

        # Convert the image to PIL format to perform resizing
        image = Image.fromarray(image[..., ::-1])

        # Resize the image to fit within a maximum size for display (if needed)
        max_width, max_height = 640, 480
        image = self.resize_image(image, max_width, max_height)

        # Update the canvas size and clear it
        self.canvas.config(width=image.width, height=image.height)
        self.canvas.delete("all")

        # Draw the new image on the canvas
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


if __name__ == "__main__":
    root = tk.Tk()
    gui = YOLOGUI(root)
    root.mainloop()
