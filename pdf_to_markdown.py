
import time
import os
from  llama_parse import LlamaParse
from unstract.llmwhisperer import LLMWhispererClientV2
from backend.constants import DATA_PATH
from dotenv import load_dotenv

load_dotenv()

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLMWhisperer_API_KEY = os.getenv("LLMWhisperer_API_KEY")


def pdf_to_markdown_llamaparse(pdf_path): 
    # Implementation for LlamaParse processing
    document = LlamaParse(result_type="markdown").load_data(pdf_path)
    return document

def pdf_to_markdown_llmwhisper(pdf_path):
    # Implementation for LLM Whisper processing
    client = LLMWhispererClientV2(base_url="https://llmwhisperer-api.us-central.unstract.com/api/v2", api_key = LLMWhisperer_API_KEY)
    result = client.whisper(file_path=pdf_path)
    
    while True:
        status = client.whisper_status(whisper_hash=result["whisper_hash"])
        if status["status"] == "processed":
            resultx = client.whisper_retrieve(
                whisper_hash=result["whisper_hash"]
            )
            break
        time.sleep(5)

    document= resultx['extraction']['result_text']
    return document


def document_to_markdown(document, markdown_path):
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(document)
        
              
# if __name__ == "__main__":
def pdf2markdown():
    for pdf in DATA_PATH.glob("*.pdf"):
        markdown_path = pdf.with_suffix(".md")
        
        if markdown_path.exists():
            print(f"{markdown_path} already exists.")
            continue
        else:
            try:
                print(f"LLM Whisper Processing... ")
                document = pdf_to_markdown_llmwhisper(pdf)
                document_to_markdown(document, markdown_path)
                
            except Exception as e:
                try:
                    print(f"LlamaParse Processing... ")
                    document = pdf_to_markdown_llamaparse(pdf)
                    document_to_markdown(document, markdown_path)
                    
                except Exception as e:
                    print(f"Failed to process {pdf.name} with both methods. Error: {e}")