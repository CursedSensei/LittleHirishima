import os, sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORPATH = os.path.join(ROOT_DIR,'Little Hirishima Crash Report.txt')
TOKENPATH = os.path.join(ROOT_DIR,'Little_Hirishima Secrets.json')

sys.path.append(os.path.join(ROOT_DIR,'lib/lib'))