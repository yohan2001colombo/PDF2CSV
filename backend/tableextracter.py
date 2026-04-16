import os
import re
import time
import random
from typing import Type, Optional

import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel

from backend.constants import DATA_PATH
from backend.data_models import ItemDocument
from backend.data_models import BuildingDocument

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini once
genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel("gemini-2.5-flash")


# -------------------------------
# Extraction Functions
# -------------------------------
def extract_items_from_markdown(markdown_path: str) -> str:
    with open(markdown_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    prompt = f"""Extract structured items from the markdown below.
    Return ONLY valid JSON matching this schema:

    {ItemDocument.model_json_schema()}

    Markdown:
    {md_text}
    """

    result = MODEL.generate_content(prompt)
    raw = result.text

    if raw is None:
        raise RuntimeError("Failed to extract items after retries")
    print(raw)
    return raw


def extract_buildings_from_markdown(markdown_path: str) -> str:
    with open(markdown_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    prompt = f"""Extract structured buildings from the markdown below.
    Return ONLY valid JSON matching this schema:

    {BuildingDocument.model_json_schema()}

    Markdown:
    {md_text}
    """

    result = MODEL.generate_content(prompt)
    raw = result.text

    if raw is None:
        raise RuntimeError("Failed to extract items after retries")
    print(raw)
    return raw


# -------------------------------
# Clean JSON from LLM Output
# -------------------------------
def extract_json(text: str) -> str:
    text = text.strip()

    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    return text


# -------------------------------
# Convert JSON → CSV 
# -------------------------------
def safe_convert_json_to_csv(clean_json: str, model_schema: Type[BaseModel]) -> Optional[str]:
    try:
        data = model_schema.model_validate_json(clean_json)

        if hasattr(data, "Item"):
            rows = [x.model_dump() for x in data.Item]
        elif hasattr(data, "Building"):
            rows = [x.model_dump() for x in data.Building]
        else:
            raise ValueError("Unknown schema")

        df = pd.DataFrame(rows)
        return df.to_csv(index=False)

    except Exception as e:
        print("ERROR:", e)
        return None


# if __name__ == "__main__":
def extract_and_convert_csv():
    for md_file in DATA_PATH.glob("*.md"):
        print(f"\nProcessing {md_file}...")

        try:
            # Extract
            raw_item_json = extract_items_from_markdown(md_file)
            time.sleep(60)  # Delay to respect rate limits
            raw_build_json = extract_buildings_from_markdown(md_file)
           

            # Clean
            clean_item_json = extract_json(raw_item_json)
            clean_build_json = extract_json(raw_build_json)

            # Convert
            csv_item_data = safe_convert_json_to_csv(clean_item_json, ItemDocument)
            csv_build_data = safe_convert_json_to_csv(clean_build_json, BuildingDocument)

            # Save
            if csv_item_data:
                item_path = md_file.with_name(md_file.stem + "_items.csv")
                with open(item_path, "w", encoding="utf-8") as f:
                    f.write(csv_item_data)
                print(f"Saved items → {item_path}")

            if csv_build_data:
                build_path = md_file.with_name(md_file.stem + "_buildings.csv")
                with open(build_path, "w", encoding="utf-8") as f:
                    f.write(csv_build_data)
                print(f"Saved buildings → {build_path}")

            # Small delay to avoid rate limits
            time.sleep(1.5)

        except Exception as e:
            print(f"[FAILED] {md_file}: {e}")