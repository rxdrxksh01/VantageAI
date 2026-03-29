from voice.listener import listen
from voice.speaker import speak
from utils.llm import get_llm
from memory.store import save_memory, recall_memory
from langchain_core.messages import HumanMessage, SystemMessage

print("=== VANTAGE AI ===")

llm = get_llm()

system_prompt = """You are VANTAGE, a smart personal AI assistant for a college student.
You are helpful, friendly, and concise.
Keep responses short and conversational — max 3 sentences.
You help with scheduling, attendance, reminders and general questions.
You will be given relevant past memories to help answer better."""

chat_history = [SystemMessage(content=system_prompt)]

speak("Hello! I am VANTAGE. How can I help you today?")

while True:
    user_input = listen()

    if not user_input:
        speak("Sorry, I didn't catch that. Try again.")
        continue

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        speak("Goodbye! Have a great day!")
        break

    # Recall relevant past memories
    past = recall_memory(user_input)
    if past:
        memory_msg = f"Relevant past conversations:\n{past}"
        chat_history.append(SystemMessage(content=memory_msg))

    chat_history.append(HumanMessage(content=user_input))

    response = llm.invoke(chat_history)
    reply = response.content

    # Save this exchange to memory
    save_memory(user_input, reply)

    chat_history.append(response)
    speak(reply)