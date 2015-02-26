import urllib2
import pafy
from bs4 import BeautifulSoup

def get_video_links(html):
	base_url = "https://www.youtube.com"
	soup = BeautifulSoup(html)
	links = soup.find_all('a')
	videos = []
	for link in links:
		try:
			video = link.get("href")
			if video.index("/watch") == 0:
				new_url = base_url+video[:video.index("&")]
				videos.append(new_url)
		except Exception, e:
			pass
	# remove duplicate video links
	return list(set(videos))

def download(playlist_url,folder_path,file_type):
	# check it the given url is a playlist url or not 
	if playlist_url.find("playlist") != -1:
		print "getting videos from playlist url"
		html = ""
		try:
			html = urllib2.urlopen(playlist_url).read()
		except Exception:
			print "your url is fishy"
			return
		video_urls = get_video_links(html)
		print "there are "+str(len(video_urls))+" videos in the playlist"
		for video_url in video_urls:
			print "doing : "+str(video_url)
			video = pafy.new(video_url)
			print "title of the video is "+str(video.title)
			try:
				best = video.getbest(preftype=file_type)
				filename = best.download(filepath=folder_path,quiet=False)
			except Exception:
				print "please provide value file type"
				return
	else:
		# incase of if the given url is not a playlist url
		try:
			# check if you download video with pafy
			print "it's a normal youtube video"
			video = pafy.new(playlist_url)
			print "title of the video is "+str(video.title)
			best = video.getbest(preftype=file_type)
			filename = best.download(filepath=folder_path,quiet=False)
		except Exception:
			# incase of invalid url or any url other than youtube 
			# this raises an exception
			print "please provide a valid url / path currently you can only download from Youtube"


# input is by system arguments 
# first if the url of the video or the playlist
# second location of the folder to save (make sure it's accessible) /Users/adithya/Desktop
# third is the file type that you want to save available are [mp4 webm flv 3gp], you do research for more with pafy

def main():
	playlist_url = str(raw_input("enter the url of video/playlist to download : "))
	folder_path = str(raw_input("enter the path of folder to save (leave blank for current folder): "))
	file_type = str(raw_input("Enter the file format[mp4 webm flv 3gp] : "))
	download(playlist_url,folder_path,file_type)

main()


