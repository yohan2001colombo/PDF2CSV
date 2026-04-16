#%%
import json
from datetime import date
from pydantic import create_model, BaseModel, Field
from typing import Optional, List, Any
from backend.constants import DATA_PATH
#%%


TYPE_MAP = {
    "Text": str,
    "Date": str,
    "Number": float,
    "Boolean": bool,
}
with open(DATA_PATH/"item_schema.json") as f:
    item_schema = json.load(f)
    
def ItemModel(schema: dict):
    fields_dict = {}

    for field in schema["fields"]:
        name = field["api_name"]
        description = field.get("description", "")
        f_type = field["type"]
        required = field.get("required", False)

        if f_type == "Picklist":
            python_type = Optional[str]
            desc = f"{description}. Allowed values: {field.get('picklist_values', [])}"
            fields_dict[name] = (python_type, Field(None, description=desc))

        else:
            python_type = TYPE_MAP.get(f_type, str)

            if required:
                fields_dict[name] = (python_type, Field(..., description=description))
            else:
                fields_dict[name] = (Optional[python_type], Field(None, description=description))
    return create_model(schema["object_name"], **fields_dict)


Item = ItemModel(item_schema)


class ItemDocument(BaseModel):
    Item: List[Item] 
  
with open(DATA_PATH/"building_schema.json") as f:
    building_schema = json.load(f)
      
def BuildingModel(schema: dict):
    fields_dict = {}

    for field in schema["fields"]:
        name = field["api_name"]
        description = field.get("description", "")
        f_type = field["type"]
        required = field.get("required", False)

        if f_type == "Picklist":
            python_type = Optional[str]
            desc = f"{description}. Allowed values: {field.get('picklist_values', [])}"
            fields_dict[name] = (python_type, Field(None, description=desc))

        else:
            python_type = TYPE_MAP.get(f_type, str)

            if required:
                fields_dict[name] = (python_type, Field(..., description=description))
            else:
                fields_dict[name] = (Optional[python_type], Field(None, description=description))

    return create_model(schema["object_name"], **fields_dict)

Building = BuildingModel(building_schema)


class BuildingDocument(BaseModel):
    Building: List[Building] 
# %%
