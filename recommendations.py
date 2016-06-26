#Збір інформації про уподобання

from math import sqrt

#перше, що потрібно - це представити людей і їхні вподобання. 
#зробимо це задопомогою вкладеного словника

#словник кінокритиків і виставлених ними оцінок для невеликого набору даних про фільми
critics={'Lisa Rose':{'Lady in the Water':2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,
						'Superman Returns':3.5,'You, Me and Dupree':2.5,'The Night Listener':3.0},
			'Gene Seymour':{'Lady in the Water':3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,
							'Superman Returns':5.0,'The Night Listener':3.0,'You, Me and Dupree':3.5},
			'Michael Phillips':{'Lady in the Water':2.5,'Snakes on a Plane':3.0,'Superman Returns':3.5,'The Night Listener':4.0},
			'Claudia Puig':{'Snakes on a Plane':3.5,'Just My Luck':3.0,'The Night Listener':4.5,'Superman Returns':4.0,'You, Me and Dupree':2.5},
			'Nick LaSalle':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Just My Luck':2.0,'Superman Returns':3.0,
							'The Night Listener':3.0,'You, Me and Dupree':2.0},
			'Jack Matthew':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'The Night Listener':3.0,'Superman Returns':5.0,'You, Me and Dupree':3.5},
			'Toby':{'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}
						}

# from recommendatins import critics
# critics['Lisa Rose']['Lady in the Water']
# 2.5

# повертає оцінку подівності пeрсон1 та персон2 на основі 
def sim_distance(prefs,person1,person2):
	# отримати спосок предметів, оцінених обома
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1

	# якщо немає жодної спільної оцінки, повертаємо 0
	if len(si)==0: return 0

	# 
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])

	return 1/(1+sqrt(sum_of_squares))
	# у книзі цей приклад без sqrt квадратного кореня, але за формулою Увклідової відстані тут потрібно взяти квадратний корінь суми квадратів різниць :)

print(sim_distance(critics,'Lisa Rose', 'Gene Seymour'))

# повертає коефіцієнт кореляції Пірсона між р1 і р2
def sim_pearson(prefs,p1,p2):
	# отримати список предметів, які оцінив кожен критик
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]: si[item]=1

	#кількість елементів
	n=len(si)

	#якщо немає жодної спільної оцінки повернути нуль
	if n==0: return 0

	#визначити суму всіх уподобань
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])

	#визначити суму квадратів
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

	#визначити суму добутків
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

	#визначити коефіцієнт Пірсона
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0

	r=num/den

	return r

print(sim_pearson(critics,'Lisa Rose','Gene Seymour'))

# Ранжування критиків

# повертає список найкращих співпадінь для людини зі словника prefs
# кількість результатів і функція подібності - необов'язкові параметри
def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

	# відсортувати список по спаду оцінок
	scores.sort()
	scores.reverse()
	return scores[0:n]

print(topMatches(critics,'Toby',n=3))

#отримати рекомендації для конкретної людини, 
#використовуючи зважені середні оцінки, які поставили всі інші користувачі

def getRecommendations(prefs,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:
		#непотрібно порівнювати мене зі мною
		if other==person: continue
		sim=similarity(prefs,person,other)

		#ігнорувати нульові та від'ємні значення
		if sim<=0: continue
		for item in prefs[other]:
			#оцінювати лише фільми, які я ще не дивилась
			if item not in prefs[person] or prefs[person][item]==0:
				# Коефіцієнт подібності*Оцінку
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim 
				# Сума коефіцієнтів подібності
				simSums.setdefault(item,0)
				simSums[item]+=sim

	# створити нормалізований список
	rankings=[(total/simSums[item],item) for item,total in totals.items()]

	# повернути відсортований список
	rankings.sort()
	rankings.reverse()
	return rankings

print(getRecommendations(critics,'Toby',))
print(getRecommendations(critics,'Toby',similarity=sim_distance))

def transformPrefs(prefs):
	result={}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item,{})

			# поміняти місцями людину і предмет
			result[item][person]=prefs[person][item]

	return result

movies= transformPrefs(critics)
print(" ")
print(topMatches(movies,'Superman Returns'))
#пошук рекомендованих критикыв для фільму
print(getRecommendations(movies,'Just My Luck'))
print(" ")
print(" ")
print(critics)
print(" ")
print(movies)


def calculateSimilarItems(prefs,n=10):
	#Create dict, which consists of same items as item
	result={}

	#Change matrix of likes to make lines be items
	itemPrefs=transformPrefs(prefs)
	c=0
	for item in itemPrefs:
		#Refresh state for big data
		c+=1
		if c%100==0: print("%d / %d" % (c,len(itemPrefs)))
		#Find items as same as item
		scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
		result[item]=scores
	return result

itemsim=calculateSimilarItems(critics)
print(" ")
print(itemsim)

def getRecommendedItems(prefs, itemMatch, user):
	userRating=prefs[user]
	scores={}
	totalSim={}

	#Cycle of items points of this user
	for (item,rating) in userRating.items():
		
		#Cycle of items same as item
		for (similarity,item2) in itemMatch[item]:

			#Skip if user rated item
			if item2 in userRating: continue
		#
			scores.setdefault(item2,0)
			scores[item2]+=similarity*rating

			#Sum of all coeficients of the saming
			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity

		#
		#
	rankings=[(score/totalSim[item],item) for (item,score) in scores.items()]

		#Return list rankings, from big to small
	rankings.sort()
	rankings.reverse()
	return rankings

print(" ")
print(getRecommendedItems(critics,itemsim,'Toby'))
















