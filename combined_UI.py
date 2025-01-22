import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class CombinedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unified Application")
        self.root.geometry("900x700")
        self.dataframe = None

        # Initialize notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add main tab
        self.init_csv_editor_tab()

    def init_csv_editor_tab(self):
        # CSV Editor Tab
        self.csv_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.csv_frame, text="Main Screen")

        self.file_label = tk.Label(self.csv_frame, text="Load CSV File:")
        self.file_label.pack(pady=5)

        self.load_button = tk.Button(self.csv_frame, text="Select File", command=self.load_csv)
        self.load_button.pack(pady=5)

        self.tree = ttk.Treeview(self.csv_frame, columns=(), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        self.entry_label = tk.Label(
            self.csv_frame, text="Enter Values Separated by Commas to Add a New Row:")
        self.entry_label.pack(pady=5)

        self.entry = tk.Entry(self.csv_frame, width=80)
        self.entry.pack(pady=5)

        self.add_row_button = tk.Button(
            self.csv_frame, text="Add Row", command=self.add_row)
        self.add_row_button.pack(pady=5)

        self.add_column_button = tk.Button(
            self.csv_frame, text="Add Column", command=self.add_column)
        self.add_column_button.pack(pady=5)

        self.save_button = tk.Button(self.csv_frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(pady=10)

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
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")], title="Select CSV File")
        if file_path:
            self.dataframe = pd.read_csv(file_path)
            self.show_data()

    def show_data(self):
        if self.dataframe is not None:
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(self.dataframe.columns)
            for col in self.dataframe.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            for _, row in self.dataframe.iterrows():
                self.tree.insert("", "end", values=row.to_list())

    def add_row(self):
        new_row = self.entry.get()
        if self.dataframe is not None and new_row:
            new_data = new_row.split(",")
            if len(new_data) == len(self.dataframe.columns):
                self.dataframe.loc[len(self.dataframe)] = new_data
                self.show_data()
                self.entry.delete(0, tk.END)
                messagebox.showinfo("Success", "New row added.")
            else:
                messagebox.showerror(
                    "Error", "The number of values does not match the number of columns.")

    def add_column(self):
        if self.dataframe is not None:
            column_name = tk.simpledialog.askstring("New Column", "Enter the name of the new column:")
            if column_name:
                self.dataframe[column_name] = ""
                self.show_data()
                messagebox.showinfo("Success", f"Column '{column_name}' added.")

    def save_csv(self):
        if self.dataframe is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save CSV File")
            if file_path:
                self.dataframe.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "File saved successfully.")

    def plot_heatmap(self):
        if self.dataframe is not None:
            if "Final" not in self.dataframe.columns or "Student" not in self.dataframe.columns or "Course" not in self.dataframe.columns:
                messagebox.showerror("Error", "Required columns 'Final', 'Student', or 'Course' not found in the data.")
                return

            # Pivot table to organize data for the heatmap
            heatmap_data = self.dataframe.pivot(index="Student", columns="Course", values="Final")

            fig, ax = plt.subplots(figsize=(10, 7))
            cax = ax.imshow(heatmap_data, cmap="viridis", aspect="auto")

            # Annotate the heatmap with the scores
            for i in range(len(heatmap_data.index)):
                for j in range(len(heatmap_data.columns)):
                    value = heatmap_data.iloc[i, j]
                    if not pd.isna(value):
                        ax.text(j, i, f"{value:.1f}", ha="center", va="center", color="white")

            ax.set_xticks(np.arange(len(heatmap_data.columns)))
            ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")
            ax.set_yticks(np.arange(len(heatmap_data.index)))
            ax.set_yticklabels(heatmap_data.index)

            plt.colorbar(cax, label="Final Scores")
            plt.title("Heatmap of Final Scores by Course and Student")
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showerror("Error", "No data loaded.")

    def plot_line_chart(self, column_index):
        if self.dataframe is not None:
            numeric_columns = self.dataframe.select_dtypes(include=["int", "float"]).columns
            if column_index < len(numeric_columns):
                column = numeric_columns[column_index]
                plt.figure(figsize=(10, 6))
                plt.plot(self.dataframe.index, self.dataframe[column], marker="o", linestyle="-", label=column)
                plt.title(f"Line Chart of {column}")
                plt.xlabel("Index")
                plt.ylabel(column)
                plt.legend()
                plt.grid(True, linestyle="--", alpha=0.7)
                plt.show()
            else:
                messagebox.showerror("Error", "Invalid column index for line chart.")
        else:
            messagebox.showerror("Error", "No data loaded.")

    def plot_pie_chart(self):
        if self.dataframe is not None:
            if "Grade" not in self.dataframe.columns:
                messagebox.showerror("Error", "Required column 'Grade' not found in the data.")
                return

            grade_counts = self.dataframe["Grade"].value_counts()
            labels = grade_counts.index
            sizes = grade_counts.values

            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.tab10.colors)
            ax.axis("equal")  # Equal aspect ratio ensures the pie chart is circular.
            plt.title("Grade Distribution")
            plt.show()
        else:
            messagebox.showerror("Error", "No data loaded.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedApp(root)
    root.mainloop()
