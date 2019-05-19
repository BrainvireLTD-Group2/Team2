from tkinter import Tk, ttk, StringVar, IntVar, messagebox, Scrollbar, Menu, Toplevel, Frame, Label, Entry, Button
from tkinter.constants import TOP, BOTTOM, LEFT, RIGHT, HORIZONTAL, VERTICAL, SOLID, W, X, Y
import urllib3
import hashlib
import sqlite3
import os  # For running Windows open shell command

root = Tk()
root.title('Personal Information Management')

width = 1024
height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)
root.config(bg='#99ff99')

# ========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
EMPLOYEE_ID = IntVar()
FIRST_NAME = StringVar()
LAST_NAME = StringVar()
COMPANY_NAME = StringVar()
HOUSE_NO = StringVar()
CITY = StringVar()
COUNTY = StringVar()
ZIP = IntVar()
EMAIL = StringVar()
SEARCH = StringVar()
global cols
cols = ('Employee ID', 'First Name', 'Last Name', 'Company Name', 'House No', 'City', 'County', 'ZIP', 'Email')

# ========================================METHODS==========================================

def database():
    global conn, cursor
    conn = sqlite3.connect('PIM.db')
    cursor = conn.cursor()


def databaseinitialise():
    database()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "Employees" ("Employee ID" INTEGER PRIMARY KEY NOT NULL, "First Name" TEXT, "Last Name" TEXT, "Company Name" TEXT, "House No" TEXT, "City" TEXT, "County" TEXT, "ZIP" INTEGER, "Email" TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS temp(firstrun BOOLEAN NOT NULL CHECK (firstrun IN (0,1)) DEFAULT 1);""")
    cursor.execute("SELECT * FROM temp LIMIT 1")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO temp DEFAULT VALUES")
    conn.commit()


def checkfirstrun():
    global firstrun
    database()
    cursor.execute("SELECT * FROM temp LIMIT 1")
    temp = cursor.fetchone()
    if temp[0] == 1:
        firstrun = True
        print('First Run')
        showdpa()
        cursor.execute("REPLACE INTO temp (ROWID, firstrun) VALUES (1, 0)")
        conn.commit()


def close():
    result = messagebox.askquestion('Personal Information Management', 'Are you sure you want to exit?', icon='warning')
    if result == 'yes':
        conn.close()
        root.destroy()
        exit()


def showloginform():
    global loginformx
    loginformx = Toplevel()
    loginformx.title('Personal Information Management/Account Login')
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginformx.resizable(0, 0)
    loginformx.geometry('%dx%d+%d+%d' % (width, height, x, y))
    loginform()


def checkdpa():
    exists = os.path.isfile('Data Protection Act.pdf')
    if exists:
        # todo check integrity
        return True
    else:
        # file not found
        return False


def showdpa():
    loop = True
    while loop:
        result = messagebox.askyesno('Personal Information Management', 'Since this is the first time running this program you must agree to the Data Protection Act Document which is about to open, is this okay?')
        if result:
            if checkdpa():
                os.startfile('Data Protection Act.pdf')
                loop = False
            else:
                result = messagebox.askyesno('Personal Information Management', 'Document not found, would you like to download it?')
                if result:
                    print('DOWNLOADING')
                    downloaddpa()
                    os.startfile('Data Protection Act.pdf')
                    loop = False
                else:
                    close()
        else:
            close()


def downloaddpa():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')
    out_file = open('Data Protection Act.pdf', 'wb')
    out_file.write(http.request('GET', "https://raw.githubusercontent.com/BrainvireLTD-Group2/PIM-System/master/Data%20Protection%20Act.pdf").data)
    out_file.close()


def loginform():
    global lbl_result
    TopLoginForm = Frame(loginformx, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text='Administrator Login', font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginformx, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text='Username:', font=('arial', 25), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text='Password:', font=('arial', 25), bd=18)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text='', font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text='Login', font=('arial', 18), width=30, command=login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    username.focus()
    password.bind('<Return>', login)


def displayhome():
    global Home
    Home = Tk()
    Home.title('Personal Information Management/Home')
    width = 1024
    height = 300
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry('%dx%d+%d+%d' % (width, height, x, y))
    Home.resizable(0, 0)
    Home.protocol('WM_DELETE_WINDOW', close)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(expand=1)
    lbl_display = Label(Title, text='Personal Information Management', font=('arial', 45))
    lbl_display.pack()
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label='View DPA', command=showdpa)
    filemenu.add_command(label='Logout', command=logout)
    filemenu.add_command(label='Exit', command=close)
    filemenu2.add_command(label='Add new', command=showaddnew)
    filemenu2.add_command(label='View all', command=showview)
    menubar.add_cascade(label='Account', menu=filemenu)
    menubar.add_cascade(label='Employees', menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg='#99ff99')


def showaddnew():
    global addnewformx
    addnewformx = Toplevel()
    addnewformx.title('Personal Information Management/Add new')
    width = 600
    height = 850
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewformx.geometry('%dx%d+%d+%d' % (width, height, x, y))
    addnewformx.resizable(0, 0)
    addnewform()


def addnewform():
    TopAddNew = Frame(addnewformx, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text='Add New Employee', font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewformx, width=600)
    MidAddNew.pack(side=TOP, pady=50)
    lbl_firstname = Label(MidAddNew, text='First Name:', font=('arial', 25), bd=10)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(MidAddNew, text='Last Name:', font=('arial', 25), bd=10)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_companyname = Label(MidAddNew, text='Company Name:', font=('arial', 25), bd=10)
    lbl_companyname.grid(row=2, sticky=W)
    lbl_houseno = Label(MidAddNew, text='House No.:', font=('arial', 25), bd=10)
    lbl_houseno.grid(row=3, sticky=W)
    lbl_city = Label(MidAddNew, text='City:', font=('arial', 25), bd=10)
    lbl_city.grid(row=4, sticky=W)
    lbl_county = Label(MidAddNew, text='County:', font=('arial', 25), bd=10)
    lbl_county.grid(row=5, sticky=W)
    lbl_zipaddress = Label(MidAddNew, text='ZIP:', font=('arial', 25), bd=10)
    lbl_zipaddress.grid(row=6, sticky=W)
    lbl_email = Label(MidAddNew, text='Email:', font=('arial', 25), bd=10)
    lbl_email.grid(row=7, sticky=W)
    firstname = Entry(MidAddNew, textvariable=FIRST_NAME, font=('arial', 25), width=15)
    firstname.grid(row=0, column=1)
    lastname = Entry(MidAddNew, textvariable=LAST_NAME, font=('arial', 25), width=15)
    lastname.grid(row=1, column=1)
    companyname = Entry(MidAddNew, textvariable=COMPANY_NAME, font=('arial', 25), width=15)
    companyname.grid(row=2, column=1)
    houseno = Entry(MidAddNew, textvariable=HOUSE_NO, font=('arial', 25), width=15)
    houseno.grid(row=3, column=1)
    city = Entry(MidAddNew, textvariable=CITY, font=('arial', 25), width=15)
    city.grid(row=4, column=1)
    county = Entry(MidAddNew, textvariable=COUNTY, font=('arial', 25), width=15)
    county.grid(row=5, column=1)
    zipaddress = Entry(MidAddNew, textvariable=ZIP, font=('arial', 25), width=15)
    zipaddress.grid(row=6, column=1)
    email = Entry(MidAddNew, textvariable=EMAIL, font=('arial', 25), width=15)
    email.grid(row=7, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=addnewemployee)
    btn_add.grid(row=8, columnspan=2, pady=20)


def addnewemployee():
    database()
    cursor.execute("""INSERT INTO "Employees" ("First Name", "Last Name", "Company Name", "House No", "City", "County", "ZIP", "Email") VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", (FIRST_NAME.get(), LAST_NAME.get(), COMPANY_NAME.get(), HOUSE_NO.get(), CITY.get(), COUNTY.get(), str(ZIP.get()), EMAIL.get()))
    conn.commit()
    FIRST_NAME.set("")
    LAST_NAME.set("")
    COMPANY_NAME.set("")
    HOUSE_NO.set("")
    CITY.set("")
    COUNTY.set("")
    ZIP.set("")
    EMAIL.set("")
    cursor.close()
    conn.close()


def viewform():
    global tree
    TopViewForm = Frame(viewformx, width=600, bd=1)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewformx, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewformx, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text='View Employees', font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text='Search', font=('arial', 15))
    lbl_txtsearch.pack(side=TOP)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    search.bind('<Return>', searchfunction)
    btn_search = Button(LeftViewForm, text='Search', command=searchfunction)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text='Reset', command=reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text='Delete', command=delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=cols, selectmode='extended', height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set, show='headings')
    for col in cols:
        tree.heading(col, text=col, anchor=W)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.pack()
    displaydata()


def displaydata():
    database()
    cursor.execute("SELECT * FROM Employees")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()


def searchfunction(Event=None):
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        database()
        temp = SEARCH.get()
        search_statement = """SELECT * FROM Employees WHERE "Employee ID" = :x OR "First Name" = :x OR "Last Name" = :x OR "Company Name" = :x OR "House NO" = :x OR "City" = :x OR "County" = :x OR "ZIP" = :x OR "Email" = :x"""
        cursor.execute(search_statement, [temp])
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()


def reset():
    tree.delete(*tree.get_children())
    displaydata()
    SEARCH.set("")


def delete():
    if not tree.selection():
        messagebox.showerror('Error', 'You need to select an entry to delete first')
    else:
        result = messagebox.askquestion('Personal Information Management', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curitem = tree.selection()
            database()
            for selected_item in curitem:
                contents = (tree.item(selected_item, 'values'))
                cursor.execute("""DELETE FROM Employees WHERE "Employee ID"=?""", [contents[0]])
                tree.delete(selected_item)
            conn.commit()


def showview():
    global viewformx
    viewformx = Toplevel()
    viewformx.title('Personal Information Management/View Employees')
    width = 600
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewformx.geometry('%dx%d+%d+%d' % (width, height, x, y))
    viewformx.resizable(0, 0)
    viewform()


def logout():
    result = messagebox.askquestion('Personal Information Management', 'Are you sure you want to logout?', icon='warning')
    if result == 'yes':
        admin_id = ''
        root.deiconify()
        Home.destroy()


def login(event = None):  # event = None so the return key binding works correctly
    global admin_id
    database()
    if USERNAME.get() == '' or PASSWORD.get() == '':
        lbl_result.config(text='Please complete the required field!', fg='red')
    else:
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set('')
            PASSWORD.set('')
            lbl_result.config(text='')
            showhome()
        else:
            lbl_result.config(text='Invalid username or password', fg='red')
            USERNAME.set('')
            PASSWORD.set('')
    cursor.close()
    conn.close()


def showhome():
    root.withdraw()
    displayhome()
    loginformx.destroy()


# ========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Account', command=showloginform)
filemenu.add_command(label='Exit', command=close)
menubar.add_cascade(label='File', menu=filemenu)
root.config(menu=menubar)
databaseinitialise()
checkfirstrun()

# ========================================FRAME============================================
Title = Frame(root, bd=1, relief=SOLID)
Title.pack(expand=1)  # Make the frame expandable so it can center itself inside of the window

# ========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text='Personal Information Management', font=('arial', 45))
lbl_display.pack()

# ========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.protocol('WM_DELETE_WINDOW', close)
    root.mainloop()
