from agents.data_agent import data_agent

state = {
    "user_query": "Show inventory"
}

result = data_agent(state)

print(result)