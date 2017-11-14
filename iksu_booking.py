# -*- coding: utf-8 -*- 
import requests
import sys
import getopt
import datetime as dt
import re
# Run script with command line argument being spin or beach

# date: 2017-11-1, start_time: 22:00:00, end_time: 23:00:00, num = 1,2,3,4 which is Las Palmas <num>
#Example of formatting of booking address, divided in two rows :
	#https://bokning.iksu.se/index.php?func=do_cal_reservation&location=100&cdate=2017-11-08
	#&res_stime=2017-11-08 07:00:00&res_etime=2017-11-08 08:00:00&objectCode=XBE1&pageId=275&RSVID=0&DETID=0
	#Could have input be start hour: start=20, then in the function have end = start+1 
	# after that: start_time=str(start)+":00:00"
	#		      end_time=str(end)+":00:00"
def getBeachUrl(date,start_time,end_time,num):
	url_book_temp = 'https://bokning.iksu.se/index.php?func=do_cal_reservation&location=100&cdate=' + date + '&res_stime='
	return url_book_temp+date+' '+start_time+'&res_etime='+date+' '+end_time+'&objectCode=XBE'+str(num)+'&pageId=275&RSVID=0&DETID=0'

# Goal of finding the ID of the class, can be done by entering an URL that has filters populated 
# The returning html code contains a lot of information, at the end of the code one can find the classes that the search returned. 
# Every class has a unique "tr id" which is an 8 digit number
def getClassID(session,fromDate,thruDate,fromTime,thruTime,daysOfWeek,locations,class_obj,instructors):
	# payload = {'fromDate': '2015-09-11', 'thruDate': '2015-09-18', 'fromTime':'06:00', 'thruTime':'23:00', 'daysOfWeek[]':'2', 'locations[]':'100', 
	#'obj_classes[g_iw]':'X', 'objects[]':'IW55', 'instructors[]':'CAHO', 'func':'fres', 'search':'T', 'btn_submit':'x'}
	# Add dictionary for instructors and class_obj I like
	tUrl = "/index.php?fromDate="+fromDate+"&thruDate="+thruDate+"&fromTime="+fromTime+"%3A00&thruTime="+ thruTime+"%3A00&daysOfWeek%5B%5D="+daysOfWeek
	tUrl2 = "&obj_classes%5B"+class_obj+"%5D=X&instructors%5B%5D="+instructors+"&func=fres&search=T&btn_submit=x&xajaxreq=1"
	url = "https://bokning.iksu.se"+tUrl+tUrl2
	print url
	print 'https://bokning.iksu.se/index.php?func=fres'+tUrl+tUrl2
	p = session.get('https://bokning.iksu.se/index.php?func=fres'+tUrl+tUrl2)
	tReturn = (p.text).encode('utf-8').split("tr id",1)[1] 
	print tReturn
	class_id = re.search(r'\d+\d+\d+\d+\d+\d+\d+\d+',tReturn)	
	return class_id.group()

def bookClass(session,class_id,location):
	url = 'https://bokning.iksu.se/index.php?func=ar&id='+str(class_id)+'&location='+str(location)+'&rsv_det_id=&pref_f=la&usebfc=1'
	print "Attempting to book spin class using url: "
	print url
	p = session.get(url)
	if "Du har nu bokat följande" and "Cykel 55" in str(p.text.encode('utf-8')):
		print "Booking of Cykel 55 Watt Successfull"
	else:
		print "Failed to book Cykel 55 Watt"
	return p

# Adds date and time to fname_
def timeStamped(fname, fmt='{fname}_%Y-%m-%d_%H%M%S'):
	return dt.datetime.now().strftime(fmt).format(fname=fname)

# Read login and password for user from txt file placed in file_directory
def readUserData(fileName):
	file = open(fileName,"r")
	user = file.readline().rstrip()
	passw = file.readline().rstrip()
	return user,passw

# Login using payload which contains user name and password
def login(payload):
	url_login = 'https://bokning.iksu.se/index.php?func=myc_login'
	with requests.Session() as session:
		p = session.post(url_login, data=payload)
		if "Du har ett aktivt träningskort" in str(p.text.encode('utf-8')):
			print "Successfull login."
			return session,p
		else:
			print "Failed to login, check login and password."
			print "Exiting."
			exit()
		
def logout(session):
	p = session.get('https://bokning.iksu.se/index.php?func=logout')
	return p

def bookBeach(url,session):
	p = session.get(url)
	if "Bokningen lyckades" in str(p.text.encode('utf-8')):
		print "Booking successfull!"
		return p, True
	else:
		print "Booking failed."
	return p, False

# link to Cykel 55 Watt 2017-11-04 10:00-11:00:
# https://bokning.iksu.se/index.php?func=rd&id=13823210&location=100&usebfc=1
# is ID constant? ID 
# when booking, just gotta find the ID, if same every week, win
# ID next week:
# tr id="13823211
# it is id = last_week_id + 1
def bookSpin(session):
	year = dt.datetime.today().year
	diff_y = 2017 - year
	weekNumber = dt.datetime.now().isocalendar()[1]
	id_w = 43
	id_w_43 = 13823210	
	diff = diff_y*52 + weekNumber-id_w
	id_current = id_w_43 + diff + diff_y
	url = 'https://bokning.iksu.se/index.php?func=rd&id=' + str(id_current) + '&location=100&usebfc=1'
	print "Attempting to book spin class using url: "
	print url
	p = session.get(url)
	#print 'https://bokning.iksu.se/index.php?func=rd&id=' + str(id_current) + '&location=100&usebfc=1'
	if "Du har nu bokat följande" and "Cykel 55" in str(p.text.encode('utf-8')):
		print "Booking of Cykel 55 Watt Successfull"
	else:
		print "Failed to book Cykel 55 Watt"
	return p

def main(argv):
	#print str(argv[0])
	#print str(argv[1])
	print str(dt.datetime.now())

	login_filename = str(argv[1])
	date = dt.date.today()
	bookDate = str(date + dt.timedelta(days=7))
	orig_sys = sys.stdout
	user,passw = readUserData(login_filename)
	payload = {
	    'txt_login': 'name',
	    'psw_password': 'password'
	}
	payload["txt_login"] =user
	payload["psw_password"] =passw
	session,p = login(payload)
	if 'beach' in str(argv[0]):
		# To check available times:
		#url_beach = 'https://bokning.iksu.se/index.php?func=mod_rc_v2&tac=&pageId=275&cdate=' + bookDate
		booktime_s = ["21:00:00","20:00:00"]
		booktime_e = ["22:00:00","21:00:00"]
		lasPalmasnum = [1,2,3,4]
		booked = False
		for i in xrange(0,len(booktime_s)):
			for court in lasPalmasnum:
				url_beach = getBeachUrl(bookDate,booktime_s[i],booktime_e[i],court)
				print ""
				print "Attempting to book Las Palmas "+str(court) +" from " +booktime_s[i]+ " to " +booktime_e[i] +" using url: "
				print url_beach
				p,booked = bookBeach(url_beach,session)
				if booked == True:
					break;
			if booked:
				break;
	elif 'spin' in str(argv[0]):
		#p = bookSpin(session)
		location = '100'
				#session,fromDate,thruDate,fromTime,thruTime,daysOfWeek,locations,class_obj,instructors
		class_id = getClassID(session,str(date),bookDate,'09','12','6',location,'g_cy','ALTE')
		bookClass(session,class_id,location)
	else:
		print "Incorrect command line argument, only supports 'spin' and 'beach'."
	#Write answer to output.txt
	#with open(timeStamped('response')+'.txt','w') as out:
	with open('response.txt','w') as out:
		sys.stdout = out
		print (p.text).encode('utf-8')
	# Add check to see that it successfully logged out
	p = logout(session)

if __name__ == "__main__":
   main(sys.argv[1:])