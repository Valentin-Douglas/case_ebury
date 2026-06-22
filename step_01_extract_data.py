import json

# ==========================================
# 1. EXTRACT (Data Extraction)
# ==========================================
def extract_data(filepath=None):
    """
    Reads the raw JSON file.
    Includes error handling to skip malformed or corrupted JSON objects (dirty data),
    which is a standard resilience pattern in Data Engineering ETLs.
    """
    extracted_records = []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read().strip()
        
        # Scenario 1: Valid continuous JSON array or single object
        if content.startswith('[') or (content.startswith('{') and content.count('{') == 1):
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Warning: Root JSON is malformed. Switching to block-by-block extraction. Error: {e}")
        
        # Scenario 2: Multiple JSON objects with potential dirty data
        decoder = json.JSONDecoder()
        index = 0
        
        while index < len(content):
            # Skip whitespaces and potential stray commas between objects
            while index < len(content) and (content[index].isspace() or content[index] == ','):
                index += 1
                
            if index >= len(content):
                break
                
            try:
                # Try to decode one valid JSON object
                obj, end_index = decoder.raw_decode(content[index:])
                extracted_records.append(obj)
                # Move index forward by the exact size of the parsed object
                index += end_index
                
            except json.JSONDecodeError as e:
                print(f"Data Quality Warning: Skipping corrupted JSON block. Reason: {e}")
                
                # Self-healing: Search for the start of the next JSON object
                next_index = content.find('{', index + 1)
                
                if next_index == -1:
                    break # No more objects found, end extraction
                
                # Advance the index to the next object and try again
                index = next_index
            
    return extracted_records
