from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load HSN Master Data
df = pd.read_excel("HSN_SAC.xlsx")
df = df.rename(columns={"\nHSNCode": "HSNCode"})
df['HSNCode'] = df['HSNCode'].astype(str).str.strip()
df['Description'] = df['Description'].astype(str).str.strip()

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

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    hsn_param = req['queryResult']['parameters'].get('hsn_code')

    # Normalize to list if single string
    if isinstance(hsn_param, str):
        hsn_codes = [hsn_param]
    elif isinstance(hsn_param, list):
        hsn_codes = hsn_param
    else:
        hsn_codes = []

    replies = []
    for code in hsn_codes:
        result = validate_hsn_code(code)
        if result['status'] == 'Valid':
            reply = f" HSN Code {code} is valid.\nDescription: {result['description']}"
        else:
            reply = f" Invalid HSN Code: {code}\nReason: {result['reason']}"
        replies.append(reply)

    final_reply = "\n\n".join(replies)
    return jsonify({"fulfillmentText": final_reply})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
