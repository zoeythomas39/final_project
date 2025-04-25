
# loading our imports

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import csv
import time
import os

# making soup

url = 'https://genius.com/artists/Elliott-smith/albums'
hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
page=requests.get(url,headers=hdr)
soup=BeautifulSoup(page.text,'html.parser')

# finding links to album titles

albums = soup.find_all("a")

album_list = [] # creating blank list to put album links

for album in albums:
    album_list.append(album.get('href')) # filling the list with the links

album_list = album_list[13:33] # trimming the list to only the album links

# there are extra albums that don't get included b/c you have to scroll. adding them here:

album_list.append("https://genius.com/albums/Elliott-smith/Elliott-smith")
album_list.append("https://genius.com/albums/Elliott-smith/Needle-in-the-hay-ep")
album_list.append("https://genius.com/albums/Elliott-smith/Roman-candle")

album_list.reverse() # we want the albums in order of release

song_list = [] # blank list for song links

# function to get song links

def get_song(album_url):
    page=requests.get(album_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    songs = soup.find_all("a")
    for song in songs:
        song_list_item = song.get('href')
        # getting rid of demos, live recordings, etc:
        if "lyrics" in song_list_item and "Elliott-smith" in song_list_item and "-version-" not in song_list_item and "-cover-" not in song_list_item and "-instrumental-" not in song_list_item and "-live-" not in song_list_item and "-alt-" not in song_list_item and "-demo-" not in song_list_item and "remastered" not in song_list_item: # getting rid of misc links
            if song_list_item not in song_list: # no duplicates here!
                song_list.append(song.get('href'))

for album_item in album_list: # calling function
    get_song(album_item)

# function to get song infos

filename = "final_project_data.csv"
myfile=open(filename,'a')
elliott_writer = csv.writer(myfile)

def get_titles(song_url):
    page = requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    title = soup.find("h1").text
    return(title)

def get_album(song_url):
    page = requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    all_album_links = soup.find_all("a")
    for iteration in all_album_links:
        if iteration.get('href') == "#primary-album":
            album_title = iteration.text
    return(album_title)

def get_date(song_url):
    page = requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    date_list = soup.find_all("span",class_="gwsJVO")
    if len(date_list) == 3:
        for item in date_list:
            if "view" not in item.text:
                date = item.text
                return(date)
    elif len(date_list) == 2:
        for item in date_list:
            if "view" not in item.text:
                date = item.text
                return(date)
    elif len(date_list) == 1:
        for item in date_list:
            if "view" in item.text:
                date = "No date available"
                return(date)
            elif "view" not in item.text:
                date = item.text
                return(date)

def get_lyrics(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        delimiter = '\n'
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        for br_tag in lyric.find_all("br"):
            br_tag.replace_with(delimiter)
        lyrics_text = lyric.text
        return(lyrics_text)


def get_themes_love(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for love theme
        if "love" in lyrics_text:
            love = 1
        elif "heart" in lyrics_text:
            love = 1
        elif "loving" in lyrics_text:
            love = 1
        else:
            love = 0
        return(love)

def get_themes_alcohol(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for alcohol theme
        if "alcohol" in lyrics_text:
            alcohol = 1
        elif "beer" in lyrics_text:
            alcohol = 1
        elif "drunk" in lyrics_text:
            alcohol = 1
        else:
            alcohol = 0
        return(alcohol)

def get_themes_lonely(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for loneliness theme
        if "loneliness" in lyrics_text:
            lonely = 1
        elif "lonely" in lyrics_text:
            lonely = 1
        elif "alone" in lyrics_text:
            lonely = 1
        elif "invisible" in lyrics_text:
            lonely = 1
        elif "isolat" in lyrics_text:
            lonely = 1
        else:
            lonely = 0
        return(lonely)

def get_themes_smoke(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for smoking theme
        if "smoke" in lyrics_text:
            smoke = 1
        elif "smoking" in lyrics_text:
            smoke = 1
        elif "cigarette" in lyrics_text:
            smoke = 1
        else:
            smoke = 0
        return(smoke)

def get_themes_dream(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for dream theme
        if "dream" in lyrics_text:
            dream = 1
        else:
            dream = 0
        return(dream)

def get_themes_astronomy(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for astronomy theme
        if "moon" in lyrics_text:
            astronomy = 1
        elif "sun" in lyrics_text:
            astronomy = 1
        elif "star" in lyrics_text:
            astronomy = 1
        else:
            astronomy = 0
        return(astronomy)

def get_themes_lie(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for lie theme
        if "lie" in lyrics_text:
            lie = 1
        elif "lying" in lyrics_text:
            lie = 1
        elif "fake" in lyrics_text:
            lie = 1
        elif "false" in lyrics_text:
            lie = 1
        else:
            lie = 0
        return(lie)

def get_themes_life(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for life theme
        if "life" in lyrics_text:
            life = 1
        elif "living" in lyrics_text:
            life = 1
        elif "alive" in lyrics_text:
            life = 1
        else:
            life = 0
        return(life)

def get_themes_death(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for death theme
        if "death" in lyrics_text:
            death = 1
        elif "die" in lyrics_text:
            death = 1
        elif "dying" in lyrics_text:
            death = 1
        elif "kill" in lyrics_text:
            death = 1
        elif "dead" in lyrics_text:
            death = 1
        elif "grave" in lyrics_text:
            death = 1
        elif "ghost" in lyrics_text:
            death = 1
        elif "murder" in lyrics_text:
            death = 1
        elif "suicide" in lyrics_text:
            death = 1
        else:
            death = 0
        return(death)
    
def get_themes_sick(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for sick theme
        if "sick" in lyrics_text:
            sick = 1
        else:
            sick = 0
        return(sick)
    
def get_themes_city(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for city theme
        if "city" in lyrics_text:
            city = 1
        else:
            city = 0
        return(city)

def get_themes_home(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for home theme
        if "home" in lyrics_text:
            home = 1
        else:
            home = 0
        return(home)

def get_themes_time(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for time theme
        if "time" in lyrics_text:
            time = 1
        elif "clock" in lyrics_text:
            time = 1
        else:
            time = 0
        return(time)

def get_themes_lost(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for lost theme
        if "lost" in lyrics_text:
            lost = 1
        elif "missing" in lyrics_text:
            lost = 1
        else:
            lost = 0
        return(lost)

def get_themes_money(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for money theme
        if "money" in lyrics_text:
            money = 1
        elif "cash" in lyrics_text:
            money = 1
        elif "coin" in lyrics_text:
            money = 1
        elif "dollar" in lyrics_text:
            money = 1
        else:
            money = 0
        return(money)

def get_themes_nothing(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for nothing theme
        if "nothing" in lyrics_text:
            nothing = 1
        elif "nobody" in lyrics_text:
            nothing = 1
        elif "no one" in lyrics_text:
            nothing = 1
        else:
            nothing = 0
        return(nothing)

def get_themes_dance(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for dance theme
        if "dance" in lyrics_text:
            dance = 1
        elif "dancing" in lyrics_text:
            dance = 1
        else:
            dance = 0
        return(dance)

def get_themes_memory(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for memory theme
        if "memory" in lyrics_text:
            memory = 1
        elif "remember" in lyrics_text:
            memory = 1
        else:
            memory = 0
        return(memory)

def get_themes_water(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for water theme
        if "water" in lyrics_text:
            water = 1
        elif "ocean" in lyrics_text:
            water = 1
        elif "river" in lyrics_text:
            water = 1
        elif "lake" in lyrics_text:
            water = 1
        else:
            water = 0
        return(water)

def get_themes_friend(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for friend theme
        if "friend" in lyrics_text:
            friend = 1
        else:
            friend = 0
        return(friend)

def get_themes_pain(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for pain theme
        if "pain" in lyrics_text:
            pain = 1
        elif "hurt" in lyrics_text:
            pain = 1
        else:
            pain = 0
        return(pain)

def get_themes_wait(song_url):
    page=requests.get(song_url,headers=hdr)
    soup=BeautifulSoup(page.text,'html.parser')
    lyrics = soup.find_all(class_="Lyrics__Container-sc-78fb6627-1")
    for lyric in lyrics:
        if "Lyrics" in lyric.text:
            lyric.find('div', class_="LyricsHeader__Container-sc-3eaf69e8-1 hvOEKL").decompose()
        lyrics_text = lyric.text.lower()
        # check for wait theme
        if "wait" in lyrics_text:
            wait = 1
        else:
            wait = 0
        return(wait)

for i in range(len(song_list)):
    title = get_titles(song_list[i])
    album = get_album(song_list[i])
    date = get_date(song_list[i])
    lyrics = get_lyrics(song_list[i])
    love = get_themes_love(song_list[i])
    alcohol = get_themes_alcohol(song_list[i])
    lonely = get_themes_lonely(song_list[i])
    smoke = get_themes_smoke(song_list[i])
    dream = get_themes_dream(song_list[i])
    moon = get_themes_astronomy(song_list[i])
    lie = get_themes_lie(song_list[i])
    life = get_themes_life(song_list[i])
    death = get_themes_death(song_list[i])
    sick = get_themes_sick(song_list[i])
    city = get_themes_city(song_list[i])
    home = get_themes_home(song_list[i])
    time = get_themes_time(song_list[i])
    lost = get_themes_lost(song_list[i])
    money = get_themes_money(song_list[i])
    nothing = get_themes_nothing(song_list[i])
    dance = get_themes_dance(song_list[i])
    memory = get_themes_memory(song_list[i])
    water = get_themes_water(song_list[i])
    friend = get_themes_friend(song_list[i])
    pain = get_themes_pain(song_list[i])
    wait = get_themes_wait(song_list[i])
    song_url = song_list[i]

    with open(filename, 'a', newline='') as myfile:
        elliott_writer = csv.writer(myfile)

        # Write the header only if the file is empty
        if os.path.getsize(filename) == 0:
            elliott_writer.writerow(['Song', 'Album', 'Date', 'Lyrics', 'Love','Alcohol','Lonely','Smoke','Dream','Moon', 'Lie', 'Life',"Death", 'Sick', 'City', 'Home', 'Time', 'Lost',
            "Money","Nothing","Dance","Memory","Water","Friend","Pain","Wait",'Link',])

        elliott_writer.writerow(list((title,album,date,lyrics,love,alcohol,lonely,smoke,dream,moon, lie, life,death, sick, city, home, time, lost,money, nothing, dance, memory,water,friend,pain,wait,song_url)))
    print(f"Processing song {i +1} out of {len(song_list)}: {title}")

myfile.close()