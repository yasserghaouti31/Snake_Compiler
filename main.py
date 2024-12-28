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
        # Display the file content in the text box
       
        # Store the source code for further analysis
        global current_source_code
        current_source_code = source_code

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
# Changing the Icon button to snake logo
photo = tk.PhotoImage(file='snake.png')
root.wm_iconphoto(False,photo)
root.title("SNAKE Compiler")

# Set up the frame
frame = tk.Frame(root)
frame.pack(padx=20, pady=10)
icon = tk.PhotoImage(file='folder.png')
# Load file button
load_button=tk.Button(frame,text='Load file .snk',command=load_file)
load_button.pack(fill=tk.X, pady=5)
# Lexique button
lexique_button = tk.Button(frame, text="Lexical Analysis", command=analyze_lexique)
lexique_button.pack(fill=tk.X, pady=5)

# Syntax button
syntax_button = tk.Button(frame, text="Syntax Analysis", command=analyze_syntax)
syntax_button.pack(fill=tk.X, pady=5)

# Semantic button
semantic_button = tk.Button(frame, text="Semantic Analysis", command=analyze_semantic)
semantic_button.pack(fill=tk.X, pady=5)


# Results box to display the analysis results
results_label = tk.Label(frame, text="Analysis Results:")
results_label.pack(anchor="w", pady=10)

results_box = ScrolledText(frame, height=30, width=50)
results_box.pack(pady=20)

# Store the source code globally
current_source_code = ""

# Run the Tkinter event loop
root.mainloop()
