from requests import get

def youtube_search(keys):
	keys = "+".join(keys.split(" "))

	x= get("https://www.youtube.com/results?search_query={}".format(keys))
	for i in x.content.decode().split("\n"):
		if '"}],"accessibility":{"accessibilityData":{"label":"'in i:
			buffed=i.split('"}],"accessibility":{"accessibilityData":{"label":"')

	out = []

	for order in range(1, 11):
		try:
			name = buffed[order - 1].split('}]},"title":{"runs":[{"text":"')[-1]
			channel = buffed[order].split('"}}},"longBylineText":{"runs":[{"text":"')[1].split('","navigationEndpoint":')[0]
			key = buffed[order].split(',"watchEndpoint":{"videoId":"')[1][:11]
		except IndexError:
			break
		out.append((name, channel, key))
	return out

if __name__ == '__main__':
	keys=input("search: ")
	outs = youtube_search(keys)
	for i in outs:
		print(i[0])
		print(i[1])
		print(i[2] + "\n")
	input("END")