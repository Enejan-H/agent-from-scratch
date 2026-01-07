import json

def llm_decide(state):
    """
    LLM'den karar alıyormuş gibi davranan decision engine.
    """

    prompt = f"""
You are an agent controller.

Current state:
- number: {state["number"]}
- step: {state["step"]}
- errors: {state["errors"]}

Rules:
- Allowed actions: increase, decrease, done
- If errors >= 3 → done
- Respond ONLY in JSON

Example:
{{"action": "increase"}}
"""

    # ŞİMDİLİK FAKE LLM RESPONSE
    #fake_llm_response = '{"action": "increase"}'
    fake_llm_response = '{"action": "fly-to-the-moon"}'  # Geçersiz eylem örneği
    #fake_llm_response = '{"action": "decrease"}'

    try:
        decision = json.loads(fake_llm_response)
        action = decision.get("action")

        return action

    except Exception:
        return "invalid"

    

def act(action, state):
        """Action function, this acts like the muscles of the agent.
        It takes the current state and an action, and returns the new state."""
        # Placeholder implementation
        if action == "increase":
            state["number"] += 2
            state["last_action"] = action

        elif action == "decrease":
            state["number"] -= 3
            state["last_action"] = action

        elif action == "done":
            state["last_action"] = action    

        else:
            state["errors"] +=1
            state["last_action"] = "invalid"
        return state
    
def run_agent(initial_number):
        """Runs the agent in a simple environment until it reaches a terminal state."""
        state = {
            "number": initial_number,
            "step": 0,
            "done": False,
            "history": [],
            "last_action": None,
            "errors": 0
            }
        
        MAX_STEPS = 4

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
    initial_number = 15
    final_state = run_agent(initial_number=initial_number)

    print("FINAL STATE:")
    for k, v in final_state.items():
        print(k, ":", v)