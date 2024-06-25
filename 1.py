from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from random import choice, randint, shuffle
import pyperclip
import json

# Initialize window
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30)


# Password Generator Function
def generate():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_length = int(length_entry.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()

    password_chars = []
    if use_letters:
        password_chars.extend(letters)
    if use_numbers:
        password_chars.extend(numbers)
    if use_symbols:
        password_chars.extend(symbols)

    password_list = [choice(password_chars) for _ in range(password_length)]
    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    update_strength_indicator(password)


# Save Password Function
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title="Confirm Details",
                                       message=f"Website: {website}\nEmail: {email}\nPassword: {password}\n\nIs it okay to save?")
        if is_ok:
            new_data = {
                website: {
                    "email": email,
                    "password": password,
                }
            }

            try:
                with open("data.json", "r") as data_file:
                    # Reading the data
                    data = json.load(data_file)
            except FileNotFoundError:
                data = new_data
            else:
                #Updating the data
                data.update(new_data)

            with open("data.json", "w") as data_file:
                #Saving the updated data
                json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


def search():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:{email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")




# Password Strength Indicator Function
def update_strength_indicator(password):
    strength = "Weak"
    if len(password) >= 8 and any(c.islower() for c in password) and any(c.isupper() for c in password):
        strength = "Medium"
    if len(password) >= 12 and any(c.isdigit() for c in password) and any(c in '!#$%&()*+' for c in password):
        strength = "Strong"
    strength_label.config(text=f"Strength: {strength}")


# UI Setup
canvas = Canvas(window, width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(window, text="Website:")
website_label.grid(row=1, column=0, pady=5)
email_label = Label(window, text="Email/Username:")
email_label.grid(row=2, column=0, pady=5)
password_label = Label(window, text="Password:")
password_label.grid(row=3, column=0, pady=5)
length_label = Label(window, text="Length:")
length_label.grid(row=4, column=0, pady=5)
strength_label = Label(window, text="Strength: ")
strength_label.grid(row=6, column=1, pady=5)

# Entries
website_entry = Entry(window, width=35)
website_entry.grid(row=1, column=1, pady=5)
website_entry.focus()
search_button = Button(text="Search", command=search, width=13)
search_button.grid(row=1, column=2)
email_entry = Entry(window, width=35)
email_entry.grid(row=2, column=1, columnspan=2, pady=5)
password_entry = Entry(window, width=20, show="*")
password_entry.grid(row=3, column=1, pady=5, sticky=W)
length_entry = Entry(window, width=5)
length_entry.insert(0, "12")
length_entry.grid(row=4, column=1, pady=5, sticky=W)


# Password Visibility Toggle
def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_button.config(text='Hide')
    else:
        password_entry.config(show='*')
        toggle_button.config(text='Show')


toggle_button = Button(window, text='Show', command=toggle_password, bg='#4CAF50', fg='white')
toggle_button.grid(row=3, column=2, padx=5)

# Checkbuttons for password criteria
letters_var = BooleanVar(value=True)
numbers_var = BooleanVar(value=True)
symbols_var = BooleanVar(value=True)

letters_check = Checkbutton(window, text="Letters", variable=letters_var, bg='white', fg='black')
letters_check.grid(row=5, column=0, pady=5)
numbers_check = Checkbutton(window, text="Numbers", variable=numbers_var, bg='white', fg='black')
numbers_check.grid(row=5, column=1, pady=5)
symbols_check = Checkbutton(window, text="Symbols", variable=symbols_var, bg='white', fg='black')
symbols_check.grid(row=5, column=2, pady=5)

# Buttons
generate_password_button = Button(window, text="Generate Password", command=generate, bg='#4CAF50', fg='white',
                                  width=20)
generate_password_button.grid(row=4, column=2, pady=5)
add_button = Button(window, text="Add", width=36, command=save, bg='#4CAF50', fg='white')
add_button.grid(row=7, column=1, columnspan=2, pady=5)

# Apply some style
style = ttk.Style(window)
style.configure('Accent.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#4CAF50', borderwidth=1,
                focusthickness=3, focuscolor='none')
style.map('Accent.TButton', background=[('active', '#45a049'), ('disabled', '#d9d9d9')])


# Add some animation (a simple example)
def animate_label():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    current_color = colors.pop(0)
    colors.append(current_color)
    website_label.config(fg=current_color)
    window.after(500, animate_label)


animate_label()



window.mainloop()
