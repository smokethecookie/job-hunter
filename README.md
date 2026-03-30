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

## Tech Stack

- **Python** — core language
- **MCP (Model Context Protocol)** — Claude integration
- **httpx + BeautifulSoup** — web scraping
- **ReportLab** — PDF generation
- **JSON** — application tracking

## Installation

### Prerequisites

- Python 3.11+
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

## Usage

### Full Analysis (recommended)
```
Full analysis: Software Engineer @ Stripe
```

or
```
Full analysis: https://company.com/jobs/12345
```

This runs the complete pipeline and generates a PDF report.

### Individual Tools

| Command | Description |
|---------|-------------|
| `analyze_job(url)` | Parse a job posting URL |
| `research_company(name, url)` | Research a company |
| `analyze_fit(requirements)` | Compare requirements to your CV |
| `find_contacts(company)` | Get contact-finding strategies |
| `draft_outreach(...)` | Draft a personalized message |
| `save_application(...)` | Track an application |
| `list_applications()` | View tracked applications |

## Project Structure
```
job-hunter/
├── CLAUDE.md              # Your CV and preferences (git-ignored)
├── README.md
├── mcp-servers/
│   └── hunter/
│       ├── server.py      # MCP server with all tools
│       ├── config.py      # Configuration
│       ├── requirements.txt
│       └── venv/          # Virtual environment (git-ignored)
├── data/
│   ├── applications.json  # Application tracker (git-ignored)
│   └── reports/           # Generated PDFs (git-ignored)
└── docs/
    └── setup-guide.md
```

## Example Output

The tool generates professional PDF reports containing:
- Company research summary
- Fit analysis (matches, gaps, score)
- Contact suggestions
- Ready-to-send outreach draft

## License

MIT