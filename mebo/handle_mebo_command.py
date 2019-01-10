from mebo.letsrobot_to_mebo_converter import LetsRobotToMeboConverter
from mebo.letsrobot_commands import LetsrobotCommands
from mebo.letsrobot_to_param_lookup import letsrobot_to_param_lookup
import mebo.mebo_constants as mebo_constants
import httplib, socket, time

converter = LetsRobotToMeboConverter()

def handle_speed(command, speed):
    command = command.encode('ascii','ignore')

    if command == "S":
        print "setting speed"
        letsrobot_to_param_lookup[LetsrobotCommands.F] = speed
        letsrobot_to_param_lookup[LetsrobotCommands.B] = speed
        return
    if command == "T":
        print "setting turning"
        letsrobot_to_param_lookup[LetsrobotCommands.L] = speed
        letsrobot_to_param_lookup[LetsrobotCommands.R] = speed
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
        
        print "\nSTART - sending GET request to: " + str(mebo_constants.MEBO_IP_ADDRESSE) + "/ajax/command.json" + mebo_command + "\n"
        conn.request("GET","/ajax/command.json" + mebo_command)
        res = conn.getresponse()
        print(res.status, res.reason)
    
        time.sleep(mebo_constants.COMMAND_DURATION)
    
        print "\nSTOP - sending GET request to: " + str(mebo_constants.MEBO_IP_ADDRESSE) + "/ajax/command.json" + mebo_command_stop + "\n"
        conn.request("GET","/ajax/command.json" + mebo_command_stop)
        res = conn.getresponse()
        print(res.status, res.reason)
    except (httplib.HTTPException, socket.error) as ex:
        print "Error: %s" % ex

def handle_mebo_command(command):
    command = command.encode('ascii','ignore')
    
    if command == "stop":
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
        
        print "\nSTART - sending GET request to: " + str(mebo_constants.MEBO_IP_ADDRESSE) + "/ajax/command.json" + mebo_command + "\n"
        conn.request("GET","/ajax/command.json" + mebo_command)
        res = conn.getresponse()
        print(res.status, res.reason)
    
        time.sleep(mebo_constants.COMMAND_DURATION)
    
        print "\nSTOP - sending GET request to: " + str(mebo_constants.MEBO_IP_ADDRESSE) + "/ajax/command.json" + mebo_command_stop + "\n"
        conn.request("GET","/ajax/command.json" + mebo_command_stop)
        res = conn.getresponse()
        print(res.status, res.reason)
    except (httplib.HTTPException, socket.error) as ex:
        print "Error: %s" % ex
