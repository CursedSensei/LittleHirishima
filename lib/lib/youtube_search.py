import json
from requests import post

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

def youtube_search(keys, limit = 10):
	headers = {
		"context": {
			"client": {
				"hl": "en",
				"gl": "PH",
				"clientName": "WEB",
				"clientVersion": "2.20240702.09.00",
			}
		},
		"query": keys
	}

	res = post("https://www.youtube.com/youtubei/v1/search?prettyPrint=false", json = headers)

	out = []
	outLen = 0

	try:
		contents = json.loads(res.content.decode())['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

		for i in contents:
			if outLen == limit:
				break

			contentType = list(i.keys())[0]

			if contentType == "videoRenderer":
				key = i[contentType]["videoId"]
				name = i[contentType]["title"]["runs"][0]["text"]
				channel = i[contentType]["ownerText"]["runs"][0]["text"]
				thumb = i[contentType]["thumbnail"]["thumbnails"][-1]["url"]
				length = strToLength(i[contentType]["lengthText"]['simpleText'])

				outLen += 1
				out.append((name, channel, key, thumb, length))

			elif contentType == "shelfRenderer":
				j = i[contentType]['content']['verticalListRenderer']['items']

				for k in j:
					if outLen == limit:
						break

					contentType = list(k.keys())[0]

					if contentType == "videoRenderer":
						key = k[contentType]["videoId"]
						name = k[contentType]["title"]["runs"][0]["text"]
						channel = k[contentType]["ownerText"]["runs"][0]["text"]
						thumb = k[contentType]["thumbnail"]["thumbnails"][-1]["url"]
						length = strToLength(k[contentType]["lengthText"]['simpleText'])

						outLen += 1
						out.append((name, channel, key, thumb, length))
	except IndexError:
		pass
	except KeyError:
		pass

	return out

if __name__ == '__main__':
	keys=input("search: ")
	outs = youtube_search(keys)
	for i in outs:
		for j in i:
			print(j)
		print("\n")
	input("END")