import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from GA import *
from SA import *
import numpy as np

# Default number of runs to get performance statistics
it = 5  

### Functions for running comparison and collecting parameters ###
def comparison():
    global it  # Ensure the updated `it` is used globally

    # GA
    GAfit = []
    for i in range(it):
        while True:
            try:
                out, ct = GA_Code.run()
                GAfit.append(ct)
                if i == 0:
                    GA_best = out
                    GA_ct = ct
                elif out < GA_best:
                    GA_best = out
                    GA_ct = ct
                break
            except (IndexError, ZeroDivisionError) as e:
                print(f"Error occurred in GA_Code.run() during iteration {i}: {e}")
                print("Retrying iteration...")
                continue

    # SA
    SAfit = []
    for i in range(it):
        while True:
            try:
                out, ct = SA_Code.run()
                SAfit.append(ct)
                if i == 0:
                    SA_best = out
                    SA_ct = ct
                elif out < SA_best:
                    SA_best = out
                    SA_ct = ct
                break
            except (IndexError, ZeroDivisionError) as e:
                print(f"Error occurred in SA_Code.run() during iteration {i}: {e}")
                print("Retrying iteration...")
                continue

    # Performance statistics
    GAavg = sum(GAfit) / it
    GAstd = np.std(GAfit)
    SAavg = sum(SAfit) / it
    SAstd = np.std(SAfit)
    return GA_best, GA_ct, GAavg, GAstd, SA_best, SA_ct, SAavg, SAstd

def collect_general_parameters():
    try:
        root = tk.Tk()
        root.title("General Parameters")
        root.attributes('-topmost', True)  
        params = {}
        labels = ["Number of drones", "Maximum distance", "Safe distance","Maximum iterations for all algorithms"]
        inputs = {}

        def submit():
            try:
                params["num_drones"] = int(inputs["Number of drones"].get())
                params["max_dist"] = float(inputs["Maximum distance"].get())
                params["safe_dist"] = float(inputs["Safe distance"].get())
                params["Max_it"] = int(inputs["Maximum iterations for all algorithms"].get())
                # Validation checks
                if params["num_drones"] <= 0:
                    messagebox.showerror("Input Error", "Number of drones must be greater than 0.")
                    return
                if params["max_dist"] < 1:
                    messagebox.showerror("Input Error", "maximum distance must be greater than 0.")
                    return
                if params["safe_dist"] <= 0:
                    messagebox.showerror("Input Error", "safe distance must be greater than 0.")
                    return
                if params["Max_it"] <= 0: 
                    messagebox.showerror("Input Error", "Number of iterations must be greater than 0.")
                    return
                
                root.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric values.")

        for i, label in enumerate(labels):
            ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            inputs[label] = entry

        ttk.Button(root, text="Submit", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)
        root.mainloop()

        return params if params else None
    except Exception:
        return None

import tkinter as tk
from tkinter import ttk, messagebox

def collect_ga_parameters():
    try:
        root = tk.Tk()
        root.title("GA Parameters")
        root.attributes('-topmost', True)

        params = {}
        labels = ["Number of parents", "Number of children", "Number of mutants", "Number of elites"]
        inputs = {}

        def submit():
            try:
                # Get inputs and convert them to integers
                params["num_parents"] = int(inputs["Number of parents"].get())
                params["num_children"] = int(inputs["Number of children"].get())
                params["num_mutants"] = int(inputs["Number of mutants"].get())
                params["num_elites"] = int(inputs["Number of elites"].get())

                # Validation checks
                if params["num_parents"] <= 1:
                    messagebox.showerror("Input Error", "Number of parents must be greater than or equal to 1.")
                    return
                if params["num_children"] > params["num_parents"] * 2:
                    messagebox.showerror("Input Error", "Number of children must not exceed twice the number of parents.")
                    return
                if params["num_mutants"] <= 0:
                    messagebox.showerror("Input Error", "Number of mutants must be greater than 0.")
                    return
                if params["num_elites"] <= 0:
                    messagebox.showerror("Input Error", "Number of elites must be greater than 0.")
                    return

                root.destroy()  # If all checks pass, close the window

            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric values.")

        # Create labels and entries dynamically
        for i, label in enumerate(labels):
            ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            inputs[label] = entry

        # Submit button
        ttk.Button(root, text="Submit", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)

        root.mainloop()

        return params if params else None

    except Exception:
        return None


def collect_sa_parameters():
    try:
        root = tk.Tk()
        root.title("SA Parameters")
        root.attributes('-topmost', True)

        params = {}
        labels = ["Final temperature", "Cooling rate", "Initial temperature", "New solutions per iteration"]
        inputs = {}

        def submit():
            try:
                params["final_temp"] = float(inputs["Final temperature"].get())
                params["cooling_rate"] = float(inputs["Cooling rate"].get())
                params["initial_temp"] = float(inputs["Initial temperature"].get())
                params["new_solutions"] = int(inputs["New solutions per iteration"].get())

                # Validation checks
                if params["final_temp"] >= params["initial_temp"]:
                    messagebox.showerror("Input Error", "Final temperature must be smaller than initial temperature.")
                    return
                if params["cooling_rate"] > 1 or params["cooling_rate"] <= 0:
                    messagebox.showerror("Input Error", "Cooling rate must be between 0 and 1.")
                    return
                if params["new_solutions"] <= 0:
                    messagebox.showerror("Input Error", "Number of new solutions must be greater than 0.")
                    return
                root.destroy()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric values.")

        for i, label in enumerate(labels):
            ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ttk.Entry(root)
            entry.grid(row=i, column=1, padx=10, pady=5)
            inputs[label] = entry

        ttk.Button(root, text="Submit", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)
        root.mainloop()

        return params if params else None
    except Exception:
        return None


def collect_it_parameter():
    try:
        root = tk.Tk()
        root.title("Number of Iterations")
        root.attributes('-topmost', True)
        new_it = None

        def submit():
            nonlocal new_it  # Make sure we are updating the new_it from the enclosing scope
            try:
                new_it = int(entry.get())
                if new_it > 0:
                    root.destroy()
                else:
                    messagebox.showerror("Input Error", "Number of iterations must be a positive integer.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric value.")

        ttk.Label(root, text="Enter number of runs for performance analysis:").grid(row=0, column=0, padx=10, pady=5)
        entry = ttk.Entry(root)
        entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(root, text="Submit", command=submit).grid(row=1, column=0, columnspan=2, pady=10)
        root.mainloop()

        return new_it if new_it else None  # Return the updated value
    except Exception:
        return None

# Results GUI
def results_gui(ga_solution, ga_fitness, ga_mean, ga_std, sa_solution, sa_fitness, sa_mean, sa_std):
    root = tk.Tk()
    root.title("Performance Comparison")
    root.attributes('-topmost', True)  # Make the window topmost

    # Create table with an extra column for labels
    table = ttk.Treeview(root, columns=("Label", "GA", "SA"), show="headings", height=4)
    table.heading("Label", text="Performance indices")
    table.heading("GA", text="Genetic Algorithm")
    table.heading("SA", text="Simulated Annealing Algorithm")

    # Insert rows with labels and corresponding values for GA and SA
    table.insert("", "end", values=("Mean Value", f"{ga_mean:.2f}", f"{sa_mean:.2f}"))
    table.insert("", "end", values=("Fitness", f"{ga_fitness:.2f}", f"{sa_fitness:.2f}"))
    table.insert("", "end", values=("Solution", f"{ga_solution}", f"{sa_solution}"))
    table.insert("", "end", values=("Standard Deviation", f"{ga_std:.2f}", f"{sa_std:.2f}"))

    table.grid(row=0, column=0, columnspan=2, pady=10)

    # Results summary (optionally)
    ttk.Label(root, text=f"Best Mean Value: {('GA', round(ga_mean,2)) if ga_mean < sa_mean else ('SA', round(sa_mean,2))}").grid(row=1, column=0, columnspan=2, pady=5)
    ttk.Label(root, text=f"Best Fitness Value: {('GA', round(ga_fitness,2)) if ga_fitness < sa_fitness else ('SA', round(sa_fitness,2))}").grid(row=2, column=0, columnspan=2, pady=5)
    ttk.Label(root, text=f"Best Solution: {('GA', ga_solution) if ga_fitness < sa_fitness else ('SA', sa_solution)}").grid(row=3, column=0, columnspan=2, pady=5)

    root.mainloop()

def ask_use_defaults():
    result = messagebox.askyesnocancel("Use Defaults", "Do you want to use default parameters?")
    if result is None:  # If the user clicks "No" or closes the dialog (which returns False or None)
        sys.exit("Operation canceled by user. Exiting.")
    return result  # Return True if "Yes" is clicked

if __name__ == "__main__":
    use_defaults = ask_use_defaults()
    if not use_defaults:

        general_params = collect_general_parameters()
        if general_params is None:
            sys.exit("General parameter input canceled. Exiting.")

        ga_params = collect_ga_parameters()
        if ga_params is None:
            sys.exit("GA parameter input canceled. Exiting.")

        sa_params = collect_sa_parameters()
        if sa_params is None:
            sys.exit("SA parameter input canceled. Exiting.")

        it=collect_it_parameter() 
        if it is None:
            sys.exit("Number of iterations input canceled. Exiting.")
            
        set_GA_params(general_params['num_drones'],general_params['max_dist'],general_params['safe_dist'],general_params['Max_it'],\
                        ga_params["num_parents"],ga_params["num_children"], ga_params["num_mutants"],ga_params["num_elites"])
        set_SA_params(general_params['num_drones'],general_params['max_dist'],general_params['safe_dist'],general_params['Max_it'],\
                        sa_params["final_temp"],sa_params["cooling_rate"], sa_params["initial_temp"],sa_params["new_solutions"])
    
    results = comparison()
    results_gui(*results)
