import os
import json
import pandas as pd
import re

def extract_title(text):
    return " ".join(re.sub(r".*\\(?:PF|PD)\d+_(.+)_results", r"\1", text).split("_"))

def extract_data_from_json(json_file, title):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        metadata = data['metadata']
        text_contexts = data['contexts']
        rows = []
        for context in text_contexts:
            row = {
                'newspaper_id': metadata['id'],
                'text_id': f"{metadata['file']}-{metadata['page']}-{context['id']}",
                'title': title,
                'year': metadata['year'],
                'city': metadata['city'],
                'text': context['text'].strip()
            }
            rows.append(row)
        return rows

def process_folder(folder_path):
    all_data = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                rows = extract_data_from_json(json_file, extract_title(root))
                all_data.extend(rows)
    return pd.DataFrame(all_data).astype({'year': 'str'})

folder_path = './data/raw'
df_latamnp = process_folder(folder_path)
df_latamnp.to_parquet('./data/original-latam-xix.parquet')
df_latamnp.to_csv('./data/original-latam-xix.tsv', sep='\t', index=False)