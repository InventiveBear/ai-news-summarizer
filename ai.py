from groq import Groq

client = Groq(api_key="")

def call_gpt(prompt, system=""):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt}
        ]
    )
    return response.choices[0].message.content