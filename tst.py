import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import algorithms as algos

sorting_functions = [algos.insertion_sort, algos.merge_sort, algos.heap_sort, algos.bubble_sort, algos.quick_sort, algos.counting_sort, algos.selection_sort, algos.shell_sort, algos.radix_sort, algos.bucket_sort]
algorithms = ["Insertion Sort", "Merge Sort", "Heap Sort", "Bubble Sort", "Quick Sort", "Counting Sort", "Selection Sort", "Shell Sort", "Radix Sort", "Bucket Sort"]
data_options = ["Custom Data", "Best Case", "Worst Case", "Random Data"]
growth_functions = ["n", "nlogn", "n^2", "2^n"]

def open_custom_data_window(n):
    def handle_confirm():
        try:
            # Create and hide the root window
            file_dialog_root = tk.Tk()
            file_dialog_root.withdraw()

            # Open file chooser dialog
            absolute_path = filedialog.askopenfilename(
                title="Select Input File",
                filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
            )

            # If user cancels file selection
            if not absolute_path:
                raise FileNotFoundError("No file selected")

            algos.readCustomArray(absolute_path, n)
            messagebox.showinfo("Success", "Custom data loaded successfully.")
            custom_data_window.destroy()
            
        except FileNotFoundError:
            messagebox.showerror("Error", "No file selected or file not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid file format. Please enter a valid CSV or XLSX file.")

    custom_data_window = tk.Toplevel()
    custom_data_window.title("Load Custom Data for Algorithm " + str(n))
    custom_data_window.geometry("400x150")
    custom_data_window.resizable(False, False)

    tk.Label(custom_data_window, text="Click to choose a CSV/XLSX file").pack(pady=10)
    confirm_button = tk.Button(custom_data_window, text="Choose", command=handle_confirm)
    confirm_button.pack(pady=10)

    return custom_data_window

def plot_graph_from_csv(parent, csv_file1, csv_file2, csv_growth_lower=None, csv_growth_upper=None, factors=None, alg1_index=None, alg2_index=None):
    data1 = pd.read_csv(csv_file1)
    if(csv_file2):
        data2 = pd.read_csv(csv_file2)
    fig, ax = plt.subplots()
    ax.plot(data1.iloc[:, 0], data1.iloc[:, 1], marker='o', linestyle='-', color='blue', label=f"{algorithms[alg1_index]}")
    if(csv_file2):    
        ax.plot(data2.iloc[:, 0], data2.iloc[:, 1], marker='s', linestyle='--', color='red', label=f"{algorithms[alg2_index]}")
    
    if csv_growth_lower and csv_growth_upper:
        growth_lower = pd.read_csv(csv_growth_lower)
        growth_upper = pd.read_csv(csv_growth_upper)
        ax.plot(growth_lower.iloc[:, 0], growth_lower.iloc[:, 1], linestyle='-.', color='green', label=f"{factors[0]:.3f} {growth_functions[dropdown_data2.current()]}")
        ax.plot(growth_upper.iloc[:, 0], growth_upper.iloc[:, 1], linestyle=':', color='orange', label=f"{factors[1]:.3f} {growth_functions[dropdown_data2.current()]}")

    ax.set_xlabel("n")
    ax.set_ylabel("steps")
    ax.legend()
    fig.tight_layout()
    fig.patch.set_facecolor("#f9f9f9")
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

current_plot = None

input_size_entry = None
step_entry = None

def update_global_values():
        try:
            algos.n = int(input_size_entry.get())
            algos.step = int(step_entry.get())
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid integers for Input Size and Step.")


def switch_to_plot(parent, placeholder):
    global current_plot
    if current_plot: current_plot.destroy()
    else: placeholder.destroy()
    current_plot = tk.Frame(parent)
    current_plot.pack(fill=tk.BOTH, expand=True)
    alg1_index, data1_index, alg2_selection = dropdown_alg1.current(), dropdown_data1.current(), dropdown_alg2.get()
    csv_file1, csv_file2 = "", ""
    csv_growth_lower, csv_growth_upper = None, None
    factors = None
    if alg1_index != -1 and data1_index != -1:
        update_global_values()
        function1, data_option1 = sorting_functions[alg1_index], data_options[data1_index]
        if data_option1 == "Custom Data":
            custom_data_window = open_custom_data_window(1)
            custom_data_window.wait_window()
            csv_file1 = f"{function1.__name__}_{data_option1.replace(' ', '_')}_1.csv"
        else:
            csv_file1 = f"{function1.__name__}_{data_option1.replace(' ', '_')}.csv"
        algos.calculateTime(sorting_functions[alg1_index], data1_index)

    if alg2_selection == "Compare to Asymptotic growth":
        growth_index = dropdown_data2.current()
        if growth_index != -1:
            csv_growth_lower = f"growth_{growth_functions[growth_index]}_lower.csv"
            csv_growth_upper = f"growth_{growth_functions[growth_index]}_upper.csv"
            factors = algos.createGrowthCSV(growth_index)

    else:
        alg2_index, data2_index = dropdown_alg2.current() - 1, dropdown_data2.current()
        if alg2_index != -1 and data2_index != -1:
            function2, data_option2 = sorting_functions[alg2_index], data_options[data2_index]
            if data_option2 == "Custom Data":
                custom_data_window = open_custom_data_window(2)
                custom_data_window.wait_window()
                csv_file2 = f"{function2.__name__}_{data_option2.replace(' ', '_')}_2.csv"
            else:
                csv_file2 = f"{function2.__name__}_{data_option2.replace(' ', '_')}.csv"
            algos.calculateTime(sorting_functions[alg2_index], data2_index)

    if csv_file1 and csv_file2:
        plot_graph_from_csv(current_plot, csv_file1, csv_file2, csv_growth_lower, csv_growth_upper, factors, alg1_index, alg2_index)

    elif csv_file1 and csv_growth_lower and csv_growth_upper:
        plot_graph_from_csv(current_plot, csv_file1, csv_file2, csv_growth_lower, csv_growth_upper, factors, alg1_index)


def create_placeholder_rectangle(parent):
    placeholder = tk.Frame(parent, bg="#d9d9d9", bd=2, relief="solid")
    placeholder.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    return placeholder

def update_second_dropdown(*args):
    if dropdown_alg2.get() == "Compare to Asymptotic growth":
        dropdown_data2["values"] = growth_functions
        label_data2["text"] = "Choose Growth Function:"
    else:
        dropdown_data2["values"] = data_options
        label_data2["text"] = "Data for Algorithm 2:"

def main():
    root = tk.Tk()
    root.title("Algorithm Comparator")
    root.geometry("900x700")
    root.configure(bg="#f2f2f2")
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=2)
    root.grid_rowconfigure(3, weight=5)
    root.grid_columnconfigure(0, weight=1)

    title = tk.Label(root, text="Algorithm Comparator", font=("Arial", 28, "bold"), bg="#f2f2f2", fg="#333333")
    title.grid(row=0, column=0, sticky="", pady=20)

    hbox1 = tk.Frame(root, bg="#f2f2f2")
    hbox1.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    hbox1.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    tk.Label(hbox1, text="Algorithm 1:", bg="#f2f2f2", font=("Arial", 12), anchor="e").grid(row=0, column=0, sticky="e", padx=5)
    global dropdown_alg1
    dropdown_alg1 = ttk.Combobox(hbox1, values=algorithms, state="readonly")
    dropdown_alg1.grid(row=0, column=1, sticky="ew", padx=5)

    tk.Label(hbox1, text="Compare To:", bg="#f2f2f2", font=("Arial", 12), anchor="e").grid(row=0, column=2, sticky="e", padx=5)
    global dropdown_alg2
    dropdown_alg2 = ttk.Combobox(hbox1, values=["Compare to Asymptotic growth"] + algorithms, state="readonly")
    dropdown_alg2.grid(row=0, column=3, sticky="ew", padx=5)
    dropdown_alg2.bind("<<ComboboxSelected>>", update_second_dropdown)

    show_graph_btn = tk.Button(hbox1, text="Show Graph", bg="#007BFF", fg="white", font=("Arial", 12, "bold"), relief="flat", command=lambda: switch_to_plot(graph_frame, placeholder))
    show_graph_btn.grid(row=0, column=4, sticky="e", padx=5)

    hbox2 = tk.Frame(root, bg="#f2f2f2")
    hbox2.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
    hbox2.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tk.Label(hbox2, text="Data for Algorithm 1:", bg="#f2f2f2", font=("Arial", 12), anchor="e").grid(row=0, column=0, sticky="e", padx=5)
    global dropdown_data1
    dropdown_data1 = ttk.Combobox(hbox2, values=data_options, state="readonly")
    dropdown_data1.grid(row=0, column=1, sticky="ew", padx=5)

    global label_data2
    label_data2 = tk.Label(hbox2, text="Data for Algorithm 2:", bg="#f2f2f2", font=("Arial", 12), anchor="e")
    label_data2.grid(row=0, column=2, sticky="e", padx=5)

    global dropdown_data2
    dropdown_data2 = ttk.Combobox(hbox2, values=data_options, state="readonly")
    dropdown_data2.grid(row=0, column=3, sticky="ew", padx=5)

    tk.Label(hbox2, text="Input Size (n):", bg="#f2f2f2", font=("Arial", 12), anchor="e").grid(row=0, column=4, sticky="e", padx=5)
    global input_size_entry
    input_size_entry = ttk.Entry(hbox2)
    input_size_entry.insert(0, "1000")  # Default value
    input_size_entry.grid(row=0, column=5, sticky="ew", padx=5)

    tk.Label(hbox2, text="Step:", bg="#f2f2f2", font=("Arial", 12), anchor="e").grid(row=0, column=6, sticky="e", padx=5)
    global step_entry
    step_entry = ttk.Entry(hbox2)
    step_entry.insert(0, "10")  # Default value
    step_entry.grid(row=0, column=7, sticky="ew", padx=5)

    graph_frame = tk.Frame(root, bg="#f2f2f2")
    graph_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
    placeholder = create_placeholder_rectangle(graph_frame)

    root.mainloop()

if __name__ == "__main__":
    main()
