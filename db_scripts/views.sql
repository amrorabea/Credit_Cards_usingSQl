GO
CREATE VIEW avg_income_by_gender AS
SELECT CODE_GENDER, AVG(AMT_INCOME_TOTAL) AS avg_income
FROM  client_data
GROUP BY CODE_GENDER;

GO
CREATE VIEW  Employment_Duration AS
SELECT  AVG(DAYS_EMPLOYED)
FROM client_data

GO
CREATE VIEW Credit_Status_Distribution AS
SELECT status,Count(*)
FROM  Credit_record
GROUP BY status;
GO
CREATE VIEW Family_Size_Distribution AS
SELECT CNT_FAM_MEMBERS, COUNT(*)
FROM client_data
GROUP BY CNT_FAM_MEMBERS;
GO

CREATE VIEW  Mobile_Phone_Ownership AS
SELECT  (Sum(FLAG_MOBIL)/count(*))*100  AS Mobile_Phone_Ownership
FROM client_data;

GO
CREATE VIEW Credit_Status_by_Employment_Duration AS
SELECT 
    client_data.DAYS_EMPLOYED,
    Credit_record.STATUS,
    COUNT(*) AS Count
FROM client_data  JOIN Credit_record  ON client_data.ID = Credit_record.ID
GROUP BY client_data.DAYS_EMPLOYED, Credit_record.STATUS;















