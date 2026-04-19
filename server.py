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

@app.get('/get/{key}')
def get_key(key: str):

    if not engine.stdin or not engine.stdout:
        raise HTTPException(status_code=500, detail="IPC Bridge Collapsed")

    command = f"GET {key}\n".encode('utf-8')

    engine.stdin.write(command)
    engine.stdin.flush()

    result = engine.stdout.readline().decode('utf-8').strip()
    if result == "NULL":
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": result}


@app.post("/set")
def set_key(cmd : SetCommand):

    if not engine.stdin or not engine.stdout:
        raise HTTPException(status_code=500, detail="IPC Bridge Collapsed")

    command = f"SET {cmd.key} {cmd.value}\n".encode('utf=8')

    engine.stdin.write(command)
    engine.stdout.flush()

    result = engine.stdout.readline().decode('utf-8').strip()
    if result == "OK":
        return {"status": "success", "key": cmd.key}
    else:
        raise HTTPException(status_code=500, detail="Engine failed to execute")

    
