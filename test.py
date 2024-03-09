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

    def open_file(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if file_paths:
            for file_path in file_paths:
                self.file_paths.append(file_path)
                #self.show_first_page(file_path)
            print(f'Files selected: {self.file_paths}')

    def show_first_page(self, file_path):
        images = convert_from_path(file_path, last_page=1)
        if images:
            image = ImageTk.PhotoImage(images[0])

            image.label = tk.Label(self, image=image)
            image.label.image = image
            image.label.pack()

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
                print(f'The files: {file_paths} were merged intro {output_file} as {output_file.name}')
        merger.close()

root = tk.Tk()

#Establecer el tamaño de la ventana
window_width = 700
window_height = 400
#Obtener el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Ubicar la ventana en el centro de la pantalla
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
myapp = App(root)
myapp.mainloop()
