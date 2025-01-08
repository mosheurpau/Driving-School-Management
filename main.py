import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk 
from fpdf import FPDF  # type: ignore # Import FPDF library
import webbrowser
from PIL import Image, ImageTk

# Database Setup
def create_db():
    conn = sqlite3.connect("driving_school.db")
    c = conn.cursor()

    # Create students table
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 address TEXT,
                 phone TEXT,
                 progress TEXT,
                 payment_status TEXT)''')

    # Create instructors table
    c.execute('''CREATE TABLE IF NOT EXISTS instructors (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 phone TEXT,
                 email TEXT,
                 instructor_type TEXT)''')

    # Create lessons table (with payment column)
    c.execute('''CREATE TABLE IF NOT EXISTS lessons (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id INTEGER,
                 student_name TEXT
                 instructor_id INTEGER,
                 instructor_name TEXT
                 lesson_type TEXT,
                 date TEXT,
                 payment INTEGER,  -- Payment for the lesson
                 status TEXT,
                 FOREIGN KEY(student_id) REFERENCES students(id),
                 FOREIGN KEY(instructor_id) REFERENCES instructors(id))''')

    # Create payments table
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id INTEGER,
                 amount INTEGER,
                 payment_date TEXT,
                 FOREIGN KEY(student_id) REFERENCES students(id))''')


    conn.commit()
    conn.close()


# Main Application Window
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Pass IT Driving School Management")
        self.root.geometry("1000x600") 
        # Set minimum width and height
        root.minsize(1200, 600) 

        # Use grid layout for responsiveness with fixed width for the left frame
        self.root.columnconfigure(0, weight=0, minsize=200)  # Fixed width for left frame
        self.root.columnconfigure(1, weight=1)  # Right frame expands
        self.root.rowconfigure(0, weight=1)

        self.create_widgets()
        # Set background colors
        # Set background colors
        self.main_frame.configure(bg="#00A300")  # Left side
        self.right_frame.configure(bg="#8AFF8A") # Right side

        # Make main_frame fill the left side
        self.main_frame.grid(row=0, column=0, sticky="nsew") 

        # Make buttons responsive (choose either option a or b)

        # Option a) Using columnconfigure
        self.main_frame.columnconfigure(0, weight=1) 

       

    def create_widgets(self):
        # Buttons for different management systems

        self.main_frame = tk.Frame(self.root, bg="#00A300")  # Green background for left frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")  # Make it fill the space

        # Configure rows and columns for button centering
        self.main_frame.rowconfigure(0, weight=1)  # Empty row above
        self.main_frame.rowconfigure(5, weight=1)  # Empty row below
        self.main_frame.columnconfigure(0, weight=1)

        # Add logo image
        try:
            # Open the image using PIL
            img = Image.open("logo.png")  # Replace "logo.png" with your image file

            # Resize the image using PIL
            img = img.resize((400, 400), Image.LANCZOS)

            # Convert back to PhotoImage
            self.logo_img = ImageTk.PhotoImage(img)  # Assign to self.logo_img

            logo_label = tk.Label(self.main_frame, image=self.logo_img, bg="#00A300")
            logo_label.grid(row=0, column=0, pady=5, padx=20,)
        except Exception as e:
            print(f"Error loading logo image: {e}")

        # Create button style
        button_style = ttk.Style()
        button_style.configure('My.TButton',
                            font=('Arial', 14, 'bold'),
                            foreground='#007500',  # White text
                            background='#023D54',  # Blue background
                            padding=20,
                            relief="flat")

        # Create buttons with styling (using ttk.Button)
        ttk.Button(self.main_frame, text="Student Management", style='My.TButton',
                command=lambda: self.open_management_window(StudentManagement)).grid(row=1, column=0, pady=5, padx=20,
                                                                                    sticky="ew")
        ttk.Button(self.main_frame, text="Instructor Management", style='My.TButton',
                command=lambda: self.open_management_window(InstructorManagement)).grid(row=2, column=0, pady=5, padx=20,
                                                                                        sticky="ew")
        ttk.Button(self.main_frame, text="Lesson Management", style='My.TButton',
                command=lambda: self.open_management_window(LessonManagement)).grid(row=3, column=0, pady=5, padx=20,
                                                                                    sticky="ew")
        ttk.Button(self.main_frame, text="Reporting", style='My.TButton',
                command=lambda: self.open_management_window(Reporting)).grid(row=4, column=0, pady=(5, 100), padx=20, sticky="ew")

        # Right frame for content
        self.right_frame = tk.Frame(self.root, bg="#007500")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
    
        # Add welcome message to right frame
        welcome_label = tk.Label(self.right_frame, text="Welcome to IT Driving School!", font=("Arial", 24, "bold"), bg="#007500", fg="white")
        welcome_label.pack(expand=True, pady=50)  # Center the label with padding

    def open_management_window(self, window_class):
        # Clear any existing widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Create an instance of the window class
        window_instance = window_class(self.right_frame) 


class StudentManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Create button style
        button_style = ttk.Style()
        button_style.configure('Student.TButton', 
                            font=('Arial', 10, 'bold'),  # Bold font
                            foreground='#007500',        # White text color
                            background='#2874A6',      # Blue background color
                            padding=10,                # Padding
                            relief="flat")             # Flat relief

        # Hover effect (change background color on hover)
        button_style.map('Student.TButton',
            background=[('active', '#3498DB'),  # Lighter blue on click
                        ('!disabled', '#21618C')])  # Darker blue on hover

        # Buttons (using ttk.Button with styling)
        self.add_student_button = ttk.Button(self.window, text="Add Student", style='Student.TButton',
                                            command=self.show_add_student_form)
        self.add_student_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Added margin

        self.view_students_button = ttk.Button(self.window, text="View Students", style='Student.TButton', 
                                            command=self.view_students)
        self.view_students_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.update_student_button = ttk.Button(self.window, text="Update Student", style='Student.TButton',
                                                command=self.show_update_student_form)
        self.update_student_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.delete_student_button = ttk.Button(self.window, text="Delete Student", style='Student.TButton',
                                                command=self.delete_student)
        self.delete_student_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Configure column weights
        for i in range(4):
            self.window.columnconfigure(i, weight=1)
            
        

        # Frames for forms (initially hidden)
        self.add_student_frame = tk.Frame(self.window)
        self.add_student_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.add_student_frame.grid_remove()

        self.update_student_frame = tk.Frame(self.window)
        self.update_student_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.update_student_frame.grid_remove()

        self.view_students_frame = tk.Frame(self.window)
        self.view_students_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.view_students_frame.grid_remove()

        self.delete_student_frame = tk.Frame(self.window)
        self.delete_student_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.delete_student_frame.grid_remove()

    def show_add_student_form(self):
        self.hide_all_forms()
        self.add_student_frame.grid()
        
        # Create labels and entry fields for the add student form within the frame
        tk.Label(self.add_student_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.add_student_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_student_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(self.add_student_frame)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.add_student_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.add_student_frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        # Progress combobox
        tk.Label(self.add_student_frame, text="Progress:").grid(row=3, column=0, padx=5, pady=5)
        self.progress_var = tk.StringVar()
        progress_combobox = ttk.Combobox(self.add_student_frame, textvariable=self.progress_var)
        progress_combobox['values'] = tuple(f"Level {i}" for i in range(1, 11))
        progress_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Payment status combobox
        tk.Label(self.add_student_frame, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5)
        self.payment_status_var = tk.StringVar()
        payment_status_combobox = ttk.Combobox(self.add_student_frame, textvariable=self.payment_status_var)
        payment_status_combobox['values'] = ("Paid", "Unpaid")
        payment_status_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Function to handle the submit button click
        def submit_data():
            name = self.name_entry.get()
            address = self.address_entry.get()
            phone = self.phone_entry.get()
            progress = self.progress_var.get()
            payment_status = self.payment_status_var.get()

            # --- Input Validation ---
            if not all([name, address, phone, progress, payment_status]):
                messagebox.showwarning("Warning", "All fields are required.")
                return
            # --- End of Input Validation ---

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("INSERT INTO students (name, address, phone, progress, payment_status) VALUES (?, ?, ?, ?, ?)",
                        (name, address, phone, progress, payment_status))
                conn.commit()
                messagebox.showinfo("Success", "Student added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add student: {e}")
            finally:
                conn.close()
                self.clear_add_student_form()

       

        submit_button = ttk.Button(self.add_student_frame, text="Submit", style='Submit.TButton', command=submit_data)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew", padx=50)

    def clear_add_student_form(self):
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.progress_var.set("")
        self.payment_status_var.set("")

    def show_update_student_form(self):
        self.hide_all_forms()
        self.update_student_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.update_student_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.update_student_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.update_student_frame, text="Search", command=self.search_student)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display search results
        self.search_results = tk.Listbox(self.update_student_frame)
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.search_results.bind("<<ListboxSelect>>", self.show_update_form) 
        # --- End of Search Functionality ---

    def search_student(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM students WHERE name LIKE ?", ('%' + search_term + '%',))
            student_data = c.fetchall()
            self.search_results.delete(0, tk.END) 
            if student_data:
                for student in student_data:
                    self.search_results.insert(tk.END, f"{student[0]} - {student[1]}") 
            else:
                messagebox.showinfo("Info", "No student found with that name.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching student: {e}")
        finally:
            conn.close()

    def show_update_form(self, event):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            selected_student = self.search_results.get(selected_index)
            student_id = selected_student.split(" - ")[0] 

            # Fetch the student data based on student_id
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("SELECT * FROM students WHERE id=?", (student_id,))
                student_data = c.fetchone()
                
                if student_data:
                    # Create update form elements dynamically
                    tk.Label(self.update_student_frame, text="Address:").grid(row=2, column=0, padx=5, pady=5)
                    self.address_entry = tk.Entry(self.update_student_frame)
                    self.address_entry.grid(row=2, column=1, padx=5, pady=5)
                    self.address_entry.insert(0, student_data[2])

                    tk.Label(self.update_student_frame, text="Phone:").grid(row=3, column=0, padx=5, pady=5)
                    self.phone_entry = tk.Entry(self.update_student_frame)
                    self.phone_entry.grid(row=3, column=1, padx=5, pady=5)
                    self.phone_entry.insert(0, student_data[3])

                     # Progress Combobox
                    tk.Label(self.update_student_frame, text="Progress:").grid(row=4, column=0, padx=5, pady=5)
                    self.progress_var = tk.StringVar(value=student_data[4])  # Set initial value
                    progress_combobox = ttk.Combobox(self.update_student_frame, textvariable=self.progress_var)
                    progress_combobox['values'] = tuple(f"Level {i}" for i in range(1, 11))
                    progress_combobox.grid(row=4, column=1, padx=5, pady=5)

                    # Payment Status Combobox
                    tk.Label(self.update_student_frame, text="Payment Status:").grid(row=5, column=0, padx=5, pady=5)
                    self.payment_status_var = tk.StringVar(value=student_data[5])  # Set initial value
                    payment_status_combobox = ttk.Combobox(self.update_student_frame, textvariable=self.payment_status_var)
                    payment_status_combobox['values'] = ("Paid", "Unpaid")
                    payment_status_combobox.grid(row=5, column=1, padx=5, pady=5)

                    # Create an update button
                    update_button = tk.Button(self.update_student_frame, text="Update", command=lambda: self.update_student(student_id))
                    update_button.grid(row=6, column=0, columnspan=2, pady=10) 

            except Exception as e:
                messagebox.showerror("Error", f"Error fetching student data: {e}")
            finally:
                conn.close()

    def update_student(self, student_id):
        # Get the updated values from the input fields
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        progress = self.progress_var.get()  # Get progress value
        payment_status = self.payment_status_var.get()  # Get payment status value

        # Update the student data in the database
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("""UPDATE students SET address=?, phone=?, progress=?, payment_status=? WHERE id=?""",
                      (address, phone, progress, payment_status, student_id))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {e}")
        finally:
            conn.close()

    def hide_all_forms(self):
        self.add_student_frame.grid_remove()
        self.update_student_frame.grid_remove()
        self.view_students_frame.grid_remove()
        self.delete_student_frame.grid_remove()

    def view_students(self):
        self.hide_all_forms()
        self.view_students_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.view_students_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.view_students_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.view_students_frame, text="Search", command=self.search_and_display_students)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        # --- End of Search Functionality ---

        # Frame to hold the canvas and scrollbar (placed below the search bar)
        self.canvas_frame = tk.Frame(self.view_students_frame)
        self.canvas_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Create a canvas and scrollbar inside the canvas_frame
        self.canvas = tk.Canvas(self.canvas_frame)
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.inner_frame = tk.Frame(self.canvas)
        canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Initial display of all students
        self.search_and_display_students()

        # Update canvas scroll region (bind to configure event)
        def on_canvas_configure(event):
            self.canvas.itemconfig(canvas_window, width=event.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind("<Configure>", on_canvas_configure)

    def search_and_display_students(self):
        search_term = self.search_entry.get()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            if search_term:
                c.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search_term + '%',))
            else:
                c.execute("SELECT * FROM students")  # Fetch all if no search term

            students = c.fetchall()

            # Clear existing widgets in the inner frame
            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            # Create labels to display student details within the inner frame
            for i, student in enumerate(students):
                student_details = f"""
                ID: {student[0]}
                Name: {student[1]}
                Address: {student[2]}
                Phone: {student[3]}
                Progress: {student[4]}
                Payment Status: {student[5]}
                """
                tk.Label(self.inner_frame, text=student_details, justify="left").grid(row=i, column=0, sticky="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching student data: {e}")
        finally:
            conn.close()
    
    def delete_student(self):
        self.hide_all_forms()
        self.delete_student_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.delete_student_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.delete_student_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.delete_student_frame, text="Search", command=self.search_student_for_deletion)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display search results
        self.search_results = tk.Listbox(self.delete_student_frame)
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.search_results.bind("<<ListboxSelect>>", self.show_delete_confirmation)
        # --- End of Search Functionality ---

    def search_student_for_deletion(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM students WHERE name LIKE ?", ('%' + search_term + '%',))
            student_data = c.fetchall()
            self.search_results.delete(0, tk.END)  # Clear previous results
            if student_data:
                for student in student_data:
                    self.search_results.insert(tk.END, f"{student[0]} - {student[1]}")  # Display ID and name
            else:
                messagebox.showinfo("Info", "No student found with that name.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching student: {e}")
        finally:
            conn.close()

    def show_delete_confirmation(self, event):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            selected_student = self.search_results.get(selected_index)
            student_id = selected_student.split(" - ")[0]  # Extract student ID

            # Show confirmation dialog
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with ID {student_id}?")
            if confirm:
                self.delete_student_from_db(student_id)

    def delete_student_from_db(self, student_id):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.search_student_for_deletion()  # Refresh the search results
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")
        finally:
            conn.close()
# Instructor Management Window
class InstructorManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Create button style
        button_style = ttk.Style()
        button_style.configure('Instructor.TButton',
                              font=('Arial', 10, 'bold'),  # Bold font
                              foreground='#00A300',  # White text color
                              background='#2874A6',  # Blue background color
                              padding=10,  # Padding
                              relief="flat")  # Flat relief

        # Hover effect (change background color on hover)
        button_style.map('Instructor.TButton',
                        background=[('active', '#3498DB'),  # Lighter blue on click
                                    ('!disabled', '#21618C')])  # Darker blue on hover

        # Buttons (using ttk.Button with styling)
        self.add_instructor_button = ttk.Button(self.window, text="Add Instructor", style='Instructor.TButton',
                                               command=self.show_add_instructor_form)
        self.add_instructor_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.view_instructors_button = ttk.Button(self.window, text="View Instructors", style='Instructor.TButton',
                                                   command=self.view_instructors)
        self.view_instructors_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.update_instructor_button = ttk.Button(self.window, text="Update Instructor", style='Instructor.TButton',
                                                   command=self.show_update_instructor_form)
        self.update_instructor_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.delete_instructor_button = ttk.Button(self.window, text="Delete Instructor", style='Instructor.TButton',
                                                   command=self.delete_instructor)
        self.delete_instructor_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Configure column weights (adjust for the new button)
        for i in range(4):
            self.window.columnconfigure(i, weight=1)

        # Frames for forms (initially hidden)
        self.add_instructor_frame = tk.Frame(self.window)
        self.add_instructor_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.add_instructor_frame.grid_remove()

        self.view_instructors_frame = tk.Frame(self.window)
        self.view_instructors_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.view_instructors_frame.grid_remove()

        self.update_instructor_frame = tk.Frame(self.window)
        self.update_instructor_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.update_instructor_frame.grid_remove()

        self.delete_instructor_frame = tk.Frame(self.window)
        self.delete_instructor_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.delete_instructor_frame.grid_remove()

    def show_add_instructor_form(self):
        self.hide_all_forms()
        self.add_instructor_frame.grid()

        # Create labels and entry fields for the add instructor form
        tk.Label(self.add_instructor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.add_instructor_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_instructor_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.add_instructor_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.add_instructor_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.add_instructor_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Instructor Type dropdown
        tk.Label(self.add_instructor_frame, text="Instructor Type:").grid(row=3, column=0, padx=5, pady=5)
        self.instructor_type_var = tk.StringVar(value="Full-time")  # Default value
        instructor_type_combobox = ttk.Combobox(self.add_instructor_frame, textvariable=self.instructor_type_var)
        instructor_type_combobox['values'] = ("Full-time", "Part-time")
        instructor_type_combobox.grid(row=3, column=1, padx=5, pady=5)

            # Function to handle the submit button click
        def submit_data():
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            instructor_type = self.instructor_type_var.get()

            # --- Input Validation ---
            if not all([name, phone, email, instructor_type]):
                messagebox.showwarning("Warning", "All fields are required.")
                return
            # --- End of Input Validation ---

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("INSERT INTO instructors (name, phone, email, instructor_type) VALUES (?, ?, ?, ?)",
                        (name, phone, email, instructor_type))
                conn.commit()
                messagebox.showinfo("Success", "Instructor added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add instructor: {e}")
            finally:
                conn.close()
                self.clear_add_instructor_form()

        # Create a submit button
        submit_button = tk.Button(self.add_instructor_frame, text="Submit", command=submit_data)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10, padx=40)  # Adjusted row number

    def clear_add_instructor_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def view_instructors(self):
        self.hide_all_forms()
        self.view_instructors_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.view_instructors_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.view_instructors_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.view_instructors_frame, text="Search", command=self.search_and_display_instructors)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        # --- End of Search Functionality ---

        # Frame to hold the canvas and scrollbar (placed below the search bar)
        self.canvas_frame = tk.Frame(self.view_instructors_frame)
        self.canvas_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Create a canvas and scrollbar inside the canvas_frame
        self.canvas = tk.Canvas(self.canvas_frame)  # Make canvas an instance variable
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.inner_frame = tk.Frame(self.canvas)  # Make inner_frame an instance variable
        canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Initial display of all instructors
        self.search_and_display_instructors()  # Call the search function to display instructors

        # Update canvas scroll region (bind to configure event)
        def on_canvas_configure(event):
            self.canvas.itemconfig(canvas_window, width=event.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind("<Configure>", on_canvas_configure)

    def search_and_display_instructors(self):
        search_term = self.search_entry.get()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            if search_term:
                c.execute("SELECT * FROM instructors WHERE name LIKE ?", ('%' + search_term + '%',))
            else:
                c.execute("SELECT * FROM instructors")  # Fetch all if no search term

            instructors = c.fetchall()

            # Clear existing widgets in the inner frame
            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            # Create labels to display instructor details within the inner frame
            for i, instructor in enumerate(instructors):
                instructor_details = f"""
                ID: {instructor[0]}
                Name: {instructor[1]}
                Phone: {instructor[2]}
                Email: {instructor[3]}
                Instructor Type: {instructor[4]} 
                """
                tk.Label(self.inner_frame, text=instructor_details, justify="left").grid(row=i, column=0, sticky="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching instructor data: {e}")
        finally:
            conn.close()

    def show_update_instructor_form(self):
        self.hide_all_forms()
        self.update_instructor_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.update_instructor_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.update_instructor_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.update_instructor_frame, text="Search", command=self.search_instructor)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display search results
        self.search_results = tk.Listbox(self.update_instructor_frame)
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.search_results.bind("<<ListboxSelect>>", self.show_instructor_update_form)
        # --- End of Search Functionality ---

    def search_instructor(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM instructors WHERE name LIKE ?", ('%' + search_term + '%',))
            instructor_data = c.fetchall()
            self.search_results.delete(0, tk.END)
            if instructor_data:
                for instructor in instructor_data:
                    self.search_results.insert(tk.END, f"{instructor[0]} - {instructor[1]}")
            else:
                messagebox.showinfo("Info", "No instructor found with that name.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching instructor: {e}")
        finally:
            conn.close()

    def show_instructor_update_form(self, event):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            selected_instructor = self.search_results.get(selected_index)
            instructor_id = selected_instructor.split(" - ")[0]

            # Fetch instructor data
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("SELECT * FROM instructors WHERE id=?", (instructor_id,))
                instructor_data = c.fetchone()

                if instructor_data:
                    # Create update form elements
                    tk.Label(self.update_instructor_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
                    self.phone_entry = tk.Entry(self.update_instructor_frame)
                    self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
                    self.phone_entry.insert(0, instructor_data[2])

                    tk.Label(self.update_instructor_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
                    self.email_entry = tk.Entry(self.update_instructor_frame)
                    self.email_entry.grid(row=3, column=1, padx=5, pady=5)
                    self.email_entry.insert(0, instructor_data[3])

                    # Instructor Type dropdown (for updating)
                    tk.Label(self.update_instructor_frame, text="Instructor Type:").grid(row=4, column=0, padx=5, pady=5)
                    self.instructor_type_var = tk.StringVar(value=instructor_data[4])  # Set initial value from database
                    instructor_type_combobox = ttk.Combobox(self.update_instructor_frame, textvariable=self.instructor_type_var)
                    instructor_type_combobox['values'] = ("Full-time", "Part-time")
                    instructor_type_combobox.grid(row=4, column=1, padx=5, pady=5)

                    # Create an update button
                    update_button = tk.Button(self.update_instructor_frame, text="Update",
                                            command=lambda: self.update_instructor(instructor_id))
                    update_button.grid(row=5, column=0, columnspan=2, pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Error fetching instructor data: {e}")
            finally:
                conn.close()

    def update_instructor(self, instructor_id):
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        instructor_type = self.instructor_type_var.get()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("""UPDATE instructors SET phone=?, email=?,  instructor_type=? WHERE id=?""",
                      (phone, email,  instructor_type, instructor_id))
            conn.commit()
            messagebox.showinfo("Success", "Instructor updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update instructor: {e}")
        finally:
            conn.close()

    def delete_instructor(self):
        self.hide_all_forms()
        self.delete_instructor_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.delete_instructor_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.delete_instructor_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.delete_instructor_frame, text="Search",
                                  command=self.search_instructor_for_deletion)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display search results
        self.search_results = tk.Listbox(self.delete_instructor_frame)
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.search_results.bind("<<ListboxSelect>>", self.show_delete_confirmation)
        # --- End of Search Functionality ---

    def search_instructor_for_deletion(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM instructors WHERE name LIKE ?", ('%' + search_term + '%',))
            instructor_data = c.fetchall()
            self.search_results.delete(0, tk.END)  # Clear previous results
            if instructor_data:
                for instructor in instructor_data:
                    self.search_results.insert(tk.END,
                                              f"{instructor[0]} - {instructor[1]}")  # Display ID and name
            else:
                messagebox.showinfo("Info", "No instructor found with that name.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching instructor: {e}")
        finally:
            conn.close()

    def show_delete_confirmation(self, event):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            selected_instructor = self.search_results.get(selected_index)
            instructor_id = selected_instructor.split(" - ")[0]  # Extract instructor ID

            # Show confirmation dialog
            confirm = messagebox.askyesno("Confirm Delete",
                                         f"Are you sure you want to delete instructor with ID {instructor_id}?")
            if confirm:
                self.delete_instructor_from_db(instructor_id)

    def delete_instructor_from_db(self, instructor_id):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("DELETE FROM instructors WHERE id=?", (instructor_id,))
            conn.commit()
            messagebox.showinfo("Success", "Instructor deleted successfully!")
            self.search_instructor_for_deletion()  # Refresh the search results
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete instructor: {e}")
        finally:
            conn.close()

    def hide_all_forms(self):
        self.add_instructor_frame.grid_remove()
        self.view_instructors_frame.grid_remove()
        self.update_instructor_frame.grid_remove()
        self.delete_instructor_frame.grid_remove()

# Lesson Management Window
class LessonManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame
        self.student_id_entry = None 
        

        # Create button style
        button_style = ttk.Style()
        button_style.configure('Lesson.TButton', 
                            font=('Arial', 10, 'bold'),  # Bold font
                            foreground='#00A300',        # White text color
                            background='#2874A6',      # Blue background color
                            padding=10,                # Padding
                            relief="flat")             # Flat relief

        # Hover effect (change background color on hover)
        button_style.map('Lesson.TButton',
            background=[('active', '#3498DB'),  # Lighter blue on click
                        ('!disabled', '#21618C')])  # Darker blue on hover

        # Buttons (using ttk.Button with styling)
        self.book_lesson_button = ttk.Button(self.window, text="Book Lesson", style='Lesson.TButton',
                                            command=self.show_book_lesson_form)
        self.book_lesson_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Added margin

        self.view_lessons_button = ttk.Button(self.window, text="View Lessons", style='Lesson.TButton', 
                                            command=self.view_lessons)
        self.view_lessons_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.delete_lesson_button = ttk.Button(self.window, text="Delete Lesson", style='Lesson.TButton',
                                                command=self.delete_lesson)
        self.delete_lesson_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        
        self.update_lesson_button = ttk.Button(self.window, text="Update Lesson", style='Lesson.TButton',
                                                command=self.show_update_lesson_form)
        self.update_lesson_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")


        # Configure column weights (4 columns now)
        for i in range(4):  
            self.window.columnconfigure(i, weight=1)

        # Frames for forms (initially hidden)
        self.book_lesson_frame = tk.Frame(self.window)
        self.book_lesson_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.book_lesson_frame.grid_remove()

        self.view_lessons_frame = tk.Frame(self.window)
        self.view_lessons_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.view_lessons_frame.grid_remove()

        self.delete_lesson_frame = tk.Frame(self.window)
        self.delete_lesson_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.delete_lesson_frame.grid_remove()
        
        self.update_lesson_frame = tk.Frame(self.window)
        self.update_lesson_frame.grid(row=1, column=0, columnspan=4, pady=10)
        self.update_lesson_frame.grid_remove()

    def show_book_lesson_form(self):
        self.hide_all_forms()
        self.book_lesson_frame.grid()

        # --- Student ID Dropdown ---
        tk.Label(self.book_lesson_frame, text="Student:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_var = tk.StringVar()
        student_id_combobox = ttk.Combobox(self.book_lesson_frame, textvariable=self.student_id_var)

        # Fetch student IDs and names from the database
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM students")
        student_data = c.fetchall()
        conn.close()

        student_id_combobox['values'] = [f"{id} - {name}" for id, name in student_data]
        student_id_combobox.grid(row=0, column=1, padx=5, pady=5)

        # --- Instructor ID Dropdown ---
        tk.Label(self.book_lesson_frame, text="Instructor:").grid(row=1, column=0, padx=5, pady=5)
        self.instructor_id_var = tk.StringVar()
        instructor_id_combobox = ttk.Combobox(self.book_lesson_frame, textvariable=self.instructor_id_var)

        # Fetch instructor IDs and names from the database
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT id, name FROM instructors")
        instructor_data = c.fetchall()
        conn.close()

        instructor_id_combobox['values'] = [f"{id} - {name}" for id, name in instructor_data]
        instructor_id_combobox.grid(row=1, column=1, padx=5, pady=5)

        # --- Lesson Type Combobox ---
        tk.Label(self.book_lesson_frame, text="Lesson Type:").grid(row=2, column=0, padx=5, pady=5)
        self.lesson_type_var = tk.StringVar()
        lesson_type_combobox = ttk.Combobox(self.book_lesson_frame, textvariable=self.lesson_type_var)
        lesson_type_combobox['values'] = ('Introductory', 'Standard', 'Pass Plus', 'Driving Test')
        lesson_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        # --- Date Entry ---
        tk.Label(self.book_lesson_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.book_lesson_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        # --- Payment Entry (disabled) ---
        tk.Label(self.book_lesson_frame, text="Payment:").grid(row=4, column=0, padx=5, pady=5)
        self.payment_entry = tk.Entry(self.book_lesson_frame, state="disabled")
        self.payment_entry.grid(row=4, column=1, padx=5, pady=5)

        # --- Status Dropdown ---
        tk.Label(self.book_lesson_frame, text="Status:").grid(row=5, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(value="Unpaid")
        status_combobox = ttk.Combobox(self.book_lesson_frame, textvariable=self.status_var)
        status_combobox['values'] = ("Paid", "Unpaid")
        status_combobox.grid(row=5, column=1, padx=5, pady=5)

        # --- Function to handle lesson type selection and update payment ---
        def on_lesson_type_select(event=None):
            lesson_type = self.lesson_type_var.get()
            payment = 0
            if lesson_type == "Introductory":
                payment = 100
            elif lesson_type == "Standard":
                payment = 200
            elif lesson_type == "Pass Plus":
                payment = 300
            elif lesson_type == "Driving Test":
                payment = 350

            self.payment_entry.config(state="normal")
            self.payment_entry.delete(0, tk.END)
            self.payment_entry.insert(0, str(payment))
            self.payment_entry.config(state="disabled")

        # --- Bind the function to the Combobox ---
        lesson_type_combobox.bind("<<ComboboxSelected>>", on_lesson_type_select)
        

        def submit_data():
            # Get the selected student and instructor IDs
            selected_student = self.student_id_var.get()
            selected_instructor = self.instructor_id_var.get()

            if selected_student and selected_instructor:
                student_id = selected_student.split(" - ")[0]
                instructor_id = selected_instructor.split(" - ")[0]
                student_name = selected_student.split(" - ")[1]  # Extract student name
                instructor_name = selected_instructor.split(" - ")[1]  # Extract instructor name

                lesson_type = self.lesson_type_var.get()
                date = self.date_entry.get()
                status = self.status_var.get()

                # Input Validation
                if not all([student_id, instructor_id, lesson_type, date, status]):
                    messagebox.showwarning("Warning", "All fields are required.")
                    return

                if lesson_type == "Pass Plus":
                    # Ask for confirmation
                    confirm = messagebox.askyesno("Confirm Booking", "Have you completed Introductory and Standard lessons?")
                    if confirm:
                        # Proceed with booking (no database check)
                        conn = sqlite3.connect("driving_school.db")
                        c = conn.cursor()
                        try:
                            # Include student_name and instructor_name in the INSERT statement
                            c.execute(
                                "INSERT INTO lessons (student_id, student_name, instructor_id, instructor_name, lesson_type, date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (student_id, student_name, instructor_id, instructor_name, lesson_type, date, status),
                            )
                            conn.commit()
                            messagebox.showinfo("Success", "Lesson booked successfully!")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to book lesson: {e}")
                        finally:
                            conn.close()
                            self.clear_book_lesson_form()
                    else:
                        # User clicked "No" in the confirmation dialog, so do not proceed
                        return
                else:
                    # For other lesson types, proceed with booking directly
                    conn = sqlite3.connect("driving_school.db")
                    c = conn.cursor()
                    try:
                        # Include student_name and instructor_name in the INSERT statement
                        c.execute(
                            "INSERT INTO lessons (student_id, student_name, instructor_id, instructor_name, lesson_type, date, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (student_id, student_name, instructor_id, instructor_name, lesson_type, date, status),
                        )
                        conn.commit()
                        messagebox.showinfo("Success", "Lesson booked successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to book lesson: {e}")
                    finally:
                        conn.close()
                        self.clear_book_lesson_form()
            else:
                messagebox.showwarning("Warning", "Please select both student and instructor.")

        # --- Create a submit button ---
        submit_button = tk.Button(self.book_lesson_frame, text="Submit", command=submit_data)
        submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    def clear_book_lesson_form(self):
        self.student_id_entry.delete(0, tk.END)
        self.instructor_id_entry.delete(0, tk.END)
        self.lesson_type_var.set("")
        self.date_entry.delete(0, tk.END)


    def view_lessons(self):
        self.hide_all_forms()
        self.view_lessons_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.view_lessons_frame, text="Search by Student ID:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.view_lessons_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.view_lessons_frame, text="Search", command=self.search_and_display_lessons)
        search_button.grid(row=0, column=2, padx=5, pady=5)
        # --- End of Search Functionality ---

        # Frame to hold the canvas and scrollbar
        self.canvas_frame = tk.Frame(self.view_lessons_frame)
        self.canvas_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Create a canvas and scrollbar inside the canvas_frame
        self.canvas = tk.Canvas(self.canvas_frame)
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.inner_frame = tk.Frame(self.canvas)
        canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Initial display of all lessons
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM lessons")  # Fetch all lessons
            lessons = c.fetchall()

            # Clear existing widgets in the inner frame
            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            # Create labels to display lesson details
            for i, lesson in enumerate(lessons):
                lesson_type = lesson[3]  # Get the lesson type from the tuple

                # Calculate payment based on lesson type
                payment = 0
                if lesson_type == "Introductory":
                    payment = 100
                elif lesson_type == "Standard":
                    payment = 200
                elif lesson_type == "Pass Plus":
                    payment = 300
                elif lesson_type == "Driving Test":
                    payment = 350

                lesson_details = f"""
                ID: {lesson[0]}
                Instructor ID: {lesson[1]}
                Student Name: {lesson[6] if len(lesson) > 2 else ""} 
                Instructor ID: {lesson[2]}
                Instructor Name: {lesson[7] if len(lesson) > 4 else ""} 
                Lesson Type: {lesson[3]}
                Date: {lesson[4]if len(lesson) > 1 else ""}
                Status: {lesson[5]if len(lesson) > 5 else ""}      
                Payment: {payment}
                """
                tk.Label(self.inner_frame, text=lesson_details, justify="left").grid(row=i, column=0, sticky="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching lesson data: {e}")
        finally:
            conn.close()

        # Update canvas scroll region (bind to configure event)
        def on_canvas_configure(event):
            self.canvas.itemconfig(canvas_window, width=event.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind("<Configure>", on_canvas_configure)  # No 'self' argument here

    def search_and_display_lessons(self):
        search_term = self.search_entry.get()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            if search_term:
                c.execute("SELECT * FROM lessons WHERE student_id LIKE ?", ('%' + search_term + '%',))
            else:
                c.execute("SELECT * FROM lessons")  # Fetch all if no search term

            lessons = c.fetchall()

            # Clear existing widgets in the inner frame
            for widget in self.inner_frame.winfo_children():
                widget.destroy()

            # Create labels to display lesson details
            for i, lesson in enumerate(lessons):
                lesson_type = lesson[3]  # Get the lesson type from the tuple

                # Calculate payment based on lesson type
                payment = 0
                if lesson_type == "Introductory":
                    payment = 100
                elif lesson_type == "Standard":
                    payment = 200
                elif lesson_type == "Pass Plus":
                    payment = 300
                elif lesson_type == "Driving Test":
                    payment = 350

                lesson_details = f"""
                ID: {lesson[0]}
                Instructor ID: {lesson[1]}
                Student Name: {lesson[6] if len(lesson) > 2 else ""} 
                Instructor ID: {lesson[2]}
                Instructor Name: {lesson[7] if len(lesson) > 4 else ""} 
                Lesson Type: {lesson[3]}
                Date: {lesson[4]if len(lesson) > 1 else ""}
                Status: {lesson[5]if len(lesson) > 5 else ""}      
                Payment: {payment}
                """
                tk.Label(self.inner_frame, text=lesson_details, justify="left").grid(row=i, column=0, sticky="w")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching lesson data: {e}")
        finally:
            conn.close()
            
    
    def show_update_lesson_form(self):
        self.hide_all_forms()
        self.update_lesson_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.update_lesson_frame, text="Search by Lesson ID:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.update_lesson_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.update_lesson_frame, text="Search", command=self.search_lesson_by_lesson_id)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display search results
        self.search_results = tk.Listbox(self.update_lesson_frame)
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.search_results.bind("<<ListboxSelect>>", self.show_lesson_update_form)
        # --- End of Search Functionality ---

    def search_lesson_by_lesson_id(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            # Fetch lesson ID and student name
            c.execute("SELECT l.id, s.name FROM lessons l JOIN students s ON l.student_id = s.id WHERE l.id LIKE ?", ('%' + search_term + '%',))
            lesson_data = c.fetchall()
            self.search_results.delete(0, tk.END)
            if lesson_data:
                for lesson in lesson_data:
                    self.search_results.insert(tk.END, f"{lesson[0]} - {lesson[1]}")  # Display lesson ID and student name
            else:
                messagebox.showinfo("Info", "No lesson found with that ID.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching lesson: {e}")
        finally:
            conn.close()

    def show_lesson_update_form(self, event):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            selected_lesson = self.search_results.get(selected_index)
            lesson_id = selected_lesson.split(" - ")[0]  # Extract lesson ID

            # Fetch lesson data
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,))
                lesson_data = c.fetchone()

                if lesson_data:
                    # Display student name (non-editable)
                    tk.Label(self.update_lesson_frame, text="Student Name:").grid(row=2, column=0, padx=5, pady=5)
                    student_name_label = tk.Label(self.update_lesson_frame, text=lesson_data[7])  # Assuming student_name is at index 7
                    student_name_label.grid(row=2, column=1, padx=5, pady=5)

                    # --- Date Entry ---
                    tk.Label(self.update_lesson_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
                    self.date_entry = tk.Entry(self.update_lesson_frame)
                    self.date_entry.grid(row=3, column=1, padx=5, pady=5)
                    self.date_entry.insert(0, lesson_data[4])

                    # --- Status Dropdown ---
                    tk.Label(self.update_lesson_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5)
                    self.status_var = tk.StringVar(value=lesson_data[6])
                    status_combobox = ttk.Combobox(self.update_lesson_frame, textvariable=self.status_var)
                    status_combobox['values'] = ("Paid", "Unpaid")
                    status_combobox.grid(row=4, column=1, padx=5, pady=5)

                    # Create an update button
                    update_button = tk.Button(self.update_lesson_frame, text="Update",
                                              command=lambda: self.update_lesson(lesson_id))
                    update_button.grid(row=5, column=0, columnspan=2, pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Error fetching lesson data: {e}")
            finally:
                conn.close()
                
    def update_lesson(self, lesson_id):
        date = self.date_entry.get()
        status = self.status_var.get()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("""UPDATE lessons SET date=?, status=? WHERE id=?""", (date, status, lesson_id))
            conn.commit()
            messagebox.showinfo("Success", "Lesson updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update lesson: {e}")
        finally:
            conn.close()

    def delete_lesson(self):
        self.hide_all_forms()
        self.delete_lesson_frame.grid()

        # Create input field for lesson ID
        tk.Label(self.delete_lesson_frame, text="Enter Lesson ID to delete:").grid(row=0, column=0, padx=5, pady=5)
        self.lesson_id_entry = tk.Entry(self.delete_lesson_frame)
        self.lesson_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create button to confirm deletion
        delete_button = tk.Button(self.delete_lesson_frame, text="Delete Lesson", command=self.confirm_delete_lesson)
        delete_button.grid(row=1, column=0, columnspan=2, pady=5)

    def confirm_delete_lesson(self):
        lesson_id = self.lesson_id_entry.get()
        if lesson_id:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete lesson with ID {lesson_id}?")
            if confirm:
                conn = sqlite3.connect("driving_school.db")
                c = conn.cursor()
                try:
                    c.execute("DELETE FROM lessons WHERE id=?", (lesson_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Lesson deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete lesson: {e}")
                finally:
                    conn.close()
                    self.lesson_id_entry.delete(0, tk.END)

    def hide_all_forms(self):
        self.book_lesson_frame.grid_remove()
        self.view_lessons_frame.grid_remove()
        self.delete_lesson_frame.grid_remove()
        self.update_lesson_frame.grid_remove()

# Reporting Window
class Reporting:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Create button style
        button_style = ttk.Style()
        button_style.configure('Report.TButton', 
                            font=('Arial', 10, 'bold'),  # Bold font
                            foreground='#00A300',        # White text color
                            background='#2874A6',      # Blue background color
                            padding=10,                # Padding
                            relief="flat")             # Flat relief

        # Hover effect (change background color on hover)
        button_style.map('Report.TButton',
            background=[('active', '#3498DB'),  # Lighter blue on click
                        ('!disabled', '#21618C')])  # Darker blue on hover

        # Buttons (using ttk.Button with styling)
        self.generate_report_button = ttk.Button(self.window, text="Generate Report", style='Report.TButton',
                                                command=self.show_report)
        self.generate_report_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")  # Added margin

        self.student_progress_button = ttk.Button(self.window, text="Student Progress", style='Report.TButton',
                                                command=self.show_student_progress_form)
        self.student_progress_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Configure column weights
        for i in range(2):
            self.window.columnconfigure(i, weight=1)

        # Frame for report (initially hidden)
        self.report_frame = tk.Frame(self.window)
        self.report_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.report_frame.grid_remove()

        # Frame for student progress (initially hidden)
        self.student_progress_frame = tk.Frame(self.window)
        self.student_progress_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.student_progress_frame.grid_remove()

    def show_report(self):
        self.hide_all_forms()  # Hide other forms
        self.report_frame.grid()  # Show the report frame

        # Generate the report content
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM lessons WHERE status = 'Booked'")
        lessons_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM students")
        students_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM instructors")
        instructors_count = c.fetchone()[0]
        conn.close()

        report_text = f"""
        Total lessons booked: {lessons_count}
        Total students: {students_count}
        Total instructors: {instructors_count}
        """

        # Display the report in a label within the frame
        tk.Label(self.report_frame, text=report_text, justify="left").pack()
        
        # Print Report button
        print_button = tk.Button(self.report_frame, text="Print Report", command=self.print_report)
        print_button.pack(pady=10)
        
   
    # Generate the report content
    def print_report(self):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()

        # Fetch data for the report
        c.execute("SELECT * FROM students")
        students = c.fetchall()
        c.execute("SELECT * FROM instructors")
        instructors = c.fetchall()
        c.execute("SELECT * FROM lessons")
        lessons = c.fetchall()

        conn.close()

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add report title
        pdf.cell(200, 10, txt="Driving School Report", ln=1, align="C")

        # Add student data to the PDF
        pdf.cell(200, 10, txt="Students", ln=1, align="L")
        for student in students:
            student_details = f"""
            ID: {student[0]}
            Name: {student[1]}
            Address: {student[2]}
            Phone: {student[3]}
            Progress: {student[4]}
            Payment Status: {student[5]}
            """
            pdf.multi_cell(0, 10, txt=student_details)

        # Add instructor data to the PDF
        pdf.cell(200, 10, txt="Instructors", ln=1, align="L")
        for instructor in instructors:
            instructor_details = f"""
            ID: {instructor[0]}
            Name: {instructor[1]}
            Phone: {instructor[2]}
            Email: {instructor[3]}
            Instructor Type: {instructor[4]}
            """
            pdf.multi_cell(0, 10, txt=instructor_details)

        # Add lesson data to the PDF
        pdf.cell(200, 10, txt="Lessons", ln=1, align="L")
        for lesson in lessons:
            lesson_details = f"""
            ID: {lesson[0]}
            Instructor ID: {lesson[1]}
            Student Name: {lesson[6] if len(lesson) > 2 else ""} 
            Instructor ID: {lesson[2]}
            Instructor Name: {lesson[7] if len(lesson) > 4 else ""} 
            Lesson Type: {lesson[3]}
            Date: {lesson[4]if len(lesson) > 1 else ""}
            Status: {lesson[5]if len(lesson) > 5 else ""}      
            """
            pdf.multi_cell(0, 10, txt=lesson_details)

        # Save the PDF
        try:
            pdf.output("driving_school_report.pdf")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")
            return  # Stop further execution if PDF generation fails

        # Open the generated PDF file
        try:
            webbrowser.open_new(r'driving_school_report.pdf')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF file: {e}")
        

    def show_student_progress_form(self):
        self.hide_all_forms()
        self.student_progress_frame.grid()

        # --- Search Functionality ---
        tk.Label(self.student_progress_frame, text="Search by Student Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.student_progress_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(self.student_progress_frame, text="Search", command=self.search_student_for_progress)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Listbox to display search results
        self.search_results = tk.Listbox(self.student_progress_frame)
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.search_results.bind("<<ListboxSelect>>", self.calculate_progress_for_selected_student)
        # --- End of Search Functionality ---

    def search_student_for_progress(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        try:
            c.execute("SELECT id, name FROM students WHERE name LIKE ?", ('%' + search_term + '%',))
            student_data = c.fetchall()
            self.search_results.delete(0, tk.END)
            if student_data:
                for student in student_data:
                    self.search_results.insert(tk.END, f"{student[0]} - {student[1]}")
            else:
                messagebox.showinfo("Info", "No student found with that name.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching student: {e}")
        finally:
            conn.close()

    def calculate_progress_for_selected_student(self, event):
        selection = self.search_results.curselection()
        if selection:
            selected_index = selection[0]
            selected_student = self.search_results.get(selected_index)
            student_id = selected_student.split(" - ")[0]  # Extract student ID

            # Now you have the student_id, you can use your existing calculate_progress logic
            self.calculate_progress(student_id)  # Pass the student_id to calculate_progress


    def calculate_progress(self, student_id):  # Modified to accept student_id
        if student_id:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("SELECT lesson_type FROM lessons WHERE student_id=?", (student_id,))
                lessons = c.fetchall()

                total_progress = 0
                for lesson in lessons:
                    lesson_type = lesson[0]  # Get the lesson type string

                    # Calculate progress based on lesson type
                    if lesson_type == "Introductory":
                        total_progress = 20  # Example progress for Introductory
                    elif lesson_type == "Standard":
                        total_progress = 60  # Example progress for Standard
                    elif lesson_type == "Pass Plus":
                        total_progress = 95  # Example progress for Pass Plus
                    elif lesson_type == "Driving Test":
                        total_progress = 100
                    # Add more elif blocks for other lesson types if needed

                # Display the progress
                result_label = tk.Label(self.student_progress_frame, text=f"Student ID: {student_id}\nProgress: {total_progress}%", justify="left")
                result_label.grid(row=2, column=0, columnspan=2, pady=5)

            except Exception as e:
                messagebox.showerror("Error", f"Error calculating progress: {e}")
            finally:
                conn.close()

    def hide_all_forms(self):
        self.report_frame.grid_remove()
        self.student_progress_frame.grid_remove()


# Main Program
if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = Application(root)
    root.mainloop()