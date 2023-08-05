#encoding: utf-8
#此类用于连接受控端业务服务和Transmitor，进行业务数据转发操作

#encoding: utf-8
#此类用于向Transmitor进行注册，并执行来自Transmitor的指令
# coding=utf-8
#this class is used to combine terminal and remote client

import select

from com.cleverworld.spring.terminator import Utils
from threading import *
from queue import Queue


class BusinessConnector(Thread):
    '''
    store paired client and terminal side socket with paired Sequence id as key
    for example: {"101" : {clientSocket, terminalSocket}}
    '''

    '''
    1、start listening
    '''

    def __init__(self, clientSequence, toTerminalSocket, toCSCLSocket, utils):
        super(BusinessConnector, self).__init__(name = "BusinessConnector: %s]"%clientSequence)
        # multiprocessing.Process.__init__(self)
        self.utils = utils
        self.utils.info("BusinessConnector", "Channel %s is created."%clientSequence)
        self.clientSequence = clientSequence

        self.inputs = []
        self.outputs = []
        self.messageQueues = {}
        self.isFirstMsg = True

        if toTerminalSocket != None:
            self.inputs.append(toTerminalSocket)
        if toCSCLSocket != None:
            self.inputs.append(toCSCLSocket)

        self.toTerminalSocket = toTerminalSocket
        self.toCSCLSocket = toCSCLSocket

        self.messageQueues[toTerminalSocket.fileno()] = Queue()
        self.messageQueues[toCSCLSocket.fileno()] = Queue()


    def run(self):
        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            except Exception as e:
                self.utils.printExceptMsg("BusinessConnector::run", "select.select error:, ", e)
                break
            for sock in readable:
                try:
                    data = sock.recv(1024)
                    if len(data) == 0:
                        if self.isFirstMsg:
                            self.isFirstMsg = False
                            continue
                        self.closeSock("recv data length is zero")
                        return
                except Exception as err:
                    self.closeSock(self.utils.getExceptMsg(err))
                    return

                if sock.fileno() == self.toTerminalSocket.fileno():
                    destSock = self.toCSCLSocket
                else:
                    destSock = self.toTerminalSocket

                self.messageQueues[destSock.fileno()].put(data)
                if destSock not in self.outputs:
                    self.outputs.append(destSock)

            for sock in writable:
                messageQueue = self.messageQueues.get(sock.fileno())
                if messageQueue is not None and not messageQueue.empty():
                    data = messageQueue.get_nowait()
                    sock.sendall(data)
                    if messageQueue.empty():
                        try:
                            index = self.outputs.index(sock)
                            self.outputs.remove(sock)
                        except Exception as e:
                            pass


    def closeSock(self, extraMsg):
        '''
        :param sock: socket to close
        :param queue: message queue of the socket
        :param inputs: inputs set
        :param outputs: outputs set
        :return: null
        '''
        try:
            self.toTerminalSocket.close()
        except Exception as e:
            pass
        try:
            self.toCSCLSocket.close()
        except Exception as e:
            pass

        self.utils.debug("BusinessConnection", "Channel %s has Closed, %s"%(self.clientSequence, extraMsg))
