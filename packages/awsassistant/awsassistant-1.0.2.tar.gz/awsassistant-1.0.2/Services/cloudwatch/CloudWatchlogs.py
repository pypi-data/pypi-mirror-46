import os
import sys
# print(sys.path)
import boto3,logging
import time,json,sys
import datetime 
from os import system
from pprint import pprint
from pytz import timezone 
# from colorama import Fore, Back, Style
from prettytable import PrettyTable
# from display.DisplayData import DisplayList
from DisplayData import DisplayList
PATH =  os.environ['HOME']
PATH +="/ReferReferencofLogGrop"
FILEPATH = PATH+'/ReferencofLogGrop.json'

if os.path.isdir(PATH) == False:
    os.mkdir(PATH)

def prGreen(skk): return("\033[92m {}\033[00m" .format(skk))
def prCyan(skk): return("\033[96m {}\033[00m" .format(skk))
def prRed(skk): return("\033[91m {}\033[00m" .format(skk)) 
def prYellow(skk): return("\033[93m {}\033[00m" .format(skk))      

def help():
    t = PrettyTable(['Command No', 'Description'])
    t.add_row(["CloudWatchlogs",prCyan("To Configure")])
    t.add_row(["CloudWatchlogs -help", prCyan("To View help")])
    t.add_row(["CloudWatchlogs -t [shorthand] -starttime [2019-05-25_15:30:5]", prCyan("To view logs realtime ")])
    t.add_row(["CloudWatchlogs -t [shorthand] -time ", prCyan("To view time of which the logs are fetching")])
    print(t)

def Configure():
    object = GetCloudWatchLogs()
    while True:
            print("Press Enter to Continoue")
            s = sys.stdin.read(1)
            system('clear')
            print(s)
            t = PrettyTable(['Command No', 'Description'])
            t.add_row(["1",prCyan("For Display ReferencofLogGrop")])
            t.add_row(["2", prCyan("Display all logGroup")])
            t.add_row(["3", prCyan("Add ReferencofLogGrop")])
            t.add_row(["4", prCyan("To View help")])
            print(t)
            print(prCyan("To View Logs \nRun Follwing Command Directly")+"\n[shorthand] prod")
            print(prRed("Type 99 To Exit \n"))
            userInput = input("Enter The following Option:- ")
            if(isinstance(userInput,str)):
                #print(userInput in object.ReferencOfLogGroup.keys())
                if (userInput in  object.ReferencOfLogGroup.keys()):
                    object.TailLogGroup(userInput,displaytime=True)
                else:
                    try:
                        userInput = int(userInput)
                    except Exception as _:
                        print(prRed('Enter proper Short hand, Press 1  to see all shorthands'))
                        pass

            if userInput == 1:
                object.DisplayReferencOfLogGroup()
            elif userInput == 2:
                userInput = input("Enter Region Name default:-us-west-2 :- ")
                if userInput == '':
                    userInput = 'us-west-2'
                object.ListLogs(region_name=userInput)
                DisplayList(object.ledger)
                # object.DisplayLogs()
            elif userInput == 3:
                key = input("Short hand term for loggroup:- ")
                userInput = input("Enter Region Name default:-us-west-2 :- ")
                if userInput == '':
                    userInput = 'us-west-2'
                object.ListLogs(region_name=userInput)
                
                data = object.ledger
                output = DisplayList(data)
                object.AddReferencOfLogGroup(key,output)
                object.TailLogGroup(key,displaytime=True)
            elif userInput == 99:
                print("Thank You for Using DevCloud © -"+prRed('axion1997'))
                exit()   
            elif userInput == 4:
                help()

class  GetCloudWatchLogs():
    def __init__(self):
        self.ledger = []
        self.ReferencOfLogGroup = self.LoadReferencOfLogGroup()
        self.client = 1

    def LoadReferencOfLogGroup(self):
        try:
            File = open(FILEPATH,'r')
            ReferencOfLogGroup =json.loads(File.read())
            return ReferencOfLogGroup
        except Exception as _:
            return {}
   
    def DisplayReferencOfLogGroup(self):
        try:
            File = open(FILEPATH,'r')
            ReferencOfLogGroup =json.loads(File.read())
            print(prGreen('-')*10)
            for k,v in ReferencOfLogGroup.items():
                print(prGreen(k),'\t',v)
            print(prGreen('-')*10)
        except Exception as _:
            pass

    def AddReferencOfLogGroup(self,key,output):
        try:
            File = open(FILEPATH,'r')
            ReferencOfLogGroup =json.loads(File.read())
            File.close()
        except Exception as _ :
            ReferencOfLogGroup={}

        ReferencOfLogGroup[key] = output
        File = open(FILEPATH,'w')
        a = json.dumps(ReferencOfLogGroup,indent=4, sort_keys=True)
        File.write(a)
        File.close()
    
    def ListLogs(self,region_name):
        self.client = boto3.client('logs',region_name = region_name)
        response = self.client.describe_log_groups()
        
        for data in response['logGroups']:
            self.ledger.append({'Name':data['logGroupName'],'region':region_name})

    def GetshorthandValue(self,shorthand):
        try:
            File = open(FILEPATH,'r')
            ReferencOfLogGroup =json.loads(File.read())
            File.close()
            return(ReferencOfLogGroup[shorthand])
        except Exception as _:
            print("Enter Proper Shorthand\n")
            Configure()


    def Checkregion(self,region_name):
        if region_name == 'us-west-2':
            return datetime.datetime.utcnow
        elif region_name == 'ap-south-1':
            return datetime.datetime.now

    def checkepoch(self,startTime,region_name):
        if region_name == 'us-west-2':
            startTime = startTime + 19800
            return startTime
        elif region_name == 'ap-south-1':
            return startTime        

    def TailLogGroup(self,shorthand,startTime = None,endTime=None,displaytime=None):
        try:
            data = self.GetshorthandValue(shorthand)
        except Exception as _:
            print("Enter Proper Shorthand\n")
            Configure()
        
        region_name = data['region']
        logGName = data['Name']
        gettime = self.Checkregion(region_name)
        if startTime == None:
            STime = gettime()
            startTime = int(STime.strftime('%s'))
            currenttime = int(gettime().strftime('%s'))
            print(logGName," Is started to tail from ",time.ctime(startTime))
        elif startTime != None:
            print(startTime)
            currenttime = int(gettime().strftime('%s'))
            epo = datetime.datetime.strptime(startTime,"%Y-%m-%d_%H:%M:%S")
            startTime = int(epo.strftime('%s'))
            print(startTime)

        
        while True:
            t1 = time.time()
            self.client = boto3.client('logs',region_name = region_name)
            
            response = self.client.filter_log_events(
                logGroupName=logGName,
                startTime=(startTime - 30)*1000,
                endTime=currenttime *1000
            )
            # pprint(response)
            if displaytime == True:
                timetoshow = time.ctime(self.checkepoch(startTime,region_name)-10) + "-" + time.ctime(self.checkepoch(currenttime,region_name)) +"-"+str(len(response['events']))
                # print(time.ctime(self.checkepoch(startTime,region_name)-10),'-',time.ctime(self.checkepoch(currenttime,region_name)),len(response['events']))
                print(prYellow(timetoshow))

            for data in response['events']:
                print(data['message'])

            # print(time.ctime(self.checkepoch(startTime,region_name)-10),'-',time.ctime(self.checkepoch(currenttime,region_name)),len(response['events']))
            # STime = gettime()
            startTime = startTime + 10#int(STime.strftime('%s'))
            # startTime = #int(STime.strftime('%s'))
            currenttime = startTime

            deta  = 10-(time.time()-t1)
            if(deta <= 0):
                pass
            else:
                time.sleep(deta)

    def DisplayLogs(self):
        t = PrettyTable(['Sr', 'LogGroupName','Region'])
        for i in range(len(self.ledger)):
            t.add_row([i,self.ledger[i]['Name'],self.ledger[i]['region']])
        print(t)


def ArgumentforCloudwatch(argument):
    #argument = sys.argv[1:]
    # print(argument,len(argument))
    length = len(argument)
    if length == 0:
        Configure()
    elif argument[0] == '-help':
        help()
    elif argument[0] == '-t':
        print("k")
        # print(length)
        if length == 2:
            shorthand = argument[1]
            object = GetCloudWatchLogs()
            object.TailLogGroup(shorthand)
        elif length == 3 :
            if argument[2] == '-time':
                shorthand = argument[1]
                object = GetCloudWatchLogs()
                object.TailLogGroup(shorthand,displaytime=True)
        elif length == 4 : 
            argument[2] == '-starttime'
            short = argument[1]
            startTime = argument[3]
            object = GetCloudWatchLogs()
            object.TailLogGroup(shorthand=short ,startTime=startTime)
        else:
            print('wrong')

# if __name__ == "__main__":
#     try:
#         # Configure()
#         argument = sys.argv[1:]
#         print(argument,len(argument))
#         length = len(argument)
#         if length == 0:
#             Configure()
#         elif argument[0] == '-help':
#             help()
#         elif argument[0] == '-t':
#             print("k")
#             # print(length)
#             if length == 2:
#                 shorthand = argument[1]
#                 object = GetCloudWatchLogs()
#                 object.TailLogGroup(shorthand)
#             elif length == 3 :
#                 if argument[2] == '-time':
#                     shorthand = argument[1]
#                     object = GetCloudWatchLogs()
#                     object.TailLogGroup(shorthand,displaytime=True)
#             elif length == 4 : 
#                 argument[2] == '-starttime'
#                 short = argument[1]
#                 startTime = argument[3]
#                 object = GetCloudWatchLogs()
#                 object.TailLogGroup(shorthand=short ,startTime=startTime)
#             else:
#                 print('wrong')

#     except Exception as identifier:
#         logging.exception(identifier)
#         # python3 CloudWatchlogs.py -t 5 now
#         # python3 CloudWatchlogs.py -list
#         # python3 CloudWatchlogs.py -t 5 2019-05-25 15:30:5
#         # python3 CloudWatchlogs.py -d 5 2019-05-25 15:30:5 2019-05-25 15:30:5
    