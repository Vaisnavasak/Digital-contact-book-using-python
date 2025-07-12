import tkinter as tk
from tkinter import messagebox
import json
import os

# --- Data Storage (Persistent - using JSON file) ---
CONTACTS_FILE = 'contacts.json'
contacts = [] # Format: [{'Name': '...', 'Phone': '...', 'Address': '...', 'Email': '...'}]

def load_contacts_from_file():
    """Loads contacts from the JSON file."""
    global contacts
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as file:
                contacts = json.load(file)
        except json.JSONDecodeError:
            messagebox.showwarning("File Error", "Could not read contacts.json. Starting with empty contacts.")
            contacts = []
    else:
        contacts = [] # Initialize as empty if file doesn't exist

def save_contacts_to_file():
    """Saves current contacts to the JSON file."""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4) # indent for readability

# --- Functions for Contact Management ---

def add_contact():
    """Adds a new contact to the list with Name, Phone, Address, and Email."""
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    address = address_entry.get().strip() # Get address
    email = email_entry.get().strip()

    if name and phone: # Name and phone are still required for basic validation
        contact = {
            'Name': name,
            'Phone': phone,
            'Address': address, # Store address
            'Email': email
        }
        contacts.append(contact)
        update_contact_listbox()
        clear_entries()
        messagebox.showinfo("Success", "Contact added successfully!")
    else:
        messagebox.showerror("Error", "Name and Phone are required fields.")

def view_contact():
    """Displays details of the selected contact, including address."""
    selected_index = contact_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        contact = contacts[index]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, contact.get('Name', ''))
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, contact.get('Phone', ''))
        address_entry.delete(0, tk.END) # Populate address entry
        address_entry.insert(0, contact.get('Address', ''))
        email_entry.delete(0, tk.END)
        email_entry.insert(0, contact.get('Email', ''))
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to view.")

def update_contact():
    """Updates the details of the selected contact, including address."""
    selected_index = contact_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip() # Get updated address
        email = email_entry.get().strip()

        if name and phone:
            contacts[index] = {
                'Name': name,
                'Phone': phone,
                'Address': address, # Update address
                'Email': email
            }
            update_contact_listbox()
            clear_entries()
            messagebox.showinfo("Success", "Contact updated successfully!")
        else:
            messagebox.showerror("Error", "Name and Phone are required fields.")
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to update.")

def delete_contact():
    """Deletes the selected contact."""
    selected_index = contact_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?"):
            del contacts[index]
            update_contact_listbox()
            clear_entries()
            messagebox.showinfo("Success", "Contact deleted successfully!")
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

def clear_entries():
    """Clears all input fields."""
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END) # Clear address entry
    email_entry.delete(0, tk.END)

def update_contact_listbox():
    """Refreshes the listbox with current contacts (displaying Name and Phone)."""
    contact_listbox.delete(0, tk.END)
    for contact in contacts:
        contact_listbox.insert(tk.END, f"{contact.get('Name', 'N/A')} - {contact.get('Phone', 'N/A')}")

def on_closing():
    """Function to call when the window is closed."""
    save_contacts_to_file()
    root.destroy()

# --- GUI Setup ---

root = tk.Tk()
root.title("Digital Contact Book")
root.geometry("650x450") # Adjusted size to accommodate new field

# Input Frame
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
name_entry = tk.Entry(input_frame, width=40)
name_entry.grid(row=0, column=1, pady=2)

tk.Label(input_frame, text="Mobile No.:").grid(row=1, column=0, sticky="w", pady=2)
phone_entry = tk.Entry(input_frame, width=40)
phone_entry.grid(row=1, column=1, pady=2)

tk.Label(input_frame, text="Address:").grid(row=2, column=0, sticky="w", pady=2)
address_entry = tk.Entry(input_frame, width=40) # New Address Entry
address_entry.grid(row=2, column=1, pady=2)

tk.Label(input_frame, text="Email ID:").grid(row=3, column=0, sticky="w", pady=2)
email_entry = tk.Entry(input_frame, width=40)
email_entry.grid(row=3, column=1, pady=2)

# Buttons Frame
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack()

add_btn = tk.Button(button_frame, text="Add Contact", command=add_contact, width=12)
add_btn.grid(row=0, column=0, padx=5)

view_btn = tk.Button(button_frame, text="View Contact", command=view_contact, width=12)
view_btn.grid(row=0, column=1, padx=5)

update_btn = tk.Button(button_frame, text="Update Contact", command=update_contact, width=12)
update_btn.grid(row=0, column=2, padx=5)

delete_btn = tk.Button(button_frame, text="Delete Contact", command=delete_contact, width=12)
delete_btn.grid(row=0, column=3, padx=5)

clear_btn = tk.Button(button_frame, text="Clear Fields", command=clear_entries, width=12)
clear_btn.grid(row=0, column=4, padx=5)

# Contact Listbox
contact_listbox = tk.Listbox(root, height=10, width=60) # Increased width
contact_listbox.pack(pady=10)

# Scrollbar for Listbox
scrollbar = tk.Scrollbar(root, orient="vertical", command=contact_listbox.yview)
scrollbar.pack(side="right", fill="y")
contact_listbox.config(yscrollcommand=scrollbar.set)

# Load contacts on startup and display them
load_contacts_from_file()
update_contact_listbox()

# Link the closing event to save contacts
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI event loop
root.mainloop()
