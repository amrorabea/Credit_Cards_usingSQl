import pandas as pd
import psycopg2
import csv

def testing_connection():
    DB_NAME = "bank"
    DB_USER = "postgres"
    DB_PASS = "Qwer.1245"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
        print("Database connected successfully")
        return conn
    except:
        print("Database not connected successfully")
        return False

def insert_csv_into_table1_database( path="D:\DownLoad\\learining courses\\DEPI-DS-AI\Projects\\SQLproject\Dataset\\application_record_cleaned.csv"):
    if(testing_connection() != False):
       conn = testing_connection()
       cursor = conn.cursor()
    else:
        print("Could not connect to the database:  ")
        return 0
    with open(path,'r') as f:
        reader=csv.reader(f)
        next(reader)

        for row in reader:
            cursor.execute("""  INSERT INTO client_data (ID,CODE_GENDER,FLAG_OWN_CAR,FLAG_OWN_REALTY,CNT_CHILDREN,AMT_INCOME_TOTAL,NAME_INCOME_TYPE,NAME_EDUCATION_TYPE,NAME_FAMILY_STATUS,NAME_HOUSING_TYPE,DAYS_BIRTH,DAYS_EMPLOYED,FLAG_MOBIL,FLAG_WORK_PHONE,FLAG_PHONE,FLAG_EMAIL,OCCUPATION_TYPE,CNT_FAM_MEMBERS)
                           Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],int(float(row[17]))))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data has been inserted into the client_data_table")


def insert_csv_into_table2_database( path="D:\DownLoad\learining courses\DEPI-DS-AI\Projects\SQLproject\Dataset\credit_record_cleaned.csv"):
    if(testing_connection()!=False):
       conn = testing_connection()
       cursor = conn.cursor()
    else:
        print("Could not connect to the database:  ")
        return 0
    with open(path,'r') as f:
        reader=csv.reader(f)
        next(reader)

        for row in reader:
            cursor.execute("""  INSERT INTO Credit_record  (ID,MONTHS_BALANCE,STATUS)
                           Values(%s,%s,%s)""",(row[0],row[1],row[2]))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data has been inserted into the client_data_table")



