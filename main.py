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
        self.root.geometry("800x400")  # Increased window width

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, side=tk.LEFT, fill=tk.Y)

        self.create_widgets()

        # Create a frame for the right side content
        self.right_frame = tk.Frame(self.root, width=400, height=400)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        # Buttons for different management systems
        tk.Button(self.main_frame, text="Student Management", width=20, 
                  command=lambda: self.open_management_window(StudentManagement)).grid(row=0, column=0, pady=5)
        tk.Button(self.main_frame, text="Instructor Management", width=20, 
                  command=lambda: self.open_management_window(InstructorManagement)).grid(row=1, column=0, pady=5)
        tk.Button(self.main_frame, text="Lesson Management", width=20, 
                  command=lambda: self.open_management_window(LessonManagement)).grid(row=2, column=0, pady=5)
        tk.Button(self.main_frame, text="Reporting", width=20, 
                  command=lambda: self.open_management_window(Reporting)).grid(row=3, column=0, pady=5)

    def open_management_window(self, window_class):
        # Clear any existing widgets in the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Create an instance of the window class and pass the right frame as the parent
        window_instance = window_class(self.right_frame)  

# Student Management Window
class StudentManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame  

        self.add_student_button = tk.Button(self.window, text="Add Student", command=self.add_student)
        self.add_student_button.pack(pady=10)
        
        self.view_students_button = tk.Button(self.window, text="View Students", command=self.view_students)
        self.view_students_button.pack(pady=10)

        self.delete_student_button = tk.Button(self.window, text="Delete Student", command=self.delete_student)
        self.delete_student_button.pack(pady=10)
    
    def add_student(self):
        # Create a new window for the form
        add_student_window = tk.Toplevel(self.window)
        add_student_window.title("Add Student")

        # Create labels and entry fields for each student attribute
        tk.Label(add_student_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(add_student_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_student_window, text="Address:").grid(row=1, column=0, padx=5, pady=5)
        address_entry = tk.Entry(add_student_window)
        address_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_student_window, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(add_student_window)
        phone_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_student_window, text="Progress:").grid(row=3, column=0, padx=5, pady=5)
        progress_entry = tk.Entry(add_student_window)
        progress_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(add_student_window, text="Payment Status:").grid(row=4, column=0, padx=5, pady=5)
        payment_status_entry = tk.Entry(add_student_window)
        payment_status_entry.grid(row=4, column=1, padx=5, pady=5)

        # Function to handle the submit button click
        def submit_data():
            name = name_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            progress = progress_entry.get()
            payment_status = payment_status_entry.get()

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO students (name, address, phone, progress, payment_status) VALUES (?, ?, ?, ?, ?)",
                      (name, address, phone, progress, payment_status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student added successfully!")
            add_student_window.destroy()  # Close the form window

        # Create a submit button
        submit_button = tk.Button(add_student_window, text="Submit", command=submit_data)
        submit_button.grid(row=5, column=0, columnspan=2, pady=10)
    
    def view_students(self):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()
        conn.close()
        
        student_list_window = tk.Toplevel(self.window)
        student_list_window.title("Students List")
        
        for student in students:
            tk.Label(student_list_window, text=f"ID: {student[0]}, Name: {student[1]}, Progress: {student[4]}").pack(pady=5)

    def delete_student(self):
        student_id = simpledialog.askinteger("Input", "Enter student ID to delete:")
        if student_id is not None:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("DELETE FROM students WHERE id=?", (student_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student deleted successfully!")

# Instructor Management Window
class InstructorManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        self.add_instructor_button = tk.Button(self.window, text="Add Instructor", command=self.add_instructor)
        self.add_instructor_button.pack(pady=10)
        
        self.view_instructors_button = tk.Button(self.window, text="View Instructors", command=self.view_instructors)
        self.view_instructors_button.pack(pady=10)
    
        self.delete_instructor_button = tk.Button(self.window, text="Delete Instructor", command=self.delete_instructor)
        self.delete_instructor_button.pack(pady=10)

    def add_instructor(self):
        # Create a new window for the form
        add_instructor_window = tk.Toplevel(self.window)
        add_instructor_window.title("Add Instructor")

        # Create labels and entry fields for each instructor attribute
        tk.Label(add_instructor_window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(add_instructor_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_instructor_window, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        phone_entry = tk.Entry(add_instructor_window)
        phone_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_instructor_window, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        email_entry = tk.Entry(add_instructor_window)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        # Function to handle the submit button click
        def submit_data():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO instructors (name, phone, email) VALUES (?, ?, ?)",
                      (name, phone, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Instructor added successfully!")
            add_instructor_window.destroy()  # Close the form window

        # Create a submit button
        submit_button = tk.Button(add_instructor_window, text="Submit", command=submit_data)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)
    
    def view_instructors(self):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM instructors")
        instructors = c.fetchall()
        conn.close()
        
        instructor_list_window = tk.Toplevel(self.window)
        instructor_list_window.title("Instructors List")
        
        for instructor in instructors:
            tk.Label(instructor_list_window, text=f"ID: {instructor[0]}, Name: {instructor[1]}").pack(pady=5)

    def delete_instructor(self):
        instructor_id = simpledialog.askinteger("Input", "Enter instructor ID to delete:")
        if instructor_id is not None:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("DELETE FROM instructors WHERE id=?", (instructor_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Instructor deleted successfully!")

# Lesson Management Window
class LessonManagement:
    def __init__(self, parent_frame):
        self.window = parent_frame

        self.book_lesson_button = tk.Button(self.window, text="Book Lesson", command=self.book_lesson)
        self.book_lesson_button.pack(pady=10)

        self.view_lessons_button = tk.Button(self.window, text="View Lessons", command=self.view_lessons)
        self.view_lessons_button.pack(pady=10)

        self.delete_lesson_button = tk.Button(self.window, text="Delete Lesson", command=self.delete_lesson)
        self.delete_lesson_button.pack(pady=10)
    
    def book_lesson(self):
        # Create a new window for the form
        book_lesson_window = tk.Toplevel(self.window)
        book_lesson_window.title("Book Lesson")

        # Create labels and entry fields for each lesson attribute
        tk.Label(book_lesson_window, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        student_id_entry = tk.Entry(book_lesson_window)
        student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(book_lesson_window, text="Instructor ID:").grid(row=1, column=0, padx=5, pady=5)
        instructor_id_entry = tk.Entry(book_lesson_window)
        instructor_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(book_lesson_window, text="Lesson Type:").grid(row=2, column=0, padx=5, pady=5)

        # Create a combobox for lesson type with levels 1 to 10
        lesson_type_var = tk.StringVar()
        lesson_type_combobox = ttk.Combobox(book_lesson_window, textvariable=lesson_type_var)
        lesson_type_combobox['values'] = tuple(f"Level {i}" for i in range(1, 11))
        lesson_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(book_lesson_window, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        date_entry = tk.Entry(book_lesson_window)
        date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Function to handle the submit button click
        def submit_data():
            student_id = student_id_entry.get()
            instructor_id = instructor_id_entry.get()
            lesson_type = lesson_type_var.get()  # Get the lesson type from the combobox
            date = date_entry.get()

            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("INSERT INTO lessons (student_id, instructor_id, lesson_type, date, status) VALUES (?, ?, ?, ?, 'Booked')",
                      (student_id, instructor_id, lesson_type, date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Lesson booked successfully!")
            book_lesson_window.destroy()  # Close the form window

        # Create a submit button
        submit_button = tk.Button(book_lesson_window, text="Submit", command=submit_data)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def view_lessons(self):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM lessons")
        lessons = c.fetchall()
        conn.close()

        lessons_list_window = tk.Toplevel(self.window)
        lessons_list_window.title("Lessons List")

        for lesson in lessons:
            lesson_details = f"""
            ID: {lesson[0]}
            Student ID: {lesson[1]}
            Instructor ID: {lesson[2]}
            Lesson Type: {lesson[3]}
            Date: {lesson[4]}
            Status: {lesson[5]}
            """
            tk.Label(lessons_list_window, text=lesson_details, justify="left").pack(pady=5)

    def delete_lesson(self):
        lesson_id = simpledialog.askinteger("Input", "Enter lesson ID to delete:")
        if lesson_id is not None:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("DELETE FROM lessons WHERE id=?", (lesson_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Lesson deleted successfully!")


# Reporting Window
class Reporting:
    def __init__(self, parent_frame):  # Accept parent_frame as argument
        self.window = parent_frame  # Set self.window to parent_frame

        self.generate_report_button = tk.Button(self.window, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(pady=10)

        self.student_progress_button = tk.Button(self.window, text="Student Progress", command=self.show_student_progress)
        self.student_progress_button.pack(pady=10)

    def generate_report(self):
        conn = sqlite3.connect("driving_school.db")
        c = conn.cursor()

        # Get total lessons booked
        c.execute("SELECT COUNT(*) FROM lessons WHERE status = 'Booked'")
        lessons_count = c.fetchone()[0]

        # Get total students
        c.execute("SELECT COUNT(*) FROM students")
        students_count = c.fetchone()[0]

        # Get total instructors
        c.execute("SELECT COUNT(*) FROM instructors")
        instructors_count = c.fetchone()[0]

        conn.close()

        report_text = f"""
        Total lessons booked: {lessons_count}
        Total students: {students_count}
        Total instructors: {instructors_count}
        """
        messagebox.showinfo("Report", report_text)

    def show_student_progress(self):
        student_id = simpledialog.askinteger("Input", "Enter student ID:")
        if student_id is not None:
            conn = sqlite3.connect("driving_school.db")
            c = conn.cursor()
            c.execute("SELECT lesson_type FROM lessons WHERE student_id=?", (student_id,))
            lessons = c.fetchall()
            conn.close()

            total_progress = 0
            for lesson in lessons:
                lesson_level = int(lesson[0].split(" ")[1])  # Extract level from "Level X"
                total_progress += lesson_level * 10  # Calculate progress based on level

            messagebox.showinfo("Student Progress", f"Student ID: {student_id}\nProgress: {total_progress}%")



# Main Program
if __name__ == "__main__":
    create_db()
    root = tk.Tk()
    app = Application(root)
    root.mainloop()