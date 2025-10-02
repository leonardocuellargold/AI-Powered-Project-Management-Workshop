# **AI for Project Management – Workshop**

This repository contains everything you need to follow along in the **AI for Project Management Workshop**.

We’ll simulate *a day in the life of a project manager*, using AI agents and Microsoft tools to turn a meeting transcript into:

- Consulting-grade documentation (Meeting Notes, RAID, RACI, Email Draft)
- A Status Deck (slide outline with visuals)
- Structured Action Items (JSON → Planner tasks)
- Automated Stakeholder Updates (via Outlook / Teams with Power Automate)

---

## **🔧 1. Pre-Workshop Setup**

We’ve kept this as light as possible. Please complete the following before the session:

### **Required**

- **Docker Desktop** (Mac/Windows/Linux) → [Download here](https://www.docker.com/products/docker-desktop/)
- **Git** (to clone this repo) → [Download here](https://git-scm.com/downloads)
- **OneDrive or SharePoint Sync Client** (already included with Microsoft 365)

### **Optional (for live runs)**

- An **OpenAI, Anthropic, or Gemini API key**
    - OpenAI: [Get API Key](https://platform.openai.com/)
    - Gemini: [Get API Key](https://aistudio.google.com/)
- Microsoft 365 account with:
    - **Planner** (for tasks)
    - **Outlook + Teams** (for email/posts)
    - **Power Automate** (standard triggers, no premium required)
    - **Copilot for M365** (if licensed, for bonus polish)

---

## **📂 2. Repository Layout**

```
agents-pm-ms/
├─ docker-compose.yml         # One command to run the orchestrator
├─ Dockerfile                 # Container image definition
├─ .env.example               # Example environment variables
├─ README.md                  # This guide
├─ app/
│  ├─ run_supervisor.py       # Orchestrator script
│  ├─ providers/llm.py        # Unified LLM adapter (OpenAI/Claude/Gemini)
│  ├─ agents/                 # Prompt templates for each “agent”
│  └─ templates/              # RAID, RACI, Email scaffolds
└─ workspace/                 # Mounted folder synced to OneDrive/SharePoint
   ├─ samples/transcript_short.txt   # Example meeting transcript
   └─ outputs/                        # Generated files will appear here
```

---

## **⚙️ 3. Setup Instructions**

1. **Clone this repo**

```
git clone https://github.com/your-org/agents-pm-ms.git
cd agents-pm-ms
```

1. 
2. **Copy environment template**

```
cp .env.example .env
```

1. 
    - Leave all keys empty to run in **Demo Mode**
    - Add your OpenAI/Anthropic/Gemini API key for **Live Mode**
2. **Ensure OneDrive/SharePoint sync is running**
    - Sync the workspace/ folder with your OneDrive or SharePoint
    - This allows **Power Automate flows** to watch the outputs/ folder
3. **Build & run**

```
docker compose up
```

1. 
    - In **Demo Mode**, you’ll see stubbed outputs
    - In **Live Mode**, AI will generate full consulting-grade outputs

---

## **🧠 4. What Happens When You Run It**

The orchestrator (run_supervisor.py) runs four “agents” in sequence:

1. **Notes Agent**
    - Input: samples/transcript_short.txt
    - Output: meeting.md, action_items.json
2. **Docs Agent**
    - Uses notes + action items to create:
        - RAID.md
        - RACI.md
        - update_email.md
3. **Deck Agent**
    - Produces status_deck.md (slide outline + diagram + speaker notes)
4. **Ops Agent**
    - Optional → preps a Teams/Outlook status update
    - (With Power Automate, this triggers downstream automations)

All results are written to workspace/outputs/.

---

## **🔁 5. Microsoft Integrations**

We’ll use **Power Automate flows** to extend the outputs:

- **Flow A – Create Planner Tasks**
    - Trigger: New action_items.json in OneDrive/SharePoint
    - Action: Parse JSON → Create tasks in Planner
- **Flow B – Distribute Meeting Summary**
    - Trigger: New meeting.md in OneDrive/SharePoint
    - Action: Create draft Outlook email or Teams channel post with summary + links

> These flows will be shown during the workshop; you’ll get a resource email with step-by-step screenshots tonight.
> 

---

## **✨ 6. Copilot for Microsoft 365 (Optional)**

If you have **Copilot access**, we’ll show how to:

- Rewrite update_email.md into a polished client-ready Outlook draft
- Turn status_deck.md into a full PowerPoint deck with visuals
- Summarize meeting.md into a one-page Word exec brief
- Post updates directly in Teams with auto-summaries

---

## **📅 7. Workshop Flow**

1. **Introduction** – Why AI in project management
2. **Run Orchestrator** – Transcript → consulting artifacts
3. **Outputs** – Open Meeting Notes, RAID, RACI, Email, Deck
4. **Power Automate** – Watch files → auto-create tasks and emails
5. **Copilot Demo** – Enhance outputs for exec audiences
6. **Wrap-Up Discussion** – Risks, guardrails, next steps

---

## **✅ 8. After the Workshop**

- All generated files will remain in your workspace/outputs/ folder
- Sample Power Automate flow definitions will be shared in the follow-up email
- Suggested extensions:
    - Add Power BI to visualize action items over time
    - Build Loop components for real-time collaboration
    - Chain multiple transcripts into a “project memory”

---

## **🛡️ 9. Notes on Safety & Governance**

- Only use **sanitized transcripts** in workshops (no client PII)
- All outputs are drafts → PM remains **human in the loop**
- Files live in **OneDrive/SharePoint** with normal Microsoft security and version history

---

📌 **Next Step:** Please make sure you’ve installed Docker and synced your OneDrive/SharePoint workspace. I’ll send a follow-up tonight with resources, transcript, and Power Automate setup steps.