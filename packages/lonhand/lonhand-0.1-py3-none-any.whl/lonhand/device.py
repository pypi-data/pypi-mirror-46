import socket
import binascii

# USR-WP1 smart socket
# https://www.usriot.com/download/LonHand/USR-WP1%20EN%20V1.3.1.pdf

# 55 AA - distinguishes a command, unlike for example the password which
#         should be sent as is (with suffix 0D 0A)
# 00 03 - represents the length in bytes of the command (real) that follows,
#         including the byte 00 (see below)
# 00    - fixed, reserved and not usable. However, it contributes to forming 
#         the length in bytes of the command, for example in case of a device
#         renaming command (which will contain the new name assigned): the
#         length byte (and the checksum) will be recalculated also according
#         to the length of the new name
# 02    - the actual command (ON)
# 01    - command parameter; in this case we are giving the ON command (02)
#         and as a parameter the channel number to be switched on (01).
# 06    - checksum, and represents the sum (in HEX) of the parts: 
#         (0x00 + 0x03 + 0x00 + 0x02 + 0x01) = 0x06
COMMAND_TURN_ON  = binascii.a2b_hex("55 AA 00 03 00 02 01 06".replace(" ", ""))
COMMAND_TURN_OFF = binascii.a2b_hex("55 AA 00 03 00 01 01 05".replace(" ", ""))
COMMAND_TOGGLE   = binascii.a2b_hex("55 AA 00 03 00 06 00 09".replace(" ", ""))
COMMAND_STATE    = binascii.a2b_hex("55 AA 00 03 00 0A 00 0D".replace(" ", ""))

# AA 55 - marks the message as a response
# 00 04 - response length
# 00    - reserved
# 82 01 - is the confirmation response to the ON command
# 01    - channel/port that was affected
# 88    - checksum: (0x00 + 0x04 + 0x00 + 0x82 + 0x01 + 0x01) = 0x88
RESPONSE_TURN_ON   = binascii.a2b_hex("AA 55 00 04 00 82 01 01 88".replace(" ", ""))
RESPONSE_TURN_OFF  = binascii.a2b_hex("AA 55 00 04 00 81 01 00 86".replace(" ", ""))
RESPONSE_STATE_ON  = binascii.a2b_hex("AA 55 00 03 00 8A 01 8E".replace(" ", ""))
RESPONSE_STATE_OFF = binascii.a2b_hex("AA 55 00 03 00 8A 00 8D".replace(" ", ""))

class WifiRelay(object):

    def __init__(self, tcp_ip='192.168.1.23', tcp_port=8899, pwd="admin"):
        self._ip = tcp_ip
        self._port = tcp_port
        self._password = pwd
        # get current state
        self.is_on()

    def is_on(self):
        self.control(COMMAND_STATE)
        return self._state

    def turn_on(self):
        self.control(COMMAND_ON)

    def turn_off(self):
        self.control(COMMAND_OFF)

    def toggle(self):
        if (self._state):
            self.turn_off()
        else:
            self.turn_on()

    def control(self, cmd):
        BUFFER_SIZE = 2048
        # create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        # send password, response is either "OK" or "NO"
        s.send(self._password + "\r\n")
        auth = s.recv(BUFFER_SIZE)
        # send actual command
        s.send(cmd)
        resp = s.recv(BUFFER_SIZE)
        # close socket
        s.close()
        # on success check penultimate byte for state
        if (auth == "OK") and (len(resp) > 1):
            self._state = (resp[len(resp)-2] == 0x01)

