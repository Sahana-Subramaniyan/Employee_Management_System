#importing
import os
import mysql.connector as m
from tkinter import *
from tkinter import messagebox
from dotenv import load_dotenv

#load enviroinment vaiables
load_dotenv()

# connecting mysql and python
con = m.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cur = con.cursor()

# Tkinter window
root = Tk()
root.title("Employee Management System")
root.geometry("1000x650")
root.configure(bg="lightgoldenrodyellow")

Label(root,text="EMPLOYEE MANAGEMENT SYSTEM",font=("Stencil", 18, "bold"),fg="lightgoldenrod4", bg="lightgoldenrodyellow",).pack(pady=(10, 45))

# navigation
nav_frame = Frame(root,bg="lightgoldenrodyellow")
nav_frame.pack(pady=10)
Button(nav_frame,text="Add New Employee",width=25,pady=5,bg="palegoldenrod",command=lambda: show_add()).pack(side=LEFT, padx=20)
Button(nav_frame,text="View Employees",width=25,pady=5,bg="palegoldenrod",command=lambda: show_view()).pack(side=LEFT, padx=20)

# content
content = Frame(root, bg="lightgoldenrodyellow")
content.pack(fill=BOTH, expand=True)

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

# add employee
def show_add():
    clear_content()
    Label(content, text="Add New Employee", font=("Stencil", 14, "bold"),fg="lightgoldenrod4",bg="lightgoldenrodyellow").pack(pady=15)
    form = Frame(content,bg="lightgoldenrodyellow")
    form.pack()
    labels = ["Employee ID", "Name", "Department", "Salary", "Phone"]
    entries = {}

    for i, lbl in enumerate(labels):
        Label(form, text=lbl, width=15,bg="palegoldenrod", anchor="w").grid(row=i, column=0, pady=6, padx=5)
        ent = Entry(form, width=30)
        ent.grid(row=i, column=1, pady=6, padx=5)
        entries[lbl] = ent

    def add_employee():
        if entries["Employee ID"].get() == "":
            messagebox.showerror("Error", "Employee ID is required")
            return
        try:
            cur.execute(
                "INSERT INTO employee VALUES (%s,%s,%s,%s,%s)",
                (
                    entries["Employee ID"].get(),
                    entries["Name"].get(),
                    entries["Department"].get(),
                    entries["Salary"].get(),
                    entries["Phone"].get()))
            con.commit()
            messagebox.showinfo("Success", "Employee Added Successfully")
            show_add()
        except:
            messagebox.showerror("Error", "Employee ID already exists")

    Button(content, text="Add", width=18,bg="palegoldenrod", command=add_employee).pack(pady=20)

# view,search,delete and edit
def show_view():
    clear_content()
    Label(content, text="View Employees", font=("Stencil", 14, "bold"),fg="lightgoldenrod4",bg="lightgoldenrodyellow").pack(pady=10)

    #search
    search_frame = Frame(content,bg="palegoldenrod")
    search_frame.pack(pady=10)
    Label(search_frame, text="Search by Employee ID",bg="lightgoldenrod4", fg="lightgoldenrodyellow").pack(side=LEFT, padx=5)
    search_entry = Entry(search_frame, width=20)
    search_entry.pack(side=LEFT, padx=5,)

    def search_employee():
        if search_entry.get() == "":
            load_table()
        else:
            load_table(search_entry.get())

    Button(search_frame, text="Search",bg="palegoldenrod",width=10, command=search_employee).pack(side=LEFT, padx=5)

    # table
    table = Frame(content,bg="palegoldenrod")
    table.pack(pady=10)

    selected = {}

    def load_table(empid=None):
        for w in table.winfo_children():
            w.destroy()

        headers = ["Select", "ID", "Name", "Dept", "Salary", "Phone"]
        for col, h in enumerate(headers):
            Label(table, text=h, width=15,bg="palegoldenrod", relief=RIDGE).grid(row=0, column=col)

        if empid:
            cur.execute("SELECT * FROM employee WHERE empid=%s", (empid,))
        else:
            cur.execute("SELECT * FROM employee")

        records = cur.fetchall()
        selected.clear()

        for r, row in enumerate(records, start=1):
            var = IntVar()
            Checkbutton(table, variable=var,bg="palegoldenrod").grid(row=r, column=0)
            selected[row[0]] = var

            for c, val in enumerate(row):
                Label(table, text=val, width=15, bg="palegoldenrod",relief=RIDGE).grid(row=r, column=c+1)

    load_table()

    # buttons
    action_frame = Frame(content,bg="palegoldenrod")
    action_frame.pack(pady=20)

    def delete_selected():
        ids = [eid for eid, v in selected.items() if v.get() == 1]
        if not ids:
            messagebox.showerror("Error", "Select employee(s) to delete")
            return
        for eid in ids:
            cur.execute("DELETE FROM employee WHERE empid=%s", (eid,))
        con.commit()
        messagebox.showinfo("Deleted", "Selected employee(s) deleted")
        show_view()

    def edit_selected():
        ids = [eid for eid, v in selected.items() if v.get() == 1]
        if len(ids) != 1:
            messagebox.showerror("Error", "Select exactly ONE employee to edit")
            return
        show_edit(ids[0])

    Button(action_frame, text="Edit Selected", width=18, bg="palegoldenrod", command=edit_selected).pack(side=LEFT, padx=15)
    Button(action_frame, text="Delete Selected", width=18, bg="palegoldenrod",command=delete_selected).pack(side=LEFT, padx=15)

# edit employee
def show_edit(empid):
    clear_content()

    cur.execute("SELECT * FROM employee WHERE empid=%s", (empid,))
    data = cur.fetchone()

    Label(content, text="Edit Employee", font=("Stencil", 14, "bold"),bg="palegoldenrod").pack(pady=15)

    form = Frame(content,bg="palegoldenrod")
    form.pack()

    labels = ["Employee ID", "Name", "Department", "Salary", "Phone"]
    entries = {}

    for i, lbl in enumerate(labels):
        Label(form, text=lbl, width=15,bg="palegoldenrod", anchor="w").grid(row=i, column=0, pady=6, padx=5)
        ent = Entry(form, width=30)
        ent.grid(row=i, column=1, pady=6, padx=5)
        ent.insert(0, data[i])
        if lbl == "Employee ID":
            ent.config(state=DISABLED)
        entries[lbl] = ent

    def update_employee():
        cur.execute(
            "UPDATE employee SET name=%s, department=%s, salary=%s, phno=%s WHERE empid=%s",
            (
                entries["Name"].get(),
                entries["Department"].get(),
                entries["Salary"].get(),
                entries["Phone"].get(),
                empid))
        con.commit()
        messagebox.showinfo("Updated", "Employee Updated Successfully")
        show_view()

    Button(content, text="Update", width=18,bg="palegoldenrod", command=update_employee).pack(pady=20)

# start
show_add()
root.mainloop()
