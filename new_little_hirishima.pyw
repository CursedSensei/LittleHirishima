import os,random,time,threading,subprocess,asyncio,sys,json,shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(ROOT_DIR,'lib/lib'))
import discord, mutagen
from discord.ext import commands
from aiohttp.client_exceptions import ClientConnectorError

