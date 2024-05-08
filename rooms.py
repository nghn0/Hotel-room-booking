import tkinter as tk
from tkinter import messagebox
import sqlite3

con = sqlite3.connect("rooms_database.db")
cur = con.cursor()
cur.execute("create table if not exists booking(name text, contact integer, room text, price integer)")

root = tk.Tk()
root.title("Room Booking")

rooms = {
        "room1": (3, 'AC', 'TV', 'W'),
        "room2": (2, 'AC', 'TV', 'NW'),
        "room3": (1, 'NAC', 'TV', 'W'),
        "room4": (3, 'AC', 'NTV', 'NW'),
        "room5": (2, 'NAC', 'NTV', 'W'),
        "room6": (3, 'NAC', 'TV', 'NW'),
        "room7": (1, 'NAC', 'NTV', 'NW'),
        "room8": (3, 'AC', 'TV', 'W'),
        "room9": (3, 'NAC', 'TV', 'W'),
        "room10": (3, 'AC', 'NTV', 'W'),
        "room11": (3, 'AC', 'TV', 'NW'),
        "room12": (3, 'NAC', 'NTV', 'W'),
        "room13": (3, 'NAC', 'TV', 'NW'),
        "room14": (3, 'AC', 'NTV', 'NW'),
        "room15": (2, 'AC', 'TV', 'W'),
        "room16": (2, 'NAC', 'TV', 'W'),
        "room17": (2, 'AC', 'NTV', 'W'),
        "room18": (2, 'AC', 'TV', 'NW'),
        "room19": (2, 'NAC', 'NTV', 'W'),
        "room20": (2, 'NAC', 'TV', 'NW'),
        "room21": (2, 'AC', 'NTV', 'NW'),
        "room22": (1, 'AC', 'TV', 'W'),
        "room23": (1, 'NAC', 'TV', 'W'),
        "room24": (1, 'AC', 'NTV', 'W'),
        "room25": (1, 'AC', 'TV', 'NW'),
        "room26": (1, 'NAC', 'NTV', 'W'),
        "room27": (1, 'NAC', 'TV', 'NW'),
        "room28": (1, 'AC', 'NTV', 'NW'),
}

def booked_rooms():
    cur.execute("select * from booking")
    row = cur.fetchall()
    if row is not []:
        book_text.config(state=tk.NORMAL)
        book_text.delete("1.0", tk.END)
        for i in row:
            book_text.insert(tk.END, f"Name: {i[0]}\nContact Number: {i[1]}\nRoom Booked: {i[2]}\nPrice: {i[3]}\n--------\n")
        book_text.config(state=tk.DISABLED)


def add_details():
    f = f_name_entry.get()
    l = l_name_entry.get()
    c = contact_entry.get()
    e = email_entry.get()
    nc = int(children_entry.get())
    na = int(adults_entry.get())
    rn = 'room' + room_number_entry.get()
    room_selected = rooms[rn]
    if (na + nc) > (room_selected[0] * 2):
        messagebox.showinfo("Limit reached", f"{rn} can store maximum of {room_selected[0] * 2} people")
    else:
        p = 100 + (room_selected[0] * 10)
        if room_selected[1] == "AC":
            p = p + 100
        if room_selected[2] == "TV":
            p = p + 100
        if room_selected[3] == "W":
            p = p + 100
        cur.execute("insert into booking values(?,?,?,?)", (f, c, rn, p))
        con.commit()
        bill_text.config(state=tk.NORMAL)
        bill_text.delete("1.0", tk.END)
        bill_text.insert(tk.END, f"First Name: {f}\nLast Name: {l}\nContact: {c}\nEmail: {e}\nNumber of Children: {nc}\nNumber of Adults: {na}\nRoom Booked: {rn}\nTotal Price: {p}")
        bill_text.config(state=tk.DISABLED)
        booked_rooms()
        p = 0
        messagebox.showinfo("Room Booked", f"{rn} is booked by {f}")



def filter_rooms():
    number_beds = int(bed_entry.get())
    ac = ac_var.get()
    tv = tv_var.get()
    w = wifi_var.get()

    cur.execute("SELECT room FROM booking")
    booked_rooms = [row[0] for row in cur.fetchall()]

    rooms_text.config(state=tk.NORMAL)
    rooms_text.delete("1.0", tk.END)

    available_rooms_found = False

    for room, attributes in rooms.items():
        if room not in booked_rooms and number_beds == attributes[0] and ac == attributes[1] and tv == attributes[2] and w == attributes[3]:
            rooms_text.insert(tk.END, f"{room} is Available\n")
            available_rooms_found = True

    if not available_rooms_found:
        rooms_text.insert(tk.END, "No rooms available.\n")

    rooms_text.config(state=tk.DISABLED)


details_frame = tk.LabelFrame(root, text="Customer Details", pady=10, padx=10)
# -------
personal_label = tk.Label(details_frame, text="Personal Information")
personal_label.grid(row=0, column=0, columnspan=5)

f_name_label = tk.Label(details_frame, text="First name: ")
f_name_label.grid(row=1, column=0)

f_name_entry = tk.Entry(details_frame)
f_name_entry.grid(row=1, column=1)

l_name_label = tk.Label(details_frame, text="Last name: ")
l_name_label.grid(row=1, column=3)

l_name_entry = tk.Entry(details_frame)
l_name_entry.grid(row=1, column=4)
# --------
contact_label = tk.Label(details_frame, text="Contact Information")
contact_label.grid(row=3, column=0, columnspan=5)

contact_label = tk.Label(details_frame, text="Contact number: ")
contact_label.grid(row=4, column=0)

contact_entry = tk.Entry(details_frame)
contact_entry.grid(row=4, column=1)

email_label = tk.Label(details_frame, text="Email: ")
email_label.grid(row=4, column=3)

email_entry = tk.Entry(details_frame)
email_entry.grid(row=4, column=4)
# --------
reserve_label = tk.Label(details_frame, text="Reserve Information")
reserve_label.grid(row=5, column=0, columnspan=5)

children_label = tk.Label(details_frame, text="Number of Children: ")
children_label.grid(row=6, column=0)

children_entry = tk.Entry(details_frame)
children_entry.grid(row=6, column=1)

adults_label = tk.Label(details_frame, text="Number of Adults: ")
adults_label.grid(row=6, column=3)

adults_entry = tk.Entry(details_frame)
adults_entry.grid(row=6, column=4)
# ------
room_number_label = tk.Label(details_frame, text="Enter the room Number: ")
room_number_label.grid(row=7, column=1)

room_number_entry = tk.Entry(details_frame)
room_number_entry.grid(row=7, column=2)

submit_btn = tk.Button(details_frame, text="Submit", command=add_details)
submit_btn.grid(row=8, column=0, columnspan=5)

details_frame.grid(row=0, column=0)

# -------------------------------------

filter_frame = tk.LabelFrame(root, text="Filter rooms", padx=10, pady=10)

# ----
bed_label = tk.Label(filter_frame, text="Number of beds: ")
bed_label.grid(row=0, column=0)

bed_entry = tk.Entry(filter_frame)
bed_entry.grid(row=0, column=1)
# -----
ac_var = tk.StringVar()
ac_label = tk.Label(filter_frame, text="AC: ")
ac_label.grid(row=1, column=0)

ac_yes = tk.Radiobutton(filter_frame, text="Yes", value='AC', variable=ac_var)
ac_yes.grid(row=1, column=0, columnspan=2)

ac_no = tk.Radiobutton(filter_frame, text="No", value='NAC', variable=ac_var)
ac_no.grid(row=1, column=1, columnspan=2)
# --------
tv_var = tk.StringVar()
tv_label = tk.Label(filter_frame, text="TV: ")
tv_label.grid(row=2, column=0)

tv_yes = tk.Radiobutton(filter_frame, text="Yes", value='TV', variable=tv_var)
tv_yes.grid(row=2, column=0, columnspan=2)

tv_no = tk.Radiobutton(filter_frame, text="No", value='NTV', variable=tv_var)
tv_no.grid(row=2, column=1, columnspan=2)
# ----
wifi_var = tk.StringVar()
wifi_label = tk.Label(filter_frame, text="Wifi: ")
wifi_label.grid(row=3, column=0)

wifi_yes = tk.Radiobutton(filter_frame, text="Yes", value='W', variable=wifi_var)
wifi_yes.grid(row=3, column=0, columnspan=2)

wifi_no = tk.Radiobutton(filter_frame, text="No", value='NW', variable=wifi_var)
wifi_no.grid(row=3, column=1, columnspan=2)
# ----
find_button = tk.Button(filter_frame, text="Find Rooms", command=filter_rooms)
find_button.grid(row=4, column=0, columnspan=2)
# ---
rooms_text = tk.Text(filter_frame, height=10, width=40, state=tk.DISABLED)
rooms_text.grid(row=5, column=0, columnspan=2)
# ------

filter_frame.grid(row=0, column=1)

# -----------------------------------------

billing_frame = tk.LabelFrame(root, text="Billing information", pady=10, padx=10)

bill_text = tk.Text(billing_frame, height=20, width=115, state=tk.DISABLED)
bill_text.grid(row=0, column=0)


billing_frame.grid(row=1, column=0)

# -----------------------------

booked_frame = tk.LabelFrame(root, text="Booked Rooms", pady=10, padx=10)

book_text = tk.Text(booked_frame, height=20, width=42, state=tk.DISABLED)
book_text.grid(row=0, column=0)


booked_frame.grid(row=1, column=1)

root.after(1000, booked_rooms)


root.mainloop()


