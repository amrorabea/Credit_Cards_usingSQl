-- Drop the Bank database if it exists
DROP DATABASE IF EXISTS Bank;
GO

-- Create the Bank database
CREATE DATABASE Bank;
GO

-- Use the newly created Bank database
USE Bank;
GO

-- Drop tables if they exist
DROP TABLE IF EXISTS Credit_record;
DROP TABLE IF EXISTS client_data;
GO

-- Create the client_data table
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
    FLAG_MOBIL INTEGER,
    FLAG_WORK_PHONE INTEGER,
    FLAG_PHONE INTEGER,
    FLAG_EMAIL INTEGER,
    OCCUPATION_TYPE VARCHAR(50),
    CNT_FAM_MEMBERS FLOAT
);
GO

-- Create the Credit_record table with a foreign key reference to client_data
CREATE TABLE Credit_record (
    ID INT,
    MONTHS_BALANCE INT,
    STATUS VARCHAR(10),
    PRIMARY KEY (ID, MONTHS_BALANCE),
    FOREIGN KEY (ID) REFERENCES client_data(ID)
);
GO

-- Create views, each in its own batch

-- View: Average Income by Gender
CREATE VIEW avg_income_by_gender AS
SELECT CODE_GENDER, AVG(AMT_INCOME_TOTAL) AS avg_income
FROM client_data
GROUP BY CODE_GENDER;
GO

-- View: Employment Duration
CREATE VIEW Employment_Duration AS
SELECT AVG(DAYS_EMPLOYED) AS avg_days_employed
FROM client_data;
GO

-- View: Credit Status Distribution
CREATE VIEW Credit_Status_Distribution AS
SELECT STATUS, COUNT(*) AS count_status
FROM Credit_record
GROUP BY STATUS;
GO

-- View: Family Size Distribution
CREATE VIEW Family_Size_Distribution AS
SELECT CNT_FAM_MEMBERS, COUNT(*) AS count_family_size
FROM client_data
GROUP BY CNT_FAM_MEMBERS;
GO

-- View: Mobile Phone Ownership
CREATE VIEW Mobile_Phone_Ownership AS
SELECT (SUM(FLAG_MOBIL) * 100.0 / COUNT(*)) AS Mobile_Phone_Ownership_Percentage
FROM client_data;
GO

-- View: Credit Status by Employment Duration
CREATE VIEW Credit_Status_by_Employment_Duration AS
SELECT 
    cd.DAYS_EMPLOYED,
    cr.STATUS,
    COUNT(*) AS Count
FROM client_data cd
JOIN Credit_record cr ON cd.ID = cr.ID
GROUP BY cd.DAYS_EMPLOYED, cr.STATUS;
GO

-- Remove the incomplete CREATE VIEW statement at the end
-- (Assuming it was an accidental duplicate)