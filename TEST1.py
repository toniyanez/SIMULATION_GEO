import streamlit as st
import pandas as pd
import os
import importlib.util
import subprocess  # Added for more robust checking
import sys #added to get executable path

# Function to check if a package is installed
def check_package_installed(package_name):
    """
    Checks if a Python package is installed.  Uses a more robust method.

    Args:
        package_name (str): The name of the package to check.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    try:
        # Use subprocess to check if the module can be imported, using the same python executable
        subprocess.run([
            sys.executable, '-c', f'import {package_name}'
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to load and analyze Excel file
def analyze_excel_file(file_path):
    """
    Loads an Excel file, analyzes its content, and returns a summary.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        str: A summary of the Excel file's content, or an error message.
    """
    try:
        # Check if openpyxl is installed for xlsx files
        if file_path.lower().endswith(('.xlsx', '.xlsm', '.xltx', '.xltm')) and not check_package_installed('openpyxl'):
            error_message = "Error: Missing optional dependency 'openpyxl'.  Please ensure it is installed.\n"
            error_message += "You can install it using either of the following commands:\n\n"
            error_message += f"**Using pip (recommended):**\n```bash\n{sys.executable} -m pip install openpyxl\n```\n\n"
            error_message += "**Using conda:**\n```bash\nconda install openpyxl\n```\n"
            error_message += f"\n\n**Important:** Use the exact command above, especially the part with '{sys.executable}', to ensure you install it for the correct Python environment."
            return error_message

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Basic analysis
        num_rows = df.shape[0]
        num_columns = df.shape[1]
        column_names = ", ".join(df.columns)

        # Get descriptive statistics for numerical columns
        numerical_summary = df.describe().to_string()

        # Get value counts for categorical columns (first 20 only)
        categorical_summary = ""
        for col in df.select_dtypes(include=['object', 'category']).columns:
            unique_values = df[col].nunique()
            if unique_values > 50:  # Limit unique values to avoid excessive output
                categorical_summary += f"\n- **{col}:** Too many unique values ({unique_values}), cannot display counts."
            elif unique_values > 0:
                top_values = df[col].value_counts().head(10).to_string() #show top 10
                categorical_summary += f"\n- **{col}**: \n{top_values}\n"
            else:
                categorical_summary += f"\n- **{col}**: No values found.\n"

        # Combine the summaries
        summary = (
            f"**File Summary:**\n"
            f"- Number of rows: {num_rows}\n"
            f"- Number of columns: {num_columns}\n"
            f"- Column names: {column_names}\n\n"
            f"**Numerical Column Summary:**\n{numerical_summary}\n\n"
            f"**Categorical Column Summary:**\n{categorical_summary}"
        )
        return summary
    except Exception as e:
        return f"Error analyzing file: {e}"

# Streamlit app
def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Excel File Analyzer")

    # File uploader
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        temp_file_path = "temp_excel_file.xlsx"  # Use a fixed name
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Analyze the Excel file
        summary = analyze_excel_file(temp_file_path)

        # Display the summary
        st.subheader("Analysis Summary")
        st.text_area("Summary", value=summary, height=400)

        # Clean up the temporary file
        try:
            os.remove(temp_file_path)
        except Exception as e:
            st.warning(f"Error deleting temporary file: {e}") #Warn, but continue

if __name__ == "__main__":
    main()

