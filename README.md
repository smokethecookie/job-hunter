# Job Hunter

An MCP-powered job application assistant that automates research, fit analysis, and outreach drafting.

## What it does

Give it a job posting URL or "Role @ Company" and it will:

1. **Research the company** — fetches website, news, culture info
2. **Analyze your fit** — compares job requirements to your CV, identifies matches and gaps
3. **Suggest contacts** — who to reach out to and how to find them
4. **Draft outreach** — personalized email ready to send
5. **Generate PDF report** — professional document with all findings
6. **Track applications** — persistent database of where you've applied
7. **Daily reminders** — notifies you to follow up on stale applications

## Tech Stack

- **Python** — core language
- **MCP (Model Context Protocol)** — Claude integration
- **httpx + BeautifulSoup** — web scraping
- **ReportLab** — PDF generation
- **JSON** — application tracking
- **cron + osascript** — daily reminder automation

## Installation

### Prerequisites

- Python 3.11+
- macOS (for notifications)
- Claude Code (VS Code extension)

### Setup
```bash
# Clone the repo
git clone https://github.com/smokethecookie/job-hunter.git
cd job-hunter

# Create virtual environment
cd mcp-servers/hunter
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Register with Claude Code
npx @anthropic-ai/claude-code mcp add hunter -s user $(pwd)/venv/bin/python $(pwd)/server.py
```

### Configuration

1. Create a `CLAUDE.md` file in the project root with your CV/background
2. Restart VS Code
3. Test with `/mcp` to verify connection

### Automation Setup (optional)

Set up daily reminders for follow-ups:
```bash
crontab -e
```

Add this line (runs at 9am daily):
```
0 9 * * * /path/to/job-hunter/mcp-servers/hunter/venv/bin/python /path/to/job-hunter/automation/reminder.py
```

## Usage

### Full Analysis (recommended)
```
Full analysis: Software Engineer @ Company
```

or
```
Full analysis: https://company.com/jobs/12345
```

This runs the complete pipeline and generates a PDF report.

### Individual Tools

| Command | Description |
|---------|-------------|
| `full_analysis(input)` | Run complete pipeline (URL or "Role @ Company") |
| `analyze_job(url)` | Parse a job posting URL |
| `analyze_role(role, company)` | Search and analyze by role name |
| `research_company(name, url)` | Research a company |
| `analyze_fit(requirements)` | Compare requirements to your CV |
| `find_contacts(company)` | Get contact-finding strategies |
| `draft_outreach(...)` | Draft a personalized message |
| `generate_report(...)` | Create PDF report |
| `save_application(...)` | Track an application |
| `list_applications()` | View tracked applications |

## Project Structure
```
job-hunter/
├── CLAUDE.md                 # Your CV and preferences (git-ignored)
├── README.md
├── mcp-servers/
│   └── hunter/
│       ├── server.py         # MCP server with all tools
│       ├── config.py         # Configuration
│       ├── requirements.txt
│       └── venv/             # Virtual environment (git-ignored)
├── automation/
│   └── reminder.py           # Daily follow-up reminders
├── data/
│   ├── applications.json     # Application tracker (git-ignored)
│   └── reports/              # Generated PDFs (git-ignored)
└── docs/
    └── setup-guide.md
```

## Automation

The `reminder.py` script checks for applications with status "applied" that are older than 7 days. It shows a macOS notification asking for an update:

- **Interviewing** — marks as interviewing
- **Rejected** — marks as rejected
- **Snooze** — skips for now

Set it up with cron to run daily.

## Example Output

The tool generates professional PDF reports containing:
- Company research summary
- Fit analysis (matches, gaps, score out of 10)
- Contact suggestions
- Ready-to-send outreach draft

## License

MIT