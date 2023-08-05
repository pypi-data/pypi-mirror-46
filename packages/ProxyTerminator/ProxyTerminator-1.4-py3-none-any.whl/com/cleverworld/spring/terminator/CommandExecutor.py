#encoding: utf-8
#此类用于向Transmitor进行注册，并执行来自Transmitor的指令
# coding=utf-8
#this class is used to combine terminal and remote client

import socket
import time
import subprocess

import threading

from com.cleverworld.spring.terminator.BusinessConnector import *
from com.cleverworld.spring.terminator import Utils
from multiprocessing import Process, Lock


class CommandExecutor(Process):
    '''
    store paired client and terminal side socket with paired Sequence id as key
    for example: {"101" : {clientSocket, terminalSocket}}
    '''
    pairedBusiness = {};

    terminatorId = -1

    transmitorIpAddr = ""

    transmitorPort = -1

    ''
    isRunning = True

    'listening business port'
    listeningPort = {}

    clientSequence = 100
    sequenceLock = Lock()


    '''
    1、start listening
    '''

    def __init__(self, utils):
        super(CommandExecutor, self).__init__()
        # multiprocessing.Process.__init__(self)

        self.utils = utils

        self.utils.info("CommandExecutor", "init")

        self.terminatorId = self.utils.get("terminator")["terminatorId"]
        self.toTerminalPort = self.utils.get("terminator")["toTerminalPort"]

        self.transmitorIpAddr = self.utils.get("transmitor")["ipAddr"]
        self.transmitorPort = self.utils.get("transmitor")["port"]

        self.utils.info("CommandExecutor", "terminalId: %d, transmitorIpAddr: %s, transmitorPort: %d" % (self.terminatorId, self.transmitorIpAddr, self.transmitorPort))

    def run(self):
        cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cmdSocket.connect((self.transmitorIpAddr, self.transmitorPort))
            cmdSocket.sendall(("Terminator:%d"%self.terminatorId).encode())
        except Exception as e:
            self.utils.printExceptMsg("CommandExecutor", "connect to the transmitor %s, %d has encounted an error, "%(self.transmitorIpAddr, self.transmitorPort), e)
            self.retry()
            return

        self.utils.info("CommandExecutor", "connected to the transmitor")

        while(self.isRunning):
            try:
                data = cmdSocket.recv(1024)
            except Exception as e:
                self.utils.printExceptMsg("CommandExecutor", "connection to the transmitor has encounted an exception, ", e)
                self.retry()
                return

            if len(data) == 0:
                self.utils.error("CommandExecutor", "connection to the transmitor has encounted an error, data len is 0")
                self.retry()
                return

            data = data.decode()
            try:
                cmdData = data.split(";")
            except Exception as e:
                self.utils.printExceptMsg("CommandExecutor", "data.split error, data:%s" % data, e)
                continue

            for data in cmdData:
                if data != "":
                    self.procCmdFromTransmitor(cmdSocket, data)

    def procCmdFromTransmitor(self, cmdSocket, data):

        self.utils.debug("CommandExecutor", "received a new command from the transmitor, %s" % data)
        try:
            cmd, service = data.split(":")
        except Exception as e:
            self.utils.printExceptMsg("CommandExecutor", "data.split error, data:%s" % data, e)
            return
        if cmd == "FromCSCL":
            #                clientSequence, terminalAddr, terminalPort, businessListenerPort = service.split(",")
            #                 cmdSocket.sendall(b"OK")
            thread = threading.Thread(target = self.startBusiness, args = (service,), name = "startBusiness:%s"%service)
            thread.start()
        elif cmd == "FromCC":
            try:
                cmd = service.split(" ")
                output = subprocess.check_output(service)
                output = output.decode("utf-8", "ignore")
                cmdSocket.sendall(("FromTerminal:%s" % output).encode())
            except Exception as e:
                msg = self.getExceptMsg(e)
                cmdSocket.sendall(("FromTerminal:%s" % msg).encode())
                self.utils.error("CommandExecutor", "execute cmd \"%s\" error, description:%s" % (cmd, msg))

    def getExceptMsg(self, e):
        if hasattr(e, "strerror"):
            return e.strerror
        elif hasattr(e, "reason"):
            return e.reason

    def retry(self):
        self.utils.info("CommandExecutor", "begin reconnect to the remote server...")
        time.sleep(6)
        self.run()

    def closeSock(self, sock):
        '''
        :param sock: socket to close
        :param queue: message queue of the socket
        :param inputs: inputs set
        :param outputs: outputs set
        :return: null
        '''
        if sock == None:
            return
        sock.close()

    def startBusiness(self, service):
        '''
        :start processing two way connect
        '''
        clientSequence, terminalAddr, terminalPort, businessListenerPort = service.split(",")

        # 1、connect to the terminal
        toTerminalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            toTerminalSocket.settimeout(15)
            toTerminalSocket.connect((terminalAddr, int(terminalPort)))
            toTerminalSocket.setblocking(False)
        except Exception as e:
            self.utils.printExceptMsg("startBusiness", "connect to terminator error, addr:%s, port: %s, "%(terminalAddr, terminalPort), e)
            toTerminalSocket = None

        # 2、after connect to terminal success, then connect to the transmitor cscl service
        try:
            toCSCLSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            toCSCLSocket.settimeout(15)
            toCSCLSocket.connect((self.transmitorIpAddr, self.toTerminalPort))
            toCSCLSocket.setblocking(False)
        except Exception as e:
            self.utils.printExceptMsg("startBusiness", "connect to transmitor error, addr:%s, port: %d, "%(self.transmitorIpAddr, self.toTerminalPort), e)
            self.closeSock(toTerminalSocket)
            return

        if toTerminalSocket == None:
            self.closeSock(toCSCLSocket)
            return

        self.utils.debug("CommandExecutor::startBusiness", "connect both terminal and client success, service %s, begin create tunnel"%service)
        # 2.1 send flag information
        toCSCLSocket.sendall(("FromTerminal:" + clientSequence).encode())

        # 3、combine the to socket to one pair
        self.pairedBusiness[clientSequence] = (toTerminalSocket, toCSCLSocket)

        # 4、start transmission
        # ...
        businessConnector = BusinessConnector(clientSequence, toTerminalSocket, toCSCLSocket, self.utils)
        businessConnector.start()
