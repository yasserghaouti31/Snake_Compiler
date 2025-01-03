import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from snake_compiler import lexique_analysis, syntax_analysis, semantic_analysis

# Function to load the .snk file
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("SNAKE Source Files", "*.snk")])
    if file_path:
        with open(file_path, 'r') as file:
            source_code = file.read()
        global current_source_code
        # Store the source code for further analysis
        current_source_code = source_code
        file_label.config(text=f"Loaded: {file_path}", fg='green')

# Function to handle lexique button
def analyze_lexique():
    if not current_source_code:
        messagebox.showerror("Error", "No file loaded.")
        return
    result = lexique_analysis(current_source_code)
    display_results(result)

# Function to handle syntax button
def analyze_syntax():
    if not current_source_code:
        messagebox.showerror("Error", "No file loaded.")
        return
    result = syntax_analysis(current_source_code)
    display_results(result)

# Function to handle semantic button
def analyze_semantic():
    if not current_source_code:
        messagebox.showerror("Error", "No file loaded.")
        return
    result = semantic_analysis(current_source_code)
    display_results(result)

# Function to display results in the text box
def display_results(result):
    results_box.delete(1.0, tk.END)  # Clear the results box before displaying
    results_box.insert(tk.END, result)

# Set up the main Tkinter window
root = tk.Tk()
root.title("SNAKE Compiler")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

# Set window icon
try:
    photo = tk.PhotoImage(file='snake.png')
    root.wm_iconphoto(False, photo)
except:
    pass

# Set up the frame
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=10)

# Load file button
load_button = tk.Button(frame, text='Load .snk File', command=load_file, bg="#4CAF50", fg="white", font=("Arial", 12), relief=tk.RAISED)
load_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

# File status label
file_label = tk.Label(frame, text="No file loaded", bg="#f0f0f0", fg="red", font=("Arial", 10))
file_label.grid(row=0, column=1, padx=10)

# Lexique button
lexique_button = tk.Button(frame, text="Lexical Analysis", command=analyze_lexique, bg="#2196F3", fg="white", font=("Arial", 12), relief=tk.RAISED)
lexique_button.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

# Syntax button
syntax_button = tk.Button(frame, text="Syntax Analysis", command=analyze_syntax, bg="#FFC107", fg="black", font=("Arial", 12), relief=tk.RAISED)
syntax_button.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

# Semantic button
semantic_button = tk.Button(frame, text="Semantic Analysis", command=analyze_semantic, bg="#E91E63", fg="white", font=("Arial", 12), relief=tk.RAISED)
semantic_button.grid(row=3, column=0, pady=5, padx=10, sticky="ew")

# Results box to display the analysis results
results_label = tk.Label(frame, text="Analysis Results:", bg="#f0f0f0", font=("Arial", 12, "bold"))
results_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

results_box = ScrolledText(frame, height=20, width=80, font=("Courier", 10))
results_box.grid(row=5, column=0, columnspan=2, pady=10)

# Store the source code globally
current_source_code = ""

# Run the Tkinter event loop
root.mainloop()
