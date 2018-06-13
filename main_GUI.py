from datetime import datetime
import calendar

from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from check_data import *
from DB import *
from reports import *
import csv

#**********************************************************************************************************


class MainUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Attendance system - main screen")
        self.master.geometry("800x400+50+50")
        self.IDenter = StringVar()
        self.password = StringVar()

        self.label1 = Label(master, text="Employee attendance", font=("Arial", 16, "bold"), fg="RoyalBlue4") \
            .grid(row=0, column=0, sticky=W, pady=10)
        self.date = Label(master, text= date.today(), font=("Arial", 12, "bold"), fg="RoyalBlue4") \
            .grid(row=0, column=3, sticky=W, pady=10)
        self.clock = Label(master, text=time.strftime('%H:%M'), font=("Arial", 12, "bold"), fg="RoyalBlue4") \
            .grid(row=0, column=4, sticky=W, pady=10)
        self.label2 = Label(master, text="Please enter your employee ID and than click on Enter or Exit button",
                            fg="RoyalBlue4").grid(row=1, column=0, columnspan=4, sticky=W, pady=10)
        self.label3 = Label(master, text="Employee ID (6 digits): ", fg="RoyalBlue4").grid(row=2, column=0, sticky=E)
        self.enterID = Entry(master, textvariable=self.IDenter, width="50").grid(row=2, column=1, columnspan=2, pady=10)
        self.BotEnt = Button(master, text="Enter working", bg="DarkOliveGreen1", width="20",
                             command=lambda: self.add_attendance_log("Enter")) \
            .grid(row=3, column=1)
        self.BotEx = Button(master, text="Exit working", bg="SkyBlue1", width="20",
                            command=lambda: self.add_attendance_log("Exit")) \
            .grid(row=3, column=2)
        self.Admin_enter = Label(master, text="For admin functions please enter password: (1234)", fg="gray") \
            .grid(row=8, column=0, pady=80)
        self.entry1 = Entry(self.master, width="20", textvariable=self.password) \
            .grid(row=8, column=1, pady=80, padx=10)
        self.button1 = Button(master, text="Enter admin. functions", width="20", bg="gray", fg="white",
                              command=self.check_password).grid(row=8, column=2, pady=80, padx=10)
        self.exlabel = Button(master, text="Exit", command=self.exit, width=10).grid(row=9, column=4, pady=10)

    def check_password(self):
        password = self.password.get()
        if password == "":
            tkinter.messagebox.showerror("Error", "Please type password")
            return
        if password == "1234":
            self.open_mng_screen()
            self.password.set("")
        else:
            tkinter.messagebox.showerror("password Error", "The password is wrong, please type again")

    def open_mng_screen(self):
        rootAddManualy = Toplevel(self.master)
        MngScreen(rootAddManualy)

    def add_attendance_log(self, inout):
        ID = self.IDenter.get()
        if ID == "":
            tkinter.messagebox.showerror("Error", "Please add Employee ID and than click \"Enter\" or \"Exit\"")
            return
        if Check_emp_data.check_id_in_list(ID) is True:
            now = datetime.datetime.now()
            db = DB("attendance_log.csv")
            db.add_to_file([ID, now, inout])
            tkinter.messagebox.showinfo("Login/out successful", "Emp No. %s %s at %s/%s/%s %s:%s"
                                        % (ID, inout, now.day, now.month, now.year, now.hour, now.minute))
            self.IDenter.set("")
        else:
            tkinter.messagebox.showerror("Wrong ID", "The Emp ID is not in the employees list, please try again")
            self.IDenter.set("")

    def exit(self):
        qexit = tkinter.messagebox.askyesno("Exit", "Do you want to exit the System?")
        if qexit > 0:
            root.destroy()


# ****************************************************************************************************************

class MngScreen(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Management screen")
        self.master.geometry("900x300+100+100")

        self.add_manual = Button(master, width=30, text="Add Employee manually", command=self.open_add_screen,
                                 bg="SkyBlue1") \
            .grid(row=0, column=0, pady=10)
        self.add_list = Button(master, width=30, text="Add Employee from file", bg="SkyBlue1",
                               command=self.add_from_file) \
            .grid(row=1, column=0, pady=10)
        self.del_manual = Button(master, width=30, text="Delete Employee", command=self.open_del_screen, bg="coral1") \
            .grid(row=0, column=1, pady=10, padx=40)
        self.del_from_list = Button(master, width=30, text="Delete Employee from list/file",
                                    command = self.delete_from_file, bg="coral1") \
            .grid(row=1, column=1, pady=10, padx=40)
        self.report_by_emp = Button(master, width=34, text="Employees list",
                                    command=self.employees_report, bg="Ivory3") \
            .grid(row=0, column=2, pady=10, padx=40)
        self.report_by_emp = Button(master, width=34, text="Attendance report by employee",
                                    command=self.attendance_report_by_emp, bg="Ivory3") \
            .grid(row=1, column=2, pady=10, padx=40)
        self.report_by_month = Button(master, width=34, text="Laters report",
                                      command = self.laters_report, bg="Ivory3") \
            .grid(row=2, column=2, pady=10, padx=40)
        self.back = Button(master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=4, column=4, pady=10)

    def open_add_screen(self):
        rootAddManualy = Toplevel(self.master)
        AddManuallyUI(rootAddManualy)

    def add_from_file(self):
        rootAdd = Toplevel(self.master)
        AddFromFile(rootAdd)

    def open_del_screen(self):
        rootAddManualy = Toplevel(self.master)
        DelManuallyUI(rootAddManualy)

    def delete_from_file(self):
        rootAdd = Toplevel(self.master)
        DeleteFromFile(rootAdd)

    def employees_report(self):
        report = Reports("emp_file.csv" , "report_employees.csv",
                         ["Employee ID", "First name", "Last name", "Age", "Phone number", "Gender", "Is manager"])
        report.prepare_emp_report()
        tkinter.messagebox.showinfo("report ready",
                                                   "The report is ready, please open the \"report_employees.csv\" file")

    def attendance_report_by_emp(self):
        rootAddManualy = Toplevel(self.master)
        AttendanceReportByEmp(rootAddManualy)

    def laters_report(self):
        rootAddManualy = Toplevel(self.master)
        LatersReport(rootAddManualy)

    def closeScreen(self, w):
        w.destroy()

#*****************************************************************************************


class AddManuallyUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Add employee")
        self.master.geometry("700x400+150+150")



        self.ID = StringVar()
        self.Fname = StringVar()
        self.Lname = StringVar()
        self.year = StringVar()
        self.month = StringVar()
        self.day = StringVar()
        self.number = StringVar()
        self.gender = IntVar()
        self.mng = IntVar()

        self.label11 = Label(self.master, text="Emp ID (6 digits):").grid(row=0, column=0, sticky=E, pady=5)
        self.entry11 = Entry(self.master, textvariable=self.ID).grid(row=0, column=1, pady=5)
        self.label12 = Label(self.master, text="First name:").grid(row=1, column=0, sticky=E, pady=5)
        self.entry12 = Entry(self.master, textvariable=self.Fname).grid(row=1, column=1, pady=5)
        self.label13 = Label(self.master, text="Last name:").grid(row=2, column=0, sticky=E, pady=5)
        self.entry13 = Entry(self.master, textvariable=self.Lname).grid(row=2, column=1, pady=5)
        self.label14 = Label(self.master, text="Birth date  ").grid(row=3, column=0, sticky=E, pady=5)
        self.label15 = Label(self.master, text="Year:").grid(row=3, column=1, sticky=E, pady=5)
        self.entry15 = Entry(self.master, textvariable=self.year).grid(row=3, column=2, pady=5)
        self.label16 = Label(self.master, text="Month:").grid(row=3, column=3, sticky=E, pady=5)
        self.entry16 = Entry(self.master, textvariable=self.month).grid(row=3, column=4, pady=5)
        self.label17 = Label(self.master, text="Day:").grid(row=3, column=5, sticky=E, pady=5)
        self.entry17 = Entry(self.master, textvariable=self.day).grid(row=3, column=6, pady=5)
        self.label18 = Label(self.master, text="Phone number (digits only):").grid(row=4, column=0, sticky=E, pady=5)
        self.entry18 = Entry(self.master, textvariable=self.number).grid(row=4, column=1, pady=5)
        self.label19 = Label(self.master, text="Gender:").grid(row=5, column=0, sticky=E, pady=5)

        self.genderF = Radiobutton(self.master, text="Female", variable=self.gender, value=1) \
            .grid(row=5, column=1, pady=5, sticky=W)
        self.genderM = Radiobutton(self.master, text="Male", variable=self.gender, value=2) \
            .grid(row=5, column=2, pady=5, sticky=W)
        self.label20 = Label(self.master, text="Manager:").grid(row=6, column=0, sticky=E, pady=5)
        self.managerY = Radiobutton(self.master, text="YES", variable=self.mng, value=1) \
            .grid(row=6, column=1, pady=5, sticky=W)
        self.managerN = Radiobutton(self.master, text="NO", variable=self.mng, value=2) \
            .grid(row=6, column=2, pady=5, sticky=W)
        self.back = Button(self.master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=10, column=6, pady=10)
        self.add_button = Button(self.master, text="Add Employee to the list", bg="green", fg="white", width="40",
                                 command=self.get_data).grid(row=8, column=1, columnspan=3, pady=5)

    def get_data(self):
        ID = self.ID.get()
        Fname = self.Fname.get()
        Lname = self.Lname.get()
        year = self.year.get()
        month = self.month.get()
        day = self.day.get()
        number = self.number.get()
        gender = "Female" if self.gender.get() == 1 else "Male"
        is_manger = "Manager" if self.mng.get() == 1 else "No manager"
        emp_data = [ID, Fname, Lname, year, month, day, number, gender, is_manger]

        for i in emp_data:
            if Check_emp_data.check_empty(i) is False:
                tkinter.messagebox.showerror("Error", "There is one or more missing values")
                return
        if Check_emp_data.check_ID(ID) is False:
            tkinter.messagebox.showerror("Error", "The employee ID should include 6 digits, please try again")
            self.ID.set("")
            return
        if Check_emp_data.check_id_in_list(ID) is True:
            tkinter.messagebox.showerror("Error", "the employee is already in the list")
            self.clean_screen()
            return
        if Check_emp_data.check_name(Fname) is False:
            tkinter.messagebox.showerror("Error", "The First name should have between 6-12 letters, please try again")
            return
        if Check_emp_data.check_name(Lname) is False:
            tkinter.messagebox.showerror("Error", "The Last name should have between 6-12 letters, please try again")
            return
        if Check_emp_data.check_year(year) is False:
            tkinter.messagebox.showerror("Error", "The year is wrong, please try again")
            return
        if Check_emp_data.check_month(month) is False:
            tkinter.messagebox.showerror("Error", "The month is wrong, please try again")
            return
        if Check_emp_data.check_day(day) is False:
            tkinter.messagebox.showerror("Error", "The day is wrong, please try again")
            return
        if Check_emp_data.check_number(number) is False:
            tkinter.messagebox.showerror("Error", "The Phone number should have 6-12 digits only , please try again")
            return

        db = DB("emp_file.csv")
        db.add_to_file( emp_data)
        more_or_close = tkinter.messagebox.askyesno("Employee added",
                                                    "The employee added to the list. Do you wand to add another employee?")
        self.master.destroy() if more_or_close == 0 else self.clean_screen()
                # עדיין צריך לראות איך החלון הזה נשאר קידמי ולא מאוחורי חלון אחר



    def clean_screen (self):
        self.ID.set("")
        self.Fname.set("")
        self.Lname.set("")
        self.year.set("")
        self.month.set("")
        self.day.set("")
        self.number.set("")
        self.gender.set("")
        self.mng.set("")

    def closeScreen(self, w):
        w.destroy()
# ********************************************************************************************************************


class AddFromFile(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Add employees from file")
        self.master.geometry("800x300+150+150")

        self.label1 = Label(self.master, width=50, text="Select the file with the employees to add", fg= "navy", anchor='w') \
            .grid(row=0, column=0, pady=5)
        self.label1 = Label(self.master,
                            text="Please make sure that the file includes the data:"
                                 "Emp ID, First name, Last name, Birth year, Birth month, Birth day,\n Phone number, "
                                 "Gender: \"Female\" or \"Male\", \"Manager\" or \" Not manager\"", anchor='w') \
                        .grid(row=1, column=0,  pady=5)
        self.add_button = Button(self.master, width=20, text="Select file", bg="SkyBlue1", command=self.select_file) \
            .grid(row=2, column=1, pady=5, padx=10)
        self.back = Button(master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=3, column=1, pady=10)

    def select_file(self):
        errors_list = ""
        mistakes_count = 0
        file = filedialog.askopenfilename()
        db1 = DB(file)
        data_from_reader = db1.read_from_file()

        for row in data_from_reader:
            for i in row:
                if Check_emp_data.check_empty(i) is False:
                    tkinter.messagebox.showerror("Error", "There are missing values in the data, please add all the needed values")
                    return
        for row in data_from_reader:
            if Check_emp_data.check_ID(row[0]) is False:
                errors_list += "Employee ID %s should be 6 digits \n" % row[0]
                mistakes_count += 1
            if Check_emp_data.check_id_in_list(row[0]) is True:
                errors_list += "Employee ID %s is already in the system \n" % row[0]
                mistakes_count +=1
            if Check_emp_data.check_name(row[1]) is False:
                errors_list += "Employee %s First name %s should have between 6-12 characters \n"\
                               % (row[0], row[1])
                mistakes_count += 1
            if Check_emp_data.check_name(row[2]) is False:
                errors_list += "Employee %s Last name %s should have between 6-12 characters \n" \
                               % (row[0], row[2])
                mistakes_count += 1
            if Check_emp_data.check_year(row[3]) is False:
                errors_list += "Employee %s birth year %s does not make sense  \n" \
                               % (row[0], row[3])
                mistakes_count += 1
            if Check_emp_data.check_month(row[4]) is False:
                errors_list += "Employee %s birth month %s should be between 1-12  \n" \
                               % (row[0], row[4])
                mistakes_count += 1
            if Check_emp_data.check_day(row[5]) is False:
                errors_list += "Employee %s birth day %s should be between 1-31  \n" \
                               % (row[0], row[5])
                mistakes_count += 1
            if Check_emp_data.check_number(row[6]) is False:
                errors_list += "Employee %s Phone number %s should have 6-12 digits only  \n" \
                               % (row[0], row[6])
                mistakes_count += 1
            if str(row[7]) == "Female" or str(row[7]) == "Male":
                pass
            else:
                errors_list += "Employee %s Gender %s should be \"Female\" or \"Male\"  \n" \
                               % (row[0], row[7])
                mistakes_count += 1
            if str(row[8]) == "Manager" or str(row[8]) == "Not manager":
                pass
            else:
                errors_list += "Employee %s \"%s\" should be \"Manager\" or \"Not manager\"  \n" \
                               % (row[0], row[8])
                mistakes_count += 1
        if mistakes_count > 0:
            errors_list += "yoe have %s Error, please change and try again" % mistakes_count
            tkinter.messagebox.showinfo("Error", errors_list)
            return
        else:
            for i in data_from_reader:
                db2 = DB("emp_file.csv")
                db2.add_to_file(i)
            tkinter.messagebox.showinfo("Data added", "The data from the file added")

    def closeScreen(self, w):
        w.destroy()

#****************************************************************************************************************


class DelManuallyUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Remove employee")
        self.master.geometry("700x100+200+200")

        self.ID_to_del = StringVar()

        self.label1 = Label(self.master, width=20, text="Emp ID to remove:").grid(row=0, column=0, sticky=E, pady=5)
        self.entry1 = Entry(self.master, width=30, textvariable=self.ID_to_del).grid(row=0, column=1, pady=5)
        self.back = Button(self.master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=10, column=6, pady=10, padx=10)
        self.del_button = Button(self.master, width=20, text="Remove Employee", bg="red", command=self.del_emp) \
            .grid(row=0, column=2, pady=5, padx=10)

    def del_emp(self):
        ID = self.ID_to_del.get()

        if Check_emp_data.check_ID(ID) is False:
            tkinter.messagebox.showerror("Error", "The employee ID should include 6 digits, please try again")
            self.ID_to_del.set("")
            return
        if Check_emp_data.check_id_in_list(ID) is False:
            tkinter.messagebox.showerror("Error", "The employee is not in the list")
            self.ID_to_del.set("")
            return

        db1 = DB("emp_file.csv")
        db1.del_from_file(ID)
        more_or_close = tkinter.messagebox.askyesno("Employee removed",
                                                    "Employee No %s removed from the list."
                                                    "Do you wand to remove another employee?" % ID)
        self.master.destroy() if more_or_close == 0 else self.ID_to_del.set("")

    def closeScreen(self, w):
        w.destroy()

# ********************************************************************************************************************


class DeleteFromFile(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Remove employees from list")
        self.master.geometry("700x400+150+150")

        self.label1 = Label(self.master, width=50, text="Brows the file with the employees to remove:") \
            .grid(row=0, column=0, sticky=W, pady=5)
        self.add_button = Button(self.master, width=20, text="Select file", bg="SkyBlue1", command=self.select_file) \
            .grid(row=3, column=1, pady=5, padx=10)
        self.back = Button(master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=4, column=3, pady=10)

    def select_file(self):
        errors_list = ""
        mistakes_count = 0
        file = filedialog.askopenfilename()
        db1 = DB(file)
        data_from_reader = db1.read_from_file()

        for row in data_from_reader:
            if Check_emp_data.check_ID(row[0]) is False:
                errors_list += "Employee ID %s should be 6 digits \n" % row[0]
                mistakes_count += 1
            if Check_emp_data.check_id_in_list(row[0]) is False:
                errors_list += "Employee ID %s is is not in the system \n" % row[0]
                mistakes_count += 1
        if mistakes_count > 0:
            errors_list += "yoe have %s Error, please change and try again" %mistakes_count
            tkinter.messagebox.showinfo("Error", errors_list)
            return
        else:
            for row in data_from_reader:
                ID_to_del = row[0]
                db2 = DB("emp_file.csv")
                db2.del_from_file(ID_to_del)
            tkinter.messagebox.showinfo("Employees removed", "The employees removed from the list")


    def closeScreen(self, w):
        w.destroy()

#*****************************************************************************************************************


class AttendanceReportByEmp(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Attendance report by employee")
        self.master.geometry("700x300+200+200")

        self.ID = StringVar()
        self.from_month = StringVar()
        self.from_year = StringVar()
        self.until_month = StringVar()
        self.until_year = StringVar()

        self.label11 = Label(self.master, text="Emp ID (6 digits):").grid(row=0, column=0, sticky=E, pady=5)
        self.entry12 = Entry(self.master, textvariable=self.ID).grid(row=0, column=1, pady=5)
        self.label13 = Label(self.master, text="From").grid(row=1, column=0, sticky=E, pady=5)
        self.label14 = Label(self.master, text="Month:").grid(row=1, column=1, sticky=E, pady=5)
        self.entry15 = Entry(self.master, textvariable=self.from_month).grid(row=1, column=2, pady=5)
        self.label16 = Label(self.master, text="Year:").grid(row=1, column=3, sticky=E, pady=5)
        self.entry17 = Entry(self.master, textvariable=self.from_year).grid(row=1, column=4, pady=5)
        self.label18 = Label(self.master, text="Until").grid(row=2, column=0, sticky=E, pady=5)
        self.label19 = Label(self.master, text="Month:").grid(row=2, column=1, sticky=E, pady=5)
        self.entry20 = Entry(self.master, textvariable=self.until_month).grid(row=2, column=2, pady=5)
        self.label21 = Label(self.master, text="Year:").grid(row=2, column=3, sticky=E, pady=5)
        self.entry22 = Entry(self.master, textvariable=self.until_year).grid(row=2, column=4, pady=5)

        self.report_by_emp = Button(master, width=30, text="Make attendance report",
                                    command=self.make_report, bg="Ivory3").grid(row=3, column=2,  columnspan = 3, pady=20)

        self.back = Button(master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=4, column=5, pady=10)

    def make_report(self):
        ID = self.ID.get()
        from_month = self.from_month.get()
        from_year = self.from_year.get()
        until_month = self.until_month.get()
        until_year = self.until_year.get()

        if ID=="" or from_month == "" or from_year == "" or until_month == "" or until_year == "":
            tkinter.messagebox.showerror("Missing data", "please make sure you fill all the parameters")
            return
        if from_month.isalpha() or from_year.isalpha() or until_year.isalpha() or until_month.isalpha() or ID.isalpha():
            tkinter.messagebox.showerror("Error", "The parameters should be digits only, please check again")
            return
        if Check_emp_data.check_id_in_list(ID) is False:
            tkinter.messagebox.showerror("Error", "The employee ID is not in the employees list")
            return
        if 1 > int(from_month) > 12 or 1 > int(until_month) > 12:
            tkinter.messagebox.showerror("Error", "Month should be between 1-12")
            return
        if int(from_year) < 2010:
            tkinter.messagebox.showerror("Error", "From year should take no long than 5 years")
            return
        if int(until_year) < int(from_year):
            tkinter.messagebox.showerror("Error", "From year should be  earlier or same as until year")
            return

        report = Reports("attendance_log.csv", "Attendance_report_by_emp.csv", ["Emp ID", "Date", "Enter", "Exit", "Duration"])
        parameters = report.prepare_date_parameters(from_month, from_year, until_month, until_year)
        log = report.get_attendance_log_from_file()
        report.prepare_report_by_emp(log, parameters, ID)

        tkinter.messagebox.showinfo\
            ("report ready", "The report is ready, please open the \"Attendance_report_by_employee.csv\" file")
        self.master.destroy()

    def closeScreen(self, w):
        w.destroy()

# ********************************************************************************************************************


class LatersReport(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Laters report")
        self.master.geometry("700x300+200+200")

        self.from_year = StringVar()
        self.from_month = StringVar()
        self.from_hour = StringVar()
        self.from_min = StringVar()
        self.until_year = StringVar()
        self.until_month = StringVar()

        self.label11 = Label(self.master, text="Arrived after (HH:MM):", font=("Arial", 8, "bold"),fg = "navy",
                             anchor= "w", width = 20).grid(row=0, column=0, pady=5, sticky=E)
        self.entry12 = Entry(self.master, textvariable=self.from_hour, width = 10).grid(row=0, column=1, pady=20)
        self.label13 = Label(self.master, text=" : ", width = 2).grid(row=0, column=2, sticky=E, pady=20)
        self.entry14 = Entry(self.master, textvariable=self.from_min, width = 10).grid(row=0, column=3, pady=20, sticky=E)

        self.label15 = Label(self.master, text="From (mm/yyyy):",font=("Arial", 8, "bold"), anchor= "w", width = 20)\
            .grid(row=1, column=0, sticky=E, pady=5)
        self.entry16 = Entry(self.master, textvariable=self.from_month, width = 10).grid(row=1, column=1, pady=5)
        self.label17 = Label(self.master, text=" / ", width = 2).grid(row=1, column=2, sticky=E, pady=20)
        self.entry18 = Entry(self.master, textvariable=self.from_year, width = 10).grid(row=1, column=3, pady=5)

        self.label19 = Label(self.master, text="Until (mm/yyyy):", font=("Arial", 8, "bold"), anchor= "w", width = 20)\
            .grid(row=2, column=0, sticky=E, pady=5)
        self.entry20 = Entry(self.master, textvariable=self.until_month, width = 10).grid(row=2, column=1, pady=5)
        self.label21 = Label(self.master, text=" / ", width = 2).grid(row=2, column=2, sticky=E, pady=20)
        self.entry22 = Entry(self.master, textvariable=self.until_year, width = 10).grid(row=2, column=3, pady=5)

        self.report_by_emp = Button(master, width=20, text="Make laters report",
                                    command=self.make_report, bg="Ivory3").grid(row=3, column=4,pady=20)
        self.back = Button(master, text="Back", command=lambda: self.closeScreen(master)) \
            .grid(row=5, column=5, pady=10)

    def make_report(self):
        from_month = self.from_month.get()
        from_year = self.from_year.get()
        from_hour = self.from_hour.get()
        from_min = self.from_min.get()
        until_month = self.until_month.get()
        until_year = self.until_year.get()

        if from_month =="" or from_year =="" or from_hour =="" or  from_min =="" or until_month =="" or until_year =="":
            tkinter.messagebox.showerror("Missing data", "please make sure you fill all the parameters")
            return
        if from_month.isalpha() or from_min.isalpha() or from_hour.isalpha() or from_year.isalpha()\
                or until_year.isalpha() or until_month.isalpha():
            tkinter.messagebox.showerror("Error", "The parameters should be digits only, please check again")
            return
        if 1 > int(from_month) > 12 :
            tkinter.messagebox.showerror("Error", "From month should be between 1-12")
            return
        if 1 > int(until_month) > 12:
            tkinter.messagebox.showerror("Error", "Until month should be between 1-12")
            return
        if 0 > int(from_hour) > 24:
            tkinter.messagebox.showerror("Error", "From hour should be between 0-24")
            return
        if 0 > int(from_min) > 60:
            tkinter.messagebox.showerror("Error", "From minute should be between 0-60")
            return

        db = Reports("attendance_log.csv", "laters_report.csv", ["Emp ID", "Date", "Enter time"])
        log = db.get_attendance_log_from_file()
        date_parameters = db.prepare_date_parameters(from_month,from_year,until_month,until_year)
        time_parameters = db.prepare_time_parameters(from_hour, from_min)
        db.prepare_laters_report(log,date_parameters,time_parameters)

        tkinter.messagebox.showinfo("report ready", "The report is ready, please open \"laters_report.csv\" file")
        self.master.destroy()

    def closeScreen(self, w):
        w.destroy()

# *******************************************************************************************************************
if __name__ == "__main__":
    root = Tk()
    sys = MainUI(root)
    root.mainloop()


"""
פונקציה לעדכון און ליין של הזמן על המסך
time1 = ''
def tick(self):
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        self.clock.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
    clock.after(200, tick)

"""
