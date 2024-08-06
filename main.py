import csv
import tkinter as tk
from main_page import MainPage
from second_page import SecondPage
from threshold import read_threshold

def write_threshold(filename, data_list):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in data_list:
            writer.writerow([item])
class YOLOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Object Detection")
        self.root.geometry("900x600")
        self.names = ['coca-cola zero (can)', 'coca-cola zero (bottle)', 'cactus mineral water', '100 plus', 'sprite', 'pepsi']

        self.can_list = read_threshold('can_threshold.csv')
        self.smallBott_list = read_threshold('small_bottle_threshold.csv')
        self.bott_list = read_threshold('bottle_threshold.csv')

        self.pages = {}
        self.create_pages()
        self.show_frame("main")

    def create_pages(self):
        self.pages["main"] = MainPage(self.root, self)
        self.pages["second"] = SecondPage(self.root, self)

    def show_frame(self, page_name):
        for frame in self.pages.values():
            frame.grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")

    def get_can_list(self):
        return self.can_list

    def get_smallBott_list(self):
        return self.smallBott_list

    def get_bott_list(self):
        return self.bott_list

    def set_can_list(self, new_list):
        self.can_list = new_list

    def set_smallBott_list(self, new_list):
        self.smallBott_list = new_list

    def set_bott_list(self, new_list):
        self.bott_list = new_list

    def save_data(self):
        write_threshold('can_threshold.csv', self.can_list)
        write_threshold('small_bottle_threshold.csv', self.smallBott_list)
        write_threshold('bottle_threshold.csv', self.bott_list)


if __name__ == "__main__":
    root = tk.Tk()
    gui = YOLOGUI(root)
    root.mainloop()







