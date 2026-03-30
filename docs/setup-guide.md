# Setup Guide

Step-by-step instructions to get Job Hunter running.

## Prerequisites

1. **Python 3.11 or higher**
```bash
   python3 --version
```

2. **macOS** (for native notifications)

3. **VS Code with Claude Code extension**
   - Install VS Code
   - Install Claude Code extension from marketplace
   - Sign in to Claude

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/smokethecookie/job-hunter.git
cd job-hunter
```

### 2. Set up Python environment
```bash
cd mcp-servers/hunter
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your CLAUDE.md

Create a file called `CLAUDE.md` in the project root with your information:
```markdown
# About me

Name: Your Name
Email: your@email.com
LinkedIn: linkedin.com/in/yourprofile

## Education
- Your degree, school, graduation date

## Skills
- Your technical skills

## Experience
- Your work experience

## Projects
- Your projects
```

### 5. Register the MCP server
```bash
cd mcp-servers/hunter
npx @anthropic-ai/claude-code mcp add hunter -s user $(pwd)/venv/bin/python $(pwd)/server.py
```

### 6. Restart VS Code

Close and reopen VS Code completely.

### 7. Verify connection

Open Claude Code and type:
```
/mcp
```

You should see `hunter` in the list of connected servers.

## Automation Setup

### Daily Follow-up Reminders

The `automation/reminder.py` script checks for stale applications and shows a macOS notification.

#### Test it manually
```bash
cd ~/path/to/job-hunter/automation
source ../mcp-servers/hunter/venv/bin/activate
python reminder.py
```

#### Schedule with cron

Run:
```bash
crontab -e
```

Add this line (runs at 9am daily):
```
0 9 * * * /full/path/to/job-hunter/mcp-servers/hunter/venv/bin/python /full/path/to/job-hunter/automation/reminder.py
```

Verify with:
```bash
crontab -l
```

## Usage

### Quick start
```
Full analysis: Software Engineer @ Google
```

### With a URL
```
Full analysis: https://careers.google.com/jobs/12345
```

### Check your applications
```
List my applications
```

## Troubleshooting

### MCP not showing up

1. Check the server runs manually:
```bash
   cd mcp-servers/hunter
   source venv/bin/activate
   python -c "from server import mcp; print('OK')"
```

2. Re-register the MCP:
```bash
   npx @anthropic-ai/claude-code mcp remove hunter -s user
   npx @anthropic-ai/claude-code mcp add hunter -s user $(pwd)/venv/bin/python $(pwd)/server.py
```

3. Restart VS Code

### PDF not generating

Make sure reportlab is installed:
```bash
pip install reportlab
```

### URL fetch failing

Some sites block scraping. Try:
- Pasting the job description directly
- Using "Role @ Company" format instead

### Notifications not appearing

1. Check macOS notification permissions for Terminal/iTerm
2. Run the script manually to test:
```bash
   python automation/reminder.py
```