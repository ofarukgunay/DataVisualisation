import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class CombinedApp:
    def __init__(self, root):
        # Initialize the application with the main window
        self.root = root
        self.root.title("Unified Application")  # Set the title of the main window
        self.root.geometry("900x700")  # Set the default window size
        self.dataframe = None  # Placeholder for the data loaded from a CSV file

        # Create a notebook widget to organize tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add the main tab for CSV operations and visualizations
        self.init_csv_editor_tab()

    def init_csv_editor_tab(self):
        # Initialize the main screen (CSV Editor Tab)
        self.csv_frame = ttk.Frame(self.notebook)  # Create a frame for the tab
        self.notebook.add(self.csv_frame, text="CSV Project")  # Add the tab to the notebook

        # UI elements for loading a CSV file
        self.file_label = tk.Label(self.csv_frame, text="Load CSV File:")  # Label for file loading
        self.file_label.pack(pady=5)

        self.load_button = tk.Button(self.csv_frame, text="Select File", command=self.load_csv)  # Button to load a file
        self.load_button.pack(pady=5)

        # Treeview widget to display the CSV data in a tabular format
        self.tree = ttk.Treeview(self.csv_frame, columns=(), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Entry for adding new rows to the CSV data
        self.entry_label = tk.Label(
            self.csv_frame, text="Enter Values Separated by Commas to Add a New Row:")
        self.entry_label.pack(pady=5)

        self.entry = tk.Entry(self.csv_frame, width=80)  # Input box for new row data
        self.entry.pack(pady=5)

        # Buttons for adding rows, columns, and saving the data
        self.add_row_button = tk.Button(
            self.csv_frame, text="Add Row", command=self.add_row)
        self.add_row_button.pack(pady=5)

        self.add_column_button = tk.Button(
            self.csv_frame, text="Add Column", command=self.add_column)
        self.add_column_button.pack(pady=5)

        self.save_button = tk.Button(self.csv_frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(pady=10)

        # Buttons for generating visualizations
        self.plot_heatmap_button = tk.Button(
            self.csv_frame, text="Plot Heatmap", command=self.plot_heatmap)
        self.plot_heatmap_button.pack(pady=5)

        self.plot_first_line_chart_button = tk.Button(
            self.csv_frame, text="Plot First Line Chart", command=lambda: self.plot_line_chart(0))
        self.plot_first_line_chart_button.pack(pady=5)

        self.plot_second_line_chart_button = tk.Button(
            self.csv_frame, text="Plot Second Line Chart", command=lambda: self.plot_line_chart(1))
        self.plot_second_line_chart_button.pack(pady=5)

        self.plot_pie_chart_button = tk.Button(
            self.csv_frame, text="Plot Pie Chart", command=self.plot_pie_chart)
        self.plot_pie_chart_button.pack(pady=5)

    def load_csv(self):
        # Load a CSV file and display its content in the Treeview widget
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")], title="Select CSV File")  # File dialog to select a CSV file
        if file_path:
            self.dataframe = pd.read_csv(file_path)  # Read the CSV file into a DataFrame
            self.show_data()  # Display the data in the Treeview

    def show_data(self):
        # Display the data from the DataFrame in the Treeview widget
        if self.dataframe is not None:
            self.tree.delete(*self.tree.get_children())  # Clear existing data in the Treeview
            self.tree["columns"] = list(self.dataframe.columns)  # Set column names from the DataFrame
            for col in self.dataframe.columns:
                self.tree.heading(col, text=col)  # Set column headings
                self.tree.column(col, width=100)  # Set column width

            # Insert rows into the Treeview
            for _, row in self.dataframe.iterrows():
                self.tree.insert("", "end", values=row.to_list())

    def add_row(self):
        # Add a new row to the DataFrame based on user input
        new_row = self.entry.get()
        if self.dataframe is not None and new_row:
            new_data = new_row.split(",")  # Split the input string into values
            if len(new_data) == len(self.dataframe.columns):  # Check if the number of values matches the columns
                self.dataframe.loc[len(self.dataframe)] = new_data  # Append the new row to the DataFrame
                self.show_data()  # Refresh the Treeview
                self.entry.delete(0, tk.END)  # Clear the input box
                messagebox.showinfo("Success", "New row added.")
            else:
                messagebox.showerror(
                    "Error", "The number of values does not match the number of columns.")

    def add_column(self):
        # Add a new column to the DataFrame
        if self.dataframe is not None:
            column_name = tk.simpledialog.askstring("New Column", "Enter the name of the new column:")  # Prompt for column name
            if column_name:
                self.dataframe[column_name] = ""  # Add an empty column to the DataFrame
                self.show_data()  # Refresh the Treeview
                messagebox.showinfo("Success", f"Column '{column_name}' added.")

    def save_csv(self):
        # Save the current DataFrame to a CSV file
        if self.dataframe is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV File")  # File dialog to specify the save location
            if file_path:
                self.dataframe.to_csv(file_path, index=False)  # Save the DataFrame to the specified file
                messagebox.showinfo("Success", "File saved successfully.")

    def plot_heatmap(self):
        # Generate a heatmap visualization of final scores
        if self.dataframe is not None:
            if "Final" not in self.dataframe.columns or "Student" not in self.dataframe.columns or "Course" not in self.dataframe.columns:
                messagebox.showerror("Error", "Required columns 'Final', 'Student', or 'Course' not found in the data.")
                return

            # Pivot table to organize data for the heatmap
            heatmap_data = self.dataframe.pivot(index="Student", columns="Course", values="Final")

            fig, ax = plt.subplots(figsize=(10, 7))  # Create a figure for the heatmap
            cax = ax.imshow(heatmap_data, cmap="viridis", aspect="auto")  # Display the heatmap

            # Annotate the heatmap with the scores
            for i in range(len(heatmap_data.index)):
                for j in range(len(heatmap_data.columns)):
                    value = heatmap_data.iloc[i, j]
                    if not pd.isna(value):
                        ax.text(j, i, f"{value:.1f}", ha="center", va="center", color="white")

            ax.set_xticks(np.arange(len(heatmap_data.columns)))  # Set x-axis ticks for courses
            ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")  # Set course names on x-axis
            ax.set_yticks(np.arange(len(heatmap_data.index)))  # Set y-axis ticks for students
            ax.set_yticklabels(heatmap_data.index)  # Set student names on y-axis

            plt.colorbar(cax, label="Final Scores")  # Add a colorbar for the heatmap
            plt.title("Heatmap of Final Scores by Course and Student")  # Set the title
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showerror("Error", "No data loaded.")

    def plot_line_chart(self, column_index):
        # Generate a line chart based on a numeric column
        if self.dataframe is not None:
            numeric_columns = self.dataframe.select_dtypes(include=["int", "float"]).columns  # Select numeric columns
            if column_index < len(numeric_columns):
                column = numeric_columns[column_index]  # Get the specified numeric column
                plt.figure(figsize=(10, 6))  # Create a figure for the line chart
                plt.plot(self.dataframe.index, self.dataframe[column], marker="o", linestyle="-", label=column)  # Plot the data
                plt.title(f"Line Chart of {column}")  # Set the title
                plt.xlabel("Index")  # Label for x-axis
                plt.ylabel(column)  # Label for y-axis
                plt.legend()  # Add a legend
                plt.grid(True, linestyle="--", alpha=0.7)  # Add grid lines
                plt.show()
            else:
                messagebox.showerror("Error", "Invalid column index for line chart.")
        else:
            messagebox.showerror("Error", "No data loaded.")

    def plot_pie_chart(self):
        # Generate a pie chart based on the distribution of grades
        if self.dataframe is not None:
            if "Grade" not in self.dataframe.columns:
                messagebox.showerror("Error", "Required column 'Grade' not found in the data.")
                return

            grade_counts = self.dataframe["Grade"].value_counts()  # Count the occurrences of each grade
            labels = grade_counts.index  # Get the unique grades as labels
            sizes = grade_counts.values  # Get the counts as sizes

            fig, ax = plt.subplots(figsize=(8, 8))  # Create a figure for the pie chart
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.tab10.colors)  # Create the pie chart
            ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular
            plt.title("Grade Distribution")  # Set the title
            plt.show()
        else:
            messagebox.showerror("Error", "No data loaded.")

if __name__ == "__main__":
    # Start the application
    root = tk.Tk()
    app = CombinedApp(root)  # Create an instance of the application
    root.mainloop()  # Run the main loop
