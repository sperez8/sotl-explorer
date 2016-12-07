import csv
import sys
import re

###########
# This is a 3.X python file. 
# Takes the responses downloaded from the UBC survey tool and
# "flips" some of the data and makes it into a readable format
# Rama Flarsheim. Nov 15, 2015
# if the name of this script is surveyCleaner.py
# use like: python surveyCleaner.py "responses (4).csv" temp.tsv
#
# creates a tab seperated CSV file
###########


inputFileName = sys.argv[1] #first argument 
outputFileName = sys.argv[2]  



csvfile=open(inputFileName,encoding="utf_16", errors="surrogateescape")
reader = csv.DictReader(csvfile, dialect="excel-tab")

#create feildnames
#hardcoded. TODO: make dynamic off of a list of context questions encountered while parsing the input file
fieldnames=reader.fieldnames #read existing feildnames



#context variables headings
fieldnames.append("Name of project")
fieldnames.append("Name of PI or project lead(s)") #append new 
fieldnames.append("Please enter your name")
fieldnames.append("Type of project")
fieldnames.append("Project stage")
fieldnames.append("Year awarded")
fieldnames.append("Faculty_School")
fieldnames.append("Department")
fieldnames.append("Short description of project")
fieldnames.append("Primary course format")
fieldnames.append("Course_Level")
fieldnames.append("Course type")
fieldnames.append("Enrolment cap")
fieldnames.append("Course location")
#for Sankey diagram
fieldnames.append("source")
fieldnames.append("target")
fieldnames.append("source long name")
fieldnames.append("target long name")
fieldnames.append("value")
#for the heat maps
fieldnames.append("matrix") #will be either innovationXimpact or impactXapproach 

#context variables
Name_of_Project = ""
Name_of_PI_or_project_lead = ""
EnterersName = ""
Type_of_project = ""
Project_Stage = ""
Year_Awarded = ""
Faculty_School = ""
Department = ""
Short_description_of_project = ""
Course_Format = ""
Course_Level = ""
Course_Type = ""
Enrolment_Cap = ""
Course_Location = ""
#for Sankey diagram
source = ""
target = ""
source_long_name = ""
target_long_name = ""

value = 1
#for the heat maps
matrix = "" 

internalIDnum = -1 #used in differentiating the different surveys. When it changes, reset the context variables
	
#for testing purposes
Name_of_Project = 'testTEST 1'	


#collection of regular expressions
innovationListRE = re.compile('\[Elements_of_Innovation_list\]') # used for filtering out the innovation list

nameOfProjectRE = re.compile("Name of project")
Name_of_PI_or_project_leadRE = re.compile("Name of PI or project lead")
EnterersNameRE = re.compile("Please enter your name")
Type_of_projectRE = re.compile("Type of project")
Project_StageRE = re.compile("Project stage")
Year_AwardedRE = re.compile("Year awarded")
Faculty_SchoolRE = re.compile("Faculty/School")
DepartmentRE = re.compile("Department")
Short_description_of_projectRE = re.compile("Short description of project")
Course_FormatRE = re.compile("Primary course format")
Course_LevelRE = re.compile("Course level")
Course_TypeRE = re.compile("Course type")
Enrolment_CapRE = re.compile("Enrolment cap") 
Course_LocationRE = re.compile("Course location")


wordFromQuestionRE = re.compile("\|\s([^\t]*)") #everything after the | and before the tab. 
matrixRE = re.compile("\[[a-z_]*") #matches [ and then lower case letters and underscore   ex)[innova_impact or [immp_eval
#notExamplesRE = re.compile("\([^\)]*\)") #matches stuff in parenthesis including the parenthesis
notExamplesRE = re.compile("(^.*)\(") #want everything from the start of the line till a (  
#notExamplesRE = re.compile(".*") 


ofile = open(outputFileName, 'w',encoding="utf_8",newline='',errors="surrogateescape")

writer=csv.DictWriter(ofile,fieldnames=fieldnames,dialect="excel-tab",restval="")  #option to quote stuff here but doesn't seem to work when using d3.tsv.parse (on a local file) instead of just d3.tsv and linking the file in

writer.writeheader() #write hearder for CSV file

for row in reader:

	print('here', row, '\n')

	
	if row["Internal ID"] != internalIDnum: #indicates bnew survey data
		internalIDnum=row["Internal ID"] 
		
		Name_of_Project = ""
		Name_of_PI_or_project_lead = ""
		EnterersName = ""
		Type_of_project = ""
		Project_Stage = ""
		Year_Awarded = ""
		Faculty_School = ""
		Department = ""
		Short_description_of_project = ""
		Course_Format = ""
		Course_Level = ""
		Course_Type = ""
		Enrolment_Cap = ""
		Course_Location = ""

	if innovationListRE.match(row["Question"])!=None:#if it's != None then it's found :)
		continue  #don't do anything when you see these. essentially delete these rows
		
	if nameOfProjectRE.match(row["Question"])!=None:
		Name_of_Project = row["Comment"]
		continue
	if Name_of_PI_or_project_leadRE.match(row["Question"])!=None:
		Name_of_PI_or_project_lead = row["Comment"]
		continue
	if EnterersNameRE.match(row["Question"])!=None:
		EnterersName = row["Comment"]
		continue	
	if Type_of_projectRE.match(row["Question"])!=None:
		Type_of_project = row["Response"]
		continue
	if Project_StageRE.match(row["Question"])!=None: 
		Project_Stage = row["Response"]
		continue
	if Year_AwardedRE.match(row["Question"])!=None: 
		Year_Awarded = row["Comment"]
		continue
	if Faculty_SchoolRE.match(row["Question"])!=None:
		Faculty_School = row["Response"]
		continue
	if DepartmentRE.match(row["Question"])!=None: 
		Department = row["Comment"]
		continue
	if Short_description_of_projectRE.match(row["Question"])!=None:
		Short_description_of_project = row["Comment"]
		continue
	if Course_FormatRE.match(row["Question"])!=None:
		if Course_Format == "":	Course_Format = row["Response"]
		else: Course_Format = Course_Format + ", " + row["Response"]
		continue
	if Course_LevelRE.match(row["Question"])!=None:
		if Course_Level == "": Course_Level = row["Response"]
		else: Course_Level = Course_Level + ", " + row["Response"]
		continue
	if Course_TypeRE.match(row["Question"])!=None:    
		if Course_Type == "": Course_Type =  row["Response"]
		else: Course_Type = Course_Type + ", " + row["Response"]
		continue
	if Enrolment_CapRE.match(row["Question"])!=None:  
		Enrolment_Cap = row["Response"]
		continue
	if Course_LocationRE.match(row["Question"])!=None:
		if Course_Location == "": Course_Location = row["Response"]
		else: Course_Location = Course_Location + ", " + row["Response"]
		continue
		
		
		
	#get some data about the nature of the question	
	print(row["Question"])
	m2 = matrixRE.match(row["Question"])

	try:
		if "If you selected" in row["Question"]:
			continue
		elif m2.group() == "[innova_impact": 
			matrix = "innovationXimpact"
		elif m2.group() == "[immp_eval": 
			matrix = "impactXapproach"
		else: matrix = ""

	except AttributeError:

		print(row)
	
	#print (matrix)	
	# parse out the part of the question that contains the source part of the link pairing.
	#ex: [INN_IMP.5] What is the impact of… [ELEMENT OF INNOVATION] on… [INTENDED AREA OF IMPACT] ? (choose all that apply) | In-class content delivery (e.g., demos)
	# should just be "In-class content delivery (e.g., demos)" in the source 
	
	m = wordFromQuestionRE.search(row["Question"])	# search() searches within the string, match() only matches if the string starts with the pattern. 
	
	if m: #m will be false if there isn't a match
		#print (m.group(1))
		
		source_long_name = m.group(1)
		source = source_long_name
		if notExamplesRE.search(source_long_name) !=None:
			source = notExamplesRE.search(source_long_name).group(1).rstrip() #rstip to remove trialling whitespace
		#I want to check if there is a match. then if there is, set the source to the first group of that
		#do this for the source and the target. THANKS Rama :) 
		
	
		#print(notExamplesRE.search(source_long_name).group(1))
		#print("source short name: " + source+ "###")
		#source = notExamplesRE.search(source_long_name).group(1)
		#print("source long name: " + source_long_name)
		
		target_long_name = row["Response"]
		target = target_long_name.rstrip()
		if notExamplesRE.search(target_long_name) !=None:
			target = notExamplesRE.search(target_long_name).group(1).rstrip()  #rstip to remove trialling whitespace
		#print("target long name: " + target_long_name)
		#print("target short name: " + target+ "###")
		
		
		
		if (source == "Other" and matrix == "impactXapproach"): 
			source = "Other Area of Impact"
			source_long_name = "Other Area of Impact"
		if (target == "Other" and matrix == "innovationXimpact" ):
			target = "Other Area of Impact"	
			target_long_name  = "Other Area of Impact"	
				
	else:
		source = ""
		target = ""
		#print (m)	
	
	

	
	row.update({"Name of project":Name_of_Project,"Name of PI or project lead(s)":Name_of_PI_or_project_lead,"Please enter your name":EnterersName,"Type of project":Type_of_project,"Project stage":Project_Stage,"Year awarded":Year_Awarded,"Faculty_School":Faculty_School,"Department":Department,"Short description of project":Short_description_of_project,"Primary course format":Course_Format,"Course_Level":Course_Level,"Course type":Course_Type,"Enrolment cap":Enrolment_Cap,"Course location":Course_Location,"source":source,"source long name":source_long_name,"target":target, "target long name":target_long_name, "value":value, "matrix":matrix})	
		
	writer.writerow(row)

		
csvfile.close()
ofile.close()


