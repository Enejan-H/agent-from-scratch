import json
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv() 

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)



def llm_decide(state):
    """
    LLM'den karar alıyormuş gibi davranan decision engine.
    """

    prompt = f"""
You are an agent controller.

Current state:
- number: {state["number"]}
- target: {state["target"]}
- step: {state["step"]}
- errors: {state["errors"]}

Rules:
- Allowed actions: "increase", "decrease", "done"
- Choose the action that moves "number" closer to "target"
- If errors >= 3 → respond with "done"
- Respond ONLY in JSON format like {{"action": "increase"}}
- Do NOT include any explanation or extra text
- Examples of valid responses:
{{"action": "increase"}}
{{"action": "decrease"}}
{{"action": "done"}}
"""

    try:
        # Groq'un chat endpoint'ini çağır
        response = client.responses.create(
                model="llama-3.3-70b-versatile",
                input=prompt,
                max_output_tokens=60,
                temperature=0.0,
                )
        
        text = response.output_text
        decision = json.loads(text)
        action = decision.get("action")

        return action

    except Exception as e:
        # JSON parse hatası, API hatası veya beklenmeyen output
        print("LLM parse/response error:", str(e))
        return "invalid"


def act(action, state):
        """Action function, this acts like the muscles of the agent.
        It takes the current state and an action, and returns the new state."""
        # Placeholder implementation
        if action == "increase":
            state["number"] += 2
            state["last_action"] = action

        elif action == "decrease":
            state["number"] -= 2
            state["last_action"] = action

        elif action == "done":
            state["last_action"] = action    

        else:
            state["errors"] +=1
            state["last_action"] = "invalid"
        return state


def run_agent(initial_number, target_number, max_steps=5):
        """Runs the agent in a simple environment until it reaches a terminal state."""
        state = {
            "number": initial_number,
            "target": target_number,
            "step": 0,
            "done": False,
            "history": [],
            "last_action": None,
            "errors": 0
            }
        
        MAX_STEPS = 5

        while not state["done"] and state["step"] < MAX_STEPS:
        
            ALLOWED_ACTIONS = ["increase", "decrease", "done"]

            decision = llm_decide(state)

            if decision not in ALLOWED_ACTIONS:
                state["errors"] += 1
                decision = "invalid"

            state["history"].append({
                "step": state["step"],
                "decision": decision,
                "number": state["number"]
                })   
            
            if decision == "done":
                state["done"] = True
                break
            
            state = act(decision, state)
            state["step"] += 1
        return state
    

if __name__ == "__main__":
    initial_number = 1
    target_number = 70
    final_state = run_agent(initial_number=initial_number, target_number=target_number, max_steps=5)

    print("FINAL STATE:")
    for k, v in final_state.items():
        print(k, ":", v)