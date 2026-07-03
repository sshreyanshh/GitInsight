from datetime import datetime
from fpdf import FPDF
import os

class GitInsightReport:

    def __init__(self, username):
        self.pdf = FPDF()
        self.pdf.set_margins(15, 15, 15)
        self.username = username
    
    def addProfileSec(self, data):
        self.pdf.add_page()
        self.pdf.set_font("Times", "B", 24)
        self.pdf.cell(0, 10, "GitInsight Report", ln = True)
        self.pdf.ln(10)

        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 0, f"GitHub Username: {self.username}", ln = True)
        self.pdf.cell(0, 10, f"Report Generated on: {datetime.now().strftime('%d %B %Y')}", ln = True)
        
        self.pdf.line(self.pdf.l_margin, self.pdf.get_y(), self.pdf.w - self.pdf.r_margin, self.pdf.get_y())
        #horizontal line
        self.pdf.ln(10)

        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 10, "Profile Information", ln = True)

        self.pdf.set_font("Times", "", 12)
        fields = [
            ("Name", data.get('name') or "N/A"),
            ("Username", data.get('login') or "N/A"),
            ("Public Repositories", str(data.get('public_repos') or "N/A")),
            ("Followers", str(data.get('followers') or "N/A")),
            ("Following", str(data.get('following') or "N/A")),
            ("Location", data.get('location') or "N/A"),
            ("Account Created on", datetime.strptime(data.get('created_at') or "N/A", "%Y-%m-%dT%H:%M:%SZ").strftime("%d %B %Y"))
        ]        

        for label, value in fields:
            self.pdf.cell(50, 10, f"{label}:", ln = False)
            self.pdf.cell(0, 10, value, ln = True)
        
        self.pdf.ln()  # Add a line break after the profile section
        
    def addStats(self, stats):
        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 10, "Statistics", ln = True)

        self.pdf.set_font("Times", "", 12)
        
        self.pdf.cell(50, 10, "Most Used Language:", ln = False)
        self.pdf.cell(0, 10, stats["lang"], ln = True)

        self.pdf.cell(50, 10, "Total Stars:", ln = False)
        self.pdf.cell(0, 10, str(stats["totalstars"]), ln = True)

        self.pdf.cell(50, 10, "Most Starred Repository:", ln = False)
        self.pdf.cell(0, 10, f"{stats['moststarred']['name']} ({stats['moststarred']['stars']} stars)", ln = True)

        self.pdf.ln()
    
    def addRepo(self, repodata, stats):
        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 10, "Repositories", ln = True)

        repodata = [repo for repo in repodata if not repo.get('fork')]
        sortedData = sorted(repodata, key = lambda x: x['stargazers_count'], reverse = True)

        col_widths = [80, 40, 30, 30]

        self.pdf.set_font("Times", "B", 12)
        headers = ["Name", "Language", "Stars", "Forks"]
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, border = 1, ln = False)
        self.pdf.ln()

        self.pdf.set_font("Times", "", 12)
        for repo in sortedData:
            self.pdf.cell(col_widths[0], 10, repo.get('name'), border = 1, ln = False)
            self.pdf.cell(col_widths[1], 10, repo.get('language') or "N/A", border = 1, ln = False)
            self.pdf.cell(col_widths[2], 10, str(repo.get('stargazers_count')), border = 1, ln = False)
            self.pdf.cell(col_widths[3], 10, str(repo.get('forks')), border = 1, ln = True)
        self.pdf.ln()

        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 10, "Language Wise Data", ln = True)
        self.pdf.set_font("Times", "", 12)

        headers = ["Language", "Count"]
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, border = 1, ln = False)
        self.pdf.ln()

        for lang, count in stats["langwise"].items():
            self.pdf.cell(col_widths[0], 10, lang, border = 1, ln = False)
            self.pdf.cell(col_widths[1], 10, str(count), border = 1, ln = True)
        self.pdf.ln()

    def addActivity(self, activity):
        self.pdf.set_font("Times", "B", 14)
        self.pdf.cell(0, 10, "Activity", ln = True)

        self.pdf.set_font("Times", "", 12)
        
        self.pdf.cell(50, 10, "Most Active Day:", ln = False)
        self.pdf.cell(0, 10, activity[1], ln = True)

        self.pdf.cell(50, 10, "Most Active Repository:", ln = False)
        self.pdf.cell(0, 10, activity[2], ln = True)

        self.pdf.ln()      
        
        col_widths = [80, 40]
        self.pdf.set_font("Times", "B", 12)
        headers = ["Event Type", "Frequency"]
        for i, header in enumerate(headers):
            self.pdf.cell(col_widths[i], 10, header, border = 1, ln = False)
        self.pdf.ln()

        self.pdf.set_font("Times", "", 12)
        for key, value in activity[0].items():
            self.pdf.cell(col_widths[0], 10, key, border = 1, ln = False)
            self.pdf.cell(col_widths[1], 10, str(value), border = 1, ln = True)
        self.pdf.ln()

    def save(self):
        os.makedirs("reports", exist_ok = True)
        filename = f"reports/{self.username}_GitInsight_Report.pdf"
        self.pdf.output(filename)

        return filename