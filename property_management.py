from gpt4all import GPT4All

model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")  # Local file in your directory

PROPERTY_KNOWLEDGE = """
You manage a property with these rules:
- Pool is open 8 AM to 10 PM
- Gym is 24/7
- Rent is due on the 5th
- Pets under 40 lbs allowed
"""

def answer_property_question_local(question: str) -> str:
    with model.chat_session():
        prompt = f"{PROPERTY_KNOWLEDGE}\n\nQuestion: {question}\nAnswer:"
        response = model.generate(prompt, max_tokens=20, temp=0.5)
        return response.strip()