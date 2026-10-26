from pathlib import Path

import server


def test_generate_pdf_report(data_dir):
    path = server.generate_pdf_report(
        filename="test_report.pdf",
        company="Acme",
        role="Junior Engineer",
        company_research="Acme builds tools.",
        fit_analysis="Strong Python match.",
        contact_suggestions="Engineering manager.",
        outreach_draft="Hi,\nI'm interested in the role.",
        job_url="https://acme.example/jobs/1",
    )
    pdf = Path(path)
    assert pdf.exists()
    assert pdf.read_bytes().startswith(b"%PDF")
