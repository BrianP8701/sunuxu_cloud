# tests/test_api_locally/admin.py
import os
import signal
import subprocess
from sunuxu.database import AzureSQLDatabase

db = AzureSQLDatabase()

def start_function_app():
    global func_process
    func_process = subprocess.Popen(["func", "start"])

def stop_function_app():
    global func_process
    if func_process:
        if os.name == 'nt':  # For Windows
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(func_process.pid)], check=True)
        else:  # For macOS/Linux
            os.killpg(os.getpgid(func_process.pid), signal.SIGTERM)
        func_process.wait()
        func_process = None
