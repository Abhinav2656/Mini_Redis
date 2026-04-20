from fastapi import FastAPI, HTTPException
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