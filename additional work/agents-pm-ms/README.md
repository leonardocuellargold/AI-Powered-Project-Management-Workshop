# Agents PM – Microsoft Edition

This folder contains the workshop-ready build that pivots the AI project management experience fully into the Microsoft 365 stack. Run one container, sync the outputs to OneDrive or SharePoint, and let Power Automate, Planner, Outlook, Teams, and Copilot do the rest.

---

## 🧱 Repository Layout

```text
agents-pm-ms/
├─ docker-compose.yml          # One command to run the orchestrator
├─ Dockerfile                  # Container image definition
├─ .env.example                # Example environment variables
├─ README.md                   # You are here
├─ app/
│  ├─ run_supervisor.py        # Orchestrator script
│  ├─ providers/llm.py         # Unified LLM adapter (OpenAI/Anthropic/Gemini)
│  ├─ agents/                  # Prompt templates for each “agent”
│  └─ templates/               # Markdown scaffolds for docs/email
└─ workspace/
   ├─ samples/transcript_short.txt  # Sample transcript
   └─ outputs/                      # Power Automate watches this folder
```

> 💡 Ask attendees to sync `workspace/` with OneDrive/SharePoint before the session. Bind-mounting that synced folder makes every generated artifact instantly flow to Microsoft 365.

---

## 🔧 Prerequisites

- Docker Desktop (Mac/Windows/Linux)
- Microsoft 365 tenant with OneDrive/SharePoint, Planner, Outlook, Teams, and Power Automate (standard connectors)
- Optional model access: OpenAI, Anthropic, or Gemini API key (leave blank for offline demo)

---

## 🚀 Quick Start

1. **Copy the environment template**

  ```bash
  cd agents-pm-ms
  cp .env.example .env
  ```
1. **Set up your workspace sync**
   - Sync `agents-pm-ms/workspace` to a personal or shared OneDrive/SharePoint library.
   - Confirm that new files dropped in `workspace/outputs` appear in OneDrive.
1. **Run the container**

  ```bash
  docker compose up --build
  ```

  - With `DRY_RUN=1` (default) the orchestrator emits realistic sample content without calling external APIs.
  - Add an API key to `.env` and unset `DRY_RUN` to turn on live LLM generation.

When the run finishes, inspect `workspace/outputs/` for:

- `meeting.md`
- `RAID.md`
- `RACI.md`
- `update_email.md`
- `status_deck.md`
- `action_items.json`
- `ops_update.md`

These are the same files that Power Automate will watch and distribute.

---

## 🔁 Power Automate Runbook (Standard Connectors)

### Flow A – Create Planner Tasks from `action_items.json`

1. **Trigger**: *When a file is created* (OneDrive or SharePoint) → Folder: `/workspace/outputs`
2. **Condition**: `Name` equals `action_items.json`
3. **Actions**:
   - Get file content → use `Identifier` from the trigger.
   - Parse JSON → paste schema below.
   - Apply to each → `body` from Parse JSON.
     - Create a task (Planner)
       - Plan Id: your workshop plan
       - Bucket Id: e.g., “Next Up”
       - Title: `items('Apply_to_each')?['title']`
       - Assigned User Ids: map owner → UPN (or leave empty)
       - Due Date: `items('Apply_to_each')?['due_date']`
     - (Optional) Update task details → Notes with tags/dependencies.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "title": {"type": "string"},
      "owner": {"type": "string"},
      "due_date": {"type": ["string", "null"]},
      "tags": {
        "type": "array",
        "items": {"type": "string"}
      },
      "dependency": {"type": ["string", "null"]}
    },
    "required": ["title"]
  }
}
```

### Flow B – Distribute Meeting Summary

1. **Trigger**: *When a file is created* (OneDrive or SharePoint) → Folder: `/workspace/outputs`
2. **Condition**: `Name` equals `meeting.md`
3. **Actions** (choose your path):
   - *Outlook*: Create draft email (V2)
     - Subject: `Project Update – @{utcNow()}`
     - Body: file content, or attach link to OneDrive file
   - *Teams*: Post adaptive card to channel with summary, plus links to `RAID.md`, `RACI.md`, `status_deck.md`

Both flows can use “Open file” dynamic content to include SharePoint/OneDrive links.

### Optional Flow C – HTTP (Premium)

- Trigger: *When an HTTP request is received*
- Body schema: `{ "summary": "...", "actions": [ { "title": "..." } ] }`
- Use Parse JSON + Planner + Outlook steps above.
- Set `FLOW_URL=` in `.env` and let the container POST results directly.

---

## 🤝 Copilot for Microsoft 365 Touchpoints

- **Outlook Copilot** → open `update_email.md` → “Improve tone for an executive audience under 120 words.”
- **Word Copilot** → open `meeting.md` → “Create a one-page exec brief with bullets and an action table.”
- **PowerPoint Copilot** → paste `status_deck.md` → “Generate a 7-slide deck with icons and a RAID visual.”
- **Teams Copilot** → “Summarize this week’s files from the Outputs folder and call out three risks.”

---

## 🛡️ Governance & Workshop Tips

- Use sanitized transcripts in shared environments.
- Keep the PM in the loop; all outputs are drafts.
- SharePoint/OneDrive maintains version history and permissions automatically.
- Demo extension ideas: Power BI view on `action_items.json`, approvals in Power Automate, Loop components for live collaboration.

---

## 🧪 Local Smoke Test

With Python installed locally you can run a quick dry-run without Docker:

```bash
pip install python-dotenv==1.0.1 httpx==0.27.2
python app/run_supervisor.py --transcript workspace/samples/transcript_short.txt --outdir workspace/outputs --dry-run
```

(Use the container for the full experience; this command simply validates the script on your machine.)

---

## 📅 Suggested Workshop Flow (45–60 min)

1. Set the story → “We just wrapped a partner meeting; need docs, tasks, comms.”
2. Run `docker compose up` → show files appearing in `workspace/outputs`.
3. Demonstrate OneDrive sync → files arrive in OneDrive/SharePoint instantly.
4. Trigger Flow A → Planner tasks land; open one and review notes.
5. Trigger Flow B → Outlook draft (or Teams post) with links to artifacts.
6. Copilot polish → upgrade the email and build slides from `status_deck.md`.
7. Open RAID/RACI → highlight governance docs delivered automatically.
8. Q&A → Extend to Power BI, approvals, Loop, or HTTP-trigger variant.

Happy shipping! ✨
