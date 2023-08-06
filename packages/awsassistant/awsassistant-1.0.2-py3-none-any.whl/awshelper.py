import sys
import logging
print(sys.path)
from prettytable import PrettyTable
import cloudwatch.CloudWatchlogs 
# cloudwatch.CloudWatchlogs.Configure()
# s =CloudWatchlogs.GetCloudWatchLogs()
# Configure()
def prGreen(skk): return("\033[92m {}\033[00m" .format(skk))
def prCyan(skk): return("\033[96m {}\033[00m" .format(skk))
def prRed(skk): return("\033[91m {}\033[00m" .format(skk)) 
def prYellow(skk): return("\033[93m {}\033[00m" .format(skk))    

class Services():
    def __init__(self):
        pass
    def CloudWatchlogs(self):
        cloudwatch.CloudWatchlogs.Configure()
    def DisplayHelp(self):
        t = PrettyTable(['Flags', 'supported Servies'])
        t.add_row(["logs",prCyan("To view Logs")])
        t.add_row(["[ServiceName ] -help",prCyan("To view help of Service")])
        print(t)

    

def main():
    try:
        argument = sys.argv[1:]
        length = len(argument)
        object = Services()
        
        if length == 0:
            object.DisplayHelp()
        elif argument[0] == '-help':
            object.DisplayHelp()
        elif argument[0] == 'logs':
            if length == 1:
                cloudwatch.CloudWatchlogs.Configure()    
            if length == 2:
                argumentforlogs = argument[1:]
                # print(argumentforlogs)
                cloudwatch.CloudWatchlogs.ArgumentforCloudwatch(argumentforlogs)
            if length == 3:
                argumentforlogs = argument[1:]
                # print(argumentforlogs)
                cloudwatch.CloudWatchlogs.ArgumentforCloudwatch(argumentforlogs)
    except Exception as identifier:
        logging.exception(identifier)
        # python3 CloudWatchlogs.py -t 5 now
        # python3 CloudWatchlogs.py -list
        # python3 CloudWatchlogs.py -t 5 2019-05-25 15:30:5
        # python3 CloudWatchlogs.py -d 5 2019-05-25 15:30:5 2019-05-25 15:30:5
    

main()