import json
from tkinter import *
from tkinter import messagebox, font
import random
import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
# Window for the tkinter
window = Tk()
window.title("Pass-Man")
window.config(padx=50, pady=50, bg="white")

# Canvas with the logo image
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=1, column=2)

FONT = "Helvetica Neue"
MB_FONT = font.Font(name='TkCaptionFont', exists=True)
MB_FONT.config(family=FONT, size=10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    pass_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]

    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    pass_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    title = title_input.get().title()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        return messagebox.showerror(title="Oops!", message="No data found. Try adding some details.")

    else:
        try:
            search_data = data[title]
        except KeyError:
            return messagebox.showerror(title="Oops!", message=f"No entry found for {title}")
        else:
            username = search_data["username"]
            password = search_data["password"]
            website = search_data["website"]
            return messagebox.showinfo(title="Search Found!",
                                       message=f"Username: {username}\nPassword: {password}\nWebsite: {website}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    title = title_input.get().title()
    website = website_input.get()
    username = username_input.get()
    password = pass_input.get()

    if title == "" or website == "" or username == "" or password == "":
        return messagebox.showerror(title="Error", message="You cannot leave these fields empty.")

    choice = messagebox.askyesno(title="Confirm Addition", message=f"Do you want to add this password:\n"
                                                                   f"Title:{title}\nWebsite:{website}\n"
                                                                   f"Username:{username}\nPassword:{password}")

    if choice:
        to_save = {
            title: {
                "username": username,
                "password": password,
                "website": website
            }
        }

        try:
            # Read data and update data to json file
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
                # Updating old data with new data
                data.update(to_save)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(to_save, data_file)

        else:
            # Save the updated data to data json file
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file)

        # Add to txt file
        # with open("data.txt", "a") as data_file:
        #     data_file.write(f"{to_save}\n")
        finally:
            title_input.delete(0, END)
            website_input.delete(0, END)
            username_input.delete(0, END)
            pass_input.delete(0, END)
            title_input.focus()


# ---------------------------- UI SETUP ------------------------------- #


# Title label
title_label = Label(text="Title:", bg="white", font=(FONT, 13))
title_label.grid(row=2, column=1, pady=10)

# Title entry box
title_input = Entry(width=22)
title_input.grid(row=2, column=2)
title_input.focus()

# Search button
search_button = Button(text="Search", highlightthickness=0, bg="white", width=10, font=(FONT, 8),
                       command=search_password)
search_button.grid(row=2, column=3)

# Website label
website_label = Label(text="Website:", bg="white", font=(FONT, 13))
website_label.grid(row=3, column=1, pady=10)

# Website entry box
website_input = Entry(width=35)
website_input.grid(row=3, column=2, columnspan=3, pady=10)

# Username label
username_label = Label(text="Email/Username:", bg="white", font=(FONT, 13))
username_label.grid(row=4, column=1)

# Username entry box
username_input = Entry(width=35)
username_input.grid(row=4, column=2, columnspan=3, pady=10, padx=10)
username_input.insert(0, "prasadsumit99544@gmail.com")

# Password label
pass_label = Label(text="Password:", bg="white", font=(FONT, 13))
pass_label.grid(row=5, column=1, pady=10)

# Password Input
pass_input = Entry(width=22)
pass_input.grid(row=5, column=2)

# Generate password button
generate_pass = Button(text="Generate", highlightthickness=0, bg="white", width=10, font=(FONT, 8),
                       command=generate_password)
generate_pass.grid(row=5, column=3)

# Add button
add_button = Button(text="Add", width=37, highlightthickness=0, bg="white", font=(FONT, 10), command=save_data)
add_button.grid(row=6, column=2, columnspan=3, padx=10, pady=10)

window.mainloop()
