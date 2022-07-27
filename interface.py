from tkinter import *
from db import Admin
from SpeechToText import SpeechToText
from captcha.image import ImageCaptcha
from PIL import ImageTk, Image
from tkinter import messagebox
from crypto import Crypto
import random
import string
import re
from verifyEmail import Verification, emailVerification
from tkinter import messagebox
from passGenerator import generate_random_password
from dashboard import Dashboard

user = dict()


# converts voice to text and sets the value of input field


def configureName(name):
    if(validate_Name(name)):
        name_field.delete(0, END)
        name_field.insert(0, name)
    else:
        return messagebox.showwarning(
            "invalid name", "Name can contain only alphabet")


def setName(event):
    name_field.config(state=NORMAL)
    name_field.delete(0, END)
    name = SpeechToText()
    configureName(name)


def configureRoll(roll):
    if(re.search('\s', roll)):
        roll = roll.replace(" ", "")
    if(validate_rollno(roll)):
        roll_no_field.delete(0, END)
        roll_no_field.insert(0, roll)
    else:
        return messagebox.showwarning(
            "invalid roll", "Roll can only be numbers")


def setRoll(event):
    roll_no_field.config(state=NORMAL)
    roll = SpeechToText()
    configureRoll(roll)


def configureEmail(email):
    if(" at the rate " in email):
        email = email.replace(" at the rate ", "@")
    if(re.search('\s', email)):
        email = email.replace(" ", "")
    if(validate_Email(email)):
        email_id_field.delete(0, END)
        email_id_field.insert(0, email)
    else:
        return messagebox.showwarning(
            "invalid email", "Email is invalid")


def setEmail(event):
    email_id_field.config(state=NORMAL)
    email = SpeechToText()
    configureEmail(email)


def configurePassword(password):
    if(validate_password(password)):
        password_field.delete(0, END)
        password_field.insert(0, password)
    else:
        text1 = generate_random_password()
        messagebox.showwarning("invalid password", "Password is not valid")
        messagebox.showinfo("password suggestion",
                            "showing strong password ")
        password_field.delete(0, END)
        password_field.insert(0, text1)
        return


def setPassword(event):
    password_field.config(state=NORMAL)
    password = SpeechToText()
    if(password != ""):
        password = password_field.get()
    if(" at the rate " in password):
        password = password.replace(" at the rate ", "@")
    if(re.search('\s', password)):
        password = password.replace(" ", "")

    configurePassword(password)


def validate_Email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(pattern, text) is None:
        return 0
    else:
        return 1


def validate_Name(username):
    if len(username) < 3:
        return False

    if not re.match('^[a-zA-Z ]*$', username):
        return False

    return True


def validate_rollno(text):
    if text.isdigit():
        return 1
    else:
        return 0


def validate_password(text):
    pattern = r'[A-za-z]+[@%^&$]+[0-9]+'

    if re.fullmatch(pattern, text) is None or len(text) < 6:
        return 0
    else:
        return 1


def toggle_password():
    if password_field.cget('show') == '':
        password_field.config(show='*')
        path = 'C:\\Users\\KIIT\\Desktop\\TT Lab\\SmartRegistration\\view.png'
        show_img = ImageTk.PhotoImage(Image.open(path))
        toggle_btn.config(image=show_img)
        toggle_btn.image_names = show_img
    else:
        password_field.config(show='')
        toggle_btn.config(text='Hide Password')
        toggle_btn.config(image=hide_img)
        toggle_btn.image_names = hide_img

# Function for clearing the
# contents of text entry boxes


def clear():
    # clear the content of text entry box
    name_field.delete(0, END)
    roll_no_field.delete(0, END)
    email_id_field.delete(0, END)
    password_field.delete(0, END)
    entry.delete(0, END)

# Function to take data from GUI


def insert():

    user["name"] = name_field.get()
    configureName(user["name"])
    user["roll"] = roll_no_field.get()
    configureRoll(user["roll"])
    user["email"] = email_id_field.get()
    configureEmail(user["email"])
    user["password"] = password_field.get()
    configurePassword(user["password"])
    user["verified"] = False

    db = Admin()
    crypto = Crypto()
    privateKey, publicKey = crypto.loadKeys()
    user["password"] = crypto.Encrypt(user["password"], publicKey)
    print(user)

    database = db.get_database()
    db.setCollection(database)
    db.insertUser(user)

    emailVerification(db, user["email"])

    # set focus on the name_field box
    name_field.focus_set()

    # call the clear() function
    clear()


def createImage():
    global random_string
    global image_label
    global image_display
    global verify_label
    global entry
    # The if block below works only when we press the
    # Reload Button in the GUI. It basically removes
    # the label (if visible) which shows whether the
    # entered string is correct or incorrect.

    # Removing the contents of the input box.
    entry.delete(0, END)

    # Generating a random string for the Captcha
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6))
    # Creating a Captcha Image
    image_captcha = ImageCaptcha(width=250, height=125)
    image_generated = image_captcha.generate(random_string)
    image_display = ImageTk.PhotoImage(Image.open(image_generated))

    image_label = Label(root, image=image_display)
    image_label.grid(row=9, column=1, columnspan=1,
                     padx=10)


def check(x, y):
    global verify_label
    # if user not fill any entry
    # then print "empty input"
    if (name_field.get() == "" or
            roll_no_field.get() == "" or
            email_id_field.get() == "" or
            password_field.get() == ""):
        messagebox.showerror(
            "Empty Input Error", "Info : All fields must be filled before submitting.")
        return

    verify_label.grid_forget()
    if(x == ""):
        messagebox.showwarning("Empty entry", "Captcha must be verified")
        return

    if x.lower() == y.lower():
        verify_label = Label(master=root,
                             text="Verified",
                             font="Arial 15",
                             bg='#ffe75c',
                             fg="#00a806"
                             )
        verify_label.grid(row=11, column=1, columnspan=1, pady=10)
        insert()
    else:
        verify_label = Label(master=root,
                             text="Incorrect!",
                             font="Arial 15",
                             bg='#ffe75c',
                             fg="#fa0800"
                             )
        verify_label.grid(row=11, column=1, columnspan=1, pady=10)
        createImage()


# Driver code
if __name__ == "__main__":

    # create a GUI window
    root = Tk()

    # set the background colour of GUI window
    root.configure(background='light green')

    # set the title of GUI window
    root.title("Smart Registration Form")

    # set the configuration of GUI window
    root.geometry("500x500")

    # create a Form label
    heading = Label(root, text="Smart Registration Form",
                    bg="light green", font=('Helvetica', 15, 'bold'), padx=10, pady=7)

    # create a Name label
    name = Label(root, text="Name", bg="light green", padx=10, pady=7)

    # create a Form No. label
    form_no = Label(root, text="Roll", bg="light green", padx=10, pady=7)

    # create a Email id label
    email_id = Label(root, text="Email id", bg="light green", padx=10, pady=7)

    # create a password label
    password = Label(root, text="Password", bg="light green", padx=10, pady=7)

    verify_label = Label(root)
    image_label = Label(root)

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    heading.grid(row=0, column=1)
    name.grid(row=1, column=0)
    form_no.grid(row=4, column=0)
    email_id.grid(row=6, column=0)
    password.grid(row=8, column=0)

    # create a text entry box
    # for typing the information
    name_field = Entry(root)
    name_field.insert(0, "Press Enter and tell your name")
    roll_no_field = Entry(root)
    email_id_field = Entry(root)
    password_field = Entry(root)
    entry = Entry(root)

    # bind method of widget is used for
    # the binding the function with the events

    # whenever the enter key is pressed
    # then call the focus1 function
    name_field.bind("<Return>", setName)

    # whenever the enter key is pressed
    # then call the focus4 function
    roll_no_field.bind("<Return>", setRoll)

    # whenever the enter key is pressed
    # then call the focus6 function
    email_id_field.bind("<Return>", setEmail)
    password_field.bind("<Return>", setPassword)

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    name_field.grid(row=1, column=1, ipadx="100", pady=7, padx=7)
    roll_no_field.grid(row=4, column=1, ipadx="100", pady=7, padx=7)
    email_id_field.grid(row=6, column=1, ipadx="100", pady=7, padx=7)
    password_field.grid(row=8, column=1, ipadx="100", pady=7, padx=7)
    entry.grid(row=10, column=1, ipadx="60", pady=10, padx=7)

    # Creating an Image for the first time.
    createImage()
    # Defining the path for the reload button image
    # and using it to add the reload button in the
    # GUI window
    path = 'C:\\Users\\KIIT\\Desktop\\TT Lab\\SmartRegistration\\reload.png'
    reload_img = ImageTk.PhotoImage(Image.open(
        path).resize((32, 32), Image.ANTIALIAS))
    reload_button = Button(image=reload_img,
                           command=lambda: createImage())
    reload_button.grid(row=10, column=2, pady=10)

    path = 'C:\\Users\\KIIT\\Desktop\\TT Lab\\SmartRegistration\\private.png'
    hide_img = ImageTk.PhotoImage(Image.open(path))
    toggle_btn = Button(root, image=hide_img,
                        width=15, command=toggle_password)
    toggle_btn.grid(row=8, column=2, pady=7, padx=7)

    # create a Submit Button and place into the root window
    submit = Button(root, text="Submit", fg="white", bg="green", width=40, height=1,
                    command=lambda: check(entry.get(), random_string))
    reload_button.grid(row=10, column=2, pady=10)
    submit.grid(row=12, column=1, pady=10, padx=10)

    view = Button(root, text="Dashboard", fg="white",
                  bg="blue", width=40, height=1, command=lambda: Dashboard())
    view.grid(row=13, column=1, pady=10, padx=10)

    # start the GUI
    root.mainloop()
