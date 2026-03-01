import json
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# environment.py
def create_state(initial_number, target_number):
    return {
        "number": initial_number,
        "target": target_number,
        "step": 0,
        "done": False,
        "history": [],
        "last_action": None,
        "errors": 0,
        "delta": target_number - initial_number  # hedefe uzaklık
    }

def update_state(state, action, value=2):
    """
    Action'ı uygula ve state'i güncelle.
    value parametresi ile adım boyutunu kontrol edebiliriz.
    """
    if action == "increase":
        state["number"] += value
    elif action == "decrease":
        state["number"] -= value
    elif action == "done":
        state["done"] = True
    else:
        state["errors"] += 1
        state["last_action"] = "invalid"
        return state
    
    state["delta"] = state["target"] - state["number"]
    state["last_action"] = action
    state["history"].append({
        "step": state["step"],
        "action": action,
        "number": state["number"],
        "delta": state["delta"]
    })
    state["step"] += 1
    return state


def compute_reward(state):
    """
    Reward: hedefe yakınlık.
    Küçük delta -> yüksek reward
    """
    if state["done"]:
        return 100  # işi bitirdiğinde yüksek reward
    return -abs(state["delta"])


import json

def llm_decide(state):
    prompt = f"""
You are a decision agent.

State:
- number: {state['number']}
- target: {state['target']}
- delta: {state['delta']}

Rules:
- Allowed actions: "increase", "decrease", "done"
- You can optionally suggest a "value" between 1 and 10
- Respond ONLY in JSON: {{"action": "increase", "value": 2}}

Examples:
{{"action": "increase", "value": 2}}
{{"action": "decrease", "value": 3}}
{{"action": "done"}}
"""
    # Burada Groq/OpenAI client çağrısı
    response = client.responses.create(
        model="llama-3.3-70b-versatile",
        input=prompt,
        max_output_tokens=60,
        temperature=0.0
    )
    try:
        decision = json.loads(response.output_text)
        action = decision.get("action")
        value = decision.get("value", 2)  # default 2
        return action, value
    except Exception as e:
        print("LLM error:", e)
        return "invalid", 0

def run_agent(initial_number, target_number, max_steps=10):
    state = create_state(initial_number, target_number)
    
    while not state["done"] and state["step"] < max_steps:
        action, value = llm_decide(state)

        # Basit allowed action kontrolü
        if action not in ["increase", "decrease", "done"]:
            state["errors"] += 1
            action = "invalid"
            value = 0
        
        state = update_state(state, action, value)
        reward = compute_reward(state)
        print(f"Step {state['step']}: action={action}, value={value}, number={state['number']}, reward={reward}")
        
        if action == "done":
            break

    return state


if __name__ == "__main__":
    final_state = run_agent(initial_number=100, target_number=15, max_steps=10)
    print("FINAL STATE:", final_state)
