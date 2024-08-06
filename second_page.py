import tkinter as tk
from tkinter import ttk, messagebox


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.grid(sticky="nsew")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        # self.grid_rowconfigure(1, weight=1)

        # title
        label = tk.Label(self, text="Threshold settings", font=25)
        label.grid(row=0, column=0, columnspan=3, pady=20, padx=10, sticky="n")

        self.entry_widgets = []
        threshold_list = [self.controller.can_list, self.controller.smallBott_list, self.controller.bott_list]
        threshold_name = ["Can Thresholds", "Small Bottle Thresholds", "Bottle Thresholds"]
        # frame for every column
        for i, item_list in enumerate(threshold_list):
            label = tk.Label(self, text=threshold_name[i], font=20)
            label.grid(row=1, column=i, sticky="n")
            label = tk.Label(self, text="Pixel Size", font=18)
            label.grid(row=2, column=i, sticky="n")
            frame = tk.Frame(self, borderwidth=1, relief="solid")
            frame.grid(row=3, column=i, sticky="nsew", padx=10, pady=10)
            frame.grid_columnconfigure(0, weight=1)

            column_entries = []
            # Add content to each column
            for j, item in enumerate(item_list):
                entry_label = tk.Label(frame, text=f"Threshold {j + 1}: (count: {len(item_list) - j+1})", font=18)
                entry_label.grid(row=j * 2, column=0, sticky="w", padx=5, pady=5)

                entry = tk.Entry(frame, font=18)
                entry.insert(0, item)
                entry.grid(row=j * 2 + 1, column=0, sticky="nsew", padx=5, pady=(0, 10))

                column_entries.append(entry)

            self.entry_widgets.append(column_entries)

        # back btn
        back_btn = ttk.Button(self, text="Back to Main Page", command=lambda: self.controller.show_frame("main"))
        back_btn.grid(row=4, column=0, pady=20, padx=10, sticky="ew")

        # save btn
        save_btn = ttk.Button(self, text="Save Changes", command=self.save_changes)
        save_btn.grid(row=4, column=2, pady=20, padx=10, sticky="ew")

        # set min size
        self.controller.root.minsize(width=800, height=600)

        # Make sure the root window uses the grid system properly
        self.controller.root.grid_rowconfigure(0, weight=1)
        self.controller.root.grid_columnconfigure(0, weight=1)

    def save_changes(self):
        # retrieve current list value
        updated_can_list = [entry.get() for entry in self.entry_widgets[0]]
        updated_smallBott_list = [entry.get() for entry in self.entry_widgets[1]]
        updated_bott_list = [entry.get() for entry in self.entry_widgets[2]]

        if not (self.validate_entries(self.entry_widgets[0]) and
                self.validate_entries(self.entry_widgets[1]) and
                self.validate_entries(self.entry_widgets[2])):
            messagebox.showerror("Error", "Threshold values invalid, must be in descending order.")
            self.reset_threshold()
            return

        # update data
        self.controller.set_can_list(updated_can_list)
        self.controller.set_smallBott_list(updated_smallBott_list)
        self.controller.set_bott_list(updated_bott_list)

        # save list data to file
        self.controller.save_data()

    def validate_entries(self, entries):
        try:
            values = [float(entry.get()) for entry in entries if entry.get()]
            # compare value with the next value in the threshold list
            for i in range(len(values) - 1):
                if values[i] < values[i + 1]:
                    return False
            return True
        except ValueError:
            # other case
            return False

    def reset_threshold(self):
        threshold_list = [
            self.controller.can_list,
            self.controller.smallBott_list,
            self.controller.bott_list
        ]
        # reset data
        for i, item_list in enumerate(threshold_list):
            for j, value in enumerate(item_list):
                if j < len(self.entry_widgets[i]):
                    self.entry_widgets[i][j].delete(0, tk.END)
                    self.entry_widgets[i][j].insert(0, value)
