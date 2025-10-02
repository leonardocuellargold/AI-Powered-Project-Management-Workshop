# DDWV AI Project Manager Workshop

This repository powers a hands-on workshop where we build **AI agents** and combine them with **research + visualization tools** to turn a meeting transcript into consulting-grade deliverables in under an hour.

- **Part 1 (30–40 min):** Build agents (Copilot + Custom GPT) and learn supporting tools (Consensus, Lucidchart AI, Gamma).
- **Part 2 (20 min):** Challenge run — from the **Banking kickoff transcript** to: Cornell notes, RAID, Action Items → Planner, RACI, email recap, and an executive deck with diagrams.

---

## What You’ll Build

1) **Agent (Copilot)** – *DDWV Meeting Notes Assistant*  
2) **Agent (ChatGPT Custom GPT)** – *PMO Dashboard Analyst*  
3) **Research workflow** – Consensus for quick, citable evidence  
4) **Visual workflow** – Lucidchart AI for diagrams, Gamma for instant slides  
---

## Core Flow

**How To Create Agents →** Create Copilot Agent → build *DDWV Meeting Notes Assistant*  
Then create a **GPT Agent** → *PMO Dashboard Analyst*  
Research → **Consensus**  
Build PowerPoint → **Lucidchart AI**, **Gamma AI**

---

## Agent #1 — DDWV Meeting Notes Assistant (for Copilot)

**Name**: `DDWV Meeting Notes Assistant`  
**Description**: An agent that processes meeting notes/transcripts and offers structured outputs: **Email Meeting Recap, Cornell-style notes, RAID tables, Action Items tables**.  
**Instructions**:
- Use consulting-specific language in all interactions.
- Refer to “partner” (not “client”).
- Provide note-taking guidance using the **Cornell Notes** method (see knowledge below).
- Keep tone professional, concise, actionable.
- Ensure outputs are clear, structured, tailored to consulting teams.
- Use **blue and gold** appearance when integrated with Teams.

**Knowledge**: https://subjectguides.york.ac.uk/note-taking/cornell

**Suggested Prompts**

| Title | Message |
| --- | --- |
| Process Meeting Transcript | I have a meeting transcript. Can you generate a recap? |
| Summarize Notes | Here are my meeting notes. Please summarize them using the Cornell note taking system. |
| List RAID Items | Extract RAID items from these meeting notes. |
| Action Items Table | Create a table of action items with owners from this transcript. |
| Email Recap | Draft an email recap of this meeting, starting with action items. |
| Internal Notes | Format these notes for internal use following the Cornell system. |

**Agent Output Guidance**

| Title | Message | Agent Output Guidance |
| --- | --- | --- |
| Process Meeting Transcript | I have a meeting transcript. Can you generate a recap? | Summarize with **Key Decisions, Risks, Action Items**, consulting tone. |
| Summarize Notes | Here are my meeting notes. Please summarize them using the Cornell note taking system. | Apply **Cornell** (Cues → Notes → Summary). Action-oriented. |
| List RAID Items | Extract RAID items from these meeting notes. | Output a **structured RAID log** (Risks, Assumptions, Issues, Dependencies) in a table. |
| Action Items Table | Create a table of action items with owners from this transcript. | Table with **Action, Owner, Due Date, Status**. |
| Email Recap | Draft an email recap of this meeting, starting with action items. | **Partner-facing** email; open with Actions, then Decisions, Risks, Next Steps (<150 words). |
| Internal Notes | Format these notes for internal use following the Cornell system. | Internal consulting-style Cornell notes; concise & actionable. |

> Copy the full spec from **`/agents/ddwv_meeting_notes_assistant.md`** into your Copilot Agent.

---

## Agent #2 — PMO Dashboard Analyst (Custom GPT)

**Name**: `PMO Dashboard Analyst`  
**Description**: A virtual PMO analyst that transforms raw project updates, RAID logs, and task trackers into **consulting-grade dashboards, summaries, and executive-ready outputs**.

**System Instructions**: copy from **`/agents/pmo_dashboard_analyst.md`** into the GPT Builder *Instructions*.  
**Capabilities**:  
- File uploads ✅ (CSV/Excel/Docs)  
- Code Interpreter ✅ (create tables/charts from uploads)  
- Web browsing ❌ (optional)

**Conversation Starters** (see `/prompts/conversation_starters.md`)
- Project Status Snapshot
- Risk Heatmap
- Action Prioritization
- Executive Update (3-slide)
- Portfolio Roll-Up
- Scenario Analysis (e.g., 2-week vendor slip)

---

## Challenge Scenario (20 min)

**Industry**: Banking (regional/community bank)  
**Goal**: Go from **kickoff transcript** to deliverables for the next meeting.

**Inputs**: `transcripts/banking_kickoff.txt`  
**Deliverables**:
1. Cornell Notes Summary  
2. RAID Log (Markdown table via PMO Analyst)  
3. Action Items JSON → (Optional) Planner tasks via Power Automate  
4. RACI Matrix  
5. Partner-facing Email Recap  
6. Executive deck (Gamma) + RAID/RACI diagram (Lucidchart AI)  
7. (Optional) Research addendum with 2–3 citations from **Consensus**

---

## Tools

- **Consensus** – fast, cited AI research. See `/tools/consensus_quickstart.md`.  
- **Lucidchart AI** – generate RAID/RACI/timeline diagrams. See `/tools/lucidchart_ai_quickstart.md`.  
- **Gamma AI** – create consulting-grade slides from text. See `/tools/gamma_ai_quickstart.md`.  

---

## Workshop Agenda (Presenter Outline)

See `workshop_outline.md` for a slide-by-slide flow:
- What agents are (Copilot vs GPT)
- Build DDWV Meeting Notes Assistant (live)
- Build PMO Dashboard Analyst (live)
- Quick tour: Consensus, Lucidchart AI, Gamma
- Challenge run:
  - Process transcript → Cornell Notes
  - RAID + Action Items + RACI (PMO Analyst)
  - Research 2 facts in Consensus (paste into notes)
  - Diagram in Lucidchart AI; export PNG
  - Build slides in Gamma AI; paste outputs

---

## Quick Start

1. Open **agents/** files; copy specs into Copilot and GPT Builder.
2. Open **transcripts/banking_kickoff.txt**.
3. Run the **challenge flow** in the outline.
4. Use **tools/** quickstarts to add research + diagrams + slides.

---
