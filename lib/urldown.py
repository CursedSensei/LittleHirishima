import sys,threading,time,os,shutil
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import requests

class download_file:
	def __init__(self, url, path):
		fd = os.path.join(path, url.split("/")[-1] + ".mp4")
		rawfd = os.path.join(path, "Data_Fragment.bin")
		if os.path.exists(fd):
			return
		if os.path.exists(rawfd):
			os.remove(rawfd)
		data = requests.get(self.get_link(url), stream=True)
		with open(rawfd, "wb") as f:
			for chunk in data.iter_content(32768):
				f.write(chunk)
		os.rename(rawfd, fd)

	def get_link(self, url):
		jar = requests.cookies.RequestsCookieJar()
		jar.set('auth', '4mGRLICwi0PoZEQvhOb7Qbl1BTFu6Ibbb8sRh2ryYLWYWrqae%2Fcba0MzhSA7zyuxagc%2Bz9BZs2hi5LbgQuxIVA%3D%3D', domain=url.split("/")[2], path=r'/')
		link = requests.get(url, cookies=jar)
		ohlink = False
		links = []
		for i in link.content.split(b"\n"):
			if ohlink:
				if b"</div>" in i:
					break
				links.append(i.decode())
			else:
				if b'<div class="cf-download">' in i:
					ohlink = True
		return links[-2].split("href=\"")[1][:-2]

def crash_reporter():
	import traceback
	with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "auto download crash.txt"), "w") as f:
		f.write(traceback.format_exc())

URL = sys.argv[1]
path = os.path.join("D:\\Movies\\Anime Buffered Space", "-".join(URL.split("/")[-1].split("-")[:-2]))
if not os.path.exists(path):
	os.makedirs(path)

timeout = 0
while True:
	try:
		download_file(URL, path)
		status = True
		link = URL.split("-")
		link[-1] = str(int(link[-1]) + 1)
		URL = "-".join(link)
	except IndexError:
		break
	except requests.exceptions.ConnectionError:
		if status:
			link = URL.split("-")
			link[-1] = str(int(link[-1]) - 1)
			URL = "-".join(link)
			fd = os.path.join(path, URL.split("/")[-1] + ".mp4")
			status = False
		if os.path.exists(fd):
			os.remove(fd)
		if timeout == 10:
			crash_reporter()
			break
		else:
			timeout += 1
			time.sleep(10)
	except:
		crash_reporter()
		break