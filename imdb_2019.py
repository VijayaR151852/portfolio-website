import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
pages=[]
names=[]
votes=[]
ratings=[]
years=[]
durations=[]
meta_scores=[]
genres=[]
sno=[]
for i in range(1,1001,50):
	url="https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31&sort=num_votes,desc&start={}&ref_=adv_nxt".format(i)
	pages.append(url)
for item in pages:
	responses=requests.get(item)
	html_soup=BeautifulSoup(responses.text,'html.parser')
	movie_container= html_soup.find_all('div', class_ = 'lister-item mode-advanced')
	for container in movie_container:
		name=container.h3.a.text
		names.append(name)
		rating=float(container.strong.text)
		ratings.append(rating)
		meta_score=container.find('span', class_ = 'metascore')
		if container.find('div',class_='ratings-metascore') is None:
			meta_score=int(0)
			meta_scores.append(meta_score)
		else:
			meta_score=int(meta_score.text)
			meta_scores.append(meta_score)
		vote=container.find('span',attrs={'name':'nv'})
		vote=int(vote['data-value'])
		votes.append(vote)
		duration=container.find('span',class_='runtime')
		if container.find('span',class_='runtime')is None:
			duration=int(0)
			durations.append(int(duration))
		else:
			duration=(duration.text)
			duration=duration.strip("min")
			durations.append(int(duration))
		genre=container.find('span',class_='genre').text
		genre=genre.strip()
		genres.append(genre)
for i in range(1,1001):
	sno.append(i)
data_header="|{:^4}|{:^70}|{:^8}|{:^8}|{:^10}|{:^8}|{:^8}".format("s.no","Movie Name","Votes","Ratings","Meta Score","Duration","Genre")
print(data_header)
for i in range(0,len(names)):
	data="|{:^4}|{:<70}|{:^8}|{:^8}|{:^10}|{:^8}|{:^8}".format(i+1,names[i],votes[i],ratings[i],meta_scores[i],durations[i],genres[i])
	print(data)

fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(ratings,sno)
axs[1].scatter(ratings,sno)
axs[2].plot(ratings,sno)
plt.show()
fig.suptitle('Categorical Plotting')
