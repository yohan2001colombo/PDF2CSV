import pandas as pd 


def reformat_items(csv_path):
    data = pd.read_csv(csv_path)
    
    # Reformatting logic (example: renaming columns, changing formats, etc.)
    # 1
    data["Item_ID__c"] = (
    "BLD-" +
    data["Building_Code__c"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", "-", regex=True) +
    "-ITEM-" +
    data["Item_ID__c"].astype(str).str.zfill(2)
    
    )
    data.to_csv(csv_path, index=False)
