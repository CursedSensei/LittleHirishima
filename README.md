# OLD README MAY CONTAIN UNDESCRIBABLE BULL$%@^ 
# Little-Hirishima-Pycord

My Python Discord Bot

# Extras

lib/lib/youtube_search.py
  - Simple api that searches and extract the following: ```Title```, ```Channel```, ```ID```

lib/urldown.py
  - Used to download anime episodes automatically if given the link of the episode in gogoanime

# Note

Following changes that should be done before running it yourself:

<br>

**Dependencies:**

* Refer to the first line of the code and Line 64 (Im lazy ik)
  
* Yt-dlp is used to download youtube audio (```pip install yt-dlp```)

* FFmpeg for audio streaming
  
#

**Changing Directories:**

  - Anime Download Location - variable name: ```bufferdirectory```

  
  (The following changes can be found in ```music.play``` function... just find a long ass directory)
  
  - FFmpeg Location
  
  - Music Library Location - also found in ```music.__init__``` function
  
  - Youtube Cache Location - also found in ```music.cleanup``` function

#

**Changing Discord Token in ```Little_Hirishima Secrets.json```** file
  
