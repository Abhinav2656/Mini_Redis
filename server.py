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
            try {
                const res = await fetch('/set', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({key: k, value: v})
                });
                const time = (performance.now() - start).toFixed(2);

                if(res.ok) log(`SET [${k}] = ${v} <span class="latency">(${time}ms)</span>`);
                else log(`ERROR: Engine rejected SET command <span class="latency">(${time}ms)</span>`);
            } catch (err) {
                log(`FATAL: Bridge disconnected.`);
            }
        }

        async function executeGet() {
            const k = keyIn.value.trim();
            if(!k) return log("ERROR: Key is required for GET operation.");

            const start = performance.now();
            try {
                const res = await fetch('/get/' + k);
                const time = (performance.now() - start).toFixed(2);

                if(res.ok) {
                    const data = await res.json();
                    log(`GET [${k}] -> ${data.value} <span class="latency">(${time}ms)</span>`);
                } else if(res.status === 404) {
                    log(`GET [${k}] -> NULL <span class="latency">(${time}ms)</span>`);
                } else {
                    log(`ERROR: Core logic failure <span class="latency">(${time}ms)</span>`);
                }
            } catch (err) {
                log(`FATAL: Bridge disconnected.`);
            }
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

@app.post("/set")
def set_value(item: dict):
    key = item.get("key")
    value = item.get("value")
    
    print(f"[BRIDGE] Writing SET command for {key}...", flush=True)
    command = f"SET {key} {value}\n"
    
    # THE TRANSLATION STRIKE: Encode to raw bytes
    engine.stdin.write(command.encode('utf-8'))
    engine.stdin.flush()
    print(f"[BRIDGE] SET command flushed. Waiting for C++...", flush=True)
    
    # THE RECEPTION STRIKE: Decode back to Python string
    response = engine.stdout.readline().decode('utf-8').strip()
    print(f"[BRIDGE] C++ Responded to SET: {response}", flush=True)
    
    return {"status": response}

@app.get("/get/{key}")
def get_value(key: str):
    print(f"[BRIDGE] Writing GET command for {key}...", flush=True)
    command = f"GET {key}\n"
    
    # THE TRANSLATION STRIKE
    engine.stdin.write(command.encode('utf-8'))
    engine.stdin.flush()
    print(f"[BRIDGE] GET command flushed. Waiting for C++...", flush=True)
    
    # THE RECEPTION STRIKE
    response = engine.stdout.readline().decode('utf-8').strip()
    print(f"[BRIDGE] C++ Responded to GET: {response}", flush=True)
    
    if response == "NULL":
        raise HTTPException(status_code=404, detail="Not Found")
    return {"value": response}