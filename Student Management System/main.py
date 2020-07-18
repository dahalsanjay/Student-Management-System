from tkinter import *
from tkinter import Toplevel
from tkinter import messagebox
import time
from tkinter.ttk import Treeview
from tkinter import filedialog
from tkinter import ttk
import pymysql
import pandas
root = Tk()
root.geometry('1350x700+0+0')
root.resizable(False, False)
root.title('Student Management System')
root.iconbitmap('sms.ico')

# ---------------------------------------------------------------------date and time
def clock_function():
    time_string = time.strftime("%H:%M:%S")
    date_string = time.strftime("%d/%m/%Y")
    clock.config(text = 'Date :' + date_string +"\n" +  "Time :" +time_string)
    clock.after(200,clock_function)

clock = Label(root,font = ("times", 16, "bold"), relief = RIDGE, borderwidth  = 4) 
clock.place(x = 0, y = 0)
clock_function()

# ---------------------------------------------------------------------slider text
wlcm_text = "Welcome to Student Management System"
count = 0
text = ''
def animate_slider():
    global count, text
    if(count>=len(wlcm_text)):
        count = 0
        text = ''
        slider_label.config(text = text)
    else:
        text = text + wlcm_text[count]
        slider_label.config(text = text)
        count += 1
    slider_label.after(200,animate_slider)

slider_label = Label(root, text = wlcm_text, font = ("arial", 20, "bold"), relief = RIDGE, borderwidth = 4, width = 35)
slider_label.place(x = 410, y = 10)
animate_slider()

# ---------------------------------------------------------------------connect to database
def connect_db_window():
    db_window = Toplevel()
    db_window.geometry("410x290+600+130")
    db_window.title("Login to Database")
    db_window.iconbitmap("sms.ico")
    db_window.resizable(FALSE, FALSE)
    db_window.grab_set()
    
    # function to connect to databse

    def submit_function():
        global con, mycursor
        host_get = host_var.get()
        user_get = user_var.get()
        password_get = password_var.get()
        try:
            con = pymysql.connect(host = host_get, user = user_get, password = password_get)
            mycursor = con.cursor()
        except:
            messagebox.showerror("Notification","Data is incorrect \n Please try again")
            return
        try:
            strr = 'create database studentmanagementsystem'
            mycursor.execute(strr)
            strr = 'use studentmanagementsystem'
            mycursor.execute(strr)
            strr = 'create table studentdata(id int, name varchar(20), mobile varchar(20), email varchar(30), address varchar(30), gender varchar(20), dob varchar(50), date varchar(100), time varchar(50))'
            mycursor.execute(strr)
            strr = 'alter table studentdata modify column id int not null'
            mycursor.execute(strr)
            strr = 'alter table studentdata modify column id int primary key'
            mycursor.execute(strr)
            messagebox.showinfo('Notification', 'Database created ! \n Now you are connected to the database',parent = db_window)

        except:
            strr = 'use studentmanagementsystem'
            mycursor.execute(strr)
            
            messagebox.showinfo('Notification', 'Now you are connected to the database !',parent = db_window)
        db_window.destroy()
        showall_submit_function()
        


    # variables for host, user and Password
    host_var = StringVar()
    user_var = StringVar()
    password_var = StringVar()

    
    def on_enter_login(e):
        connect_db_botton.configure(bg = "light blue")
    def on_leave_login(e):
        connect_db_botton.configure(bg = '#f0f0f0') 

    host_lbl = Label(db_window, text = "Host ID:", font = ("times", 15, "bold"))
    host_lbl.place(x = 30, y = 20)

    host_entry = Entry(db_window, font = ("times", 15, "bold"), bd = 2, relief = SUNKEN, textvariable = host_var)
    host_entry.place(x = 140, y = 20)
    host_entry.focus()

    user_lbl = Label(db_window, text = "User Name:", font = ("times", 15, "bold"))
    user_lbl.place(x = 30, y = 80)

    user_entry = Entry(db_window, font = ("times", 15, "bold"), bd = 2, relief = SUNKEN, textvariable = user_var)
    user_entry.place(x = 140, y = 80)

    pass_lbl = Label(db_window, text = "Password:", font = ("times", 15, "bold"))
    pass_lbl.place(x = 30, y = 140)

    pass_entry = Entry(db_window, font = ("times", 15, "bold"), bd = 2, relief = SUNKEN, textvariable = password_var)
    pass_entry.place(x = 140, y = 140)

    connect_db_botton = Button(db_window, text = "Log In", font = ("times", 15, "bold"), bd = 4, relief = SUNKEN, width = 15, activebackground = 'green', activeforeground = 'white', command = submit_function)
    connect_db_botton.place(x = 100, y = 200)

    # hover for connect databse bottom

    connect_db_botton.bind('<Enter>', on_enter_login)
    connect_db_botton.bind('<Leave>', on_leave_login)

    db_window.mainloop()




# ---------------------------------------------------------------------Frames

all_menus_frame = Frame(root, bd = 5, borderwidth = 5, relief = GROOVE)
all_menus_frame.place(x = 30, y = 90, height = 570, width = 480)

database_frame = Frame(root, bd = 5, borderwidth = 5, relief = GROOVE)
database_frame.place(x = 530, y = 90, height = 570, width = 790)

# ---------------------------------------------------------------------all menus frame content
welcome_label = Label(all_menus_frame, text = "---------------------Welcome---------------------",font = ("times", 18, "bold"))
welcome_label.place(x = 10, y = 20)

# variables 

idval = StringVar()
nameval = StringVar()
mobileval = StringVar()
emailval = StringVar()
addressval = StringVar()
gendervar = StringVar()
dobvar  = StringVar() 
datevar = StringVar()
timevar = StringVar()
    
# -------------------------------------------add student content
def add_student_function():
    addstudent_window = Toplevel()
    addstudent_window.title('Add Student To Database')
    addstudent_window.iconbitmap('sms.ico')
    addstudent_window.geometry('410x450+40+50')
    addstudent_window.resizable(FALSE, FALSE)
    addstudent_window.grab_set()

    

    space_lbl = Label(addstudent_window)
    space_lbl.grid(row = 0, column = 0, padx = 30, pady =2)

    # Inside add_student_function submit Button 
    def add_submit_function():
        get_id = idval.get()
        get_name = nameval.get()
        get_mobile = mobileval.get()
        get_email = emailval.get()
        get_address = addressval.get()
        get_gender = gendervar.get()
        get_dob = dobvar.get()
        get_date = time.strftime("%d/%m/%Y")
        get_time = time.strftime("%H:%M:%S")
        try:
            strr = 'insert into studentdata values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(strr,(get_id, get_name,get_mobile,get_email,get_address, get_gender,get_dob, get_date, get_time))
            con.commit()
            res = messagebox.askyesnocancel('Notification','Data of ID {} is added successfully \n Want to clean the form ?'.format(get_id),parent = addstudent_window)
            if(res == True):
                idval.set('')
                nameval.set('')
                mobileval.set('')
                emailval.set('')
                addressval.set('')
                gendervar.set('')
                dobvar.set('')

        except:
            messagebox.showerror('Notification',"ID already exists !", parent = addstudent_window)
        strr = 'select * from studentdata'
        mycursor.execute(strr)
        datas = mycursor.fetchall()
        student_mgmt_table .delete(*student_mgmt_table.get_children())
        for i in datas:
            vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
            student_mgmt_table.insert('',END,values=vv)
        

    add_id_lbl = Label(addstudent_window, text = "Enter ID : ", font = ("times", 14, "bold"))
    add_id_lbl.grid(row = 1, column = 0, padx = 20, pady =10)
    add_id_entry = Entry(addstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = idval)
    add_id_entry.grid(row = 1, column = 1)
    add_id_entry.focus()

    add_name_lbl = Label(addstudent_window, text = "Enter Name : ", font = ("times", 14, "bold"))
    add_name_lbl.grid(row = 2, column = 0, padx = 20, pady =10)
    add_name_entry = Entry(addstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4,textvariable = nameval)
    add_name_entry.grid(row = 2, column = 1)

    add_mobile_lbl = Label(addstudent_window, text = "Enter Mobile : ", font = ("times", 14, "bold"))
    add_mobile_lbl.grid(row = 3, column = 0, padx = 20, pady =10)
    add_mobile_entry = Entry(addstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4,textvariable = mobileval)
    add_mobile_entry.grid(row = 3, column = 1)

    add_email_lbl = Label(addstudent_window, text = "Enter Email : ", font = ("times", 14, "bold"))
    add_email_lbl.grid(row = 4, column = 0, padx = 20, pady =10)
    add_email_entry = Entry(addstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4,textvariable = emailval)
    add_email_entry.grid(row = 4, column = 1)

    add_address_lbl = Label(addstudent_window, text = "Enter Address : ", font = ("times", 14, "bold"))
    add_address_lbl.grid(row = 5, column = 0, padx = 20, pady =10)
    add_address_entry = Entry(addstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4,textvariable = addressval)
    add_address_entry.grid(row = 5, column = 1)

    add_gender_lbl = Label(addstudent_window, text = "Enter Gender : ", font = ("times", 14, "bold"))
    add_gender_lbl.grid(row = 6, column = 0, padx = 20, pady =10)
    add_gender_entry = ttk.Combobox(addstudent_window, textvariable =gendervar,font = ("times", 14, "bold"),state = 'readonly', width = 18)
    add_gender_entry['values'] = ("male", "female", "other")
    add_gender_entry.grid(row = 6, column = 1)

    add_dob_lbl = Label(addstudent_window, text = "Enter D.O.B : ", font = ("times", 14, "bold"))
    add_dob_lbl.grid(row = 7, column = 0, padx = 20, pady =10)
    add_dob_entry = Entry(addstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4,textvariable = dobvar)
    add_dob_entry.grid(row = 7, column = 1)

    add_student_submit = Button(addstudent_window, text = "Submit", font = ("times", 14, "bold"), width = 20, bd = 5, relief = SUNKEN, activebackground = 'green', activeforeground = 'white', command = add_submit_function)
    add_student_submit.place(x = 90, y = 370)

    addstudent_window.mainloop()

    # ---------------------------------------------------------------------------search student

def search_student_function():
    searchstudent_window = Toplevel()
    searchstudent_window.title('Search Student To Database')
    searchstudent_window.iconbitmap('sms.ico')
    searchstudent_window.geometry('410x500+40+50')
    searchstudent_window.resizable(FALSE, FALSE)
    searchstudent_window.grab_set()

    # submit button inside the search button

    def search_submit_function():

        get_id = idval.get()
        get_name = nameval.get()
        get_mobile = mobileval.get()
        get_email = emailval.get()
        get_address = addressval.get()
        get_gender = gendervar.get()
        get_dob = dobvar.get()
        get_date = datevar.get()

        if(get_id != ''):
            strr = 'select * from studentdata where id = %s'
            mycursor.execute(strr, (get_id))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)
        
        elif(get_name != ''):
            strr = 'select * from studentdata where name = %s'
            mycursor.execute(strr, (get_name))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)
        
        elif(get_mobile != ''):
            strr = 'select * from studentdata where mobile = %s'
            mycursor.execute(strr, (get_mobile))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)

        elif(get_email != ''):
            strr = 'select * from studentdata where email = %s'
            mycursor.execute(strr, (get_email))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)

        elif(get_address != ''):
            strr = 'select * from studentdata where address = %s'
            mycursor.execute(strr, (get_address))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)

        elif(get_gender != ''):
            strr = 'select * from studentdata where gender = %s'
            mycursor.execute(strr, (get_gender))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)
        elif(get_dob != ''):
            strr = 'select * from studentdata where dob = %s'
            mycursor.execute(strr, (get_dob))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)

        elif(get_date != ''):
            strr = 'select * from studentdata where date = %s'
            mycursor.execute(strr, (get_date))
            datas = mycursor.fetchall()
            student_mgmt_table .delete(*student_mgmt_table.get_children())
            for i in datas:
                vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
                student_mgmt_table.insert('',END,values=vv)



    space_lbl = Label(searchstudent_window)
    space_lbl.grid(row = 0, column = 0, padx = 30, pady =2)

    search_id_lbl = Label(searchstudent_window, text = "Enter ID : ", font = ("times", 14, "bold"))
    search_id_lbl.grid(row = 1, column = 0, padx = 20, pady =10)
    search_id_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = idval)
    search_id_entry.grid(row = 1, column = 1)
    search_id_entry.focus()

    search_name_lbl = Label(searchstudent_window, text = "Enter Name : ", font = ("times", 14, "bold"))
    search_name_lbl.grid(row = 2, column = 0, padx = 20, pady =10)
    search_name_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = nameval)
    search_name_entry.grid(row = 2, column = 1)

    search_mobile_lbl = Label(searchstudent_window, text = "Enter Mobile : ", font = ("times", 14, "bold"))
    search_mobile_lbl.grid(row = 3, column = 0, padx = 20, pady =10)
    search_mobile_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = mobileval)
    search_mobile_entry.grid(row = 3, column = 1)

    search_email_lbl = Label(searchstudent_window, text = "Enter Email : ", font = ("times", 14, "bold"))
    search_email_lbl.grid(row = 4, column = 0, padx = 20, pady =10)
    search_email_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = emailval)
    search_email_entry.grid(row = 4, column = 1)

    search_address_lbl = Label(searchstudent_window, text = "Enter Address : ", font = ("times", 14, "bold"))
    search_address_lbl.grid(row = 5, column = 0, padx = 20, pady =10)
    search_address_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = addressval)
    search_address_entry.grid(row = 5, column = 1)

    search_gender_lbl = Label(searchstudent_window, text = "Enter Gender : ", font = ("times", 14, "bold"))
    search_gender_lbl.grid(row = 6, column = 0, padx = 20, pady =10)
    search_gender_entry = ttk.Combobox(searchstudent_window, font = ("times", 14, "bold"),state = 'readonly', width = 18, textvariable =gendervar)
    search_gender_entry['values'] = ("male", "female", "other")
    search_gender_entry.grid(row = 6, column = 1)

    search_dob_lbl = Label(searchstudent_window, text = "Enter D.O.B : ", font = ("times", 14, "bold"))
    search_dob_lbl.grid(row = 7, column = 0, padx = 20, pady =10)
    search_dob_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = dobvar)
    search_dob_entry.grid(row = 7, column = 1)

    search_date_lbl = Label(searchstudent_window, text = "Enter Date : ", font = ("times", 14, "bold"))
    search_date_lbl.grid(row = 8, column = 0, padx = 20, pady =10)
    search_date_entry = Entry(searchstudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = datevar)
    search_date_entry.grid(row = 8, column = 1)

    search_student_submit = Button(searchstudent_window, text = "Submit", font = ("times", 14, "bold"), width = 20, bd = 5, relief = SUNKEN, activebackground = 'green', activeforeground = 'white', command = search_submit_function)
    search_student_submit.place(x = 90, y = 420)

    searchstudent_window.mainloop()

# ---------------------------------------------------------------------------Delete content function

def delete_student_function():
    cc = student_mgmt_table.focus()
    content = student_mgmt_table.item(cc)
    pp = content['values'][0]
    strr = 'delete from studentdata where id = %s'
    mycursor.execute(strr,(pp))
    con.commit()
    messagebox.showinfo('Notification','ID {} deleted successfully.'.format(pp))
    strr = 'select * from studentdata'
    mycursor.execute(strr)
    datas = mycursor.fetchall()
    student_mgmt_table .delete(*student_mgmt_table.get_children())
    for i in datas:
        vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
        student_mgmt_table.insert('',END,values=vv)


# ---------------------------------------------------------------------------Update content function

def update_student_function():
    updatestudent_window = Toplevel()
    updatestudent_window.title('Search Student To Database')
    updatestudent_window.iconbitmap('sms.ico')
    updatestudent_window.geometry('410x540+40+50')
    updatestudent_window.resizable(FALSE, FALSE)
    updatestudent_window.grab_set()

    def update_submit_function():
        get_id = idval.get()
        get_name = nameval.get()
        get_mobile = mobileval.get()
        get_email = emailval.get()
        get_address = addressval.get()
        get_gender = gendervar.get()
        get_dob = dobvar.get()
        get_date = datevar.get()
        get_time = timevar.get()

        strr = 'update studentdata set name = %s, mobile = %s, email = %s, address = %s, gender = %s, dob = %s, date = %s, time = %s where id = %s'
        mycursor.execute(strr, (get_name, get_mobile, get_email, get_address , get_gender, get_dob, get_date, get_time, get_id))
        con.commit()
        messagebox.showinfo('Notification', 'ID {} updated successfully !'.format(get_id), parent = updatestudent_window)
        strr = 'select * from studentdata'
        mycursor.execute(strr)
        datas = mycursor.fetchall()
        student_mgmt_table .delete(*student_mgmt_table.get_children())
        for i in datas:
            vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
            student_mgmt_table.insert('',END,values=vv)



    space_lbl = Label(updatestudent_window)
    space_lbl.grid(row = 0, column = 0, padx = 30, pady =2)

    update_id_lbl = Label(updatestudent_window, text = "Enter ID : ", font = ("times", 14, "bold"))
    update_id_lbl.grid(row = 1, column = 0, padx = 20, pady =10)
    update_id_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = idval)
    update_id_entry.grid(row = 1, column = 1)
    update_id_entry.focus()

    update_name_lbl = Label(updatestudent_window, text = "Enter Name : ", font = ("times", 14, "bold"))
    update_name_lbl.grid(row = 2, column = 0, padx = 20, pady =10)
    update_name_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = nameval)
    update_name_entry.grid(row = 2, column = 1)

    update_mobile_lbl = Label(updatestudent_window, text = "Enter Mobile : ", font = ("times", 14, "bold"))
    update_mobile_lbl.grid(row = 3, column = 0, padx = 20, pady =10)
    update_mobile_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = mobileval)
    update_mobile_entry.grid(row = 3, column = 1)

    update_email_lbl = Label(updatestudent_window, text = "Enter Email : ", font = ("times", 14, "bold"))
    update_email_lbl.grid(row = 4, column = 0, padx = 20, pady =10)
    update_email_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = emailval)
    update_email_entry.grid(row = 4, column = 1)

    update_address_lbl = Label(updatestudent_window, text = "Enter Address : ", font = ("times", 14, "bold"))
    update_address_lbl.grid(row = 5, column = 0, padx = 20, pady =10)
    update_address_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = addressval)
    update_address_entry.grid(row = 5, column = 1)

    update_gender_lbl = Label(updatestudent_window, text = "Enter Gender : ", font = ("times", 14, "bold"))
    update_gender_lbl.grid(row = 6, column = 0, padx = 20, pady =10)
    update_gender_entry = ttk.Combobox(updatestudent_window, font = ("times", 14, "bold"),state = 'readonly', width = 18, textvariable =gendervar)
    update_gender_entry['values'] = ("male", "female", "other")
    update_gender_entry.grid(row = 6, column = 1)

    update_dob_lbl = Label(updatestudent_window, text = "Enter D.O.B : ", font = ("times", 14, "bold"))
    update_dob_lbl.grid(row = 7, column = 0, padx = 20, pady =10)
    update_dob_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = dobvar)
    update_dob_entry.grid(row = 7, column = 1)

    update_date_lbl = Label(updatestudent_window, text = "Enter Date : ", font = ("times", 14, "bold"))
    update_date_lbl.grid(row = 8, column = 0, padx = 20, pady =10)
    update_date_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = datevar)
    update_date_entry.grid(row = 8, column = 1)

    update_time_lbl = Label(updatestudent_window, text = "Enter Time : ", font = ("times", 14, "bold"))
    update_time_lbl.grid(row = 9, column = 0, padx = 20, pady =10)
    update_time_entry = Entry(updatestudent_window, font = ("times", 14, "bold"), relief = SUNKEN, bd = 4, textvariable = timevar)
    update_time_entry.grid(row = 9, column = 1)

    update_student_submit = Button(updatestudent_window, text = "Submit", font = ("times", 14, "bold"), width = 20, bd = 5, relief = SUNKEN, activebackground = 'green', activeforeground = 'white', command = update_submit_function)
    update_student_submit.place(x = 90, y = 470)

    # get the selected datas

    cc = student_mgmt_table.focus()
    content = student_mgmt_table.item(cc)
    pp = content['values']
    if(len(pp) != 0):
        idval.set(pp[0])
        nameval.set(pp[1])
        mobileval.set(pp[2])
        emailval.set(pp[3])
        addressval.set(pp[4])
        gendervar.set(pp[5])
        dobvar.set(pp[6])
        datevar.set(pp[7])
        timevar.set(pp[8])



    updatestudent_window.mainloop()

#------------------------------------------------------------------------------------showall function content

def showall_submit_function():
    strr = 'select * from studentdata'
    mycursor.execute(strr)
    datas = mycursor.fetchall()
    student_mgmt_table .delete(*student_mgmt_table.get_children())
    for i in datas:
        vv = [i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
        student_mgmt_table.insert('',END,values=vv)

#------------------------------------------------------------------------------------export function content

def export_submit_function():
    ff = filedialog.asksaveasfilename()
    gg = student_mgmt_table.get_children()
    id, name, mobile, email, address, gender, dob,addeddate, addedtime =[], [], [], [], [], [], [], [] ,[]
    for i in gg:
        content = student_mgmt_table.item(i)
        pp = content['values']
        id.append(pp[0]), name.append(pp[1]), mobile.append(pp[2]), email.append(pp[3]), address.append(pp[4]), gender.append(pp[5]), dob.append(pp[6]), addeddate.append(pp[7]), addedtime.append(pp[8])
    dd = ['Id', 'Name', 'Mobile No', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time']
    df = pandas.DataFrame(list(zip(id, name, mobile, email, address, gender, dob,addeddate, addedtime)), columns = dd)
    paths = r'{}.csv'.format(ff)
    df.to_csv(paths,index = False)
    messagebox.showinfo('Notification', 'Student Data is exported ! in {}'.format(paths))




#------------------------------------------------------------------------------------exit function content

def exit():
    res = messagebox.askyesno("Notification", "Are you sure want to exit ?")
    if(res == 1):
        root.destroy()
    else:
        return

#-----------------------------------------------binding function (function for hover)

    
def on_enter_connectdb(e):
    connect_db.configure(bg = "light blue")
def on_leave_connectdb(e):
    connect_db.configure(bg = "#f0f0f0")

def on_enter_addstudent(e):
    add_student_btn.configure(bg = "light blue")
def on_leave_addstudent(e):
    add_student_btn.configure(bg = '#f0f0f0')

def on_enter_searchstudent(e):
    search_student_btn.configure(bg = "light blue")
def on_leave_searchstudent(e):
    search_student_btn.configure(bg = '#f0f0f0')

def on_enter_deletestudent(e):
    delete_student_btn.configure(bg = "light blue")
def on_leave_deletestudent(e):
    delete_student_btn.configure(bg = '#f0f0f0')

def on_enter_updatestudent(e):
    update_student_btn.configure(bg = "light blue")
def on_leave_updatestudent(e):
    update_student_btn.configure(bg = '#f0f0f0')

def on_enter_showallstudent(e):
    showall_student_btn.configure(bg = "light blue")
def on_leave_showallstudent(e):
    showall_student_btn.configure(bg = '#f0f0f0')

def on_enter_exportstudent(e):
    export_student_btn.configure(bg = "light blue")
def on_leave_exportstudent(e):
    export_student_btn.configure(bg = '#f0f0f0')

def on_enter_exitstudent(e):
    exit_student_btn.configure(bg = "light blue")
def on_leave_exitstudent(e):
    exit_student_btn.configure(bg = '#f0f0f0')






connect_db = Button(root, text = "Connect to DB", font = ("arial", 15, "bold"), bd = 5, relief = RIDGE, borderwidth = 4, command = connect_db_window, activebackground = 'green', activeforeground = 'white')
connect_db.place(x = 1180, y= 10)


add_student_btn = Button(all_menus_frame,text = "Add Student", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white', command = add_student_function)
add_student_btn.place(x = 100, y = 70)

search_student_btn = Button(all_menus_frame,text = "Search Student", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white',command = search_student_function)
search_student_btn.place(x = 100, y = 140)

delete_student_btn = Button(all_menus_frame,text = "Delete Student", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white', command = delete_student_function)
delete_student_btn.place(x = 100, y = 210)

update_student_btn = Button(all_menus_frame,text = "Update Student", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white', command = update_student_function)
update_student_btn.place(x = 100, y = 280)

showall_student_btn = Button(all_menus_frame,text = "Show All", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white',command = showall_submit_function)
showall_student_btn.place(x = 100, y = 350)

export_student_btn = Button(all_menus_frame,text = "Export Data", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white', command = export_submit_function)
export_student_btn.place(x = 100, y = 420)

exit_student_btn = Button(all_menus_frame,text = "Exit", font = ("times", 15, "bold"), bd = 5, borderwidth = 5, relief = GROOVE, width = 20, activebackground = 'green', activeforeground = 'white', command = exit)
exit_student_btn.place(x = 100, y = 490)

#--------------------------------------------------------------------- binding property for hover

connect_db.bind('<Enter>', on_enter_connectdb)
connect_db.bind('<Leave>', on_leave_connectdb)


add_student_btn.bind('<Enter>', on_enter_addstudent)
add_student_btn.bind('<Leave>', on_leave_addstudent)

search_student_btn.bind('<Enter>', on_enter_searchstudent)
search_student_btn.bind('<Leave>', on_leave_searchstudent)

delete_student_btn.bind('<Enter>', on_enter_deletestudent)
delete_student_btn.bind('<Leave>', on_leave_deletestudent)

update_student_btn.bind('<Enter>', on_enter_updatestudent)
update_student_btn.bind('<Leave>', on_leave_updatestudent)

showall_student_btn.bind('<Enter>', on_enter_showallstudent)
showall_student_btn.bind('<Leave>', on_leave_showallstudent)

export_student_btn.bind('<Enter>', on_enter_exportstudent)
export_student_btn.bind('<Leave>', on_leave_exportstudent)

exit_student_btn.bind('<Enter>', on_enter_exitstudent)
exit_student_btn.bind('<Leave>', on_leave_exitstudent)



# ======================================================================database_frame content

style = ttk.Style()
style.configure('Treeview.Heading', font = ('arial', 10, 'bold'))
style.configure('Treeview', font = ('times', 12, 'bold'))

scroll_x = Scrollbar(database_frame, orient = HORIZONTAL)
scroll_y = Scrollbar(database_frame, orient = VERTICAL)
scroll_x.pack(side = BOTTOM, fill = X)
scroll_y.pack(side = RIGHT, fill = Y)

student_mgmt_table = Treeview(database_frame, columns = ('Id', 'Name', 'Mobile No', 'Email', 'Address', 'Gender', 'DOB', 'Added Date', 'Added Time'), yscrollcommand = scroll_y.set, xscrollcommand = scroll_x.set)
student_mgmt_table.pack(fill =BOTH , expand = 1)
scroll_x.config(command = student_mgmt_table.xview)
scroll_y.config(command = student_mgmt_table.yview)
student_mgmt_table.heading('Id',text = 'ID')
student_mgmt_table.heading('Name',text = 'Name')
student_mgmt_table.heading('Mobile No',text = 'Mobile No')
student_mgmt_table.heading('Email',text = 'Email')
student_mgmt_table.heading('Address',text = 'Address')
student_mgmt_table.heading('Gender',text = 'Gender')
student_mgmt_table.heading('DOB',text = 'DOB')
student_mgmt_table.heading('Added Date',text = 'Added Date')
student_mgmt_table.heading('Added Time',text = 'Added Time')
student_mgmt_table['show'] = 'headings'

student_mgmt_table.column('Id', width = 100)
student_mgmt_table.column('Name', width = 100)
student_mgmt_table.column('Mobile No', width = 100)
student_mgmt_table.column('Email', width = 200)
student_mgmt_table.column('Address', width = 200)
student_mgmt_table.column('Gender', width = 100)
student_mgmt_table.column('DOB', width = 100)
student_mgmt_table.column('Added Date', width = 100)
student_mgmt_table.column('Added Time', width = 100)









root.mainloop()