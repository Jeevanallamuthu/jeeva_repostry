import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jee1130@",
    database="StudentDB"
)
mycursor = mydb.cursor()

def validate_inputs():
    if not name_entry.get() or not age_entry.get().isdigit() or not gender_entry.get() or not course_entry.get():
        messagebox.showerror("Error", "Please fill in all fields correctly")
        return False
    return True

def add_student():
    if not validate_inputs():
        return
    try:
        sql = "INSERT INTO Students (name, age, gender, course) VALUES (%s, %s, %s, %s)"
        val = (name_entry.get(), age_entry.get(), gender_entry.get(), course_entry.get())
        mycursor.execute(sql, val)
        mydb.commit()
        fetch_data()
        messagebox.showinfo("Success", "Record added successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def fetch_data():
    mycursor.execute("SELECT * FROM Students")
    rows = mycursor.fetchall()
    if len(rows) != 0:
        student_tree.delete(*student_tree.get_children())
        for row in rows:
            student_tree.insert("", END, values=row)
        mydb.commit()

def get_cursor(event):
    cursor_row = student_tree.focus()
    contents = student_tree.item(cursor_row)
    row = contents['values']
    if row:
        name_entry.delete(0, END)
        name_entry.insert(END, row[1])
        age_entry.delete(0, END)
        age_entry.insert(END, row[2])
        gender_entry.delete(0, END)
        gender_entry.insert(END, row[3])
        course_entry.delete(0, END)
        course_entry.insert(END, row[4])

def update_student():
    if not validate_inputs():
        return
    try:
        sql = "UPDATE Students SET name = %s, age = %s, gender = %s, course = %s WHERE id = %s"
        val = (name_entry.get(), age_entry.get(), gender_entry.get(), course_entry.get(), student_tree.item(student_tree.focus())['values'][0])
        mycursor.execute(sql, val)
        mydb.commit()
        fetch_data()
        messagebox.showinfo("Success", "Record updated successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_student():
    try:
        sql = "DELETE FROM Students WHERE id = %s"
        val = (student_tree.item(student_tree.focus())['values'][0],)
        mycursor.execute(sql, val)
        mydb.commit()
        fetch_data()
        messagebox.showinfo("Success", "Record deleted successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter setup
root = Tk()
root.title("Student Data Entry")
root.geometry("800x600")

# Background Image
background_image = Image.open("studentproject_bg.jpg")
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Frames
input_frame = Frame(root, bd=10, relief=RIDGE, padx=10, bg="lightblue")
input_frame.pack(side=TOP, fill=X)

button_frame = Frame(root, bd=10, relief=RIDGE, padx=10, bg="lightblue")
button_frame.pack(side=TOP, fill=X)

tree_frame = Frame(root, bd=10, relief=RIDGE, padx=10, bg="lightblue")
tree_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

# Input Labels and Entry Widgets
Label(input_frame, text="Name").grid(row=0, column=0, padx=10, pady=10)
Label(input_frame, text="Age").grid(row=0, column=1, padx=10, pady=10)
Label(input_frame, text="Gender").grid(row=0, column=2, padx=10, pady=10)
Label(input_frame, text="Course").grid(row=0, column=3, padx=10, pady=10)

name_entry = Entry(input_frame)
age_entry = Entry(input_frame)
gender_entry = Entry(input_frame)
course_entry = Entry(input_frame)

name_entry.grid(row=1, column=0, padx=10, pady=10)
age_entry.grid(row=1, column=1, padx=10, pady=10)
gender_entry.grid(row=1, column=2, padx=10, pady=10)
course_entry.grid(row=1, column=3, padx=10, pady=10)

# Buttons for CRUD Operations
Button(button_frame, text="Add", command=add_student).grid(row=0, column=0, padx=10, pady=10)
Button(button_frame, text="Update", command=update_student).grid(row=0, column=1, padx=10, pady=10)
Button(button_frame, text="Delete", command=delete_student).grid(row=0, column=2, padx=10, pady=10)

# Treeview for Displaying Data
scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(tree_frame, orient=VERTICAL)

student_tree = ttk.Treeview(tree_frame, columns=("id", "name", "age", "gender", "course"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=student_tree.xview)
scroll_y.config(command=student_tree.yview)

student_tree.heading("id", text="ID")
student_tree.heading("name", text="Name")
student_tree.heading("age", text="Age")
student_tree.heading("gender", text="Gender")
student_tree.heading("course", text="Course")
student_tree['show'] = 'headings'

student_tree.column("id", width=50)
student_tree.column("name", width=150)
student_tree.column("age", width=50)
student_tree.column("gender", width=100)
student_tree.column("course", width=150)

student_tree.pack(fill=BOTH, expand=True)

# Bind the treeview to get data on click
student_tree.bind("<ButtonRelease-1>", get_cursor)

# Fetch initial data
fetch_data()

# Run the Tkinter event loop
root.mainloop()
