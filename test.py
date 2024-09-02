import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageTk


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self.open_file_button = tk.Button(self, text="Open File", command=self.open_file, width=20, height=2)
        self.open_file_button.pack()

        self.merge_button = tk.Button(self, text="Merge PDF", command=self.merge_files, width=20, height=2)
        self.merge_button.pack()

        self.file_paths = []
        self.thumbnail_images = []
        self.image_items = []

        # Canvas for displaying thumbnails
        self.canvas = tk.Canvas(self, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.drag_data = {"x": 0, "y": 0, "item": None, "index": None}

        # Grid layout
        self.rows = 2
        self.cols = 5
        self.cell_width = 110
        self.cell_height = 160

    def open_file(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if file_paths:
            self.file_paths.extend(file_paths)
            print(f'Files selected: {self.file_paths}')
            for file_path in file_paths:
                self.show_first_page(file_path)

    def show_first_page(self, file_path):
        images = convert_from_path(file_path, last_page=1)
        if images:
            image = images[0]
            image.thumbnail((100, 150))  # Resize image to a smaller size for display
            photo = ImageTk.PhotoImage(image)

            # Store reference to avoid garbage collection
            self.thumbnail_images.append(photo)

            # Calculate the position based on the grid layout
            index = len(self.thumbnail_images) - 1
            row = index // self.cols
            col = index % self.cols
            x = col * self.cell_width + 5
            y = row * self.cell_height + 5

            # Add the image to the canvas at the calculated position
            img_id = self.canvas.create_image(x, y, anchor="nw", image=photo)
            self.image_items.append(img_id)

            # Bind events to make the image draggable
            self.canvas.tag_bind(img_id, "<ButtonPress-1>", self.on_start_drag)
            self.canvas.tag_bind(img_id, "<B1-Motion>", self.on_drag)
            self.canvas.tag_bind(img_id, "<ButtonRelease-1>", self.on_stop_drag)

    def on_start_drag(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = item
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["index"] = self.image_items.index(item)

    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        # Update positions in real-time
        self.update_positions_realtime()

    def update_positions_realtime(self):
        dragged_index = self.drag_data["index"]
        dragged_coords = self.canvas.coords(self.drag_data["item"])

        for i, item in enumerate(self.image_items):
            if i != dragged_index:
                x, y = self.get_grid_position(i if i < dragged_index else i - 1)
                self.canvas.coords(item, x, y)

    def on_stop_drag(self, event):
        dragged_item = self.drag_data["item"]
        old_index = self.drag_data["index"]
        new_index = self.get_drop_index(event.x, event.y)

        if new_index is not None and new_index != old_index:
            # Update data structures
            self.file_paths.insert(new_index, self.file_paths.pop(old_index))
            self.thumbnail_images.insert(new_index, self.thumbnail_images.pop(old_index))
            self.image_items.insert(new_index, self.image_items.pop(old_index))

        # Reset positions
        self.update_all_positions()

        # Reset drag data
        self.drag_data = {"x": 0, "y": 0, "item": None, "index": None}

    def get_drop_index(self, x, y):
        row = int(y // self.cell_height)
        col = int(x // self.cell_width)
        index = row * self.cols + col
        return min(index, len(self.image_items) - 1)

    def get_grid_position(self, index):
        row = index // self.cols
        col = index % self.cols
        return col * self.cell_width + 5, row * self.cell_height + 5

    def update_all_positions(self):
        for i, item in enumerate(self.image_items):
            x, y = self.get_grid_position(i)
            self.canvas.coords(item, x, y)

    def merge_files(self):
        if self.file_paths:
            self.merge_pdf(self.file_paths)
        else:
            print('No files selected')

    def merge_pdf(self, file_paths):
        merger = PdfWriter()
        for file_path in file_paths:
            reader = PdfReader(file_path)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                merger.add_page(page)
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf")
        if output_file:
            with open(output_file, "wb") as output_file:
                merger.write(output_file)
                print(f'The files: {file_paths} were merged into {output_file} as {output_file.name}')
        merger.close()


root = tk.Tk()

window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
myapp = App(root)
myapp.mainloop()