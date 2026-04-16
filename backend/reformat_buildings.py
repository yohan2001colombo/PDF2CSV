import pandas as pd 


def reformat_buildings(csv_path):
    data = pd.read_csv(csv_path)
    
    # Reformatting logic (example: renaming columns, changing formats, etc.)
    # 1
    data["External_ID__c"]  = (
    "BLD-" +
        data["Building_Name__c"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", "-", regex=True)
    )
    
    data.to_csv(csv_path, index=False)
    
    

    