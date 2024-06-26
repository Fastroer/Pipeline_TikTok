from datetime import datetime
import os

def generate_report(videos_processed, time_taken, issues, report_path):
    issues_str = "\n".join(issues) if issues else "No issues"
    report_content = f"""
# TikTok Video Processing Report

**Number of videos processed:** {videos_processed}

**Time taken for the entire process:** {time_taken} seconds

**Issues encountered and resolutions:**
{issues_str}

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write(report_content)

if __name__ == "__main__":
    generate_report(100, 3600, ["No issues"], "reports/summary_report.md")
