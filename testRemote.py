import sys

from tests import run as runTest

if __name__ == '__main__':
    runTest(sys.argv[-1] + ':50051')
    print('pass')
