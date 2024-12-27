import editCSV
import inser_data
import time


print("==============CLEANING STAGE==============")
dataframe, dataframe2=editCSV.create_cleaned_csv()
editCSV.To_csv(dataframe, dataframe2)
time.sleep(5)

print("==============Insert values into first table (Client)==============")
inser_data.insert_csv_into_table1_database()
print("==============Insert values into second table (Credit)==============")
inser_data.insert_csv_into_table2_database()
