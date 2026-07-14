import subprocess
import sys

# Start drx.py
p1 = subprocess.Popen([sys.executable, "api.py"])

# Start API.PY
p2 = subprocess.Popen([sys.executable, "drx.py"])

print("Both scripts are running...")

# Wait for both scripts to finish
p1.wait()
p2.wait()
