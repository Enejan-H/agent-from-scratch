def decide(state):
    """Decision function, this acts like a brain of the agent.  
    It takes the current state of the environment and returns an action."""
    # Placeholder implementation
    number = state["number"]
    if number > 10:
        return "decrease"
    elif number < 5:
        return "increase"
    else:
        return "done"
    

def act(action, state):
        """Action function, this acts like the muscles of the agent.
        It takes the current state and an action, and returns the new state."""
        # Placeholder implementation
        if action == "increase":
            state["number"] += 2
        elif action == "decrease":
            state["number"] -= 3
        return state
    
def run_agent(initial_number):
        """Runs the agent in a simple environment until it reaches a terminal state."""
        state = {
            "number": initial_number,
            "steps": 0,
            "done": False,
            "history": []
            }
        
        MAX_STEPS = 20

        while not state["done"] and state["steps"] < MAX_STEPS:
            decision = decide(state)

            state["history"].append({
                "steps": state["steps"],
                "decision": decision,
                "number": state["number"]
                })   
            
            if decision == "done":
                state["done"] = True
                break
            state = act(decision, state)
            state["steps"] += 1
        return state
    

if __name__ == "__main__":
    initial_number = 1
    final_state = run_agent(initial_number=initial_number)

    print("FINAL STATE:")
    for k, v in final_state.items():
        print(k, ":", v)