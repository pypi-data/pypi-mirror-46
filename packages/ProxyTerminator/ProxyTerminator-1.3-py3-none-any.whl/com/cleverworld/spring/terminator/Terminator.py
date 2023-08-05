#encoding: utf-8

from com.cleverworld.spring.terminator.CommandExecutor import *
from com.cleverworld.spring.terminator.BusinessConnector import *
from com.cleverworld.spring.terminator.Utils import *

def main():
    # 1、read configuration
    utils = Utils()

    utils.info("main", "starting CommandExecutor...")
    # 2.start all real transmit service that previewsly specified in configuration file
    commandExecutor = CommandExecutor(utils)
    commandExecutor.daemon = True
    commandExecutor.start()

    commandExecutor.join()

    utils.info("main", "exit.")


'''
    p_list=[]
    for i in range(3):
        p = MyProcess()
        p.start()
        p_list.append(p)
    for p in p_list:
        p.join()
    print('end')
'''

if __name__ == '__main__':
    main()