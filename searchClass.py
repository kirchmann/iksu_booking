# -*- coding: utf-8 -*- 
import re

# Goal of finding the ID of the class, can be done by entering an URL that has filters populated 
# The returning html code contains a lot of information, at the end of the code one can find the classes that the search returned. 
# Every class has a unique "tr id" which is an 8 digit number
def getClassID(session,fromDate,thruDate,fromTime,thruTime,weekday,location,class_obj,instructors):
	dayDict = {'Monday': '1', 'Tuesday': '2', 'Wednesday': '3','Thursday': '4','Friday': '5','Saturday': '6','Sunday': '7'}
	locationDict = {'IKSU Sport': '100','IKSU SPA': '200','IKSU PLUS': '300'}
	dayOfWeek = dayDict[weekday]
	print len(location)
	# payload = {'fromDate': '2015-09-11', 'thruDate': '2015-09-18', 'fromTime':'06:00', 'thruTime':'23:00', 'daysOfWeek[]':'2', 'locations[]':'100', 
	#'obj_classes[g_iw]':'X', 'objects[]':'IW55', 'instructors[]':'CAHO', 'func':'fres', 'search':'T', 'btn_submit':'x'}
	# Add dictionary for instructors and class_obj I like

	tUrl = "/index.php?fromDate="+fromDate+"&thruDate="+thruDate+"&fromTime="+fromTime+"%3A00&thruTime="+ thruTime+"%3A00&daysOfWeek%5B%5D="+dayOfWeek
	tUrl2 = "&locations%5B%5D="+ locationDict[location]+"&obj_classes%5B"+class_obj+"%5D=X&instructors%5B%5D="+instructors+"&func=fres&search=T&btn_submit=x&xajaxreq=1"
	url = "https://bokning.iksu.se"+tUrl+tUrl2
	print url
	print 'https://bokning.iksu.se'+tUrl+tUrl2
	p = session.get('https://bokning.iksu.se/index.php?func=fres'+tUrl+tUrl2)
	extracttemp = (p.text).encode('utf-8').split("Lördag "+thruDate,1)[1] 
	tReturn = extracttemp.split("tr id",1)[1] 
	print tReturn
	class_id = re.search(r'\d+\d+\d+\d+\d+\d+\d+\d+',tReturn)	
	return class_id.group(),locationDict[location]