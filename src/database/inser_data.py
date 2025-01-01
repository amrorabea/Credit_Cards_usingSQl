import pandas as pd
import os
from dotenv import load_dotenv
import psycopg2
import csv

load_dotenv()

def testing_connection():
    try:
        conn = psycopg2.connect(database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"))
        print("Database connected successfully")
        return conn
    except:
        print("Error while connecting to database")
        return False

def insert_csv_into_table1_database(path=os.getenv("APP_RECORD_CLEANED")):
    conn = testing_connection()
    if conn:
        cursor = conn.cursor()
    else:
        print("Could not connect to the database")
        return 0
    with open(path,'r') as f:
        reader=csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute("""
                INSERT INTO client_data (ID,CODE_GENDER,FLAG_OWN_CAR,FLAG_OWN_REALTY,CNT_CHILDREN,AMT_INCOME_TOTAL,NAME_INCOME_TYPE,NAME_EDUCATION_TYPE,NAME_FAMILY_STATUS,NAME_HOUSING_TYPE,DAYS_BIRTH,DAYS_EMPLOYED,FLAG_MOBIL,FLAG_WORK_PHONE,FLAG_PHONE,FLAG_EMAIL,OCCUPATION_TYPE,CNT_FAM_MEMBERS)
                Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],int(float(row[17]))))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data has been inserted into the client_data table")


def insert_csv_into_table2_database(path=os.getenv("CREDIT_RECORD_CLEANED")):
    conn = testing_connection()
    if conn:
        cursor = conn.cursor()
    else:
        print("Could not connect to the database")
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
    print("Data has been inserted into the Credit_record table")
