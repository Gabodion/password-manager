from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
# import pyperclip
import json
FONT = ("Arial", 8, "bold")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    pass_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH DETAILS ------------------------------- #


def find_password():
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)  # read file
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        web_names = [key for (key, value) in data.items()]  # create a list of website names in json file
        website_name = website_entry.get()
        # check for web_name
        if website_name in web_names:
            email_name = data[website_name]["email"]  # selected website email
            password = data[website_name]["password"]  # selected website password
            messagebox.showinfo(title=website_name, message=f"Email: {email_name}\n Password: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_name} exits")
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()  # retrieve web_name, email, password
    email_username = email_entry.get()
    password = pass_entry.get()
    new_dict = {
        website: {
            "email": email_username,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:  # check fields if empty
        messagebox.showwarning(title="error", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", mode="r") as data_entries:
                data = json.load(data_entries)  # read file
        except FileNotFoundError:
            with open("data.json", mode="w") as data_entries:
                json.dump(new_dict, data_entries, indent=4)  # write to file to create file
        else:
            data.update(new_dict)  # update file
            with open("data.json", mode="w") as data_entries:
                json.dump(data, data_entries, indent=4)  # write to file
                # data_entries.write(f"{website} | {email_username} | password:{password}\n")
        finally:
            website_entry.delete(0, END)  # starts from the beginning of the range to the end 0-end
            pass_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx="60", pady="60")


# Canvas
canvas = Canvas(width=200, height=200)
pass_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pass_image)
canvas.grid(row=0, column=1)


# Labels
website_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
pass_label = Label(text="Password:")
website_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
pass_label.grid(row=3, column=0)

# boxes
website_entry = Entry(width=35)
email_entry = Entry(width=55)
pass_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry.grid(row=2, column=1, columnspan=3)
email_entry.insert(0, "gabodion@gmail.com")
pass_entry.grid(row=3, column=1)

# Button
generate_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=49, command=save)
search_button = Button(text="Search", width=14, command=find_password)
generate_button.grid(row=3, column=3)
add_button.grid(row=4, column=1, columnspan=3)
search_button.grid(row=1, column=3)


window.mainloop()