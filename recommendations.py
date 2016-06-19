#Збір інформації про уподобання

from math import sqrt

#перше, що потрібно - це представити людей і їхні вподобання. 
#зробимо це задопомогою вкладеного словника

#словник кінокритиків і виставлених ними оцінок для невеликого набору даних про фільми
critics={'Lisa Rose':{'Lady in the Water':2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,
						'Superman Returns':3.5,'You, Me and Dupree':2.5,'The Night Listener':3.0},
			'Gene Seymour':{'Lady in the Water':3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,
							'Superman Returns':5.0,'The Night Listener':3.0,'You, Me and Dupree':3.5},
			'Michael Phillips':{'Lady in the Water':2.5,'Snakes on a Plane':3.0,'Super Returns':3.5,'The Night Listener':4.0},
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


















