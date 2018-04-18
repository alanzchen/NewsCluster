from multiprocessing import Process

from app import serve
from models import clear_all_data, create_all
from tests import run as runTest

import time
import sys

if __name__ == '__main__':
    create_all()
    clear_all_data()
    print("RPC tests running...")
    mainProcess = Process(target=serve)
    clientProcess = Process(target=runTest, args=('localhost:50051',))
    print("Running service...")
    mainProcess.start()
    time.sleep(1) # +1s
    print("Running client...")
    clientProcess.start()
    clientProcess.join()
    mainProcess.terminate()
    sys.exit(clientProcess.exitcode)
