import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Second Semester External Practicals Section K to X", layout="centered"
)


@st.cache  # Cache student data for faster retrieval
def load_data(filepath):
    try:
        return pd.read_csv(filepath)  # Handle errors internally
    except FileNotFoundError:
        st.error(f"Error: Student data file '{filepath}' not found.")
        return None


@st.cache  # Cache batchmate results for efficiency
def find_batchmates(student_data, erp_id, batch_column="Batch"):
    if student_data is not None and batch_column in student_data.columns:
        student_batch = student_data[student_data["ERP ID"] == erp_id][batch_column].values[0]
        return student_data.query(f"`{batch_column}` == @student_batch")
    else:
        if student_data is None:
            st.error("Error: Student data could not be loaded.")
        else:
            st.error(f"Column '{batch_column}' not found in student data.")
        return None


def format_date_column(dataframe, date_column="Date"):
    try:
        dataframe[date_column] = pd.to_datetime(dataframe[date_column]).dt.strftime("%d-%m-%Y")
    except:
        st.warning(f"Error: Failed to format '{date_column}' column. Check data format.")


def display_timetable(timetable):
    if not timetable.empty:
        st.subheader("Timetable")
        st.dataframe(timetable, width=1000)  # Consider lazy loading if data is large
    else:
        st.write("Timetable data not available.")


def find_timetable_file(batch):
    for filename in os.listdir():  # No need for data_folder here
        if filename.startswith(batch) and filename.endswith(".csv"):
            return filename
    return None


def main():
    student_data_path = "c to x.csv"  # Update with your data file path
    timetable_data_path = None

    st.subheader("Second Semester External Practicals Section K to X")
    erp_id = st.text_input("Enter your ERP ID:")

    if erp_id:
        try:
            erp_id = int(erp_id)
        except ValueError:
            st.error("Invalid ERP ID. Please enter a valid number.")
            return

        student_data = load_data(student_data_path)
        timetable_data = None

        if student_data is not None:
            student_info = student_data[student_data["ERP ID"] == erp_id]
            batchmates = find_batchmates(student_data.copy(), erp_id)

            if not student_info.empty:
                st.subheader("Your Information")
                st.dataframe(student_info)

            if batchmates is not None and not batchmates.empty:
                st.subheader("Batchmates")
                st.dataframe(batchmates)

            if "Batch" in student_info.columns:
                student_batch = student_info["Batch"].values[0]
                timetable_data_path = find_timetable_file(student_batch)
                if timetable_data_path:
                    timetable_data = load_data(timetable_data_path)
                    if timetable_data is not None:
                        format_date_column(timetable_data)
                        display_timetable(timetable_data)
                    else:
                        st.write(
                            f"Error: Failed to read timetable data from '{timetable_data_path}'.")
                else:
                    st.write(f"Timetable data not found for batch '{student_batch}'.")


if __name__ == "__main__":
    main()
