import subprocess
import shutil

#-----------------------------usergroup.py-------------------------
#This script creates users and groups, adds users to groups, and grants sudo permissions to said groups.
#Features:
#-Interactive Menu
#-Validation
#-Troubleshooting Menu
#Use case:
#Managing large groups of users in a linux enviroment

#Commands for troubleshooting:
# Switch to root user: sudo su - 
# Create User: useradd {user}
# Check for user: id {user}
# Remove User: userdel {name}
# Remove user and directory: userdel -r {user}
# Remove user directory: rm -r {directory}

# Create Group: sudo groupadd {group}
# Check for group: getent group {group}
# Change users group: sudo usermod -aG {group} {user}
# Remove group: sudo groupdel {group}

#Variables for bash command function
showOutput = True #Shows ouput
noShow = False #Doesn't show output

#Colors for text
class Colors:
    Error = '\033[91m' #User Errors
    Info = '\033[92m' #Information from the script
    RESET = '\033[0m' # Reset, blank text for console information

#Run bash commands
def run_bash_commands(commandString, show):
    print(f"This is the command string: {commandString}")
    result = subprocess.run(
        [commandString],
        text=True,
        shell=True,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        check=True,
    )
    show_bash_error(result)
    #Check to see if output is to be dsplayed
    if (show == True): 
        print(result.stdout)
    return result

def show_bash_error(result):
    if(result.returncode == 1):
        print(f"{Colors.Error}There was an error running the bash command{Colors.RESET}\n{result.stderr}")

#get alphabetical strings
def get_alpha_string(message, error_message):
    valid = False
    only_chars = False
    user_name = ""
    while(valid == False): #Run this loop until the user name is only letters
        user_name = input(message) #Get the input from the user
        only_chars = user_name.isalpha() #Check to see if the user name is only alpha/chars
        if(only_chars == False):
            print(error_message) #If there is something other than letter print error
        elif(only_chars == True):
            valid = True #If only letters then end the loop
    return user_name

#Get User
def getUserName():
    user_name = get_alpha_string(
        f"{Colors.Info}Please enter the new user name: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
    return user_name


#Get Pass
def getUserPass():
    password = get_alpha_string(
        f"{Colors.Info}Please enter the password for {user_name}: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
    return password

#Create the user
def createUser(username, password):
    try:
        run_bash_commands(f"useradd {user_name}", noShow)
        run_bash_commands(f"echo '{user_name}:{password}' | chpasswd", noShow)
        print(f"\n{Colors.Info}Success in making User. \n Name: {user_name} \n Password: {password}{Colors.RESET}")
        run_bash_commands(f"id {username}", showOutput)
    except(subprocess.CalledProcessError):
        print(f"\n{Colors.Error}Error Making the user.\n Do they already exist?\n Do you have permissions?{Colors.RESET}")

#Get Group
def getGroup():
    group = get_alpha_string(
    f"{Colors.Info}Please enter the name of your group: {Colors.RESET}",
    f"{Colors.Error}Only letters please!{Colors.RESET}")
    return group

#Create Group
def createGroup(name):
    try:
        run_bash_commands(f"groupadd {group}", noShow)
        print(f"\n{Colors.Info}Group {name} created successfully!{Colors.RESET}")
        run_bash_commands(f"getent group {group}", showOutput)
    except(subprocess.CalledProcessError):
        print(f"\n{Colors.Error}Error creating group. \nDo they already exist?\n Do you have permissions?{Colors.RESET}")
       
#Check if user exists
def validUser(user):
    try:
        if user == "":
            raise subprocess.CalledProcessError
        run_bash_commands(f"id {user}", noShow)
        return True
    except(subprocess.CalledProcessError):
        print(f"\n{Colors.Error}User does not exist!{Colors.RESET}")
        return False

#Check if group exists.
def validGroup(group):
    try:
        if group == "":
            raise subprocess.CalledProcessError
        run_bash_commands(f"getent group {group}", noShow)
        return True
    except(subprocess.CalledProcessError):
        print(f"\n{Colors.Error}Group does not exist!{Colors.RESET}")
        return False

# Add user to group.
def addUser(user, group):
    try:
        run_bash_commands(f"sudo usermod -aG {group} {user}", noShow)
        print(f"\n{Colors.Info}Added {user} to {group} successfully!{Colors.RESET}")
        print(f"\n{Colors.Info}Here are the groups {user} is a member:{Colors.RESET}")
        run_bash_commands(f"groups {user}", showOutput)
    except:
        print(f"\n{Colors.Error}Error adding {user} to {group}.\n Are they already in it?\n Do you have permissions? {Colors.RESET}")

def sudoGroup(groupName):
    try:
        # Paths to files
        sudoers_file = "/etc/sudoers"
        sudoers_temp_copy = "/etc/sudoers.tmp"
        sudoers_backup = "/etc/sudoers.backup"

        #Create a backup for any errors, just in case
        print(f"Creating backup sudoers file...")
        shutil.copy(sudoers_file, sudoers_backup)
        print(f"{Colors.Info}Backup sudoers file created in '/etc/sudoers.backup'. Delete if everything was successful.{Colors.RESET}")

        # Open the original sudoers file 
        with open(sudoers_file, 'r') as f_src:
            # Create a temporary copy of the sudoers file
            with open(sudoers_temp_copy, 'w') as f_dst:
                # Copy contents from the original sudoers file to the temporary copy
                for line in f_src:
                    # Write the line from the original sudoers file to the temporary copy
                    f_dst.write(line)
                    # Look for the line that starts with '%sudo'
                    if line.startswith('%sudo'):
                        # Add the new line for the group below the '%sudo' line
                        f_dst.write(f"%{groupName}   ALL=(ALL:ALL) ALL\n")

        # Replace the original sudoers file with the modified temporary copy
        shutil.move(sudoers_temp_copy, sudoers_file)

        print(f"Successfully added {groupName} to sudoers.")
    except Exception as e:
        print(f"{Colors.Error}Could not add group to sudo.\n Check files and replace original with backup if neccesary.{Colors.RESET}")
        print(f'Error: {e}')


# ------------- Begin ---------------
print(f"{Colors.Info}Welcome to the User/Group Script.{Colors.RESET}")
print(f"{Colors.Error}Ensure this script is run as sudo.{Colors.RESET}")
#Switch to check for which option
while True:
    print(f"{Colors.Info}Options:\n{Colors.RESET}\n1. Create User\n2. Create Group\n3. Add User to Group\n4. Set User Sudo\n5. Set Group Sudo\n6. Show User Info.\n7. Show Group Info\n8. Exit")
    choice = input(f"\n{Colors.Info}Enter your choice: {Colors.RESET}")

    #Create User
    if choice == "1":
        user_name = getUserName()
        password = getUserPass()
        createUser(user_name, password)

    #Create Group
    elif choice == "2":
        group = getGroup()
        createGroup(group)

    #Add User to Group
    elif choice == "3":
        #Show the users
        print(f"{Colors.Info}Here are all availible Users.{Colors.RESET}")
        run_bash_commands("awk -F: '{ print $1 }' /etc/passwd", showOutput)
        user_name = get_alpha_string(
        f"{Colors.Info}Please enter the user's name: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
        #Show the groups
        print(f"{Colors.Info}Here are all availible groups.{Colors.RESET}")
        run_bash_commands(f"getent group", showOutput)
        group = get_alpha_string(
        f"{Colors.Info}Please enter the group's name: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
        #Confirm both exist then add user to group
        if (validUser(user_name) == True) and (validGroup(group) == True):
            addUser(user_name, group)
    #Set User Sudo
    elif choice == "4":
        #Show users
        print(f"{Colors.Info}Here are all availible Users.{Colors.RESET}")
        run_bash_commands("awk -F: '{ print $1 }' /etc/passwd", showOutput)
        user_name = get_alpha_string(
        f"{Colors.Info}Please enter the user's name: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
        #If a valid user add them to sudo group
        if (validUser(user_name) == True):
            addUser(user_name, "sudo")

    #Set Group Sudo
    elif choice == "5":
        #Show Groups
        print(f"{Colors.Info}Here are all availible groups.{Colors.RESET}")
        run_bash_commands(f"getent group", showOutput)
        group = get_alpha_string(
        f"{Colors.Info}Please enter the group's name you wish to give permission: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
        #if valid group add them to sudoers file
        if validGroup(group) == True:
            sudoGroup(group)
    #Show user info (For troubleshooting)
    elif choice == "6":
        user_name = get_alpha_string(
        f"{Colors.Info}Please enter the user's name: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
        if validUser(user_name) == True:
            print(f"\n{Colors.Info}Here is the info:{Colors.RESET}")
            run_bash_commands(f"id {user_name}", showOutput)

    #Show user group info (For Troubleshooting)
    elif choice == "7":
        group = get_alpha_string(
        f"{Colors.Info}Please enter the group's name: {Colors.RESET}",
        f"{Colors.Error}Only letters please!{Colors.RESET}")
        if validGroup(group) == True:
            print(f"\n{Colors.Info}Here is the info:{Colors.RESET}")
            run_bash_commands(f"getent group {group}", showOutput)

    #Exit
    elif choice == "8":
          break
    
    #Secret choice for deleting user and group, for troubleshooting. This was a seperate file I made but decided to add it for myslelf.
    elif choice == '9':
        try:       
            user = input("Provide user: ")
            group = input("Provide Group: ")
            if group != "":
                run_bash_commands(f"groupdel {group}", noShow) 
            if user != "":
                run_bash_commands(f"userdel {user}", noShow)
        except(subprocess.CalledProcessError):
            print(f"{Colors.Error}Something didnt work{Colors.RESET}")

        if user != "":
            try:
                print("Checking success for deleting user.")
                run_bash_commands(f"id {user}", showOutput)
                print(f"{Colors.Error}User still exists{Colors.RESET}")
            except(subprocess.CalledProcessError):
                print(f"{Colors.Info}User Removed Successfully{Colors.RESET}")

        if group != "":
            try:
                print("Checking success for deleting group.")
                run_bash_commands(f"getent group {group}", showOutput)
                print(f"{Colors.Error}Group still exists{Colors.RESET}")
            except(subprocess.CalledProcessError):
                print(f"{Colors.Info}Group Removed Successfully{Colors.RESET}")
        print(f"{Colors.Info}Finished{Colors.RESET}")

    else:
        print(f"\n{Colors.Error}Invalid choice. They are 1-6 numbskull.{Colors.RESET}")
    print("")
    








