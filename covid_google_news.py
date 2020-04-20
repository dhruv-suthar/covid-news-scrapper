import requests
from bs4 import BeautifulSoup
import json
import csv
import itertools


headers = {
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
		}


url = requests.get("https://news.google.com/search?q=COVID-19%20INDIA&hl=en-IN&gl=IN&ceid=IN%3Aen",headers=headers)

soup = BeautifulSoup(url.content,'html.parser')

get_news_data = soup.select('main.HKt8rc.CGNRMc > c-wiz > div > div > div > article ')
get_news_img =  soup.select('main.HKt8rc.CGNRMc > c-wiz > div > div ')

outfile = open('covid_news.csv','w', newline='')
writer = csv.writer(outfile)
writer.writerow(["Title", "Url","Image Url","Description","Time"])

news_data_ls = []

for (get_news_data,get_news_img) in itertools.zip_longest(get_news_data,get_news_img):
	if get_news_data is not None and get_news_img is not None:

		news_title = get_news_data.select('h3 > a')[0].text
		news_url = "https://news.google.com" + get_news_data.select('h3 > a')[0]['href'][1:len(str(get_news_data.select('h3 > a')[0]['href']))]
		if get_news_img.select_one('a > figure > img') is not None:
			news_image = get_news_img.select_one('a > figure > img')['src']
		else:
			news_image = 'None'
		news_desc = get_news_data.select('div.Da10Tb.gEABFF.Rai5ob > span')[0].text	
		time = get_news_data.select('div.QmrVtf.RD0gLb > div > time')[0]['datetime'].replace("T", "")
		time = time.replace("Z", "")

		# time_hr = get_news_data.select('div.QmrVtf.RD0gLb > div > time')[0].text
		info = {
				 "Title": 		str(news_title),
				 "Url" : 		str(news_url),
				 "Image Url": 	str(news_image),
				 "Description": str(news_desc),
				 "Time":		str(time),
				 # "TimeHr":		str(time_hr)

			   }
		news_data_ls.append(info)	   

		
		writer.writerow([news_title, news_url,news_image,news_desc,time])

	
	
outfile.close()

data = {}
data['COVID NEWS DATA'] = news_data_ls
with open('covid_news.json', 'w') as outfile:
	json.dump(data, outfile,indent=4)	
