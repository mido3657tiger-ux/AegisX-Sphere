import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="AegisX-Sphere Central Core API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PhishingCampaign(BaseModel):
    target_domain: str
    template_name: str
    target_emails: List[str]

class ExploitConfig(BaseModel):
    target_ip: str
    target_port: int
    exploit_type: str
    payload_type: str

class DefenseRule(BaseModel):
    rule_name: str
    action: str
    trigger_condition: str

ACTIVE_ATTACKS: List[Dict] = []
COMPROMISED_HOSTS: List[Dict] = []
PHISHING_LOGS: List[Dict] = []

@app.get("/api/v1/status")
async def get_system_status():
    return {
        "status": "OPERATIONAL",
        "red_team_engine": "READY",
        "blue_team_engine": "MONITORING",
        "phishing_lab": "IDLE",
        "active_simulations": len(ACTIVE_ATTACKS)
    }

@app.post("/api/v1/attack/launch")
async def launch_exploit(config: ExploitConfig):
    attack_id = f"ATK-{os.urandom(4).hex()}"
    execution_data = {
        "attack_id": attack_id,
        "target": f"{config.target_ip}:{config.target_port}",
        "type": config.exploit_type,
        "payload": config.payload_type,
        "status": "RUNNING"
    }
    ACTIVE_ATTACKS.append(execution_data)
    return {"status": "SUCCESS", "message": f"Exploit orchestrator initiated.", "data": execution_data}

@app.post("/api/v1/phishing/deploy")
async def deploy_phishing(campaign: PhishingCampaign):
    campaign_id = f"FISH-{os.urandom(4).hex()}"
    log_entry = {
        "campaign_id": campaign_id,
        "domain": campaign.target_domain,
        "template": campaign.template_name,
        "targets_count": len(campaign.target_emails),
        "status": "ACTIVE_HARVESTING"
    }
    PHISHING_LOGS.append(log_entry)
    return {"status": "SUCCESS", "message": "Phishing portal online and dynamic cloner active.", "campaign_id": campaign_id}

@app.post("/api/v1/defense/rules")
async def add_defense_rule(rule: DefenseRule):
    return {"status": "RULE_ACTIVATED", "rule_name": rule.rule_name, "orchestration": "KERNEL_HIDS_SYNCED"}

@app.websocket("/api/v1/ws/live-matrix")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(1)
            telemetry_payload = {
                "active_exploits": ACTIVE_ATTACKS,
                "phishing_hits": PHISHING_LOGS,
                "compromised_nodes": COMPROMISED_HOSTS,
                "system_load": {"cpu": "14%", "memory": "32%"},
                "hids_alerts": [{"event": "PROCESS_HOLLOWING_DETECTED", "severity": "HIGH", "pid": 4102}] if ACTIVE_ATTACKS else []
            }
            await websocket.send_text(json.dumps(telemetry_payload))
    except WebSocketDisconnect:
        pass

