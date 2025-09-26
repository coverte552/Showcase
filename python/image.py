import subprocess

#-----------------------------image.py-------------------------
#This script is used to image virtual machines with needed applications, but is most definetely outdated.
#Features:
#-Runs multiple install types based on needs.
#-Updates before installing
#-Prompts for reboots
#Use case:
#Users can change and use their systems differently, and it may be needed to re-image them every night in cases similar to this.

#Variables for bash command function
showOutput = True #Shows ouput
noShow = False #Doesn't show output

class Colors:
    Error = '\033[91m' #Errors
    Info = '\033[92m' #Information from the script
    RESET = '\033[0m' # Reset, blank text for console information

def run_bash_commands(commandString, show):
    #Check if the command is a string, if it is convert the string to a array with one element
    if isinstance(commandString, str):
        command = [commandString]  # Convert the string command into a array with one element
    else:
        command = commandString
    #Run each command in the array, this way if the install process has multiple steps it works correctly
    for cmd in command:
        print(f"This is the command string: {cmd}")
        result = subprocess.run(
            [cmd],
            text=True,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
        )
        show_bash_error(result)
        if (show == True): 
            print(result.stdout)
    

def show_bash_error(result):
    if(result.returncode == 1):
        print(f"{Colors.Error}There was an error running the bash command{Colors.RESET}\n{result.stderr}")

#Yes or no Funciton
def yesOrNo(string):
    while True:
        answer = input(f"{string} (yes/no): ").lower()
        if answer in ["yes", "y"]:
            return True
        if answer in["no", "n"]:
            return False
        else:
            print(f"{Colors.Error}Incorrect input{Colors.RESET}")

#Different Mongo COmmand
#Mongo server was strange to install. But technically through this method it is downloaded and unpackaged into it's own directory. So I consider that installed.
#Plus this is the way the install page directs you to install it.
newMongoDbServer = [
    'curl -O http://downloads.mongodb.org/linux/mongodb-linux-x86_64-2.2.7.tgz',
    'tar -zxvf mongodb-linux-x86_64-2.2.7.tgz',
    'mkdir -p mongodb',
    'cp -R -n mongodb-linux-x86_64-2.2.7/ mongodb',
    'curl -O http://downloads.mongodb.org/linux/mongodb-linux-i686-2.2.7.tgz',
    'tar -zxvf mongodb-linux-i686-2.2.7.tgz',
    'mkdir -p mongodb',
    'cp -R -n mongodb-linux-i686-2.2.7/ mongodb',
    'mkdir -p /data/db',
]

# Array of software names, if they are to be installed, and their installation command
softwareList = [
    ["Visual Code", " ", "snap install --classic code"],
    ["GIMP", " ", "apt-get install -y gimp"],
    ["Blender", " ", "apt-get install -y blender"],
    ["OBS", " ", "apt-get install -y obs-studio"],
    ["Gnome Tweaks", " ", "apt-get install -y gnome-tweaks"], 
    ["VLC", " ", "apt-get install -y vlc"],
    ["Node JS", " ", "apt-get install -y nodejs"],
    ["Mongo DB Server", " ", newMongoDbServer],  
    ["Mongo DB Compass", " ", 'apt-get install -y mongodb-mongosh'],  
    ["Figma", " ", "snap install figma-linux"],
    ["Enpass", " ", "snap install enpass"],
    ["Chromium", " ", "apt-get install -y chromium-browser"],
    ["Inkscape", " ", "apt-get install -y inkscape"],
    ["X-Mind", " ", "snap install xmind"],
    ["Discord", " ", "snap install discord"],
    ["CIFS", " ", "apt-get install -y cifs-utils"],
    ["Wine", " ", "apt-get install -y wine"],
    ["Zoom", " ", "snap install zoom-client"],
    ["Git", " ", "apt-get install -y git"],
    ["Putty", " ", "apt-get install -y putty"],
    ["Curl", " ", "apt-get install -y curl"],
    ["Docker", " ", "apt-get install -y docker"],  
    ["Postgresql", " ", "apt-get install -y postgresql postgresql-contrib"],
    ["Golang", " ", "apt-get install -y golang-go"],
    ["Spotify", " ", "snap install spotify"],
    ["Postman", " ", "snap install postman"],
]

#Valid selection as true to not print error message
validSelection = True
#Run true, to loop until user wants it to stop.
run = True
while run == True:
    while True:
            #Clear it so it acts like a cheklist
            run_bash_commands("clear", showOutput)

            print(f"Please select a Software to install.\n Select it again to de-select it.\n {Colors.Error}This script only installs software. Uninstallation must be done manually.{Colors.RESET}")
            print(f"{Colors.Info}--------------------Software--------------------{Colors.RESET}")
            #Loop to display all softwares and their selected option
            for i, softwareSelection in enumerate(softwareList):
                checked = softwareSelection[1]
                software = softwareSelection[0]
                print(f"    {i +1}: [{checked}] {software}")

            #Print the extra script options
            print(f"{Colors.Info}--------------------Controls--------------------{Colors.RESET}")
            print("    27: All\n    28: None\n    29: Run")

            #Moved this down here so it looks better, displays if the previous selection was correct.
            if validSelection == False:
                print(f"{Colors.Error}Invalid selection. Please enter a valid number.{Colors.RESET}")
            else:
                print() #Blank line for consistency in the interface

            # Get user input for selection
            selected_index = input("Enter the number of the software you want to install: ")
            try:
                # Convert input to integer and adjust for zero-indexing
                selected_index = int(selected_index) - 1

                # Check if the selected index is within bounds
                if 0 <= selected_index < len(softwareList):
                    # Mark the selected software with either X for marked, or blank for not marked.
                    if softwareList[selected_index][1] == 'X':
                        softwareList[selected_index][1] = ' '
                        validSelection = True
                    else:
                        softwareList[selected_index][1] = "X"
                        validSelection = True
                # Check for other inputs to control the script
                #Select all
                elif selected_index == 26:
                    for softwareSelection in softwareList:
                        softwareSelection[1] = "X"
                #Select none
                elif selected_index == 27:
                    for softwareSelection in softwareList:
                        softwareSelection[1] = " "
                #Run the rest of the script
                elif selected_index == 28:
                    break
                #If it doesn't fit within the bounds, print a error
                else:
                    validSelection = False
            #Any errors, like using words instead of numbers, will also print a error
            except:
                validSelection = False

    #Sudo apt update
    print("Getting latest packages...")
    try:
        run_bash_commands("apt update", showOutput)
        print(f"{Colors.Info}Got latest Packages!{Colors.RESET}")
    except:
        print(f"{Colors.Error}Fatal Error! Could not Get latest Packages!\n Ensure this is run as Sudo\n Exiting.{Colors.RESET}")
        #Exit because if it cant do this the rest wont work.
        exit()

    # Check if each index is checked and print the resulting process
    for i, softwareSelection in enumerate(softwareList):
        check = softwareSelection[1]
        software = softwareSelection[0]
        command = softwareSelection[2]
        #If software has a check in the array then install the software
        if check == "X":
            try:
                print(f"{Colors.Info}--------------------{software}--------------------{Colors.RESET}")
                print(f"Installing Software: {software}...")
                run_bash_commands(command, showOutput)
                print(f"{Colors.Info}Successfully Installed {software}!{Colors.RESET}")
            except:
                #If it doesnt work, say it didnt then move on
                print(f"{Colors.Error}Could not Install {software}!{Colors.RESET}")

    #Ask user to reboot after 
    print(f"{Colors.Info}It is recommended you restart your system after installing any software.{Colors.RESET}")
    reboot = yesOrNo("Would you like to reboot?")
    if reboot == True:
        print(f"{Colors.Error}Rebooting...{Colors.RESET}")
        run_bash_commands("reboot", noShow)
    else:
        #If no reboot, ask to run script again
        print(f"{Colors.Info}No reboot requested.{Colors.RESET}")

        run = yesOrNo("Do you want to run the script again?")
