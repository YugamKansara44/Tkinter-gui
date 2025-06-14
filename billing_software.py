import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Initialize the window
root = tk.Tk()
root.title("Rainbow Collection - Billing System")
root.geometry("1000x750")
root.minsize(900, 700)
root.config(bg="#f7f1e3")
root.resizable(True, True)

items = []
discount_percent = tk.DoubleVar(value=0.0)

# Top Branding
branding_label = tk.Label(root, text="🌈 Rainbow Collection", font=("Arial Rounded MT Bold", 26), bg="#f7f1e3", fg="#6c5ce7")
branding_label.pack(pady=10)

# Customer Frame
cust_frame = tk.LabelFrame(root, text="Customer Details", bg="#dff9fb", padx=10, pady=10)
cust_frame.pack(fill="x", padx=10)

name_var = tk.StringVar()
phone_var = tk.StringVar()

for i in range(4):
    cust_frame.grid_columnconfigure(i, weight=1)

# Entries
fields = [("Name:", name_var), ("Phone:", phone_var)]
for idx, (label, var) in enumerate(fields):
    tk.Label(cust_frame, text=label, bg="#dff9fb").grid(row=0, column=idx*2, padx=5, pady=5, sticky="e")
    tk.Entry(cust_frame, textvariable=var).grid(row=0, column=idx*2+1, padx=5, pady=5, sticky="ew")

# Discount
discount_frame = tk.Frame(root, bg="#f7f1e3", pady=5)
discount_frame.pack(fill="x", padx=10)
tk.Label(discount_frame, text="Discount (%):", bg="#f7f1e3").pack(side="left", padx=5)
tk.Entry(discount_frame, textvariable=discount_percent, width=10).pack(side="left")

# Item Frame
item_frame = tk.LabelFrame(root, text="Bill Details", bg="#c7ecee", padx=10, pady=10)
item_frame.pack(fill="x", padx=10, pady=10)

item_name_var = tk.StringVar()
item_qty_var = tk.IntVar()
item_price_var = tk.DoubleVar()

columns = ("Item", "Quantity", "Price")
tree = ttk.Treeview(item_frame, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')
tree.grid(row=1, column=0, columnspan=8, pady=10, sticky="nsew")

for i in range(8):
    item_frame.grid_columnconfigure(i, weight=1)

# Item Entry
tk.Label(item_frame, text="Item Name:", bg="#c7ecee").grid(row=2, column=0, padx=5, pady=5, sticky="e")
tk.Entry(item_frame, textvariable=item_name_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
tk.Label(item_frame, text="Quantity:", bg="#c7ecee").grid(row=2, column=2, padx=5, pady=5, sticky="e")
tk.Entry(item_frame, textvariable=item_qty_var).grid(row=2, column=3, padx=5, pady=5, sticky="ew")
tk.Label(item_frame, text="Price:", bg="#c7ecee").grid(row=2, column=4, padx=5, pady=5, sticky="e")
tk.Entry(item_frame, textvariable=item_price_var).grid(row=2, column=5, padx=5, pady=5, sticky="ew")

def add_item():
    name = item_name_var.get().strip()
    qty = item_qty_var.get()
    price = item_price_var.get()
    if name and qty > 0 and price > 0:
        items.append((name, qty, price))
        tree.insert('', 'end', values=(name, qty, price))
        item_name_var.set("")
        item_qty_var.set(0)
        item_price_var.set(0.0)
    else:
        messagebox.showwarning("Invalid Input", "Enter valid item details.")

def remove_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select an item to remove.")
        return
    for iid in selected:
        val = tree.item(iid, 'values')
        try:
            items.remove((val[0], int(val[1]), float(val[2])))
        except:
            continue
        tree.delete(iid)

tk.Button(item_frame, text="Add Item", command=add_item, bg="#00cec9", fg="white").grid(row=2, column=6, padx=5)
tk.Button(item_frame, text="Remove Item", command=remove_item, bg="#e17055", fg="white").grid(row=2, column=7, padx=5)

# Bill Preview
preview_frame = tk.LabelFrame(root, text="Bill Preview", bg="#f7f1e3")
preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

bill_text = tk.Text(preview_frame, height=12, bg="#ecf0f1", fg="#2c3e50", font=("Consolas", 10))
bill_text.pack(fill="both", expand=True, padx=5, pady=5)

def calculate_total():
    bill_text.delete(1.0, tk.END)
    subtotal = sum(q * p for _, q, p in items)
    discount = subtotal * (discount_percent.get() / 100)
    total = subtotal - discount

    bill_text.insert(tk.END, f"\t\tRainbow Collection\n")
    bill_text.insert(tk.END, f"\t\t  (Your Address Here)\n\n")
    bill_text.insert(tk.END, f"Customer: {name_var.get()}\tPhone: {phone_var.get()}\n")
    bill_text.insert(tk.END, "=" * 50 + "\n")
    bill_text.insert(tk.END, f"{'Item':<15}{'Qty':<10}{'Total Price':<10}\n")
    bill_text.insert(tk.END, "=" * 50 + "\n")
    for n, q, p in items:
        bill_text.insert(tk.END, f"{n:<15}{q:<10}{q*p:.2f}\n")
    bill_text.insert(tk.END, "=" * 50 + "\n")
    bill_text.insert(tk.END, f"Subtotal: {subtotal:.2f}\n")
    bill_text.insert(tk.END, f"Discount ({discount_percent.get():.1f}%): {discount:.2f}\n")
    bill_text.insert(tk.END, f"Total Amount: {total:.2f}\n")
    bill_text.insert(tk.END, "=" * 50 + "\nThank you for shopping with us!\n")

def print_bill():
    messagebox.showinfo("Print", "Simulating sending bill to printer...")

def generate_pdf():
    content = bill_text.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("Empty Bill", "Please calculate the bill first.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not filename:
        return
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 40, "Rainbow Collection")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 60, "Your Address, City, State")
    current_y = height - 90
    c.setFont("Helvetica", 10)
    for line in content.split("\n"):
        c.drawString(50, current_y, line)
        current_y -= 14
        if current_y < 50:
            c.showPage()
            current_y = height - 50
    c.save()
    messagebox.showinfo("Saved", f"PDF saved to {filename}")

# Buttons
btn_frame = tk.Frame(root, bg="#f7f1e3")
btn_frame.pack(fill="x", padx=10, pady=10)
btn_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

buttons = [
    ("Calculate Bill", calculate_total, "#0984e3"),
    ("Print", print_bill, "#00b894"),
    ("Clear All", lambda: [bill_text.delete(1.0, tk.END), items.clear(), tree.delete(*tree.get_children()), name_var.set(""), phone_var.set(""), discount_percent.set(0.0)], "#d63031"),
    ("Exit", root.destroy, "#636e72"),
    ("Generate PDF", generate_pdf, "#6c5ce7")
]

for idx, (txt, cmd, color) in enumerate(buttons):
    tk.Button(btn_frame, text=txt, command=cmd, bg=color, fg="white").grid(row=0, column=idx, padx=5, sticky="ew")

# Watermark
watermark_label = tk.Label(root, text="By Satyam...", font=("Helvetica", 8, "italic"), fg="#2200FF", bg="#f7f1e3")
watermark_label.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

root.mainloop()
