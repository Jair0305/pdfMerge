import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageTk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.open_file_button = tk.Button(self, text="Open File", command=self.open_file, width=20, height=2)
        self.open_file_button.pack()

        self.merge_button = tk.Button(self, text="Merge PDF", command=self.merge_files, width=20, height=2)
        self.merge_button.pack()

        self.file_paths = []
        self.thumbnail_images = []
        self.image_positions = []

        # Canvas for displaying thumbnails
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.drag_data = {"x": 0, "y": 0, "item": None, "index": None}

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

            # Calculate the position based on the number of images
            position_x = 10 + (len(self.thumbnail_images) - 1) * 110
            position_y = 10
            self.image_positions.append((position_x, position_y))

            # Add the image to the canvas at the calculated position
            img_id = self.canvas.create_image(position_x, position_y, anchor="nw", image=photo)

            # Bind events to make the image draggable
            self.canvas.tag_bind(img_id, "<ButtonPress-1>", self.on_start_drag)
            self.canvas.tag_bind(img_id, "<B1-Motion>", self.on_drag)
            self.canvas.tag_bind(img_id, "<ButtonRelease-1>", self.on_stop_drag)

    def on_start_drag(self, event):
        """Save the item and its location when the drag starts."""
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = item
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        # Find the index of the item in the array
        self.drag_data["index"] = self.find_image_index(event.x, event.y)

    def find_image_index(self, x, y):
        """Find the index of the image based on its position."""
        for i, (pos_x, pos_y) in enumerate(self.image_positions):
            if pos_x <= x <= pos_x + 100 and pos_y <= y <= pos_y + 150:  # Assuming image size 100x150
                return i
        return None

    def on_drag(self, event):
        """Handle the dragging of the item."""
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.move(self.drag_data["item"], dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_stop_drag(self, event):
        """Handle the stop of dragging and swap positions if necessary."""
        new_index = self.find_image_index(event.x, event.y)
        if new_index is not None and new_index != self.drag_data["index"]:
            # Swap the positions in the canvas
            self.swap_positions(self.drag_data["index"], new_index)

            # Swap the positions in the array
            self.file_paths[self.drag_data["index"]], self.file_paths[new_index] = (
                self.file_paths[new_index],
                self.file_paths[self.drag_data["index"]],
            )

            self.thumbnail_images[self.drag_data["index"]], self.thumbnail_images[new_index] = (
                self.thumbnail_images[new_index],
                self.thumbnail_images[self.drag_data["index"]],
            )

        # Reset the drag data
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.drag_data["index"] = None

        # Update canvas positions for all images after the swap
        self.update_canvas_positions()

    def swap_positions(self, index1, index2):
        """Swap the positions of two images in the canvas and update their positions."""
        # Swap positions in the list
        self.image_positions[index1], self.image_positions[index2] = (
            self.image_positions[index2],
            self.image_positions[index1],
        )

    def update_canvas_positions(self):
        """Update the positions of all images in the canvas."""
        for i, (x, y) in enumerate(self.image_positions):
            item = self.canvas.find_closest(x + 50, y + 75)[0]
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

window_width = 700
window_height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
myapp = App(root)
myapp.mainloop()
