import urllib.request
import lxml.html as html

LESSON_ON_EVEN_WEEK = 0 
LESSON_ON_NOT_EVEN_WEEK = 1
LESSON_ON_BOTH_WEEKS = 2

class Shedule(object):
	def __init__(self): 
		self.lessons = []

	def append(self, lesson): 
		self.lessons.append(lesson)

	def week_even(self): 
		return self.__dayly(LESSON_ON_EVEN_WEEK)

	def week_not_even(self):
		return self.__dayly(LESSON_ON_NOT_EVEN_WEEK)

	def __dayly(self, week_type): 
		if week_type not in (LESSON_ON_EVEN_WEEK, LESSON_ON_NOT_EVEN_WEEK): 
			raise Exception("Unsupported week type")

		dayly = {day_name: [] for day_name in ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")} 

		LESSON_PARAMS = ("btime", "etime", "name", "lesson_type", "place", "tutors")

		for lesson in self.lessons: 
			if lesson.square == LESSON_ON_BOTH_WEEKS or lesson.square == week_type: 
				dayly[lesson.day].append({attr_name: getattr(lesson, attr_name) for attr_name in LESSON_PARAMS })

		return dayly


class Lesson(object): 
	def __init__(self, square, day, time_range, name, lesson_type, place, tutors): 
		self.square = {
			"Еженедельно": LESSON_ON_BOTH_WEEKS,
			"Четная неделя": LESSON_ON_EVEN_WEEK,
			"Нечетная неделя": LESSON_ON_NOT_EVEN_WEEK
		}[square]

		self.day = day 
		self.btime = time_range[0]
		self.etime = time_range[1]
		self.name = name 
		self.lesson_type = ",".join(lesson_type)
		self.place = place
		self.tutors = ",".join(tutors)

	def __str__(self): 
		return "{square} {day} {btime}-{etime} {place} {lesson_type} {name} {tutors}".format(
			square     ="Ч/Н" if self.square == LESSON_ON_BOTH_WEEKS else " Ч " if self.square == LESSON_ON_EVEN_WEEK else " Н ",
			day        =self.day, 
			btime      =self.btime, 
			etime      =self.etime, 
			place      =self.place, 
			lesson_type=self.lesson_type, 
			name       =self.name, 
			tutors     =",".join(self.tutors))

def get_shedule(): 
	result = Shedule()

	url = "https://home.mephi.ru/study_groups/774/schedule?period=0"

	response = urllib.request.urlopen(url)

	page = html.document_fromstring(response.read().decode('utf-8'))

	days = [day.text_content().strip() for day in page.cssselect(".lesson-wday")]
	shedules = page.cssselect(".lesson-wday + div")

	for day_num, day_shedule in enumerate(shedules): 
		periods = day_shedule.cssselect(".list-group-item")

		for period in periods:
			time_str = period.cssselect(".lesson-time")[0].text_content()
			time_range = time_str.split("\xa0— ")

			for lesson in period.cssselect(".lesson"): 
				lessson_type = [type_name.text_content() for type_name in lesson.cssselect(".label")]
				place = lesson.cssselect("a[href^='/rooms/']")[0].text_content()
				tutors = [name.text_content() for name in lesson.cssselect("a[href^='/tutors/']")]
				square = lesson.cssselect(".lesson-square")[0].get("title")

				for line in lesson.text_content().splitlines():
					if len(line) != 0 and line not in [time_str, place] + lessson_type + tutors: 
						lesson_name = line
						break 

				result.append(Lesson(square, days[day_num], time_range, lesson_name, lessson_type, place, tutors))

	return result
