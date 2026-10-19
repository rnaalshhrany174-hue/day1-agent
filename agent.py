import csv, json, os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)
MODEL = "openai/gpt-4o-mini"

with open("maintenance_assets.csv", newline="") as f:
    ASSETS = list(csv.DictReader(f))

def search_assets(status=None, criticality=None, asset_type=None, location=None):
    rows = ASSETS
    for key, val in [("status", status), ("criticality", criticality),
                    ("asset_type", asset_type), ("location", location)]:
        if val:
            rows = [r for r in rows if val.lower() in r[key].lower()]
    return rows[:20]

TOOLS = [{
    "type": "function",
    "function": {
        "name": "search_assets",
        "description": "Search the plant asset maintenance records.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "criticality": {"type": "string"},
                "asset_type": {"type": "string"},
                "location": {"type": "string"}
            }
        }
    }
}]

def run_agent(user_query):
    messages = [{"role": "user", "content": user_query}]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS
    )
    msg = response.choices[0].message
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        results = search_assets(**args)
        messages.append(msg)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(results)
        })
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return final_response.choices[0].message.content
    return msg.content

while True:
    query = input("Ask about plant assets (or exit): ")
    if query.lower() == "exit":
        break
    if query.strip():
        print(run_agent(query))