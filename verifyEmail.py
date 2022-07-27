import smtplib
from tkinter import *
import random
from tkinter import messagebox
from db import Admin


class Verification:
    def __init__(self, db, email):
        self.success = False
        self.generated_code = str()
        self.db = db
        self.email = email

    def VerifyEmail(self):
        code = code_field.get()
        if (code == self.generated_code):
            self.db.updateUser(self.email, True)
            master.quit()
            messagebox.showinfo("Success", "Email verified")
        else:
            messagebox.showinfo("Failure", "Code is Invalid")
            master.quit()

    def send_Verification(self, sender_email="relaxwithnature578@gmail.com", sender_password="Sandesh@578", address_info="sandesh57801@gmail.com"):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        self.generated_code = ''.join(random.choice('0123456789ABCDEF')
                                      for i in range(6))
        email_body_info = "Confirmation code is {}".format(self.generated_code)
        server.sendmail(sender_email, address_info,
                        email_body_info)
        server.quit()
        print("Code Sent Successfully to mail ")


def emailVerification(db, email):
    global master
    global code_field
    verify = Verification(db, email)
    verify.send_Verification()
    master = Tk()
    code = Label(master, text="Enter the code")
    code.grid(row=0, column=0)
    code_field = Entry(master)
    code_field.grid(row=0, column=1)
    quit = Button(master,
                  text='Quit',
                  command=master.quit)
    quit.grid(row=2,
              column=0,
              pady=4)

    verify = Button(master,
                    text='Verify', command=verify.VerifyEmail)
    verify.grid(row=2,
                column=1,
                pady=4)
    master.mainloop()
