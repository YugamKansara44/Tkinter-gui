import tkinter as tk
from tkinter import messagebox

# Constants
ORIGINAL_COST_PER_PAGE = 2.5
DUPLICATE_COST_PER_PAGE = 2.0
COMPOSING_CHARGE = 100.0
PRINTING_CHARGE_BASE = 250
PRINTING_CHARGE_PER_EXTRA = 20
BINDING_COST_PER_BOOK = 25

SIZE_DIVISORS = {
    "1/4": 4,
    "1/5": 5,
    "1/6": 6,
    "1/8": 8,
    "1/12": 12
}

def calculate_price():
    try:
        quantity = int(entry_quantity.get())
        size = size_var.get()

        if size not in SIZE_DIVISORS:
            messagebox.showerror("Invalid Size", "Please select a valid size.")
            return

        divisor = SIZE_DIVISORS[size]
        original_sheets = (100 * quantity) / divisor
        duplicate_sheets = (100 * quantity) / divisor

        original_cost = original_sheets * ORIGINAL_COST_PER_PAGE
        duplicate_cost = duplicate_sheets * DUPLICATE_COST_PER_PAGE
        composing_cost = COMPOSING_CHARGE

        if quantity <= 10:
            printing_cost = PRINTING_CHARGE_BASE
        else:
            printing_cost = PRINTING_CHARGE_BASE + (quantity - 10) * PRINTING_CHARGE_PER_EXTRA

        binding_cost = quantity * BINDING_COST_PER_BOOK

        total_cost = original_cost + duplicate_cost + composing_cost + printing_cost + binding_cost
        cost_per_book = total_cost / quantity

        label_cost_per_book.config(text=f"Cost per Book: ₹{cost_per_book:.2f}")
        label_total_cost.config(text=f"Total Cost: ₹{total_cost:.2f}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid quantity.")

# GUI Setup
root = tk.Tk()
root.title("🧾 Bill Book Price Calculator")
root.geometry("460x460")
root.configure(bg="#f0f2f5")

# ---------- Frames ----------

frame_input = tk.LabelFrame(root, text="🔢 Input", bg="#e9ecef", padx=10, pady=10, font=("Arial", 10, "bold"))
frame_input.pack(padx=15, pady=10, fill="both")

frame_output = tk.LabelFrame(root, text="📊 Output", bg="#e9ecef", padx=10, pady=10, font=("Arial", 10, "bold"))
frame_output.pack(padx=15, pady=5, fill="both")

frame_info = tk.LabelFrame(root, text="📌 Charges Info", bg="#e9ecef", padx=10, pady=5, font=("Arial", 10, "bold"))
frame_info.pack(padx=15, pady=5, fill="both")

# ---------- Inputs ----------
tk.Label(frame_input, text="Quantity of Bill Books:", bg="#e9ecef", font=("Arial", 10)).pack(anchor="w")
entry_quantity = tk.Entry(frame_input, font=("Arial", 10))
entry_quantity.pack(fill="x", pady=5)

tk.Label(frame_input, text="Select Paper Size:", bg="#e9ecef", font=("Arial", 10)).pack(anchor="w")
size_var = tk.StringVar(value="1/4")
size_dropdown = tk.OptionMenu(frame_input, size_var, *SIZE_DIVISORS.keys())
size_dropdown.config(width=10)
size_dropdown.pack(pady=5)

tk.Button(frame_input, text="💰 Calculate Price", command=calculate_price, font=("Arial", 10, "bold"), bg="#007bff", fg="white").pack(pady=10)

# ---------- Output ----------
label_cost_per_book = tk.Label(frame_output, text="Cost per Book: ₹0.00", font=("Arial", 12), bg="#e9ecef")
label_cost_per_book.pack()

label_total_cost = tk.Label(frame_output, text="Total Cost: ₹0.00", font=("Arial", 12, "bold"), bg="#e9ecef")
label_total_cost.pack()

# ---------- Charges Info ----------
tk.Label(frame_info, text=f"""Original Sheet: ₹{ORIGINAL_COST_PER_PAGE}
Duplicate Sheet: ₹{DUPLICATE_COST_PER_PAGE}
Composing (once): ₹{COMPOSING_CHARGE}
Printing:
- ₹{PRINTING_CHARGE_BASE} for up to 10 books
- +₹{PRINTING_CHARGE_PER_EXTRA} per book above 10
Binding per book: ₹{BINDING_COST_PER_BOOK}""",
         font=("Arial", 9), bg="#e9ecef", justify="left").pack(anchor="w")

# Run the app
root.mainloop()
