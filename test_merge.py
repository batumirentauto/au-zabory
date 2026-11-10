import json
import re

# Load data
with open('colorbond_modular_fencing_australia.json', 'r', encoding='utf-8') as f:
    raw_contractors = json.load(f)

with open('contractors_real_reviews.json', 'r', encoding='utf-8') as f:
    real_data = json.load(f)

print(f"Loaded {len(raw_contractors)} raw contractors and {len(real_data)} real data records.")
