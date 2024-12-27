CREATE DATABASE Bank;
Drop DATABASE IF EXISTS Bank;
-- Column Descriptions

-- ID: A unique identifier for each individual.
-- CODE_GENDER: The gender of the individual (M for Male, F for Female).
-- FLAG_OWN_CAR: Indicates whether the individual owns a car (Y for Yes, N for No).
-- FLAG_OWN_REALTY: Indicates whether the individual owns real estate (Y for Yes, N for No).
-- CNT_CHILDREN: The number of children the individual has.
-- AMT_INCOME_TOTAL: The individual's total annual income.
-- NAME_INCOME_TYPE: The source of the individual's income (e.g., Working, Pensioner, etc.).
-- NAME_EDUCATION_TYPE: The highest level of education the individual has achieved.
-- NAME_FAMILY_STATUS: The individual's marital status.
-- NAME_HOUSING_TYPE: The type of housing the individual lives in.
-- DAYS_BIRTH: The number of days since the individual's birth (negative value indicates the individual is alive).
-- DAYS_EMPLOYED: The number of days since the individual started their current employment (negative value indicates the individual is currently employed).
-- FLAG_MOBIL: Indicates whether the individual has a mobile phone (1 for Yes, 0 for No).
-- FLAG_WORK_PHONE: Indicates whether the individual has a work phone (1 for Yes, 0 for No).
-- FLAG_PHONE: Indicates whether the individual has a home phone (1 for Yes, 0 for No).
-- FLAG_EMAIL: Indicates whether the individual has an email address (1 for Yes, 0 for No).
-- OCCUPATION_TYPE: The individual's occupation.
-- CNT_FAM_MEMBERS: The total number of members in the individual's family.

DROP TABLE IF EXISTS client_data;
DROP TABLE IF EXISTS Credit_record;

CREATE TABLE client_data (
    ID INTEGER PRIMARY KEY,
    CODE_GENDER CHAR(1),
    FLAG_OWN_CAR CHAR(1),
    FLAG_OWN_REALTY CHAR(1),
    CNT_CHILDREN INTEGER,
    AMT_INCOME_TOTAL DECIMAL(15, 2),
    NAME_INCOME_TYPE VARCHAR(50),
    NAME_EDUCATION_TYPE VARCHAR(50),
    NAME_FAMILY_STATUS VARCHAR(50),
    NAME_HOUSING_TYPE VARCHAR(50),
    DAYS_BIRTH INTEGER,
    DAYS_EMPLOYED INTEGER,
    FLAG_MOBIL  INTEGER,
    FLAG_WORK_PHONE INTEGER,
    FLAG_PHONE INTEGER,
    FLAG_EMAIL INTEGER,
    OCCUPATION_TYPE VARCHAR(50),
    CNT_FAM_MEMBERS FLOAT
);


CREATE TABLE Credit_record(
ID INT,
MONTHS_BALANCE INT,
STATUS VARCHAR(10),
PRIMARY KEY (ID, MONTHS_BALANCE),
FOREIGN KEY (ID) REFERENCES client_data(ID)
)
