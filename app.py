import random, urllib2
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
	numberOfStudents = 3
	index = random.randint(1,numberOfStudents)
	students = getStudents(numberOfStudents)
	for i in range(0,len(students)):
		if i == index:
			students[i].status = 'featured'
		else:
			students[i].status = 'notfeatured'	
	featuredPerson = students[index]
	return render_template('index.html', featured=featuredPerson, featured1=students[0], featured2=students[1], featured3=students[2])
	
	
def getStudents(num=3):
	url = 'http://www.ischool.berkeley.edu/people/students/masters/'
	req = urllib2.Request(url, headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'}) 
	results_html = urllib2.urlopen(req).read()
	soup = BeautifulSoup(results_html)
	tables = soup.find_all('table', {'class':'person-teaser'})
	students = []
	for i in range(0,num):
		students.append(getStudent(tables))
	return students
	
def getStudent(tables):
	randTableIndex = random.randint(1, len(tables)) - 1
	randT = tables[randTableIndex]
	sd = StudentData()
	sd.name = randT.find('div', {'class':'title'}).find('a').contents[0]
	sd.year = randT.find('div', {'class': 'field-field-person-degree-year'}).contents[0]
	sd.status = "notfeatured"
	url = randT.find('img')['src']
	sd.pic = 'http://www.ischool.berkeley.edu' + url
	return sd

class StudentData:
    pass

if __name__ == "__main__":
	app.run()
	