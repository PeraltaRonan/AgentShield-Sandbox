#!/bin/bash
echo "[*] Launching AgentShield Sandbox..."
docker compose up -d

echo "[*] Simulating unauthorized process execution (/bin/sh spawn)..."
docker exec -it agentshield_sandbox /bin/sh -c "whoami"

echo "[*] Sandbox status:"
docker ps --filter "name=agentshield_sandbox"
