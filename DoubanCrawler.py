"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
import expanddouban
import csv
from bs4 import BeautifulSoup

# Task1
# 类别和地区的获取Url方法
def getMovieUrl(category, location):

	url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影'
	url += ",{},{}".format(category,location)
	return url

	


# Task 2
url = getMovieUrl('动作','美国')
html = expanddouban.getHtml(url)






# Task3
# 定义类与构造函数
# https://www.tutorialspoint.com/python/python_classes_objects.htm
class Movies:
	"""
	自己摸索出来的pattern
	name = soup.find(class_="list-wp").find_all(class_="title")[_].string
	rate = soup.find(class_="list-wp").find_all(class_="rate")[_].string
	info_link	= soup.find(class_="list-wp").find_all(class_="item")[_]['href']
	cover_link = soup.find(class_="list-wp").find_all(class_="cover-wp")[_].img['src']
	"""
	#构造函数
	def __init__(self,name, rate, location, category, info_link, cover_link):
		self.name = name
		self.rate = rate
		self.location = location
		self.category =	category
		self.info_link = info_link
		self.cover_link = cover_link
		
		
# Task4
# 定义getMovies()方法
def getMovies(category,location):
	desired_movies_list = []
	#调用getMovieUrl()
	url = getMovieUrl(category,location)
	html = expanddouban.getHtml(url,True,0)
	soup = BeautifulSoup(html,'html.parser')
	movies_list = soup.find(class_="list-wp")
	names = movies_list.find_all(class_="title")
	rates =	movies_list.find_all(class_="rate")
	info_links = movies_list.find_all(class_="item")
	cover_links = movies_list.find_all(class_="cover-wp")
	list_size = len(movies_list)
	for _ in range(list_size):
		movie = Movies(names[_].string,rates[_].string,location,category,info_links[_]['href'],cover_links[_].img['src'])
		desired_movies_list.append(movie)
	return desired_movies_list
	
	
#Task5
# 喜欢的三个标签
favorite_tags = ['喜剧','爱情','家庭']
#所有地区的列表
country_list=['大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
movies_list=[]
#迭代地区列表，用getMovies()方法获得电影列表将列表延伸
for country in country_list:
	for tag in favorite_tags:
		movies_list += getMovies(tag,country)

#将结果写入movies.csv
#https://docs.python.org/3.5/library/csv.html
with open('movies.csv','w',  encoding = 'utf-8') as csvfile:
	fieldnames = ['name', 'rate','category','location','info_link','cover_link']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	writer.writeheader()
	for _ in movies_list:
		writer.writerow({'name':_.name, 'rate':_.rate,'category':_.category,'location':_.location,'info_link':_.info_link,'cover_link':_.cover_link})
#Task6
"""
movies_list是Movie对象的集合
"""
comedy_movies=[]
romance_movies=[]
family_movies=[]

for _ in movies_list:
	if _.category == "喜剧":
		comedy_movies.append(_.location)

for _ in movies_list:
	if _.category == "爱情":
		romance_movies.append(_.location)
		
for _ in movies_list:
	if _.category == "家庭":
		family_movies.append(_.location)

#用字典记录该类别中各地区出现的次数，老办法：没有定1，有就加1

comedy_movie_dict = {}

for location in comedy_movies:
	if comedy_movie_dict.get(location):
		comedy_movie_dict[location] += 1
	else:
		comedy_movie_dict[location] = 1
	
romance_movie_dict = {}

for location in romance_movies:
	if romance_movie_dict.get(location):
		romance_movie_dict[location] += 1
	else:
		romance_movie_dict[location] = 1

family_movie_dict = {}

for location in family_movies:
	if family_movie_dict.get(location):
		family_movie_dict[location] += 1
	else:
		family_movie_dict[location] = 1

#个类别电影总数
comedy_movie_total = len(comedy_movie_dict)
comedy_movie_first_place = sorted(comedy_movie_dict,key=lambda x:comedy_movie_dict[x])[-1]
comedy_movie_second_place = sorted(comedy_movie_dict,key=lambda x:comedy_movie_dict[x])[-2]
comedy_movie_third_place = sorted(comedy_movie_dict,key=lambda x:comedy_movie_dict[x])[-3]


romance_movie_total = len(romance_movie_dict)

romance_movie_first_place = sorted(romance_movie_dict,key=lambda x:romance_movie_dict[x])[-1]
romance_movie_second_place = sorted(romance_movie_dict,key=lambda x:romance_movie_dict[x])[-2]
romance_movie_third_place = sorted(romance_movie_dict,key=lambda x:romance_movie_dict[x])[-3]

family_total = len(family_movie_dict)

family_movie_first_place = sorted(family_movie_dict,key=lambda x:family_movie_dict[x])[-1]
family_movie_second_place = sorted(family_movie_dict,key=lambda x:family_movie_dict[x])[-2]
family_movie_third_place = sorted(family_movie_dict,key=lambda x:family_movie_dict[x])[-3]

with open("output.txt","w", encoding = 'utf-8') as f:
		f.write("喜剧电影的地区排行是第一：{}，第二：{}，第三：{}".format(comedy_movie_first_place,comedy_movie_second_place,comedy_movie_third_place))
		f.write("爱情电影的地区排行是第一：{}，第二：{}，第三：{}".format(comedy_movie_first_place,comedy_movie_second_place,comedy_movie_third_place))
		f.write("家庭电影的地区排行是第一：{}，第二：{}，第三：{}".format(comedy_movie_first_place,comedy_movie_second_place,comedy_movie_third_place))
