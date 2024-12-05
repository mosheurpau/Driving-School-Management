import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk 

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
                email TEXT)''')
    
    # Create lessons table
    c.execute('''CREATE TABLE IF NOT EXISTS lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                instructor_id INTEGER,
                lesson_type TEXT,
                date TEXT,
                status TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(instructor_id) REFERENCES instructors(id))''')
    
    # Create payments table
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                amount REAL,
                payment_date TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id))''')
    
    conn.commit()
    conn.close()

# Main Application Window
class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Pass IT Driving School Management")
        self.root.geometry("800x400") 
        # Set minimum width and height
        root.minsize(600, 300) 

        # Use grid layout for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3) 
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
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="ns")
        tk.Button(self.main_frame, text="Student Management", width=20, 
                 command=lambda: self.open_management_window(StudentManagement)).grid(row=0, column=0, pady=5)
        tk.Button(self.main_frame, text="Instructor Management", width=20, 
                 command=lambda: self.open_management_window(InstructorManagement)).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="Lesson Management", width=20, 
                 command=lambda: self.open_management_window(LessonManagement)).grid(row=2, column=0, pady=5)
        tk.Button(self.main_frame, text="Reporting", width=20, 
                 command=lambda: self.open_management_window(Reporting)).grid(row=3, column=0, pady=5)

        # Right frame for content
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

    def open_management_window(self, window_class):
        # Clear any existing widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Create an instance of the window class
        window_instance = window_class(self.right_frame) 


class StudentManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Buttons
        self.add_student_button = tk.Button(self.window, text="Add Student", command=self.show_add_student_form)
        self.add_student_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.view_students_button = tk.Button(self.window, text="View Students", command=self.view_students)
        self.view_students_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.update_student_button = tk.Button(self.window, text="Update Student", command=self.show_update_student_form)
        self.update_student_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.delete_student_button = tk.Button(self.window, text="Delete Student", command=self.delete_student)
        self.delete_student_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

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

        # Create a submit button
        submit_button = tk.Button(self.add_student_frame, text="Submit", command=submit_data)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def clear_add_student_form(self):
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.progress_var.set("")
        self.payment_status_var.set("")

    def show_update_student_form(self):
        self.hide_all_forms()
        self.update_student_frame.grid()

        student_id = simpledialog.askinteger("Input", "Enter student ID to update:")
        if student_id is not None:
            # Fetch existing student data
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT * FROM students WHERE id=?", (student_id,))
            student_data = c.fetchone()
            conn.close()

            if student_data:
                # Create labels and entry fields for the update student form within the frame
                tk.Label(self.update_student_frame, text="Address:").grid(row=0, column=0, padx=5, pady=5)
                self.address_entry = tk.Entry(self.update_student_frame)
                self.address_entry.grid(row=0, column=1, padx=5, pady=5)
                self.address_entry.insert(0, student_data[2])

                tk.Label(self.update_student_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
                self.phone_entry = tk.Entry(self.update_student_frame)
                self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
                self.phone_entry.insert(0, student_data[3])

                # Progress combobox
                tk.Label(self.update_student_frame, text="Progress:").grid(row=2, column=0, padx=5, pady=5)
                self.progress_var = tk.StringVar(value=student_data[4])
                progress_combobox = ttk.Combobox(self.update_student_frame, textvariable=self.progress_var)
                progress_combobox['values'] = tuple(f"Level {i}" for i in range(1, 11))
                progress_combobox.grid(row=2, column=1, padx=5, pady=5)

                # Payment status combobox
                tk.Label(self.update_student_frame, text="Payment Status:").grid(row=3, column=0, padx=5, pady=5)
                self.payment_status_var = tk.StringVar(value=student_data[5])
                payment_status_combobox = ttk.Combobox(self.update_student_frame, textvariable=self.payment_status_var)
                payment_status_combobox['values'] = ("Paid", "Unpaid")
                payment_status_combobox.grid(row=3, column=1, padx=5, pady=5)

                # Function to handle update submission
                def submit_update():
                    address = self.address_entry.get()
                    phone = self.phone_entry.get()
                    progress = self.progress_var.get()
                    payment_status = self.payment_status_var.get()
                    
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

                # Create a submit button for update
                submit_button = tk.Button(self.update_student_frame, text="Submit Update", command=submit_update)
                submit_button.grid(row=4, column=0, columnspan=2, pady=10)

            else:
                messagebox.showerror("Error", "Student not found.")

    def hide_all_forms(self):
        self.add_student_frame.grid_remove()
        self.update_student_frame.grid_remove()
        self.view_students_frame.grid_remove()
        self.delete_student_frame.grid_remove()

    def view_students(self):
        self.hide_all_forms()
        self.view_students_frame.grid()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()
        conn.close()

        # Clear existing widgets in the frame
        for widget in self.view_students_frame.winfo_children():
            widget.destroy()

        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.view_students_frame)
        scrollbar = ttk.Scrollbar(self.view_students_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas to hold the labels
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

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
            tk.Label(inner_frame, text=student_details, justify="left").grid(row=i, column=0, sticky="w")

        # Update canvas scroll region
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def delete_student(self):
        self.hide_all_forms()
        self.delete_student_frame.grid()

        # Create input field for student ID
        tk.Label(self.delete_student_frame, text="Enter Student ID to delete:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = tk.Entry(self.delete_student_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create button to confirm deletion
        delete_button = tk.Button(self.delete_student_frame, text="Delete Student", command=self.confirm_delete)
        delete_button.grid(row=1, column=0, columnspan=2, pady=5)

    def confirm_delete(self):
        student_id = self.student_id_entry.get()
        if student_id:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with ID {student_id}?")
            if confirm:
                conn = sqlite3.connect("driving_school.db")
                c = conn.cursor()
                try:
                    c.execute("DELETE FROM students WHERE id=?", (student_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Student deleted successfully!") 

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete student: {e}")
                finally:
                    conn.close()
                    self.student_id_entry.delete(0, tk.END)
# Instructor Management Window
class InstructorManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Buttons
        self.add_instructor_button = tk.Button(self.window, text="Add Instructor", command=self.show_add_instructor_form)
        self.add_instructor_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.view_instructors_button = tk.Button(self.window, text="View Instructors", command=self.view_instructors)
        self.view_instructors_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.delete_instructor_button = tk.Button(self.window, text="Delete Instructor", command=self.delete_instructor)
        self.delete_instructor_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Configure column weights
        for i in range(3):
            self.window.columnconfigure(i, weight=1)

        # Frames for forms (initially hidden)
        self.add_instructor_frame = tk.Frame(self.window)
        self.add_instructor_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.add_instructor_frame.grid_remove()

        self.view_instructors_frame = tk.Frame(self.window)
        self.view_instructors_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.view_instructors_frame.grid_remove()

        self.delete_instructor_frame = tk.Frame(self.window)
        self.delete_instructor_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.delete_instructor_frame.grid_remove()

    def show_add_instructor_form(self):
        self.hide_all_forms()
        self.add_instructor_frame.grid()

        # Create labels and entry fields for the add instructor form within the frame
        tk.Label(self.add_instructor_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.add_instructor_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.add_instructor_frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.add_instructor_frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.add_instructor_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.add_instructor_frame)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Function to handle the submit button click
        def submit_data():
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("INSERT INTO instructors (name, phone, email) VALUES (?, ?, ?)",
                          (name, phone, email))
                conn.commit()
                messagebox.showinfo("Success", "Instructor added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add instructor: {e}")
            finally:
                conn.close()
                self.clear_add_instructor_form()

        # Create a submit button
        submit_button = tk.Button(self.add_instructor_frame, text="Submit", command=submit_data)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def clear_add_instructor_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def view_instructors(self):
        self.hide_all_forms()
        self.view_instructors_frame.grid()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM instructors")
        instructors = c.fetchall()
        conn.close()

        # Clear existing widgets in the frame
        for widget in self.view_instructors_frame.winfo_children():
            widget.destroy()

        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.view_instructors_frame)
        scrollbar = ttk.Scrollbar(self.view_instructors_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        inner_frame = tk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=inner_frame, anchor="nw")  # Assign to canvas_window

        # Create labels to display instructor details within the inner frame
        for i, instructor in enumerate(instructors):
            instructor_details = f"""
            ID: {instructor[0]}
            Name: {instructor[1]}
            Phone: {instructor[2]}
            Email: {instructor[3]}
            """
            tk.Label(inner_frame, text=instructor_details, justify="left").grid(row=i, column=0, sticky="w")

        # Update canvas scroll region (bind to configure event)
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_canvas_configure)

    def delete_instructor(self):
        self.hide_all_forms()
        self.delete_instructor_frame.grid()

        # Create input field for instructor ID
        tk.Label(self.delete_instructor_frame, text="Enter Instructor ID to delete:").grid(row=0, column=0, padx=5, pady=5)
        self.instructor_id_entry = tk.Entry(self.delete_instructor_frame)
        self.instructor_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create button to confirm deletion
        delete_button = tk.Button(self.delete_instructor_frame, text="Delete Instructor", command=self.confirm_delete)
        delete_button.grid(row=1, column=0, columnspan=2, pady=5)

    def confirm_delete(self):
        instructor_id = self.instructor_id_entry.get()
        if instructor_id:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete instructor with ID {instructor_id}?")
            if confirm:
                conn = sqlite3.connect("driving_school.db")
                c = conn.cursor()
                try:
                    c.execute("DELETE FROM instructors WHERE id=?", (instructor_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Instructor deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete instructor: {e}")
                finally:
                    conn.close()
                    self.instructor_id_entry.delete(0, tk.END)

    def hide_all_forms(self):
        self.add_instructor_frame.grid_remove()
        self.view_instructors_frame.grid_remove()
        self.delete_instructor_frame.grid_remove()

# Lesson Management Window
class LessonManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Buttons
        self.book_lesson_button = tk.Button(self.window, text="Book Lesson", command=self.show_book_lesson_form)
        self.book_lesson_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.view_lessons_button = tk.Button(self.window, text="View Lessons", command=self.view_lessons)
        self.view_lessons_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.delete_lesson_button = tk.Button(self.window, text="Delete Lesson", command=self.delete_lesson)
        self.delete_lesson_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Configure column weights (3 columns now)
        for i in range(3):  
            self.window.columnconfigure(i, weight=1)

        # Frames for forms (initially hidden)
        self.book_lesson_frame = tk.Frame(self.window)
        self.book_lesson_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.book_lesson_frame.grid_remove()

        self.view_lessons_frame = tk.Frame(self.window)
        self.view_lessons_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.view_lessons_frame.grid_remove()

        self.delete_lesson_frame = tk.Frame(self.window)
        self.delete_lesson_frame.grid(row=1, column=0, columnspan=3, pady=10)
        self.delete_lesson_frame.grid_remove()

    def show_book_lesson_form(self):
        self.hide_all_forms()
        self.book_lesson_frame.grid()

        # Create labels and entry fields for booking lesson within the frame
        tk.Label(self.book_lesson_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = tk.Entry(self.book_lesson_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.book_lesson_frame, text="Instructor ID:").grid(row=1, column=0, padx=5, pady=5)
        self.instructor_id_entry = tk.Entry(self.book_lesson_frame)
        self.instructor_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.book_lesson_frame, text="Lesson Type:").grid(row=2, column=0, padx=5, pady=5)
        self.lesson_type_var = tk.StringVar()
        lesson_type_combobox = ttk.Combobox(self.book_lesson_frame, textvariable=self.lesson_type_var)
        lesson_type_combobox['values'] = ('Introductory', 'Standard', 'Pass Plus', 'Driving Test')
        lesson_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.book_lesson_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.book_lesson_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Function to handle the submit button click
        def submit_data():
            student_id = self.student_id_entry.get()
            instructor_id = self.instructor_id_entry.get()
            lesson_type = self.lesson_type_var.get()
            date = self.date_entry.get()

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            try:
                c.execute("INSERT INTO lessons (student_id, instructor_id, lesson_type, date, status) VALUES (?, ?, ?, ?, 'Booked')",
                          (student_id, instructor_id, lesson_type, date))
                conn.commit()
                messagebox.showinfo("Success", "Lesson booked successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to book lesson: {e}")
            finally:
                conn.close()
                self.clear_book_lesson_form()

        # Create a submit button
        submit_button = tk.Button(self.book_lesson_frame, text="Submit", command=submit_data)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def clear_book_lesson_form(self):
        self.student_id_entry.delete(0, tk.END)
        self.instructor_id_entry.delete(0, tk.END)
        self.lesson_type_var.set("")
        self.date_entry.delete(0, tk.END)

    def view_lessons(self):
        self.hide_all_forms()
        self.view_lessons_frame.grid()

        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM lessons")
        lessons = c.fetchall()
        conn.close()

        # Clear existing widgets in the frame
        for widget in self.view_lessons_frame.winfo_children():
            widget.destroy()

        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.view_lessons_frame)
        scrollbar = ttk.Scrollbar(self.view_lessons_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas to hold the labels
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Create labels to display lesson details within the inner frame
        for i, lesson in enumerate(lessons):
            lesson_details = f"""
            ID: {lesson[0]}
            Student ID: {lesson[1]}
            Instructor ID: {lesson[2]}
            Lesson Type: {lesson[3]}
            Date: {lesson[4]}
            Status: {lesson[5]}
            """
            tk.Label(inner_frame, text=lesson_details, justify="left").grid(row=i, column=0, sticky="w")

        # Update canvas scroll region
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

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

# Reporting Window
class Reporting:
    def __init__(self, parent_frame):
        self.window = parent_frame

        # Buttons
        self.generate_report_button = tk.Button(self.window, text="Generate Report", command=self.show_report)
        self.generate_report_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.student_progress_button = tk.Button(self.window, text="Student Progress", command=self.show_student_progress_form)
        self.student_progress_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

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

    def show_student_progress_form(self):
        self.hide_all_forms()  # Hide other forms
        self.student_progress_frame.grid()  # Show the student progress form

        # Create input field for student ID
        tk.Label(self.student_progress_frame, text="Enter Student ID:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = tk.Entry(self.student_progress_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create button to calculate progress
        calculate_button = tk.Button(self.student_progress_frame, text="Calculate Progress", command=self.calculate_progress)
        calculate_button.grid(row=1, column=0, columnspan=2, pady=5)

    def calculate_progress(self):
        student_id = self.student_id_entry.get()
        if student_id:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT lesson_type FROM lessons WHERE student_id=?", (student_id,))
            lessons = c.fetchall()
            conn.close()

            total_progress = 0
            for lesson in lessons:
                try:
                    lesson_level = int(lesson[0].split(" ")[1])
                    total_progress += lesson_level * 10
                except (ValueError, IndexError):
                    messagebox.showerror("Error", "Invalid lesson type format in database.")
                    return

            # Display the progress in a label within the frame
            result_label = tk.Label(self.student_progress_frame, text=f"Student ID: {student_id}\nProgress: {total_progress}%", justify="left")
            result_label.grid(row=2, column=0, columnspan=2, pady=5)

    def hide_all_forms(self):
        self.report_frame.grid_remove()
        self.student_progress_frame.grid_remove()


# Main Program
if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = Application(root)
    root.mainloop()