from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess

app = FastAPI(title='Mini Redis Engine API')

try:
    engine = subprocess.Popen(
        ["./mini_redis"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
except FileNotFoundError:
    print("Fatal Error: C++ executable not found. Compile it first.")
    exit(1)

# ---------------------------------------------------------
# THE VISUAL SHIELD (FRONTEND DASHBOARD)
# ---------------------------------------------------------
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini-Redis Memory Core</title>
    <style>
        body { background: #050505; color: #00ff00; font-family: monospace; padding: 2rem; margin: 0; }
        .container { max-width: 800px; margin: 0 auto; border: 1px solid #333; padding: 20px; background: #0a0a0a; box-shadow: 0 0 15px rgba(0,255,0,0.1); }
        h1 { border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 0; text-transform: uppercase; letter-spacing: 2px; }
        .control-panel { display: flex; gap: 10px; margin-bottom: 20px; }
        input { background: #000; color: #00ff00; border: 1px solid #444; padding: 12px; font-family: monospace; flex: 1; outline: none; }
        input:focus { border-color: #00ff00; }
        button { background: #111; color: #00ff00; border: 1px solid #00ff00; padding: 12px 24px; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: all 0.2s; }
        button:hover { background: #00ff00; color: #000; }
        #terminal { background: #000; border: 1px solid #333; height: 350px; padding: 15px; overflow-y: auto; font-size: 14px; line-height: 1.5; }
        .log-entry { margin-bottom: 5px; }
        .latency { color: #ff3366; font-weight: bold; }
        .timestamp { color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>[ C++ LRU Memory Arena ]</h1>
        <p style="color: #888;">Direct IPC Bridge Active. Awaiting commands...</p>
        
        <div class="control-panel">
            <input id="keyInput" placeholder="ENTER KEY (e.g., player)" autocomplete="off" />
            <input id="valInput" placeholder="ENTER VALUE (e.g., Abhinav)" autocomplete="off" />
            <button onclick="executeSet()">SET</button>
            <button onclick="executeGet()">GET</button>
        </div>

        <div id="terminal">
            <div class="log-entry"><span class="timestamp">[SYSTEM]</span> Engine Ready. Monitoring execution latency...</div>
        </div>
    </div>

    <script>
        const term = document.getElementById('terminal');
        const keyIn = document.getElementById('keyInput');
        const valIn = document.getElementById('valInput');

        function log(msg) { 
            const time = new Date().toLocaleTimeString();
            term.innerHTML += `<div class="log-entry"><span class="timestamp">[${time}]</span> > ${msg}</div>`; 
            term.scrollTop = term.scrollHeight; 
        }

        async function executeSet() {
            const k = keyIn.value.trim();
            const v = valIn.value.trim();
            if(!k || !v) return log("ERROR: Key and Value are required for SET operation.");

            const start = performance.now();
            const keys = k.split(',');
            const vals = v.split(',');

            if (keys.length > 1 && keys.length === vals.length) {
                // BATCH EXECUTION
                const payload = keys.map((key, i) => ({key: key.trim(), value: vals[i].trim()}));
                const res = await fetch('/mset', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({items: payload})
                });
                const data = await res.json();
                const netTime = (performance.now() - start).toFixed(2);
                const coreMs = (data.total_engine_us / 1000).toFixed(4);
                
                log(`MSET [${data.keys_processed} Keys] <span class="latency">(Net: ${netTime}ms | Core: ${coreMs}ms)</span>`);
            } else {
                // SINGLE EXECUTION
                const res = await fetch('/set', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({key: k, value: v})
                });
                const data = await res.json();
                const netTime = (performance.now() - start).toFixed(2);
                const coreMs = (data.engine_us / 1000).toFixed(4);
                
                log(`SET [${k}] = ${v} <span class="latency">(Net: ${netTime}ms | Core: ${coreMs}ms)</span>`);
            }
        }

        async function executeGet() {
            const k = keyIn.value.trim();
            if(!k) return log("ERROR: Key is required.");
            
            // THE SHIELD: Prevent poisoned inputs
            if(k.includes(',') || k.includes(' ')) {
                return log("FATAL: GET only accepts a single, solid key without spaces.");
            }

            const start = performance.now();
            const res = await fetch('/get/' + k);
            const data = await res.json();
            const netTime = (performance.now() - start).toFixed(2);
            const coreMs = (data.engine_us / 1000).toFixed(4);
            
            log(`GET [${k}] -> ${data.value} <span class="latency">(Net: ${netTime}ms | Core: ${coreMs}ms)</span>`);
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    return HTML_UI

class SetCommand(BaseModel):
    key: str
    value: str

class BatchSetRequest(BaseModel):
    items: List[SetCommand]

# -- YOUR EXISTING SET ROUTE --
@app.post("/set")
def set_value(item: dict):
    key = item.get("key")
    value = item.get("value")
    engine.stdin.write(f"SET {key} {value}\n".encode('utf-8'))
    engine.stdin.flush()
    
    # Python reads "OK|15" and splits it
    raw_response = engine.stdout.readline().decode('utf-8').strip()
    parts = raw_response.split('|')
    
    return {"status": parts[0], "engine_us": parts[1] if len(parts) > 1 else "0"}

# -- THE NEW BATCH ROUTE --
@app.post("/mset")
def mset_values(batch: BatchSetRequest):
    total_engine_us = 0
    
    for item in batch.items:
        engine.stdin.write(f"SET {item.key} {item.value}\n".encode('utf-8'))
        engine.stdin.flush()
        raw_response = engine.stdout.readline().decode('utf-8').strip()
        parts = raw_response.split('|')
        if len(parts) > 1:
            total_engine_us += int(parts[1])
            
    return {"status": "BATCH_OK", "keys_processed": len(batch.items), "total_engine_us": total_engine_us}

# -- YOUR EXISTING GET ROUTE --
@app.get("/get/{key}")
def get_value(key: str):
    engine.stdin.write(f"GET {key}\n".encode('utf-8'))
    engine.stdin.flush()
    
    raw_response = engine.stdout.readline().decode('utf-8').strip()
    parts = raw_response.split('|')
    value = parts[0]
    engine_us = parts[1] if len(parts) > 1 else "0"
    
    if value == "NULL":
        return {"value": "NULL", "engine_us": engine_us} # Don't throw 404, just return NULL so UI can show it
    return {"value": value, "engine_us": engine_us}

