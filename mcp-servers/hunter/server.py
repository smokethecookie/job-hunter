from mcp.server.fastmcp import FastMCP
import httpx
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import datetime
from config import PROJECT_ROOT, DATA_DIR

# PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER

mcp = FastMCP("hunter")

# Load CV from CLAUDE.md
CLAUDE_MD = PROJECT_ROOT / "CLAUDE.md"
REPORTS_DIR = DATA_DIR / "reports"


def get_cv() -> str:
    """Read CV from CLAUDE.md"""
    if CLAUDE_MD.exists():
        return CLAUDE_MD.read_text()
    return ""


def fetch_url(url: str) -> str:
    """Fetch and parse a URL to text"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = httpx.get(url, headers=headers, follow_redirects=True, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
        
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"Error fetching URL: {e}"


def generate_pdf_report(
    filename: str,
    company: str,
    role: str,
    company_research: str,
    fit_analysis: str,
    contact_suggestions: str,
    outreach_draft: str,
    job_url: str = ""
) -> str:
    """Generate a PDF report with all analysis results."""
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = REPORTS_DIR / filename
    
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2563eb')
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceBefore=6,
        spaceAfter=6,
        leading=14
    )
    
    # Build document content
    story = []
    
    # Title
    story.append(Paragraph(f"Job Application Report", title_style))
    story.append(Paragraph(f"{role} @ {company}", styles['Heading2']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    if job_url:
        story.append(Paragraph(f"URL: {job_url}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Company Research Section
    story.append(Paragraph("Company Research", heading_style))
    for line in company_research.split('\n'):
        if line.strip():
            # Handle markdown-style headers
            if line.startswith('## '):
                story.append(Paragraph(line[3:], subheading_style))
            elif line.startswith('# '):
                story.append(Paragraph(line[2:], subheading_style))
            elif line.startswith('- '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            elif line.startswith('* '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            else:
                story.append(Paragraph(line, body_style))
    story.append(Spacer(1, 15))
    
    # Fit Analysis Section
    story.append(Paragraph("Fit Analysis", heading_style))
    for line in fit_analysis.split('\n'):
        if line.strip():
            if line.startswith('## '):
                story.append(Paragraph(line[3:], subheading_style))
            elif line.startswith('# '):
                story.append(Paragraph(line[2:], subheading_style))
            elif line.startswith('- '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            elif line.startswith('* '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            else:
                story.append(Paragraph(line, body_style))
    story.append(Spacer(1, 15))
    
    # Contact Suggestions Section
    story.append(Paragraph("Contact Suggestions", heading_style))
    for line in contact_suggestions.split('\n'):
        if line.strip():
            if line.startswith('## '):
                story.append(Paragraph(line[3:], subheading_style))
            elif line.startswith('# '):
                story.append(Paragraph(line[2:], subheading_style))
            elif line.startswith('- '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            elif line.startswith('* '):
                story.append(Paragraph(f"• {line[2:]}", body_style))
            else:
                story.append(Paragraph(line, body_style))
    story.append(Spacer(1, 15))
    
    # Outreach Draft Section
    story.append(Paragraph("Outreach Draft", heading_style))
    for line in outreach_draft.split('\n'):
        if line.strip():
            story.append(Paragraph(line, body_style))
    
    # Build PDF
    doc.build(story)
    
    return str(filepath)


@mcp.tool()
def full_analysis(input_text: str) -> str:
    """
    Run a complete job application analysis pipeline.
    
    This orchestrator tool runs the full workflow:
    1. Parse input (URL or "Role @ Company" format)
    2. Fetch/search for job posting
    3. Research the company
    4. Analyze fit against your CV
    5. Suggest contacts
    6. Draft outreach message
    7. Generate PDF report
    8. Save application to tracker
    
    Args:
        input_text: Either a job URL OR "Role @ Company" format (e.g., "Software Engineer @ Stripe")
    
    Returns:
        Instructions for Claude to execute the full pipeline and generate a PDF report.
    """
    cv = get_cv()
    
    # Detect input type
    is_url = input_text.startswith("http://") or input_text.startswith("https://")
    
    if is_url:
        job_content = fetch_url(input_text)
        if job_content.startswith("Error"):
            return f"Could not fetch URL: {job_content}\n\nPlease provide the job details in 'Role @ Company' format instead."
        
        return f"""# Full Analysis Pipeline — URL Mode

## Job Posting Content
URL: {input_text}

{job_content[:15000]}

## Your CV/Background
{cv}

---

## INSTRUCTIONS

You are running a complete job application analysis. Execute ALL of the following steps WITHOUT asking for confirmation. Provide comprehensive output for each section.

### Step 1: Extract Job Details
From the job posting above, extract:
- Company name
- Role title  
- Location
- Key requirements (must-have)
- Nice-to-have requirements
- Responsibilities

### Step 2: Company Research
Based on the company name, provide:
- Company overview (what they do, size, industry)
- Company culture (if apparent)
- Recent news or developments
- Tech stack (if relevant)
- Any red flags or highlights

Use web search if needed to find current information.

### Step 3: Fit Analysis
Compare the job requirements against my CV and provide:

**Strong Matches ✓**
(Requirements I clearly meet with evidence)

**Partial Matches ~**
(Requirements I partially meet or have related experience)

**Gaps ✗**
(Requirements I don't currently meet)

**Unlisted Strengths**
(My skills that weren't required but add value)

**Overall Fit Score**
(X/10 with brief justification)

### Step 4: Contact Suggestions
Suggest how to find the right person to contact:
- Job titles to search for on LinkedIn
- What to look for on company website
- Prioritized contact types

### Step 5: Draft Outreach
Write a professional email that:
- Is personalized to the company and role
- Highlights my most relevant experience
- Shows genuine interest
- Has a clear call to action
- Is concise (under 200 words)

### Step 6: Generate Report
After completing all analysis, call the `generate_report` tool with all the information gathered.

### Step 7: Save Application
Call `save_application` with:
- Company name
- Role title
- URL: {input_text}
- Status: "researching"
- Notes: Include fit score and key highlights

---

BEGIN ANALYSIS NOW. Do not ask for confirmation. Provide complete output for all sections.
"""
    
    else:
        # Parse "Role @ Company" format
        if " @ " in input_text:
            parts = input_text.split(" @ ", 1)
            role = parts[0].strip()
            company = parts[1].strip()
        elif " at " in input_text.lower():
            parts = input_text.lower().split(" at ", 1)
            role = input_text[:len(parts[0])].strip()
            company = input_text[len(parts[0])+4:].strip()
        else:
            return "Please provide input as 'Role @ Company' (e.g., 'Software Engineer @ Stripe') or a job posting URL."
        
        return f"""# Full Analysis Pipeline — Search Mode

## Target
- Role: {role}
- Company: {company}

## Your CV/Background
{cv}

---

## INSTRUCTIONS

You are running a complete job application analysis. Execute ALL of the following steps WITHOUT asking for confirmation. Provide comprehensive output for each section.

### Step 1: Find Job Posting
Search the web for this role at {company}. Look for:
- Official job posting on company careers page
- LinkedIn job listing
- Other job boards (Indeed, Glassdoor)

Extract:
- Job URL (if found)
- Key requirements
- Nice-to-have requirements
- Responsibilities

### Step 2: Company Research
Research {company} and provide:
- Company overview (what they do, size, industry, funding)
- Company culture
- Recent news or developments
- Tech stack (if relevant)
- Any red flags or highlights

Use web search to find current information.

### Step 3: Fit Analysis
Compare typical requirements for {role} at {company} against my CV:

**Strong Matches ✓**
(Requirements I clearly meet with evidence)

**Partial Matches ~**
(Requirements I partially meet or have related experience)

**Gaps ✗**
(Requirements I don't currently meet)

**Unlisted Strengths**
(My skills that weren't required but add value)

**Overall Fit Score**
(X/10 with brief justification)

### Step 4: Contact Suggestions
Suggest how to find the right person to contact at {company}:
- Specific job titles to search on LinkedIn
- What to look for on company website
- Prioritized contact types

### Step 5: Draft Outreach
Write a professional email to a hiring manager/recruiter that:
- Is personalized to {company} and the {role} role
- Highlights my most relevant experience
- Shows genuine interest
- Has a clear call to action
- Is concise (under 200 words)

### Step 6: Generate Report
After completing all analysis, call the `generate_report` tool with:
- company: {company}
- role: {role}
- All sections of analysis

### Step 7: Save Application
Call `save_application` with:
- Company: {company}
- Role: {role}
- URL: (job posting URL if found, otherwise company careers page)
- Status: "researching"
- Notes: Include fit score and key highlights

---

BEGIN ANALYSIS NOW. Do not ask for confirmation. Provide complete output for all sections.
"""


@mcp.tool()
def generate_report(
    company: str,
    role: str,
    company_research: str,
    fit_analysis: str,
    contact_suggestions: str,
    outreach_draft: str,
    job_url: str = ""
) -> str:
    """
    Generate a PDF report with all job application analysis.
    
    Call this after completing the full analysis to create a downloadable PDF.
    
    Args:
        company: Company name
        role: Job title
        company_research: Company research findings
        fit_analysis: Fit analysis results (matches, gaps, score)
        contact_suggestions: Contact finding suggestions
        outreach_draft: Draft outreach message
        job_url: Job posting URL (optional)
    """
    # Generate filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_company = company.lower().replace(" ", "-").replace(".", "")[:30]
    safe_role = role.lower().replace(" ", "-").replace(".", "")[:30]
    filename = f"{safe_company}-{safe_role}-{date_str}.pdf"
    
    try:
        filepath = generate_pdf_report(
            filename=filename,
            company=company,
            role=role,
            company_research=company_research,
            fit_analysis=fit_analysis,
            contact_suggestions=contact_suggestions,
            outreach_draft=outreach_draft,
            job_url=job_url
        )
        return f"""# Report Generated Successfully

**File:** {filepath}

The PDF report has been saved to: `{filepath}`

It contains:
- Company Research
- Fit Analysis
- Contact Suggestions  
- Outreach Draft

You can find it in the `data/reports/` folder.
"""
    except Exception as e:
        return f"Error generating PDF: {e}"


@mcp.tool()
def analyze_job(url: str) -> str:
    """
    Analyze a job posting URL. Extracts requirements, company info, and role details.
    
    Args:
        url: The job posting URL
    """
    content = fetch_url(url)
    
    if content.startswith("Error"):
        return content
    
    return f"""# Job Posting Content

URL: {url}

{content[:15000]}

---
Please analyze this job posting and extract:
1. Company name
2. Role title
3. Location
4. Key requirements (must-have)
5. Nice-to-have requirements
6. Responsibilities
7. Any other relevant details
"""


@mcp.tool()
def research_company(company_name: str, website_url: str = "") -> str:
    """
    Research a company by fetching their website and searching for news.
    
    Args:
        company_name: Name of the company
        website_url: Company website URL (optional, will try to find if not provided)
    """
    results = []
    
    if website_url:
        about_content = fetch_url(website_url)
        if not about_content.startswith("Error"):
            results.append(f"## Company Website Content\n\n{about_content[:8000]}")
    
        for path in ["/about", "/about-us", "/company", "/team"]:
            about_url = website_url.rstrip("/") + path
            about_content = fetch_url(about_url)
            if not about_content.startswith("Error") and len(about_content) > 500:
                results.append(f"## About Page ({path})\n\n{about_content[:5000]}")
                break
    
    if not results:
        results.append(f"Could not fetch company website. Please provide the correct URL or search manually.")
    
    return f"""# Company Research: {company_name}

{chr(10).join(results)}

---
Based on this information, please provide:
1. Company overview
2. What they do
3. Company culture (if apparent)
4. Tech stack (if mentioned)
5. Any red flags or highlights
"""


@mcp.tool()
def analyze_fit(job_requirements: str) -> str:
    """
    Compare job requirements against my CV and analyze fit.
    
    Args:
        job_requirements: The extracted requirements from a job posting
    """
    cv = get_cv()
    
    return f"""# Fit Analysis Request

## My CV/Background

{cv}

## Job Requirements

{job_requirements}

---
Please analyze and provide:

## Strong Matches ✓
(Requirements I clearly meet with evidence from my CV)

## Partial Matches ~
(Requirements I partially meet or have related experience)

## Gaps ✗
(Requirements I don't currently meet)

## My Unlisted Strengths
(Relevant skills/experience I have that weren't in the requirements but could be valuable)

## Overall Fit Assessment
(Summary: Am I a good fit? What should I emphasize? What gaps should I address?)
"""


@mcp.tool()
def find_contacts(company_name: str, role_type: str = "engineering") -> str:
    """
    Suggest how to find relevant contacts at a company for outreach.
    
    Args:
        company_name: Name of the company
        role_type: Type of role (engineering, recruiting, etc.)
    """
    return f"""# Finding Contacts at {company_name}

## Suggested Search Strategies

1. **LinkedIn Search**
   - Search: "{company_name} recruiter"
   - Search: "{company_name} hiring manager {role_type}"
   - Search: "{company_name} talent acquisition"
   - Look for recent hires in similar roles (potential referrals)

2. **Company Website**
   - Check /team or /about pages
   - Look for leadership/management listed

3. **Job Posting**
   - Sometimes lists hiring manager or recruiter name
   - Check who posted it on LinkedIn

## Contact Prioritization
1. Hiring manager for the role (best)
2. Recruiter/talent acquisition (good)
3. Recent hire in similar role (for referral)
4. Team lead in relevant department (good)

---
Once you find a contact, use `draft_outreach` to create a personalized message.
"""


@mcp.tool()
def draft_outreach(
    contact_name: str,
    contact_role: str,
    company: str,
    job_title: str,
    channel: str = "email",
    additional_context: str = ""
) -> str:
    """
    Draft a personalized outreach message.
    
    Args:
        contact_name: Name of the person to contact
        contact_role: Their role (recruiter, hiring manager, etc.)
        company: Company name
        job_title: The job you're applying for
        channel: "email" or "linkedin" 
        additional_context: Any additional context for personalization
    """
    cv = get_cv()
    
    return f"""# Outreach Draft Request

## Contact
- Name: {contact_name}
- Role: {contact_role}
- Company: {company}

## Job
- Title: {job_title}

## Channel
- {channel}

## My Background
{cv}

## Additional Context
{additional_context if additional_context else "None provided"}

---
Please draft a {"short LinkedIn message (under 300 characters for connection request, or longer InMail)" if channel == "linkedin" else "professional email"} that:

1. Is personalized to the contact and company
2. Briefly highlights my most relevant experience
3. Shows genuine interest in the role
4. Has a clear call to action
5. Is concise and respectful of their time

Provide the draft, then ask for my approval before sending.
"""


@mcp.tool()
def save_application(
    company: str,
    role: str,
    url: str,
    status: str = "researching",
    notes: str = ""
) -> str:
    """
    Save a job application to track it.
    
    Args:
        company: Company name
        role: Job title
        url: Job posting URL
        status: Status (researching, applied, interviewing, offer, rejected)
        notes: Any notes
    """
    DATA_DIR.mkdir(exist_ok=True)
    applications_file = DATA_DIR / "applications.json"
    
    if applications_file.exists():
        applications = json.loads(applications_file.read_text())
    else:
        applications = []
    
    application = {
        "id": len(applications) + 1,
        "company": company,
        "role": role,
        "url": url,
        "status": status,
        "notes": notes,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    applications.append(application)
    
    applications_file.write_text(json.dumps(applications, indent=2))
    
    return f"Saved application #{application['id']}: {role} at {company}"


@mcp.tool()
def list_applications(status: str = "") -> str:
    """
    List tracked job applications.
    
    Args:
        status: Filter by status (optional)
    """
    applications_file = DATA_DIR / "applications.json"
    
    if not applications_file.exists():
        return "No applications tracked yet."
    
    applications = json.loads(applications_file.read_text())
    
    if status:
        applications = [a for a in applications if a["status"] == status]
    
    if not applications:
        return f"No applications found{' with status: ' + status if status else ''}."
    
    result = "# Tracked Applications\n\n"
    for app in applications:
        result += f"**#{app['id']} {app['role']} at {app['company']}**\n"
        result += f"- Status: {app['status']}\n"
        result += f"- URL: {app['url']}\n"
        result += f"- Added: {app['created_at'][:10]}\n"
        if app['notes']:
            result += f"- Notes: {app['notes']}\n"
        result += "\n"
    
    return result


@mcp.tool()
def analyze_role(role: str, company: str) -> str:
    """
    Analyze a job role at a company by searching for information.
    Use this when you don't have a direct job posting URL.
    
    Args:
        role: Job title (e.g., "Software Engineer", "Graduate AI Specialist")
        company: Company name (e.g., "Google", "Sandberg Development")
    """
    cv = get_cv()
    
    return f"""# Role Analysis Request

## Target Role
- Position: {role}
- Company: {company}

## My Background
{cv}

---
Please:

1. **Search for this role** at {company} — find the job posting, requirements, and details
2. **Research {company}** — what they do, culture, tech stack, recent news
3. **Analyze my fit** — match my background against typical requirements for this role
4. **Generate reports**:
   - Company Report
   - Fit Analysis (matches, partial matches, gaps)
5. **Suggest contacts** to reach out to

Use web search to find current information.
"""


if __name__ == "__main__":
    mcp.run()
