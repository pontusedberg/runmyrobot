from mebo.letsrobot_to_mebo_converter import LetsRobotToMeboConverter
from mebo.letsrobot_commands import LetsrobotCommands
from mebo.letsrobot_to_param_lookup import letsrobot_to_param_lookup
import mebo.mebo_constants as mebo_constants
import httplib, socket, time

converter = LetsRobotToMeboConverter()

def handle_mebo_command(command):
    command = command.encode('ascii','ignore')
    
    if command == "stop":
        return

    if command == "S1":
        print "SET TURNING_SPEED S1"
        letsrobot_to_param_lookup[LetsrobotCommands.L] = mebo_constants.TURNINGSPEEDS1
        letsrobot_to_param_lookup[LetsrobotCommands.R] = mebo_constants.TURNINGSPEEDS1
        return
    if command == "S2":
        print "SET TURNING SPEED S2"
        letsrobot_to_param_lookup[LetsrobotCommands.L] = mebo_constants.TURNINGSPEEDS2
        letsrobot_to_param_lookup[LetsrobotCommands.R] = mebo_constants.TURNINGSPEEDS2
        return
    if command == "S3":
        print "SET TURNING SPEED S3"
        letsrobot_to_param_lookup[LetsrobotCommands.L] = mebo_constants.TURNINGSPEEDS3
        letsrobot_to_param_lookup[LetsrobotCommands.R] = mebo_constants.TURNINGSPEEDS3
        return
    
    mebo_command = converter.convert({
        "command": command,
        "parameter": letsrobot_to_param_lookup[LetsrobotCommands(command)]
    })

    mebo_command_stop = converter.convert({
        "command": "F",
        "parameter": 0
    }, {
        "command": "AU",
        "parameter": 0
    }, {
        "command": "WU",
        "parameter": 0
    }, {
        "command": "RL",
        "parameter": 0
    })

    try:
        conn = httplib.HTTPConnection(mebo_constants.MEBO_IP_ADDRESSE)
        
        print "sending GET request to: " + str(mebo_constants.MEBO_IP_ADDRESSE) + "/ajax/command.json" + mebo_command
        conn.request("GET","/ajax/command.json" + mebo_command)
        print "AA - " + mebo_command
        res = conn.getresponse()
        print(res.status, res.reason)
    
        time.sleep(mebo_constants.COMMAND_DURATION)
    
        print "sending GET request to: " + str(mebo_constants.MEBO_IP_ADDRESSE) + "/ajax/command.json" + mebo_command_stop
        conn.request("GET","/ajax/command.json" + mebo_command_stop)
        print "AB - " + mebo_command_stop
        res = conn.getresponse()
        print(res.status, res.reason)
    except (httplib.HTTPException, socket.error) as ex:
        print "Error: %s" % ex
