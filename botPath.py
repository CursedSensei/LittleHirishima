import os, sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ERRORPATH = os.path.join(ROOT_DIR,'Little Hirishima Crash Report.txt')
WORKERERRORPATH = os.path.join(ROOT_DIR,'Little Hirishima Worker Crash Report.txt')
TOKENPATH = os.path.join(ROOT_DIR,'Little_Hirishima Secrets.json')

GUILDPATH = os.path.join(ROOT_DIR, 'lib', 'Guild')
LIBRARYPATH = os.path.join(ROOT_DIR, 'lib', 'Song_Library')
LIBRARYLOG = os.path.join(LIBRARYPATH, 'library.json')

ANIMEDIRECTORY = "/var/www/html/Anime"
ANIMEDOWNLOADER = os.path.join(ROOT_DIR, 'lib/urldown.py')
CHATLOG = os.path.join(ROOT_DIR, 'Chat log.txt')

REQUESTSDIRECTORY = os.path.join(ROOT_DIR, 'webLink', 'requests')
PIPESDIRECTORY = os.path.join(ROOT_DIR, 'webLink', 'pipes')


if not os.path.join(ROOT_DIR, "lib", "lib") in sys.path:
    sys.path.append(os.path.join(ROOT_DIR, "lib", "lib"))
