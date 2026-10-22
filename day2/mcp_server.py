import csv, json, os
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("maintenance")
 
with open("maintenance_assets.csv", newline="") as f:
    ASSETS = list(csv.DictReader(f))
 
MEMORY_FILE = "agent_memory.json"
 
def _load_mem():
    return json.load(open(MEMORY_FILE)) if os.path.exists(MEMORY_FILE) else {}
 
@mcp.tool()
def search_assets(status: str = "", criticality: str = "",
                  asset_type: str = "", location: str = "") -> list[dict]:
    """Search the plant asset maintenance records."""
    rows = ASSETS
    for key, val in [("status", status), ("criticality", criticality),
                     ("asset_type", asset_type), ("location", location)]:
        if val:
            rows = [r for r in rows if val.lower() in r[key].lower()]
    return rows[:20]
 
@mcp.tool()
def remember(key: str, note: str) -> str:
    """Store a note in the agent's long-term memory."""
    mem = _load_mem(); mem[key] = note
    json.dump(mem, open(MEMORY_FILE, "w"), indent=2)
    return f"stored under '{key}'"
 
@mcp.tool()
def recall(key: str = "") -> dict:
    """Recall notes from long-term memory (all notes if no key)."""
    mem = _load_mem()
    return mem if not key else {key: mem.get(key, "nothing stored")}
 
@mcp.resource("assets://flagged")
def flagged_assets() -> str:
    """All assets currently flagged for inspection."""
    return json.dumps([r for r in ASSETS
                       if r["status"] == "Flagged for Inspection"], indent=2)
 
@mcp.prompt()
def maintenance_briefing(unit: str) -> str:
    """Prompt template: brief an engineer on a unit's assets."""
    return (f"Summarize the maintenance posture of {unit}: flagged items, "
            "high-criticality equipment, overdue inspections. Cite asset_ids.")
 
if __name__ == "__main__":
    mcp.run()                     # stdio transport