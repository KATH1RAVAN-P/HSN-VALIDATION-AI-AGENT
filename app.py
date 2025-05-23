#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install pandas flask openpyxl


# In[1]:


from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)


# In[3]:


# Load HSN Master Data
df = pd.read_excel("HSN_SAC.xlsx")
df = df.rename(columns = {"\nHSNCode":"HSNCode"})
df['HSNCode'] = df['HSNCode'].astype(str).str.strip()
df['Description'] = df['Description'].astype(str).str.strip()


# In[5]:


# HSN Validation Function
def validate_hsn_code(hsn_code):
    hsn_code = str(hsn_code).strip()
    if not hsn_code.isdigit():
        return {"status": "Invalid", "reason": "HSN must be numeric"}
    if not (2 <= len(hsn_code) <= 8):
        return {"status": "Invalid", "reason": "HSN must be 2 to 8 digits"}
    match = df[df['HSNCode'] == hsn_code]
    if not match.empty:
        return {"status": "Valid", "description": match.iloc[0]['Description']}
    else:
        return {"status": "Invalid", "reason": "Not found in master data"}


# In[7]:


# Webhook Endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    hsn_code = req['queryResult']['parameters'].get('hsn_code')
    result = validate_hsn_code(hsn_code)

    reply = f"✅ HSN Code {hsn_code} is valid.\nDescription: {result['description']}" \
        if result['status'] == 'Valid' \
        else f"❌ Invalid HSN Code: {hsn_code}\nReason: {result['reason']}"

    return jsonify({"fulfillmentText": reply})


# In[ ]:


if __name__ == '__main__':
    # Run locally on a fixed port (no ngrok)
    app.run(host='127.0.0.1', port=8000)


# In[ ]:





# In[ ]:





# In[ ]:




