import aiohttp
from re import match

def strToLength(length : str):
	out = 0

	try:
		length = [int(i) for i in length.split(":")]

		out += length[-1]
		out += length[-2] * 60
		out += length[-3] * 3600

	except IndexError:
		pass

	return out

async def youtube_search(keys : str, limit = 10):
	headers = {
		"context": {
			"client": {
				"hl": "en",
				"gl": "PH",
				"clientName": "WEB",
				"clientVersion": "2.20240702.09.00",
			}
		}
	}

	out = []
	outLen = 0

	if match(r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})', keys):
		keys = keys.split("?si=")
		if len(keys) > 1:
			keys = keys[0][-11:]
		else:
			keys = keys[0][-11:]

		headers['query'] = "https://www.youtube.com/watch?v=" + keys
		limit = -1
	else:
		limit = limit if limit != 0 else -1
		headers['query'] = keys
		keys = None

	try:
		async with aiohttp.ClientSession() as client:
			async with client.post("https://www.youtube.com/youtubei/v1/search?prettyPrint=false", json = headers) as res:
				contents = (await res.json())['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

		for i in contents:
			if outLen == limit:
				break

			contentType = list(i.keys())[0]

			if contentType == "videoRenderer":
				try:
					length = strToLength(i[contentType]["lengthText"]['simpleText'])
				except KeyError:
					continue

				key = i[contentType]["videoId"]
				name = i[contentType]["title"]["runs"][0]["text"]
				channel = i[contentType]["ownerText"]["runs"][0]["text"]
				thumb = i[contentType]["thumbnail"]["thumbnails"][-1]["url"]

				if keys:
					if keys != key:
						continue
					else:
						return [(name, channel, key, thumb, length)]
				outLen += 1
				out.append((name, channel, key, thumb, length))

			elif contentType == "shelfRenderer":
				try:
					j = i[contentType]['content']['verticalListRenderer']['items']
				except KeyError:
					continue

				for k in j:
					if outLen == limit:
						break

					contentType = list(k.keys())[0]

					if contentType == "videoRenderer":
						try:
							length = strToLength(k[contentType]["lengthText"]['simpleText'])
						except KeyError:
							continue

						key = k[contentType]["videoId"]
						name = k[contentType]["title"]["runs"][0]["text"]
						channel = k[contentType]["ownerText"]["runs"][0]["text"]
						thumb = k[contentType]["thumbnail"]["thumbnails"][-1]["url"]

						if keys:
							if keys != key:
								continue
							else:
								return [(name, channel, key, thumb, length)]
						outLen += 1
						out.append((name, channel, key, thumb, length))
	except IndexError:
		pass
	except KeyError:
		pass
	except aiohttp.ClientResponseError:
		pass
	
	return out

if __name__ == '__main__':
	import asyncio

	async def main():
		keys=input("search: ")
		outs = await youtube_search(keys)
		for i in outs:
			for j in i:
				print(j)
			print("\n")
		input("END")
	
	asyncio.run(main())