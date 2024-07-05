import os
import sys
import paramiko

class SynchronizeDB:
    def __init__(self, parent):
        self._parent = parent
        self._hostName = 'xxx.xx.xx.xxx' #Whatever the IP address is, that is written to the device.
        self._port = 22
        self._userName = None
        self._password = None
        self._SSH_Client = paramiko.SSHClient()
        self.dev_id = "14587-48771-85617-862318765" #If there is a special device id, it is taken from db or wherever it is written.

    def check_hotspot(self):
        command = "nmcli dev wifi list"
        output = os.popen(command).read()
        lines = output.split('\n')

        priv_networks = [line for line in lines if 'priv_' in line]

        if priv_networks:
            for network in priv_networks:
                print(network)
        else:
            self.create_hotspot()

    def create_hotspot(self):
        ssid = "priv_" + self.dev_id[-8:]  # The name that will appear on the wifii list is created from the device id.
        passphrase = self.dev_id[-26:-8]  # the password of the created hotspot or wifii network
        exit_code = os.system(f"sudo nmcli dev wifi hotspot ifname wlan ssid {ssid} password {passphrase}")
        if exit_code == 0:
            print(f"Hotspot succesfully created")
        else:
            print(f"Hotspot creation failed")


    def connect_hotspot(self):
        try:
            dev_username = "priv_" + self.dev_id[-8:]
            dev_password = self.dev_id[-26:-8]
            self._password = dev_password

            exit_code = os.system(f"nmcli dev wifi connect {dev_username} password {dev_password}")
            if exit_code == 0:
                print(f"Connection succesfully established")
            else:
                print(f"Connection failed")

        except Exception as e:
            print("hotspot connection fault: ", e)
            return None


    def disable_hotspot(self):
        dev_username = "priv_" + self.dev_id[-8:]
        exit_code = os.system(f"nmcli connection down {dev_username}")
        if exit_code == 0:
            print(f"Hotspot successfully disabled: {dev_username}")
        else:
            print(f"Error disabling hotspot: {dev_username}")