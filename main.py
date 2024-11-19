import tkinter as tk
from tkinter import messagebox, filedialog

def generate_gcode():
    dispenser_position = dispenser_position_entry.get().strip() # NEED TO ADD DECRIMENTS AFTER EACH LAYER
    layer_height = layer_height_entry.get().strip()
    dlp_position = dlp_position_entry.get().strip()

    if not dispenser_position or not layer_height or not dlp_position:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        dispenser_position = float(dispenser_position)
        layer_height = float(layer_height)
        dlp_position = float(dlp_position)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please use numeric values.")
        return

    if layer_height <= 0:
        messagebox.showerror("Error", "Layer height must be greater than zero.")
        return

    # Generate GCode for a single layer
    gcode = (
        "G21 ; Set units to millimeters\n"
        "G90 ; Use absolute positioning\n"
        f"G1 Z{layer_height:.2f} F100 ; Set layer height\n"
        f"G1 X{dispenser_position:.2f} F500 ; Move dispenser to absolute position\n"
        f"G1 Y{dlp_position:.2f} F300 ; Move DLP to specified position\n"
        f"M0 ; Pause for manual verification\n"
    ) # ADD MORE FUNCTIONS HERERE

    gcode_output.delete("1.0", tk.END)
    gcode_output.insert(tk.END, gcode)

def save_gcode():
    gcode = gcode_output.get("1.0", tk.END).strip()
    if not gcode:
        messagebox.showwarning("Warning", "No GCode to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".gcode",
        filetypes=[("GCode files", "*.gcode"), ("Text files", "*.txt")],
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(gcode)
        messagebox.showinfo("Success", f"GCode saved to {file_path}")

def show_about():
    messagebox.showinfo(
        "About",
        "GCode Generator for Single Layer Setup\n\n"
        "Created by Kevin Wan\n"
        "This tool generates GCode for a custom setup involving "
        "a dispenser, DLP positioning, and layer height adjustments."
    )


app = tk.Tk()
app.title("GCode Generator for Single Layer Setup")
app.geometry("600x500")

# Input fields
tk.Label(app, text="Dispenser Position (Absolute, mm):").pack(pady=5)
dispenser_position_entry = tk.Entry(app, width=50)
dispenser_position_entry.pack()

tk.Label(app, text="Layer Height (mm):").pack(pady=5)
layer_height_entry = tk.Entry(app, width=50)
layer_height_entry.pack()

tk.Label(app, text="DLP Position (mm):").pack(pady=5)
dlp_position_entry = tk.Entry(app, width=50)
dlp_position_entry.pack()

# Buttons
generate_button = tk.Button(app, text="Generate GCode", command=generate_gcode)
generate_button.pack(pady=10)

save_button = tk.Button(app, text="Save GCode", command=save_gcode)
save_button.pack(pady=5)

# Output display
tk.Label(app, text="Generated GCode:").pack(pady=5)
gcode_output = tk.Text(app, height=20, width=70)
gcode_output.pack()

# Attribution
tk.Label(app, text="Made by Kevin Wan", font=("Arial", 12, "italic")).pack(side="bottom", pady=10)

# Run the application
app.mainloop()
