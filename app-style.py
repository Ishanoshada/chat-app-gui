# This is a simple chat application using Tkinter for the GUI and providing login and signup functionality.
# Chat App (ishanoshada)+(Styled)

import tkinter as tk
from tkinter import messagebox
import pymongo
import json
import os

# Choose your storage method: "pymongo" or "json"
storage_method = "json"
username= ""

# MongoDB setup
if storage_method == "pymongo":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["chat_app_db"]
    users_collection = db["users"]
    messages_collection = db["messages"]

# JSON file setup
elif storage_method == "json":
    json_file_path = "chat_data.json"
    if not os.path.exists(json_file_path):
        with open(json_file_path, "w") as file:
            json.dump({"users": [], "messages": []}, file)

# Tkinter app setup
app = tk.Tk()
app.title("Chat App")
app.geometry("400x400")

# Login interface
def login():
    global username
    username = username_entry.get()
    
    password = password_entry.get()
    if not username or not password:
        messagebox.showinfo("Signup Error", "Not defined")
        return False

    if storage_method == "pymongo":
        user = users_collection.find_one({"username": username})
        if user and user["password"] == password:
            messagebox.showinfo("Login Successful", "Welcome to the chat!")
            show_chat_interface(username)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
    elif storage_method == "json":
        with open(json_file_path, "r") as file:
            data = json.load(file)
        
        for user in data["users"]:
            if user["username"] == username and user["password"] == password:
                messagebox.showinfo("Login Successful", "Welcome to the chat!")
                show_chat_interface(username)
                return
        
        messagebox.showerror("Login Failed", "Invalid credentials")
        
# Signup interface
def signup():
    new_username = new_username_entry.get()
    new_password = new_password_entry.get()
    if not new_username or not new_password:
        messagebox.showinfo("Signup Error", "Not defined")
        return False

    if storage_method == "pymongo":
        if users_collection.find_one({"username": new_username}):
            messagebox.showerror("Signup Failed", "Username already taken")
        else:
            users_collection.insert_one({"username": new_username, "password": new_password})
            messagebox.showinfo("Signup Successful", "Account created successfully")
            show_login_interface()
    elif storage_method == "json":
        with open(json_file_path, "r") as file:
            data = json.load(file)
        
        for user in data["users"]:
            if user["username"] == new_username:
                messagebox.showerror("Signup Failed", "Username already taken")
                return
        
        data["users"].append({"username": new_username, "password": new_password})
        
        with open(json_file_path, "w") as file:
            json.dump(data, file)
        
        messagebox.showinfo("Signup Successful", "Account created successfully")
        show_login_interface()

def send_message():
        # ... (Send message functionality code)
        message = message_entry.get()
        if message:
            if storage_method == "pymongo":
                messages_collection.insert_one({"username": username, "message": message})
            elif storage_method == "json":
                with open(json_file_path, "r") as file:
                    data = json.load(file)
                
                data["messages"].append({"username": username, "message": message})
                
                with open(json_file_path, "w") as file:
                    json.dump(data, file)
            
            update_chat_text()
            message_entry.delete(0, tk.END)

def update_chat_text():
         # ... (Update chat text functionality code)
        chat_text.config(state=tk.NORMAL)
        chat_text.delete(1.0, tk.END)
        
        if storage_method == "pymongo":
            messages = messages_collection.find()
        elif storage_method == "json":
            with open(json_file_path, "r") as file:
                data = json.load(file)
            messages = data["messages"]
        
        for message in messages:
            chat_text.insert(tk.END, f"{message['username']}: {message['message']}\n")
        chat_text.config(state=tk.DISABLED)

# Chat interface
def show_chat_interface(username):
    
    login_frame.pack_forget()
    signup_frame.pack_forget()
    signup_button_.pack_forget()

    chat_label.pack()
    chat_text.pack()
    message_entry.pack()
    send_button.pack()

    update_chat_text()


    
# Signup  interface
def show_signup_interface():
    welcome_label.pack_forget()
    login_frame.pack_forget()
    signup_button_.pack_forget()
    

    signup_frame.pack()
    new_username_label.pack()
    new_username_entry.pack()
    new_password_label.pack()
    new_password_entry.pack()
    signup_button.pack()
    
# Login interface
def show_login_interface():
    welcome_label.pack_forget()
    signup_frame.pack_forget()
    login_button_.pack_forget()

    login_frame.pack()
    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()

# Style
button_style = {
    "font": ("Helvetica", 12),
    "bg": "#4CAF50",
    "fg": "white",
    "borderwidth": 2,
    "relief": "raised"
}

text_style = {
    "font": ("Helvetica", 12),
    "bg": "white",
    "fg": "black"
}

# Welcome widgets
welcome_label = tk.Label(app, text="Welcome to the Chat App!", **text_style)
welcome_label.pack()

login_button_ = tk.Button(app, text="Login", command=show_login_interface, **button_style)
login_button_.pack()

signup_button_ = tk.Button(app, text="Signup", command=show_signup_interface, **button_style)
signup_button_.pack()


# Login widgets
login_frame = tk.Frame(app)
username_label = tk.Label(login_frame, text="Username:", **text_style)
username_entry = tk.Entry(login_frame)
password_label = tk.Label(login_frame, text="Password:", **text_style)
password_entry = tk.Entry(login_frame, show="*")
login_button = tk.Button(login_frame, text="Login", command=login, **button_style)

# Signup widgets
signup_frame = tk.Frame(app)
new_username_label = tk.Label(signup_frame, text="New Username:", **text_style)
new_username_entry = tk.Entry(signup_frame)
new_password_label = tk.Label(signup_frame, text="New Password:", **text_style)
new_password_entry = tk.Entry(signup_frame, show="*")
signup_button = tk.Button(signup_frame, text="Signup", command=signup, **button_style)

# Chat widgets
chat_label = tk.Label(app, text="Chat:", **text_style)
chat_text = tk.Text(app, state=tk.DISABLED, **text_style)
message_entry = tk.Entry(app)
send_button = tk.Button(app, text="Send", command=send_message, **button_style)

 


# Start the Tkinter main loop
app.mainloop()
