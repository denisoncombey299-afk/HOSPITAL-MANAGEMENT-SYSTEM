import tkinter as tk
from tkinter import messagebox

# ---------------------------
# DATA STORAGE
# ---------------------------
users = {}
appointments = []

doctors = [
    {"name": "Dr. Smith", "specialty": "General"},
    {"name": "Dr. Johnson", "specialty": "Dentist"},
    {"name": "Dr. Brown", "specialty": "Cardiologist"},
    {"name": "Dr. Adams", "specialty": "Neurologist"},
    {"name": "Dr. Wilson", "specialty": "Pediatrics"},
]

illness_map = {
    "Tooth Pain": "Dr. Johnson",
    "Heart Problem": "Dr. Brown",
    "Headache": "Dr. Adams",
    "Child Illness": "Dr. Wilson",
    "General Checkup": "Dr. Smith",
}

current_user = None


# ---------------------------
# LOGIN PAGE
# ---------------------------
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital System - Login")
        self.root.geometry("400x350")

        tk.Label(root, text="Login", font=("Arial", 20)).pack(pady=20)

        tk.Label(root, text="Username").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=10)
        tk.Button(root, text="Create Account", command=self.register).pack()

    def login(self):
        global current_user
        u = self.username.get().strip()
        p = self.password.get().strip()

        if u in users and users[u] == p:
            current_user = u
            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid login")

    def register(self):
        win = tk.Toplevel(self.root)
        win.title("Register")
        win.geometry("300x250")

        tk.Label(win, text="Create Account").pack()

        u_entry = tk.Entry(win)
        p_entry = tk.Entry(win, show="*")

        tk.Label(win, text="Username").pack()
        u_entry.pack()

        tk.Label(win, text="Password").pack()
        p_entry.pack()

        def save():
            u = u_entry.get().strip()
            p = p_entry.get().strip()

            if u == "" or p == "":
                messagebox.showerror("Error", "Fill all fields")
                return

            users[u] = p
            messagebox.showinfo("Success", "Account created")
            win.destroy()

        tk.Button(win, text="Save", command=save).pack()


# ---------------------------
# DASHBOARD
# ---------------------------
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("500x450")

        tk.Label(root, text=f"Welcome {current_user}", font=("Arial", 14)).pack(pady=10)

        tk.Button(root, text="Book Appointment", width=30, command=self.book).pack(pady=5)
        tk.Button(root, text="View Appointments", width=30, command=self.view).pack(pady=5)
        tk.Button(root, text="Search Appointment", width=30, command=self.search).pack(pady=5)
        tk.Button(root, text="Logout", width=30, command=self.logout).pack(pady=5)

    def book(self):
        BookAppointment(self.root)

    def view(self):
        ViewAppointments(self.root)

    def search(self):
        SearchAppointment(self.root)

    def logout(self):
        self.root.destroy()
        main()


# ---------------------------
# BOOK APPOINTMENT
# ---------------------------
class BookAppointment:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Book Appointment")
        self.win.geometry("400x500")

        # Patient info
        tk.Label(self.win, text="Name").pack()
        self.name = tk.Entry(self.win)
        self.name.pack()

        tk.Label(self.win, text="Age").pack()
        self.age = tk.Entry(self.win)
        self.age.pack()

        tk.Label(self.win, text="Gender").pack()
        self.gender = tk.Entry(self.win)
        self.gender.pack()

        tk.Label(self.win, text="Contact").pack()
        self.contact = tk.Entry(self.win)
        self.contact.pack()

        # Illness
        tk.Label(self.win, text="Illness").pack()
        self.illness = tk.StringVar(self.win)
        self.illness.set("General Checkup")
        tk.OptionMenu(self.win, self.illness, *illness_map.keys()).pack()

        tk.Label(self.win, text="Symptoms").pack()
        self.symptoms = tk.Entry(self.win)
        self.symptoms.pack()

        tk.Label(self.win, text="Date").pack()
        self.date = tk.Entry(self.win)
        self.date.pack()

        tk.Label(self.win, text="Time").pack()
        self.time = tk.Entry(self.win)
        self.time.pack()

        tk.Button(self.win, text="Book", command=self.save).pack(pady=10)

    def save(self):
        doctor = illness_map.get(self.illness.get(), "Dr. Smith")

        data = {
            "patient": self.name.get().strip(),
            "age": self.age.get().strip(),
            "gender": self.gender.get().strip(),
            "contact": self.contact.get().strip(),
            "illness": self.illness.get(),
            "symptoms": self.symptoms.get().strip(),
            "doctor": doctor,
            "date": self.date.get().strip(),
            "time": self.time.get().strip()
        }

        # validation
        for v in data.values():
            if v == "":
                messagebox.showerror("Error", "Fill all fields")
                return

        # prevent duplicate booking
        for a in appointments:
            if a["doctor"] == data["doctor"] and a["date"] == data["date"] and a["time"] == data["time"]:
                messagebox.showerror("Error", "Doctor already booked at this time")
                return

        appointments.append(data)
        messagebox.showinfo("Success", f"Booked with {doctor}")
        self.win.destroy()


# ---------------------------
# VIEW APPOINTMENTS
# ---------------------------
class ViewAppointments:
    def __init__(self, root):
        win = tk.Toplevel(root)
        win.title("Appointments")
        win.geometry("450x400")

        if not appointments:
            tk.Label(win, text="No appointments").pack()
            return

        for i, a in enumerate(appointments, 1):
            text = f"""
{i}.
Patient: {a['patient']}
Age: {a['age']}
Gender: {a['gender']}
Illness: {a['illness']}
Symptoms: {a['symptoms']}
Doctor: {a['doctor']}
Date: {a['date']}
Time: {a['time']}
Contact: {a['contact']}
"""
            tk.Label(win, text=text, justify="left", anchor="w").pack()


# ---------------------------
# SEARCH APPOINTMENT
# ---------------------------
class SearchAppointment:
    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Search")
        self.win.geometry("300x200")

        tk.Label(self.win, text="Enter Patient Name").pack()
        self.search = tk.Entry(self.win)
        self.search.pack()

        tk.Button(self.win, text="Search", command=self.find).pack()

    def find(self):
        name = self.search.get().strip()

        results = [a for a in appointments if a["patient"] == name]

        if not results:
            messagebox.showinfo("Result", "No record found")
            return

        msg = ""
        for a in results:
            msg += f"{a['patient']} - {a['illness']} - {a['doctor']} - {a['date']} {a['time']}\n"

        messagebox.showinfo("Result", msg)


# ---------------------------
# START APP
# ---------------------------
def open_dashboard():
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()


def main():
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
