def decide(state):
    print("DECIDE STATE TYPE:", type(state), state)
    number = state["number"]
    
    if state["errors"] > 2:
        return "done"
    if number >= 10:
        return "decrease"
    elif number <=2:
        return "increase"
    else:
        return "done"



def act(action, state):
    if action == "increase":
        state["number"] += 1
        state["last_action"] = action
        
    elif action == "decrease":
        state["number"] -= 1
        state["last_action"] = action

    elif action == "error":
        state["errors"] +=1
        state["last_action"] = action

    elif action == "done":
        state["last_action"] = action
    return state




def run_agent(initial_number):
    state = {
        "number": initial_number,
        "step": 0,
        "done": False,
        "history": [],
        "last_action": None,
        "errors": 0
    }

    max_steps = 10
    while not state["done"] and state["step"] < max_steps:
        decision = decide(state)
        state = act(decision, state)

        state["history"].append({
            "step": state["step"],
            "decision": decision,
            "number": state["number"]
        })

        if decision == "done":
            state["done"] = True

        state["step"] += 1
    return state
        

if __name__ == "__main__":

    initial_number = 7
    final_state = run_agent(initial_number)
    print("Final State:", final_state)


# yukarida yazilan iki fonksiyonu run_agent fonksiyonunda kullanarak bir agent olusturuyoruz
# yani decide fonksiyonu ile karar veriyor, act fonksiyonu ile bu karari uyguluyor
# burda ana govde run_agent fonksiyonu olacak, ilk iki fonksiyon ise yardimci fonksiyonlar olacak



