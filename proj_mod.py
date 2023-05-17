import string
import pickle
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform

def docgen(dta):
	s_name=dta[0]
	s_rollno=dta[1]
	s_mailid=dta[2]
	sl=dta[5]
	k=len(sl)
	s_totalpercentage=dta[4]
	p1="""<html><head></head><body><hr size="5px" noshade><font color="blue"><h1 align="center">REPORT CARD</h1><hr size="5px" noshade></font>
	<table align="center" width="20%"><tr><th>          </th><th>          </th><th>          </th></tr><tr><td><b>Name</b></td><td><b>:</b></td><td>"""
	p2="""</td></tr><tr><td><b>Roll No</b></td><td><b>:</b></td><td>"""
	p3="""</td></tr><tr><td><b>E-mail ID</b></td><td><b>:</b></td><td>"""
	p4="""</td></tr>
	</table><br><br><br><table width="50%" border=1 align="center"><tr><th><font color="red">SUBJECT</font></th><th><font color="red">MARKS Obtained</font></th>
	<th><font color="red">Total MARKS</font></th><th><font color="red">PERCENTAGE</font></th></tr>"""
	p5="""<tr><td><font color="green">"""
	p6="""</font></td><td align="center">"""
	p7="""</td><td align="center">"""
	p8="""</td><td align="center">"""
	p9=""" %</td></tr>"""
	p10="""</table>
	<br><br><table align="center" width="20%">
	<tr><th>          </th><th>          </th><th>          </th></tr><tr><td><b>Total Percentage</b></td><td><b>:</b></td><td align="right"><font color="red">"""
	p11=""" %</font></td></tr></table><br><br><br><br><hr size="5px" noshade></body></html>"""
	textcontent=p1+s_name+p2+str(s_rollno)+p3+s_mailid+p4
	i=0
	while (i<k):
		s_subject=dta[5][i]
		s_omark=dta[6][i]
		s_tmark=dta[7][i]
		s_percentage=dta[8][i]
		textcontent=textcontent+p5+str(s_subject)+p6+str(s_omark)+p7+str(s_tmark)+p8+str(s_percentage)+p9
		i=i+1
	textcontent=textcontent+p10+str(s_totalpercentage)+p11
	return textcontent

class Student: 
    name=""   
    email=""
    rno=0
    sub=[]
    marks=[]
    stot=[]
    sper=[]
    total=0
    per=0
    def __init__(self):
         self.sub=[]
         self.marks=[]
         self.stot=[]
         self.sper=[]
    def ToList(self):
         lst=[]
         lst.append(self.name)
         lst.append(self.rno)
         lst.append(self.email)
         lst.append(self.total)
         lst.append(self.per)
         lst.append(self.sub)
         lst.append(self.marks)
         lst.append(self.stot)
         lst.append(self.sper)
         return lst
    def FromList(self,lst):
         self.name = lst[0]
         self.rno = lst[1]
         self.email = lst[2]
         self.total = lst[3]
         self.per = lst[4]
         self.sub = lst[5]
         self.marks = lst[6]
         self.stot = lst[7]
         self.sper = lst[8]
    def ReadData(self):
         self.name=raw_input("Enter Student Name : ")
         self.rno=input("Enter Student Roll Number : ")
         ch='y'
         while(ch=='Y' or ch=='y'):
             print "-"*40
             self.sub.append(raw_input("Enter Subject Name : "))
             self.stot.append(input("Enter the maximum marks that can be awarded (Default=100): "))
             if(self.stot[len(self.stot)-1]<=0):
                 self.stot[len(self.stot)-1]=100
             mks=input("Enter Subject Marks : ")
             while(mks<0 or mks>self.stot[len(self.stot)-1]):
                  print "ERROR : Subject Marks should be >= 0 and Subject Marks should be < ",self.stot[len(self.stot)-1]
                  mks=input("Enter Subject Marks : ")
             self.marks.append(mks)
             ch = raw_input("Do you want to enter another subject (y/n) : ")
         self.email=raw_input("Enter Student Email Address : ")
         while(self.email.find('@')<= 0 or self.email.find('.com')<=0):
             print "ERROR : Not A Valid Email Address "
             self.email=raw_input("Enter Student Email Address : ")
         cnt=0
         for i in self.marks:
             self.total+=i
             self.sper.append((i*100)/(self.stot[cnt]))
             cnt+=1
         for i in self.sper:
             self.per+=i
         self.per/=len(self.sper)
    def Display(self):
         print "Name : ",self.name
         print "Roll No : ",self.rno
         print "Email : ",self.email
         cnt=0
         for (i,j) in zip(self.sub,self.marks):
            print i," : ",j," / ",self.stot[cnt],"   Per = ",self.sper[cnt]
            cnt+=1
         print "Total : ",self.total," Percentage : ",self.per
         
opt=0
opt=input("MARKSHEET AUTOMATION SOFTWARE\nDeveloped By : Eldhose K A & Georgy M Rajan\n\t(1)-Write Student Data\n\t(2)-Read Student Data\n\t(3)-Email Student Report\n\t(4)-Exit\nPlease Select Your Option : ")
while(opt!=4):
  if(opt==1):          
      c='y'  
      fout=open("data.dat","ab")
      while(c=='Y' or c=='y'):
          s=Student()
          s.ReadData()
          s.Display()
          c = raw_input("Do you want to enter another student details (y/n) : ")
          lst = s.ToList()
          pickle.dump(lst,fout,pickle.HIGHEST_PROTOCOL)
      fout.close()
  elif(opt==2):
      fin=open("data.dat","rb")
      flg=0
      found=0
      rno=input("Enter the roll no of student to be searched : ")
      lst=pickle.load(fin)
      s=Student()
      s.FromList(lst)
      while(flg==0):
          if(s.rno == rno):
               s.Display()
               found=1
               break
          try:
             lst=pickle.load(fin)
             s.FromList(lst)
          except:
             flg=1
      if(found==0):
          print "Student Record Not Found !!!"
      fin.close()
  elif(opt==3):
      smail=raw_input("Enter your email id : ")
      while(smail.find('@')<=0 or smail.find('.com')<=0):
          print "ERROR: Invalid Email Address"
          smail=input("Enter your email id : ")
      spass=raw_input("Enter your password : ")
      if(platform.system()=='Linux'):
          clr='clear'
      else:
          clr='cls'
      os.system(clr)
      fin=open("data.dat","rb")
      flg=0
      s=Student()
      while(flg==0):
          try:
              lst=pickle.load(fin)
              s.FromList(lst)
              chk='y'
              s.Display()
              chk=raw_input("Do you want to generate report for this record (y/n): ")
              if(chk=='y'or chk=='Y'):
                  try:
                      msg=MIMEMultipart('alternative')
                      msg['Subject'] = "Report Card"
                      msg['From'] = smail
                      msg['To'] = lst[2]
                      text=""
                      htmldoc=docgen(lst)
                      msg.attach(MIMEText(text,'plain'))
                      msg.attach(MIMEText(htmldoc,'html'))
                      s=smtplib.SMTP('smtp.gmail.com',587)
                      s.ehlo()
                      s.starttls()
                      s.login(smail,spass)
                      s.sendmail(smail, lst[2], msg.as_string())
                      s.quit()
                      print "The email has been successfully delivered "
                  except:
                      print "ERROR: Unable to sent email\n(Check if 'Less Secure Apps' is Turned On in your Email Account)"
          except EOFError:
              flg=1
      fin.close()
  else:
      print "Invalid Option"
  opt=input("MARKSHEET AUTOMATION SOFTWARE\nDeveloped By : Eldhose K A & Georgy M Rajan\n\t(1)-Write Student Data\n\t(2)-Read Student Data\n\t(3)-Email Student Report\n\t(4)-Exit\nPlease Select Your Option : ")  



        
         

         
      
