import sys, os
print("CWD:", os.getcwd())
print("sys.path:", sys.path)
# Try to manually import and report exceptions:
try:
    import backend.ai.agent_base
    print("Manual import: SUCCESS")
except Exception as e:
    print("Manual import: FAILED", e)