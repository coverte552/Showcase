import subprocess
import argparse

#Variables for bash command function
showOutput = True #Shows ouput
noShow = False #Doesn't show output

#Colors for text
class Colors:
    Error = '\033[91m' #User Errors
    Info = '\033[92m' #Information from the script
    RESET = '\033[0m' # Reset, blank text for console information

#Print bash errors
def show_bash_error(result):
    if(result.returncode == 1):
        print(f"{Colors.Error}There was an error running the bash command{Colors.RESET}\n{result.stderr}")

#Run bash commands
def run_bash_commands(commandString, show):
    result = subprocess.run(
        [commandString],
        text=True,
        shell=True,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        check=True
    )
    show_bash_error(result)
    #Check to see if output is to be dsplayed
    if (show == True): 
        print(result.stdout)
    return result

#Get user input for NICE
def getNICE():
    valid = False
    while valid == False:
        newNICE = input(f"{Colors.Info}Enter the value of your new NICE value, ranking -20 to 19:{Colors.RESET} ")
        valid = validNICE(newNICE)
        if valid == True:
            return newNICE  
        else:
            print(f"{Colors.Error}Not a valid NICE value.{Colors.RESET}")

#Check if the number is a valid NICE amount
def validNICE(number):
    valid_nice = False
    try:
        NICE = int(number) #Confirm info entered is a integer
        valid_nice = -20 <= NICE <= 19 #Cehck if number follows NICE parameters
        return valid_nice #if a integer return wether or not it follows parameters
    except (ValueError): #If not a integer, return the false valid value
        return valid_nice

#Get user input for Process ID
def getPID():
    userInt = 0
    valid = False
    while valid == False:
        showProc()   
        userInt = input(f"{Colors.Info}Please Enter the PID of the process you wish to change:{Colors.RESET} ")
        valid = validPID(userInt)
        if (valid == True):
            print(f"{Colors.Info}You wish to change the NICE of Process:{Colors.RESET}")
            run_bash_commands(f"ps -p {userInt} -o comm=", showOutput)
            print(f"{Colors.Info}With current NICE value:{Colors.RESET}")
            run_bash_commands(f"ps -p {userInt} -o nice=", showOutput)
            return userInt
        else:
            print(f"{Colors.Error}Invalid PID. Please enter an valid Process ID (PID).{Colors.RESET}")
            
#Check if the entered number is a valid Process.
def validPID(number):
    try:
        run_bash_commands(f"ps -p {number} -o comm=", noShow) #Run a command to search for the process by ID
        return True 
    except (subprocess.CalledProcessError): #If no process is returned, false returned.
        return False
    
# Show the list of processes ranked by nice value, decending.
def showProc():
    run_bash_commands("ps -eo pid,ni,comm --sort=-ni", showOutput) #Command to show processes, PID, and NICE
    print(f"{Colors.Info}Here are all processes ranked by priority.{Colors.RESET}")
    print() #Blank line for easy reading

#Change the NICE
def changeProcNICE(procID, NICE):
    try:
        run_bash_commands(f"renice {NICE} -p {procID}", showOutput) #command to change nice, showing output
    except (subprocess.CalledProcessError):
        print(f"{Colors.Error}Invalid authority. Run as sudo.{Colors.RESET}")
        
# CLI Args 
parser = argparse.ArgumentParser(description="A script to change process priority")
parser.add_argument('-p', '--pid', type=str, help="enter the proccess ID (PID) of you wish to change NICE value of.")
parser.add_argument('-n', '--nice', type=str, help=" Enter the new NICE value for your priority.")
cli_args = parser.parse_args()

#Check for CLI args. If none prompt User
if (cli_args.pid == None): 
    procID = getPID()

if (cli_args.nice == None):
    NICE = getNICE()

#if both are present assign variables accordingly
#Assume if user is smart enough to use CLI Args they don't need the proccess list
#If the entered CLI is not valid, prompt

if (cli_args.pid != None): 
    if validPID(cli_args.pid) == False: 
        print(f"{Colors.Error}Invalid PID CLI Arg. Please Enter manually.{Colors.RESET}")
        procID = getPID()
    else:
        procID = cli_args.pid 

if (cli_args.nice != None):
    if validNICE(cli_args.nice) == False: 
        print(f"{Colors.Error}Invalid NICE CLI Arg. Please enter manually.{Colors.RESET}")
        NICE = getNICE()
    else:
        NICE = cli_args.nice

#Execute the change Nice process, Nice.
changeProcNICE(procID, NICE)