from pydelicious import get_popular, get_userposts, get_urlposts

def initializeUserDict(tag, count=5):
	user_dict={}
	# отримати рахунок найпопулярніших лінків
	for p1 in get_popular(tag=tag)[0:count]:
		# знайти всіх користувачів, які зберегли цей лінк
		for p2 in get_urlposts(p1['href']):
			user=p2['user']
			user_dict[user]={}
		return user_dict

# вичислити оцінки для всіх користувачів
def fillItems(user_dict):
	all_items={}
	# find links, which saved by all users
	for user in user_dict:
		for i in range(3):
			try:
				posts=get_userposts(user)
				break
			except:
				print("Error for user "+user+", try again")
				time.sleep(4)

		for post in posts:
			url=post['href']
			user_dict[user][url]=1.0

	# If not exist write 0
	for ratings in user_dict.values():
		for item in all_items:
			if item not in ratings:
				ratings[item]=0.0


delusers=initializeUserDict('programming')
delusers['tsegaran']={}
print(fillItems(delusers))


