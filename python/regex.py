import re

#-----------------------------regex.py-------------------------
#This script was used to learn regular expressions and their uses, I do not have the csv file source.
#Features:
#-Uses regez to match valid U.S. numbers
#-Prints and saves output
#Use case:
#Clean up lists and databases in mass.

class Colors:
    Error = '\033[91m' #User Errors
    Info = '\033[92m' #Information from the script
    RESET = '\033[0m' # Reset, blank text for console information

#Check if the file is a USA number
def isUsaNumber(number):
    # Pattern for Numbers.
    # 1? Looks for 1 for United States
    #\s? Looks for a space
    #\d{3} looks for area code
    #\s? Another space
    #\d{3} Again looks for 3 for the number
    #\s? Another Space
    #\d{4} Looks for the 4 final numbers
    #\b Makes sure theres no more characters
    pattern = r"1?\s?\d{3}\s?\d{3}\s?\d{4}\b"
    return re.match(pattern, number)

#Get the numbers
def extractUsaNumbers(file_path):
    #Create aray for the numbers
    usaNumbers = []
    #Open the file, sort it by lines, then sort it delimited by commas, then run the check. And return the number
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            numbers = line.split(',')
            for number in numbers:
                number = number.strip()
                print(f"Cheking number: {number}")
                if isUsaNumber(number):
                    print(f"{Colors.Info}{number} Match!{Colors.RESET}")
                    usaNumbers.append(number)
                else:
                    print(f"{Colors.Error}{number} No Match.{Colors.RESET}")
    print(usaNumbers) #I added this because it looks cool.
    print(f"{Colors.Info}Found all these Numbers.{Colors.RESET}")
    return usaNumbers

#Save the numbers in a file each one taking a line
def saveToFile(numbers, outputFile):
    with open(outputFile, 'w') as file:
        for number in numbers:
            file.write(number + '\n')

# Path to the file containing phone numbers
filePath = "phoneNumbers.csv"

# Extract numbers starting with 1
usaNumbers = extractUsaNumbers(filePath)

# Save USA numbers to a new file
outputFile = "usaPhoneNums.txt"
saveToFile(usaNumbers, outputFile)

# Show where they are

print(f"{Colors.Info}USA phone numbers have been extracted and saved to {outputFile}{Colors.RESET}")
