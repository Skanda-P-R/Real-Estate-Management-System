import requests

api_url = "https://api.groq.com/openai/v1/chat/completions"

def send_to_groq(user_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer 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"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI that answers questions related to Property and Sales."},
            {"role": "user", "content": "Question : " + user_prompt}
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        
        content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return content
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

