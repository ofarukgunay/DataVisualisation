import pandas as pd
import matplotlib.pyplot as plt

def read_csv(file_path):
    """Reads a CSV file and returns its contents as a pandas DataFrame."""
    try:
        data = pd.read_csv(file_path)
        print("CSV file loaded successfully.")
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def display_table(data):
    """Displays the contents of a DataFrame in a tabular format."""
    if data is not None:
        print(data.to_string(index=False))
    else:
        print("No data to display.")

def visualize_table(data):
    """Visualizes the contents of the DataFrame as a bar plot for numeric data."""
    if data is not None:
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            data[numeric_cols].plot(kind='bar', figsize=(10, 6))
            plt.title('Bar Plot of Numeric Data')
            plt.xlabel('Index')
            plt.ylabel('Values')
            plt.legend(numeric_cols)
            plt.show()
        else:
            print("No numeric columns to visualize.")
    else:
        print("No data to visualize.")

def edit_value(data, row, column, new_value):
    """Edits a specific value in the DataFrame."""
    try:
        data.at[row, column] = new_value
        print("Value updated successfully.")
    except Exception as e:
        print(f"Error updating value: {e}")

def add_row(data, row_data):
    """Adds a new row to the DataFrame."""
    try:
        data.loc[len(data)] = row_data
        print("Row added successfully.")
    except Exception as e:
        print(f"Error adding row: {e}")

def add_column(data, column_name, default_value):
    """Adds a new column to the DataFrame."""
    try:
        data[column_name] = default_value
        print("Column added successfully.")
    except Exception as e:
        print(f"Error adding column: {e}")

def save_csv(data, file_path):
    """Saves the DataFrame back to a CSV file."""
    try:
        data.to_csv(file_path, index=False)
        print("File saved successfully.")
    except Exception as e:
        print(f"Error saving file: {e}")

# Example Usage
if __name__ == "__main__":
    file_path = input("Enter the CSV file path: ")
    data = read_csv(file_path)

    if data is not None:
        while True:
            print("\nOptions:")
            print("1. Display table")
            print("2. Visualize table")
            print("3. Edit value")
            print("4. Add new row")
            print("5. Add new column")
            print("6. Save CSV")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                display_table(data)
            elif choice == "2":
                visualize_table(data)
            elif choice == "3":
                row = int(input("Enter row index to edit: "))
                column = input("Enter column name to edit: ")
                new_value = input("Enter new value: ")
                edit_value(data, row, column, new_value)
            elif choice == "4":
                row_data = input("Enter new row data as comma-separated values: ").split(',')
                add_row(data, row_data)
            elif choice == "5":
                column_name = input("Enter new column name: ")
                default_value = input("Enter default value for the column: ")
                add_column(data, column_name, default_value)
            elif choice == "6":
                save_file_path = input("Enter path to save the CSV file: ")
                save_csv(data, save_file_path)
            elif choice == "7":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")
