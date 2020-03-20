import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import math
import numpy as np
from collections import Counter
import operator
from itertools import islice
pages=[]
names=[]
votes=[]
ratings=[]
years=[]
durations=[]
meta_scores=[]
Metascores=[]
genres=[]
Metaratings=[]
for i in range(1,1001,50):
	url="https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31&sort=num_votes,desc&start={}&ref_=adv_nxt".format(i)
	pages.append(url)
for item in pages:
	responses=requests.get(item)
	html_soup=BeautifulSoup(responses.text,'html.parser')
	movie_container= html_soup.find_all('div', class_ = 'lister-item mode-advanced')
	for container in movie_container:
	#names
		name=container.h3.a.text
		names.append(name)
	#ratings
		rating=float(container.strong.text)
		ratings.append(rating)
	#metascore
		meta_score=container.find('span', class_ = 'metascore')
		if container.find('div',class_='ratings-metascore') is None:
			meta_score="-"
			meta_scores.append(meta_score)
		else:
			meta_score=int(meta_score.text)
			meta_scores.append(meta_score)
			Metascores.append(meta_score)
	#ratings of movie which contains metascore values
			Metarating=float(container.strong.text)
			Metaratings.append(Metarating)
	#votes of movies
		vote=container.find('span',attrs={'name':'nv'})
		vote=int(vote['data-value'])
		votes.append(vote)
	#duration of movies
		duration=container.find('span',class_='runtime')
		if container.find('span',class_='runtime')is None:
			duration=int(-1)
			durations.append(int(duration))
		else:
			duration=(duration.text)
			duration=duration.strip("min")
			durations.append(int(duration))
	#jonar of movie
		genre=container.find('span',class_='genre').text
		genre=genre.strip()
		genre=genre.split(',')
		genres.extend(genre)
		
#header of the data
border="+{:^4}-{:^70}-{:^8}-{:^8}-{:^10}-{:^8}-{:^12}+".format("-"*4,"-"*70,"-"*8,"-"*8,"-"*10,"-"*8,"-"*12)
print(border)
data_header="|{:^4}|{:^70}|{:^8}|{:^8}|{:^10}|{:^8}|{:^12}|".format("s.no","Movie Name","Votes","Ratings","Meta Score","Duration","Genre")
print(data_header)
print(border)
#printing the data
for i in range(0,len(names)):
	data="|{:^4}|{:<70}|{:^8}|{:^8}|{:^10}|{:^8}|{:^12}|".format(i+1,names[i],votes[i],ratings[i],meta_scores[i],durations[i],genres[i])
	print(data)
print(border)
#plotting graph for ratings
slabed_ratings  = [math.ceil(i) for i in ratings]
slabed_ratings = dict(Counter(slabed_ratings))
rating_names=list(slabed_ratings.keys())
rating_values=list(slabed_ratings.values())
plt.subplot(2,2,1)
plt.title('IMDB rating')
plt.bar(rating_names,rating_values)

#plotting graph for metascores
Metascore=dict(Counter(Metascores))
meta_names=list(Metascore.keys())
meta_values=list(Metascore.values())
plt.subplot(2,2,2)
plt.title('MetaScore')
plt.bar(meta_names,meta_values)

#plotting graphs for both metascores and ratings
meta_ratings = [(i)*10 for i in Metaratings]
meta_ratings = dict(Counter(meta_ratings))
metarating_names=list(meta_ratings.keys())
metarating_values=list(meta_ratings.values())
plt.subplot(2,2,3)
plt.bar(metarating_names,metarating_values,label="rating")
plt.bar(meta_names,meta_values,label="meta_score")
plt.grid(axis='x', color='0.95')
plt.legend(title='values')
plt.title('Normalized Distributions')

#plotting graphs of genres
genres=[i.strip() for i in genres]
genres=[i.strip('\n') for i in genres]
Genres=dict(Counter(genres))
Genres=dict(sorted(Genres.items(),key=operator.itemgetter(1),reverse=True))
sorted_genres= dict(islice(Genres.items(),5))
genres_names=list(sorted_genres.keys())
genres_values=list(sorted_genres.values())
ax=plt.subplot(2,2,4)
plt.title("Genres")
def func(pct, allvals):
	absolute = int(pct/100.*np.sum(allvals))
	return "{:.2f}%\n({:d})".format(pct, absolute)
	
wedges, texts, autotexts = ax.pie(genres_values, autopct=lambda pct: func(pct, genres_values),
                                  textprops=dict(color="w"))
ax.legend(wedges, genres_names,
          title="Genre names",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")
plt.show()
