import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import re

# Load the Hugging Face model and tokenizer
model_name = "microsoft/DialoGPT-medium"
chatbot = pipeline("text-generation", model=model_name)

# Initialize conversation history
conversation_history = []

# Function to generate chatbot response
def chatbot_response(prompt):
    global conversation_history

    #write your code below
    if prompt == "hello":
      conversation_history.append(f"User: {prompt}")
      conversation_history.append(f"Bot: Hi there! How can I help you today?")
    elif prompt == "bye":
      conversation_history.append(f"User: {prompt}")
      conversation_history.append(f"Bot: Goodbye! Have a great day!")
    elif "calculate" in prompt:
      extract_and_calculate(prompt)
      conversation_history.append(f"User: {prompt}")
      conversation_history.append(f"Bot: The result is {extract_and_calculate(prompt)}")
    else:
      outputs = chatbot([{"role": "user", "content": prompt}], max_new_tokens=2)
      response = outputs[0]['generated_text'][1]['content']
      conversation_history.append(f"User: {prompt}")
      conversation_history.append(f"Bot: {response}")
      
    history = "\n".join(conversation_history[-6:])  # Show last 3 interactions
    
    return history

def extract_and_calculate(text):
    match = re.search(r'calculate (\d+)\s*([\+\-\*/])\s*(\d+)', text)
    
    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = num1 / num2 if num2 != 0 else "Error: Division by zero"
        
        return result
    else:
        return "Invalid operator and/or calculation format. Please use 'calculate <num1> <operator> <num2>"

# Create a Gradio interface below
demo = gr.Interface(
    fn=chatbot_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your message here..."),
    outputs=gr.Textbox()
)

demo.launch()