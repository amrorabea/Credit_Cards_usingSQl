import editCSV
import inser_data
import time

# Clean data and save it
dataframe, dataframe2=editCSV.create_cleaned_csv()
editCSV.To_csv(dataframe, dataframe2)
time.sleep(5)
inser_data.insert_csv_into_table1_database()
inser_data.insert_csv_into_table2_database()
