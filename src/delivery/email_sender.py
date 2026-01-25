"""Email sender for daily AI digest."""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class EmailSender:
    """Email delivery for daily digest."""
    
    def __init__(self, smtp_host: str, smtp_port: int, smtp_user: str,
                 smtp_password: str, from_email: str):
        """
        Initialize email sender.
        
        Args:
            smtp_host: SMTP server host
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
            from_email: From email address
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_email = from_email
    
    def send_digest(self, to_email: str, items: List[Dict],
                   digest_summary: str, stats: Dict,
                   subject_prefix: str = "[AI Daily Digest]") -> bool:
        """
        Send daily digest email.
        
        Args:
            to_email: Recipient email address
            items: List of top items to include
            digest_summary: Summary text for introduction
            stats: Statistics dictionary (items analyzed, sources, etc.)
            subject_prefix: Subject line prefix
            
        Returns:
            True if sent successfully
        """
        # Generate subject line
        date_str = datetime.now().strftime('%B %d, %Y')
        subject = f"{subject_prefix} {date_str}"
        
        # Create HTML and plain text versions
        html_content = self._generate_html(items, digest_summary, stats, date_str)
        text_content = self._generate_plain_text(items, digest_summary, stats, date_str)
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = to_email
        
        # Attach both versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        try:
            logger.info(f"Connecting to SMTP server {self.smtp_host}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def _generate_html(self, items: List[Dict], summary: str,
                      stats: Dict, date_str: str) -> str:
        """Generate HTML email content."""
        # Group items by category
        categorized = self._categorize_items(items)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2563eb;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #1e40af;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .summary {{
            background-color: #eff6ff;
            padding: 15px;
            border-left: 4px solid #2563eb;
            margin: 20px 0;
            font-style: italic;
        }}
        .stats {{
            background-color: #f3f4f6;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 0.9em;
        }}
        .item {{
            margin: 20px 0;
            padding: 15px;
            border-left: 3px solid #e5e7eb;
            background-color: #fafafa;
        }}
        .item-title {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .item-title a {{
            color: #2563eb;
            text-decoration: none;
        }}
        .item-title a:hover {{
            text-decoration: underline;
        }}
        .item-meta {{
            font-size: 0.85em;
            color: #6b7280;
            margin: 5px 0;
        }}
        .item-summary {{
            margin: 10px 0;
            color: #4b5563;
        }}
        .score {{
            display: inline-block;
            background-color: #2563eb;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .category {{
            display: inline-block;
            background-color: #10b981;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            text-transform: uppercase;
            margin-left: 5px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            font-size: 0.85em;
            color: #6b7280;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Daily Digest</h1>
        <p style="color: #6b7280; font-size: 0.95em;">{date_str}</p>
        
        <div class="summary">
            {summary}
        </div>
        
        <div class="stats">
            <strong>📊 Today's Stats:</strong><br>
            Items Analyzed: {stats.get('total_items', 0)} | 
            Sources Checked: {stats.get('sources', 0)} | 
            Top Items: {len(items)}
        </div>
"""
        
        # Add sections for each category
        for category, category_items in categorized.items():
            if not category_items:
                continue
                
            category_name = self._format_category_name(category)
            html += f"\n        <h2>🎯 {category_name}</h2>\n"
            
            for item in category_items:
                html += self._generate_item_html(item)
        
        # If no categories, just list all items
        if not any(categorized.values()):
            html += "\n        <h2>🎯 Top Highlights</h2>\n"
            for item in items:
                html += self._generate_item_html(item)
        
        html += f"""
        <div class="footer">
            <p>This digest was automatically generated by Daily AI News Scraper</p>
            <p>Powered by local LLM analysis • Built with ❤️ for the AI community</p>
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_item_html(self, item: Dict) -> str:
        """Generate HTML for a single item."""
        title = item.get('title', 'Untitled')
        url = item.get('url', item.get('permalink', '#'))
        source = item.get('source', 'unknown')
        score = item.get('llm_score', 0)
        
        analysis = item.get('llm_analysis', {})
        summary = analysis.get('summary', '')
        category = analysis.get('category', 'general')
        
        # Get source-specific metadata
        meta_parts = [f"Source: {source}"]
        
        if source == 'reddit':
            subreddit = item.get('subreddit', '')
            upvotes = item.get('score', 0)
            meta_parts.append(f"r/{subreddit}")
            meta_parts.append(f"⬆️ {upvotes}")
        elif source == 'github':
            stars = item.get('stars', 0)
            meta_parts.append(f"⭐ {stars}")
        elif source == 'huggingface':
            item_type = item.get('type', '')
            meta_parts.append(item_type)
        
        meta_text = " • ".join(meta_parts)
        
        return f"""
        <div class="item">
            <div class="item-title">
                <a href="{url}" target="_blank">{title}</a>
                <span class="score">{score}/10</span>
                <span class="category">{category}</span>
            </div>
            <div class="item-meta">{meta_text}</div>
            {f'<div class="item-summary">{summary}</div>' if summary else ''}
        </div>
"""
    
    def _generate_plain_text(self, items: List[Dict], summary: str,
                            stats: Dict, date_str: str) -> str:
        """Generate plain text email content."""
        lines = [
            "=" * 70,
            "AI DAILY DIGEST",
            "=" * 70,
            f"{date_str}",
            "",
            summary,
            "",
            f"📊 Today's Stats:",
            f"Items Analyzed: {stats.get('total_items', 0)}",
            f"Sources Checked: {stats.get('sources', 0)}",
            f"Top Items: {len(items)}",
            "",
            "=" * 70,
            "TOP HIGHLIGHTS",
            "=" * 70,
            ""
        ]
        
        for idx, item in enumerate(items, 1):
            title = item.get('title', 'Untitled')
            url = item.get('url', item.get('permalink', ''))
            source = item.get('source', 'unknown')
            score = item.get('llm_score', 0)
            
            analysis = item.get('llm_analysis', {})
            summary_text = analysis.get('summary', '')
            
            lines.extend([
                f"{idx}. {title}",
                f"   Score: {score}/10 | Source: {source}",
                f"   URL: {url}",
            ])
            
            if summary_text:
                lines.append(f"   {summary_text}")
            
            lines.append("")
        
        lines.extend([
            "=" * 70,
            "This digest was automatically generated by Daily AI News Scraper",
            "Powered by local LLM analysis",
            "=" * 70
        ])
        
        return "\n".join(lines)
    
    def _categorize_items(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """Group items by category."""
        categories = {
            'model': [],
            'paper': [],
            'tool': [],
            'technique': [],
            'application': [],
            'discussion': []
        }
        
        for item in items:
            analysis = item.get('llm_analysis', {})
            category = analysis.get('category', 'discussion')
            
            if category in categories:
                categories[category].append(item)
            else:
                categories['discussion'].append(item)
        
        return categories
    
    def _format_category_name(self, category: str) -> str:
        """Format category name for display."""
        names = {
            'model': 'New Models & Architectures',
            'paper': 'Research Papers',
            'tool': 'Tools & Libraries',
            'technique': 'Techniques & Methods',
            'application': 'Applications & Use Cases',
            'discussion': 'Community Discussions'
        }
        return names.get(category, category.title())
