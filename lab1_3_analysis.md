# 📄 Lab 1.3: Agent Structure Analysis Document

### 1. Overview
This document presents an engineering analysis of the baseline maintenance assistant agent developed in **Lab 1.1** (Option B). The agent is designed to interface with maintenance equipment records (`maintenance_assets.csv`) via natural language queries, translating user requests into structured tool calls (`search_assets`) and returning relevant asset information with source citations.

---

### 2. Mapping Code to Core Agent Elements
The four fundamental elements of the agent architecture are mapped directly to `agent.py` as follows:

| Agent Element | Location in `agent.py` | Role & Concept |
| :--- | :--- | :--- |
| **Prompt** | `SYSTEM` string variable | Defines system boundaries, persona, citation rules, and fallback instructions. |
| **Agent Loop** | `for _ in range(5)` inside `run_agent()` | Implements the autonomous **Plan $\rightarrow$ Act $\rightarrow$ Observe** cycle up to a maximum step count. |
| **Tool Interface** | `TOOLS` schema + `search_assets()` function | Formats and executes function calling capabilities over local CSV data. |
| **Memory** | `messages` list | Serves as short-term conversational context and message/tool call tracking. |

---

### 3. Functional Requirements
* **FR-1:** The agent shall parse user questions regarding plant equipment and extract structured search parameters (status, criticality, asset type, location).
* **FR-2:** The agent shall invoke the `search_assets` tool with appropriate parameters when information retrieval from the database is required.
* **FR-3:** The agent shall cite specific `asset_id`s in every response containing equipment details.
* **FR-4:** The agent shall state clearly when requested records or equipment information cannot be found in the dataset.
* **FR-5:** The agent shall maintain conversational context and tool responses within a short-term memory buffer (`messages` list).
* **FR-6:** The agent shall limit autonomous loop execution to a maximum of 5 iterations to prevent infinite loops.

---

### 4. Component Diagram (PlantUML)

```plantuml
@startuml
skinparam componentStyle uml2

actor User
package "Baseline Agent Architecture" {
    component "User Interface (CLI)" as UI
    component "Agent Loop\n(run_agent)" as Loop
    component "System Prompt" as Prompt
    component "LLM Client\n(OpenAI / OpenRouter)" as Model
    component "Tool Interface\n(search_assets)" as Tools
    database "Memory\n(messages list)" as Mem
    database "Asset CSV File\n(maintenance_assets.csv)" as DB
}

User --> UI : 1. Submit Query
UI --> Loop : 2. Initialize Task
Loop --> Prompt : 3. Load System Rules
Loop --> Mem : 4. Append Context
Loop --> Model : 5. Send Prompt + Tools + History
Model --> Loop : 6. Return Thought / Tool Call
Loop --> Tools : 7. Execute Tool Call
Tools --> DB : 8. Query Asset Records
DB --> Tools : 9. Return Matching Rows
Tools --> Loop : 10. Observation Feedback
Loop --> Mem : 11. Append Tool Result
Loop --> UI : 12. Deliver Final Answer
@enduml