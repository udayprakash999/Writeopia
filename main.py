import tkinter as tk
from tkinter import filedialog, font, colorchooser, messagebox
from tkinter import scrolledtext
from fpdf import FPDF
import os

class WriteoPia:
    def __init__(self, root):
        self.root = root
        self.root.title("Writeopia")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E3440")

        self.create_widgets()

    def create_widgets(self):
      
        toolbar = tk.Frame(self.root, bg="#4C566A", height=50, relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=5)


        self.font_var = tk.StringVar(value="Arial")
        font_selector = tk.OptionMenu(toolbar, self.font_var, *font.families(), command=self.change_font)
        font_selector.config(bg="#88C0D0", fg="#2E3440", font=("Arial", 10, "bold"), relief=tk.FLAT)
        font_selector.pack(side=tk.LEFT, padx=5, pady=5)


        self.size_var = tk.IntVar(value=12)
        size_selector = tk.Spinbox(toolbar, from_=8, to=72, textvariable=self.size_var, width=5, command=self.change_font,
                                   font=("Arial", 10), bg="#88C0D0", fg="#2E3440", relief=tk.FLAT)
        size_selector.pack(side=tk.LEFT, padx=5, pady=5)


        self.bold_var = tk.BooleanVar(value=False)
        bold_button = tk.Checkbutton(toolbar, text="B", command=self.toggle_bold, variable=self.bold_var, onvalue=True,
                                     offvalue=False, font=("Arial", 10, "bold"), bg="#5E81AC", fg="white", relief=tk.FLAT)
        bold_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.italic_var = tk.BooleanVar(value=False)
        italic_button = tk.Checkbutton(toolbar, text="I", command=self.toggle_italic, variable=self.italic_var, onvalue=True,
                                       offvalue=False, font=("Arial", 10, "italic"), bg="#5E81AC", fg="white", relief=tk.FLAT)
        italic_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.underline_var = tk.BooleanVar(value=False)
        underline_button = tk.Checkbutton(toolbar, text="U", command=self.toggle_underline, variable=self.underline_var, onvalue=True,
                                          offvalue=False, font=("Arial", 10, "underline"), bg="#5E81AC", fg="white", relief=tk.FLAT)
        underline_button.pack(side=tk.LEFT, padx=5, pady=5)


        highlight_button = tk.Button(toolbar, text="Highlight", command=self.highlight_text, bg="#D08770", fg="white",
                                     font=("Arial", 10), relief=tk.FLAT)
        highlight_button.pack(side=tk.LEFT, padx=5, pady=5)


        undo_button = tk.Button(toolbar, text="Undo", command=self.undo_action, bg="#A3BE8C", fg="white",
                                 font=("Arial", 10), relief=tk.FLAT)
        undo_button.pack(side=tk.LEFT, padx=5, pady=5)


        redo_button = tk.Button(toolbar, text="Redo", command=self.redo_action, bg="#A3BE8C", fg="white",
                                 font=("Arial", 10), relief=tk.FLAT)
        redo_button.pack(side=tk.LEFT, padx=5, pady=5)


        print_button = tk.Button(toolbar, text="Print", command=self.print_document, bg="#88C0D0", fg="#2E3440",
                                  font=("Arial", 10), relief=tk.FLAT)
        print_button.pack(side=tk.LEFT, padx=5, pady=5)


        download_button = tk.Button(toolbar, text="Download", command=self.download_file, bg="#B48EAD", fg="white",
                                     font=("Arial", 10), relief=tk.FLAT)
        download_button.pack(side=tk.LEFT, padx=5, pady=5)


        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True, bg="#ECEFF4", fg="#2E3440",
                                                   font=("Arial", 12), relief=tk.FLAT, insertbackground="#2E3440")
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.change_font()


        menu_bar = tk.Menu(self.root, bg="#3B4252", fg="white")
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0, bg="#3B4252", fg="white", activebackground="#808080")
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Download", command=self.download_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def change_font(self, *args):
        font_name = self.font_var.get()
        font_size = self.size_var.get()
        is_bold = "bold" if self.bold_var.get() else "normal"
        self.text_area.configure(font=(font_name, font_size, is_bold))

    def toggle_bold(self):
        self.change_font()

    def toggle_italic(self):
        self.change_font()

    def toggle_underline(self):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if "underline" in current_tags:
                self.text_area.tag_remove("underline", "sel.first", "sel.last")
            else:
                underline_font = font.Font(self.text_area, self.text_area.cget("font"))
                underline_font.configure(underline=True)
                self.text_area.tag_configure("underline", font=underline_font)
                self.text_area.tag_add("underline", "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showinfo("Underline", "Select text to underline.")

    def highlight_text(self):
        color = colorchooser.askcolor(title="Choose Highlight Color")[1]
        if color:
            try:
                self.text_area.tag_configure("highlight", background=color)
                self.text_area.tag_add("highlight", "sel.first", "sel.last")
            except tk.TclError:
                messagebox.showinfo("Highlight", "Select text to highlight.")

    def undo_action(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            messagebox.showinfo("Undo", "Nothing to undo.")

    def redo_action(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            messagebox.showinfo("Redo", "Nothing to redo.")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def download_file(self):
        file_types = [("PDF File", "*.pdf"), ("Text File", "*.txt"), ("Word File", "*.doc")]
        file_path = filedialog.asksaveasfilename(filetypes=file_types)

        if file_path:
            ext = os.path.splitext(file_path)[-1].lower()

            if ext == ".pdf":
                self.save_as_pdf(file_path)
            elif ext == ".txt":
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            elif ext == ".doc":
                self.save_as_doc(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file type.")

    def save_as_pdf(self, file_path):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            content = self.text_area.get(1.0, tk.END).split("\n")
            for line in content:
                pdf.cell(200, 10, txt=line, ln=True, align="L")

            pdf.output(file_path)
            messagebox.showinfo("Success", f"File saved as PDF: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save as PDF: {e}")

    def save_as_doc(self, file_path):
        try:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Success", f"File saved as DOC: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save as DOC: {e}")



    def print_document(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                os.startfile(file_path, "print")
        except Exception as e:
            messagebox.showerror("Print Error", f"An error occurred while printing: {e}")


    

if __name__ == "__main__":
    root = tk.Tk()
    app = WriteoPia(root)
    root.mainloop()
