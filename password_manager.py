from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import rsa

# colors for gui
ORANGE = '#FAD7A0'
LORANGE = '#FDEBD0'
DARKBLUE = '#17202A'

# for generate passwords
letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
small_letters = list('abcdefghijklmnopqrstuvwxyz')
numbers = list('0123456789')
symbols = list('!@#$%^&*()_+')

publicKey, privateKey = rsa.newkeys(512)


# encryption function
def encrypt(password):
    encMessage = rsa.encrypt(password.encode(), publicKey)
    return encMessage

# decryption function
def decrypt(encMsg):
    decMessage = rsa.decrypt(encMsg, privateKey).decode()
    return decMessage


def save_info(): # register function
    username_info = username_entry.get()
    password_info = password_entry.get()

    Specials = ['$', '@', '#', '%', '!', '&']

    if len(password_info) < 6 or len(password_info) > 20 or (not any(char.isdigit() for char in password_info)) or not (any(char.isupper() for char in password_info)) or (not any(char.islower() for char in password_info)) or (not any(char in Specials for char in password_info)):
        messagebox.showwarning(
            title='Error',
            message="Password must contain at least one a small letter, a capital letter, a number and a special character"
        )
    else:
        file = open("users.txt", "w")
        file.write(username_info)
        file.write("\n")
        file.write(password_info)
        file.close()
        messagebox.showwarning(
            message="Registration success"
        )
        app.destroy()


def user_login(): # login function
    username_info = username_entry.get()
    password_info = password_entry.get()

    with open('users.txt') as f:
        file = f.read()
        if username_info in file:
            if password_info in file:
                messagebox.showwarning(
                    title='',
                    message="Login success"
                )
                app.destroy()
        else:
            messagebox.showwarning(
                title='',
                message="User not found"
            )


app = Tk()
app.title("Password Manager")
app.config(padx=50, pady=50, bg=ORANGE)

canvas = Canvas(height=200, width=200, bg=ORANGE, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)


username_label = Label(text='Username:', bg=ORANGE, fg=DARKBLUE)
username_label.grid(row=2,column=0,sticky="W")
username_entry = Entry(font=('Arial',10))
username_entry.grid(row=2,column=1, columnspan=2,sticky="EW")
username_entry.insert(0, '')

password_label = Label(text='Password:', bg=ORANGE, fg=DARKBLUE)
password_label.grid(row=3,column=0,sticky="W")

password_entry = Entry(font=('Arial',10))
password_entry.grid(row=3,column=1,sticky="EW")


button = Button(text='Create Master Password', bg=LORANGE, command=save_info)
button.grid(row=5,column=1,columnspan=2,sticky="EW")
button.config(pady=2)

button2 = Button(text='Login', bg=LORANGE, command=user_login)
button2.grid(row=4,column=1,columnspan=2,sticky="EW")
button2.config(pady=2)

app.mainloop()


# Generate passwords
def random_password():
    num_letters = random.randint(8,10)
    num_capletters = random.randint(8, 10)
    num_numbers = random.randint(1,2)
    num_symbols = random.randint(1,2)

    rand_capletters = [random.choice(small_letters) for i in range(num_capletters)]
    rand_letters = [random.choice(letters) for i in range(num_letters)]
    rand_numbers = [random.choice(numbers) for i in range(num_numbers)]
    rand_symbols = [random.choice(symbols) for i in range(num_symbols)]

    created_password = rand_letters + rand_numbers + rand_symbols + rand_capletters

    random.shuffle(created_password)
    created_password = ''.join(created_password)
    password_entry.delete(0, END)
    password_entry.insert(0, created_password)

    pyperclip.copy(created_password)


# Add new record to json file
def saved_entries():
    # GETTING THE USER INPUTS
    user_website = website_entry.get()
    user_email = email_entry.get()
    user_password = password_entry.get()

    Specials = ['$','@','#','%','!','&']

    if len(user_password) < 6 or len(user_password) > 20 or (not any(char.isdigit() for char in user_password)) or not (any(char.isupper() for char in user_password)) or (not any(char.islower() for char in user_password)) or (not any(char in Specials for char in user_password)):
        messagebox.showwarning(
            title='Error',
            message="Password must contain at least one a small letter, a capital letter, a number and a special character"
        )
    else:
        global encrpass
        encrpass = encrypt(user_password)
        new_data = {
            user_website: {
                'email': user_email,
                'password': str(encrpass)
            }
        }
        if len(user_website) != 0 and len(user_password) != 0:

            try:
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
            except FileNotFoundError:
                with open('data.json', 'w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                is_correct = messagebox.askyesno(
                    title=f"{user_website}",
                    message=f"\n'Email': {user_email}\n'Password': {user_password}\n\nAre you sure?")
                if is_correct:
                    with open('data.json', 'w') as data_file:
                        json.dump(data, data_file, indent=4)
                        website_entry.delete(0, END)
                        password_entry.delete(0, END)
                else:
                    messagebox.showwarning(
                        title='Error',
                        message="One of the fields is empty!"
                    )


# ---------------------------- SEARCH FUNCTION ------------------------------- #
def search_website():

    user_website = website_entry.get()
    try:
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
            user_password = data[user_website]['password']
            decrpass = decrypt(encrpass)
            password_entry.delete(0, END)
            password_entry.insert(0, decrpass)
    except KeyError as error:
        messagebox.showinfo(title="Key Error", message=f"{error} password does not exist")


# Password manager screen
root = Tk()
root.title("Password Manager")
root.config(padx=50, pady=50, bg=ORANGE)

# ROW 0
canvas = Canvas(height=200, width=200, bg=ORANGE, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=img)
canvas.grid(row=0,column=1)

# ROW 1
website_label = Label(text='Website:', bg=ORANGE, fg=DARKBLUE)
website_label.grid(row=1,column=0,sticky="W")

website_entry = Entry(font=('Arial',10))
website_entry.grid(row=1,column=1, columnspan=2,sticky="EW")
website_entry.focus()

website_search = Button(text='Search', bg=LORANGE, command=search_website)
website_search.grid(row=1,column=2,sticky="EW")

# ROW 2
email_label = Label(text='Email/Username:', bg=ORANGE, fg=DARKBLUE)
email_label.grid(row=2,column=0,sticky="W")

email_entry = Entry(font=('Arial',10))
email_entry.grid(row=2,column=1, columnspan=2,sticky="EW")
email_entry.insert(0, '')

# ROW 3
password_label = Label(text='Password:', bg=ORANGE, fg=DARKBLUE)
password_label.grid(row=3,column=0,sticky="W")

password_entry = Entry(font=('Arial',10))
password_entry.grid(row=3,column=1,sticky="EW")

password_button = Button(text='Generate Password', bg=LORANGE, command=random_password)
password_button.grid(row=3,column=2,sticky="EW")

# ROW 4
button = Button(text='Add', bg=LORANGE, command=saved_entries)
button.grid(row=4,column=1,columnspan=2,sticky="EW")
button.config(pady=2)


root.mainloop()
