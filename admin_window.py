import tkinter as tk
from tkinter import ttk, messagebox
import logging

class AdminWindow(tk.Toplevel):  
    def __init__(self, root, db):
        super().__init__(root)
        self.root = root
        self.title("Admin Control Panel")
        self.geometry("1000x700")
        self.db = db
        
        # Define color theme
        self.COLOR_THEME = {
            'background': '#f0f0f0',
            'text': '#333333',
            'button_bg': '#4a7a8c',
            'button_fg': '#ffffff',
            'button_active': '#3a6a7c',
            'button_pressed': '#2a5a6c',
            'field_bg': '#ffffff',
            'header_bg': '#3a6a7c',
            'header_fg': '#ffffff',
            'selected_bg': '#d4e6f1'
        }
        
        self.configure(bg=self.COLOR_THEME['background'])
        self.style = ttk.Style()
        self._configure_styles()
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.create_ui()
        self.load_questions()

    def _configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('.', 
                           background=self.COLOR_THEME['background'],
                           foreground=self.COLOR_THEME['text'])
        
        # Frame style
        self.style.configure('Custom.TFrame', 
                           background=self.COLOR_THEME['background'],
                           borderwidth=2,
                           relief='groove')
        
        # Label style
        self.style.configure('Custom.TLabel',
                           background=self.COLOR_THEME['background'],
                           foreground=self.COLOR_THEME['text'],
                           font=('Helvetica', 10, 'bold'))
        
        # Button style
        self.style.configure('Custom.TButton',
                           background=self.COLOR_THEME['button_bg'],
                           foreground=self.COLOR_THEME['button_fg'],
                           font=('Helvetica', 9),
                           borderwidth=1)
        self.style.map('Custom.TButton',
                     background=[('active', self.COLOR_THEME['button_active']),
                                ('pressed', self.COLOR_THEME['button_pressed'])])
        
        # Combobox style
        self.style.configure('Custom.TCombobox',
                           fieldbackground=self.COLOR_THEME['field_bg'],
                           background=self.COLOR_THEME['button_bg'],
                           foreground=self.COLOR_THEME['text'])
        
        # Treeview style
        self.style.configure('Custom.Treeview',
                           background=self.COLOR_THEME['field_bg'],
                           foreground=self.COLOR_THEME['text'],
                           fieldbackground=self.COLOR_THEME['field_bg'],
                           rowheight=25)
        self.style.configure('Custom.Treeview.Heading',
                          background=self.COLOR_THEME['header_bg'],
                          foreground=self.COLOR_THEME['header_fg'],
                          font=('Helvetica', 9, 'bold'))
        self.style.map('Custom.Treeview',
                     background=[('selected', self.COLOR_THEME['selected_bg'])])
        
        # Scrollbar style
        self.style.configure('Custom.Vertical.TScrollbar',
                           background=self.COLOR_THEME['button_bg'])
        self.style.configure('Custom.Horizontal.TScrollbar',
                           background=self.COLOR_THEME['button_bg'])

    def create_ui(self):
        # Main container frame
        main_frame = ttk.Frame(self, style='Custom.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # --- Header Section ---
        header_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title label
        title_label = ttk.Label(header_frame, 
                              text="Quiz Administration Panel",
                              style='Custom.TLabel',
                              font=('Helvetica', 14, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Back button
        self.back_button = ttk.Button(header_frame, 
                                    text="← Back to Main",
                                    style='Custom.TButton',
                                    command=self._go_back_to_main)
        self.back_button.pack(side=tk.RIGHT)
        
        # --- Language Selection ---
        lang_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        lang_frame.pack(fill=tk.X, pady=5)
        
        self.language_label = ttk.Label(lang_frame, 
                                      text="Select Language:",
                                      style='Custom.TLabel')
        self.language_label.pack(side=tk.LEFT, padx=5)
        
        self.language_combobox = ttk.Combobox(lang_frame, 
                                            style='Custom.TCombobox',
                                            values=self.db.fetch_languages())
        self.language_combobox.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.language_combobox.bind("<<ComboboxSelected>>", self.load_questions)
        
        # --- Question List ---
        tree_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, style='Custom.Vertical.TScrollbar')
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = ttk.Scrollbar(tree_frame, 
                                    orient=tk.HORIZONTAL,
                                    style='Custom.Horizontal.TScrollbar')
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.question_tree = ttk.Treeview(tree_frame,
                                        style='Custom.Treeview',
                                        columns=("ID", "Question", "Option 1", "Option 2", "Option 3", "Option 4", "Correct Answer"),
                                        show="headings",
                                        yscrollcommand=tree_scroll_y.set,
                                        xscrollcommand=tree_scroll_x.set)
        self.question_tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y.config(command=self.question_tree.yview)
        tree_scroll_x.config(command=self.question_tree.xview)
        
        # Configure column headings and widths
        columns = {
            "ID": {"width": 50, "anchor": tk.CENTER},
            "Question": {"width": 250, "anchor": tk.W},
            "Option 1": {"width": 120, "anchor": tk.W},
            "Option 2": {"width": 120, "anchor": tk.W},
            "Option 3": {"width": 120, "anchor": tk.W},
            "Option 4": {"width": 120, "anchor": tk.W},
            "Correct Answer": {"width": 100, "anchor": tk.CENTER}
        }
        
        for col, settings in columns.items():
            self.question_tree.heading(col, text=col)
            self.question_tree.column(col, **settings)
        
        # --- CRUD Buttons ---
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.create_button = ttk.Button(button_frame, 
                                      text="Create New Question",
                                      style='Custom.TButton',
                                      command=self.create_question)
        self.create_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.update_button = ttk.Button(button_frame, 
                                      text="Update Selected",
                                      style='Custom.TButton',
                                      command=self.update_question)
        self.update_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.delete_button = ttk.Button(button_frame, 
                                      text="Delete Selected",
                                      style='Custom.TButton',
                                      command=self.delete_question)
        self.delete_button.pack(side=tk.LEFT, padx=5, expand=True)

    def load_questions(self, event=None):
        selected_language = self.language_combobox.get()
        if selected_language:
            questions = self.db.fetch_all_questions(selected_language)
            # Clear existing data
            for item in self.question_tree.get_children():
                self.question_tree.delete(item)
            # Insert new data
            for q in questions:
                self.question_tree.insert("", tk.END, values=(q['id'], q['question'], *q['options'], q['correct_answer']))

    def create_question(self):
        selected_language = self.language_combobox.get()
        if not selected_language:
            messagebox.showerror("Error", "Please select a language.")
            return
        CreateQuestionDialog(self, self.db, selected_language, self.load_questions, self.COLOR_THEME)

    def update_question(self):
        selected_language = self.language_combobox.get()
        if not selected_language:
            messagebox.showerror("Error", "Please select a language.")
            return
        selected_item = self.question_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a question to update.")
            return
        question_id = self.question_tree.item(selected_item, 'values')[0]
        question_data = {
            "question": self.question_tree.item(selected_item, 'values')[1],
            "option1": self.question_tree.item(selected_item, 'values')[2],
            "option2": self.question_tree.item(selected_item, 'values')[3],
            "option3": self.question_tree.item(selected_item, 'values')[4],
            "option4": self.question_tree.item(selected_item, 'values')[5],
            "correct_answer": self.question_tree.item(selected_item, 'values')[6],
        }
        UpdateQuestionDialog(self, self.db, selected_language, question_id, self.load_questions, question_data, self.COLOR_THEME)

    def delete_question(self):
        selected_language = self.language_combobox.get()
        if not selected_language:
            messagebox.showerror("Error", "Please select a language.")
            return
        selected_item = self.question_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a question to delete.")
            return
        question_id = self.question_tree.item(selected_item, 'values')[0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?"):
            self.db.delete_question(selected_language, question_id)
            self.load_questions()

    def _go_back_to_main(self):
        logging.info("Closing Admin Panel and going back to Main Screen")
        self.destroy()
        if self.root.winfo_exists():
            self.root.deiconify() # Show the main window if it exists

    def _on_closing(self):
        logging.info("Admin Panel closing")
        self.destroy()
        if self.root.winfo_exists():
            self.root.deiconify()


class CreateQuestionDialog(tk.Toplevel):
    def __init__(self, parent, db, language, callback, color_theme):
        super().__init__(parent)
        self.title("Create New Question")
        self.geometry("500x500")
        self.COLOR_THEME = color_theme
        self.configure(bg=self.COLOR_THEME['background'])
        self.db = db
        self.language = language
        self.callback = callback
        self._configure_styles()
        self.create_ui()
        
    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('Dialog.TFrame', background=self.COLOR_THEME['background'])
        self.style.configure('Dialog.TLabel', 
                           background=self.COLOR_THEME['background'],
                           foreground=self.COLOR_THEME['text'],
                           font=('Helvetica', 9))
        self.style.configure('Dialog.TButton',
                           background=self.COLOR_THEME['button_bg'],
                           foreground=self.COLOR_THEME['button_fg'],
                           font=('Helvetica', 9))
        self.style.configure('Dialog.TEntry',
                           fieldbackground=self.COLOR_THEME['field_bg'],
                           foreground=self.COLOR_THEME['text'])
        self.style.configure('Dialog.TText',
                           background=self.COLOR_THEME['field_bg'],
                           foreground=self.COLOR_THEME['text'])

    def create_ui(self):
        main_frame = ttk.Frame(self, style='Dialog.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Create New Question",
                               style='Dialog.TLabel',
                               font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Question Entry
        question_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        question_frame.pack(fill=tk.X, pady=5)
        
        self.question_label = ttk.Label(question_frame, 
                                      text="Question Text:",
                                      style='Dialog.TLabel')
        self.question_label.pack(anchor=tk.W)
        
        self.question_entry = tk.Text(question_frame, 
                                    height=4, 
                                    width=50,
                                    bg=self.COLOR_THEME['field_bg'],
                                    fg=self.COLOR_THEME['text'],
                                    insertbackground=self.COLOR_THEME['text'],
                                    relief=tk.SOLID,
                                    borderwidth=1)
        self.question_entry.pack(fill=tk.X, pady=5)
        
        # Options Frame
        options_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        options_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Option 1
        option1_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option1_frame.pack(fill=tk.X, pady=2)
        self.option1_label = ttk.Label(option1_frame, 
                                      text="Option 1:",
                                      style='Dialog.TLabel')
        self.option1_label.pack(side=tk.LEFT, padx=5)
        self.option1_entry = ttk.Entry(option1_frame, style='Dialog.TEntry')
        self.option1_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Option 2
        option2_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option2_frame.pack(fill=tk.X, pady=2)
        self.option2_label = ttk.Label(option2_frame, 
                                      text="Option 2:",
                                      style='Dialog.TLabel')
        self.option2_label.pack(side=tk.LEFT, padx=5)
        self.option2_entry = ttk.Entry(option2_frame, style='Dialog.TEntry')
        self.option2_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Option 3
        option3_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option3_frame.pack(fill=tk.X, pady=2)
        self.option3_label = ttk.Label(option3_frame, 
                                      text="Option 3:",
                                      style='Dialog.TLabel')
        self.option3_label.pack(side=tk.LEFT, padx=5)
        self.option3_entry = ttk.Entry(option3_frame, style='Dialog.TEntry')
        self.option3_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Option 4
        option4_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option4_frame.pack(fill=tk.X, pady=2)
        self.option4_label = ttk.Label(option4_frame, 
                                      text="Option 4:",
                                      style='Dialog.TLabel')
        self.option4_label.pack(side=tk.LEFT, padx=5)
        self.option4_entry = ttk.Entry(option4_frame, style='Dialog.TEntry')
        self.option4_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Correct Answer
        answer_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        answer_frame.pack(fill=tk.X, pady=10)
        
        self.correct_answer_label = ttk.Label(answer_frame, 
                                            text="Correct Answer:",
                                            style='Dialog.TLabel')
        self.correct_answer_label.pack(side=tk.LEFT, padx=5)
        
        self.correct_answer_entry = ttk.Entry(answer_frame, style='Dialog.TEntry')
        self.correct_answer_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.cancel_button = ttk.Button(button_frame, 
                                      text="Cancel",
                                      style='Dialog.TButton',
                                      command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.save_button = ttk.Button(button_frame, 
                                    text="Save Question",
                                    style='Dialog.TButton',
                                    command=self.save_question)
        self.save_button.pack(side=tk.LEFT, padx=5, expand=True)

    def save_question(self):
        question = self.question_entry.get("1.0", tk.END).strip()
        options = [
            self.option1_entry.get().strip(),
            self.option2_entry.get().strip(),
            self.option3_entry.get().strip(),
            self.option4_entry.get().strip()
        ]
        correct_answer = self.correct_answer_entry.get().strip()

        if not question or not all(options) or not correct_answer:
            messagebox.showerror("Error", "All fields are required.")
            return

        if correct_answer not in options:
            messagebox.showerror("Error", "Correct answer must match one of the options.")
            return

        question_data = {
            "question": question,
            "option1": options[0],
            "option2": options[1],
            "option3": options[2],
            "option4": options[3],
            "correct_answer": correct_answer
        }

        try:
            if self.db.add_new_question(self.language, question_data):
                self.callback() 
                self.destroy()
                messagebox.showinfo("Success", "Question created successfully!")
            else:
                messagebox.showerror("Error", "Failed to create question.")
        except Exception as e:
            logging.error(f"Error creating question: {e}")
            messagebox.showerror("Error", f"Failed to create question: {e}")


class UpdateQuestionDialog(tk.Toplevel):
    def __init__(self, parent, db, language, question_id, callback, question_data, color_theme):
        super().__init__(parent)
        self.title("Update Question")
        self.geometry("500x500")
        self.COLOR_THEME = color_theme
        self.configure(bg=self.COLOR_THEME['background'])
        self.db = db
        self.language = language
        self.question_id = question_id
        self.callback = callback
        self.question_data = question_data
        self._configure_styles()
        self.create_ui()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.configure('Dialog.TFrame', background=self.COLOR_THEME['background'])
        self.style.configure('Dialog.TLabel', 
                           background=self.COLOR_THEME['background'],
                           foreground=self.COLOR_THEME['text'],
                           font=('Helvetica', 9))
        self.style.configure('Dialog.TButton',
                           background=self.COLOR_THEME['button_bg'],
                           foreground=self.COLOR_THEME['button_fg'],
                           font=('Helvetica', 9))
        self.style.configure('Dialog.TEntry',
                           fieldbackground=self.COLOR_THEME['field_bg'],
                           foreground=self.COLOR_THEME['text'])
        self.style.configure('Dialog.TText',
                           background=self.COLOR_THEME['field_bg'],
                           foreground=self.COLOR_THEME['text'])

    def create_ui(self):
        main_frame = ttk.Frame(self, style='Dialog.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Update Question",
                               style='Dialog.TLabel',
                               font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Question Entry
        question_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        question_frame.pack(fill=tk.X, pady=5)
        
        self.question_label = ttk.Label(question_frame, 
                                      text="Question Text:",
                                      style='Dialog.TLabel')
        self.question_label.pack(anchor=tk.W)
        
        self.question_entry = tk.Text(question_frame, 
                                    height=4, 
                                    width=50,
                                    bg=self.COLOR_THEME['field_bg'],
                                    fg=self.COLOR_THEME['text'],
                                    insertbackground=self.COLOR_THEME['text'],
                                    relief=tk.SOLID,
                                    borderwidth=1)
        self.question_entry.insert("1.0", self.question_data['question'])
        self.question_entry.pack(fill=tk.X, pady=5)
        
        # Options Frame
        options_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        options_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Option 1
        option1_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option1_frame.pack(fill=tk.X, pady=2)
        self.option1_label = ttk.Label(option1_frame, 
                                      text="Option 1:",
                                      style='Dialog.TLabel')
        self.option1_label.pack(side=tk.LEFT, padx=5)
        self.option1_entry = ttk.Entry(option1_frame, style='Dialog.TEntry')
        self.option1_entry.insert(0, self.question_data['option1'])
        self.option1_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Option 2
        option2_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option2_frame.pack(fill=tk.X, pady=2)
        self.option2_label = ttk.Label(option2_frame, 
                                      text="Option 2:",
                                      style='Dialog.TLabel')
        self.option2_label.pack(side=tk.LEFT, padx=5)
        self.option2_entry = ttk.Entry(option2_frame, style='Dialog.TEntry')
        self.option2_entry.insert(0, self.question_data['option2'])
        self.option2_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Option 3
        option3_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option3_frame.pack(fill=tk.X, pady=2)
        self.option3_label = ttk.Label(option3_frame, 
                                      text="Option 3:",
                                      style='Dialog.TLabel')
        self.option3_label.pack(side=tk.LEFT, padx=5)
        self.option3_entry = ttk.Entry(option3_frame, style='Dialog.TEntry')
        self.option3_entry.insert(0, self.question_data['option3'])
        self.option3_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Option 4
        option4_frame = ttk.Frame(options_frame, style='Dialog.TFrame')
        option4_frame.pack(fill=tk.X, pady=2)
        self.option4_label = ttk.Label(option4_frame, 
                                      text="Option 4:",
                                      style='Dialog.TLabel')
        self.option4_label.pack(side=tk.LEFT, padx=5)
        self.option4_entry = ttk.Entry(option4_frame, style='Dialog.TEntry')
        self.option4_entry.insert(0, self.question_data['option4'])
        self.option4_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Correct Answer
        answer_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        answer_frame.pack(fill=tk.X, pady=10)
        
        self.correct_answer_label = ttk.Label(answer_frame, 
                                            text="Correct Answer:",
                                            style='Dialog.TLabel')
        self.correct_answer_label.pack(side=tk.LEFT, padx=5)
        
        self.correct_answer_entry = ttk.Entry(answer_frame, style='Dialog.TEntry')
        self.correct_answer_entry.insert(0, self.question_data['correct_answer'])
        self.correct_answer_entry.pack(fill=tk.X, expand=True, padx=5)
        
        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Dialog.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.cancel_button = ttk.Button(button_frame, 
                                      text="Cancel",
                                      style='Dialog.TButton',
                                      command=self.destroy)
        self.cancel_button.pack(side=tk.LEFT, padx=5, expand=True)
        
        self.update_button = ttk.Button(button_frame, 
                                      text="Update Question",
                                      style='Dialog.TButton',
                                      command=self.update_question_data)
        self.update_button.pack(side=tk.LEFT, padx=5, expand=True)

    def update_question_data(self):
        question = self.question_entry.get("1.0", tk.END).strip()
        options = [
            self.option1_entry.get().strip(),
            self.option2_entry.get().strip(),
            self.option3_entry.get().strip(),
            self.option4_entry.get().strip()
        ]
        correct_answer = self.correct_answer_entry.get().strip()

        if not question or not all(options) or not correct_answer:
            messagebox.showerror("Error", "All fields are required.")
            return

        if correct_answer not in options:
            messagebox.showerror("Error", "Correct answer must match one of the options.")
            return

        question_data = {
            "question": question,
            "option1": options[0],
            "option2": options[1],
            "option3": options[2],
            "option4": options[3],
            "correct_answer": correct_answer
        }

        try:
            if self.db.update_question(self.language, self.question_id, question_data):
                self.callback()
                self.destroy()
                messagebox.showinfo("Success", "Question updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update question.")
        except Exception as e:
            logging.error(f"Error updating question: {e}")
            messagebox.showerror("Error", f"Failed to update question: {e}")
