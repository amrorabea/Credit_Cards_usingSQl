import pandas as pd





# Create Cleaned Csv FilE 
def create_cleaned_csv():
    df= pd.read_csv("D:\\DownLoad\\learining courses\\DEPI-DS-AI\\Projects\\SQLproject\Dataset\\application_record.csv")
    dataframe=pd.DataFrame(df)
    print(dataframe.info())
    print("\n \n \n")
    print(dataframe.describe())
    print(dataframe['ID'].duplicated().sum()) # Checking for duplicates
    print("\n")
    print(dataframe.isnull().sum()) # Checking for nulls
    dataframe=dataframe.drop_duplicates(subset='ID') # Drop duplicates in primary key
    print(dataframe['ID'].duplicated().sum())
    print(dataframe.isnull().sum())
    dataframe=dataframe.fillna("Unknown") # Fill nulls with Unknown
    print(dataframe.isnull().sum())
    # Add removal of id's that doesn't exist in application table
    df2 = pd.read_csv("D:\DownLoad\learining courses\DEPI-DS-AI\Projects\SQLproject\Dataset\credit_record.csv")
    df2 = df2[df2['ID'].isin(df['ID'])]

    return dataframe, df2


def To_csv(dataframe, dataframe2):
    path="D:\DownLoad\\learining courses\\DEPI-DS-AI\Projects\\SQLproject\Dataset\\application_record_cleaned.csv"
    path2="D:\DownLoad\\learining courses\\DEPI-DS-AI\Projects\\SQLproject\Dataset\\credit_record_cleaned.csv"
    dataframe.to_csv(path, index=False)
    dataframe2.to_csv(path2, index=False)
    print("File has been created\n")

