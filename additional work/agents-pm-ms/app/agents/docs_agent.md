# Docs Agent Prompt

Using the meeting summary and ACTION_ITEMS JSON, produce the following Markdown files:

- RAID.md with concise rows for Risks, Assumptions, Issues, Dependencies (include owners/mitigations where possible)
- RACI.md with a Markdown table showing Responsible, Accountable, Consulted, Informed
- update_email.md written for an executive audience, 120 words max, action-oriented tone

Inputs:
{{ inputs }}
