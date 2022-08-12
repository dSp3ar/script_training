#!/bin/python

# Author: Denys Spys
# Created: 12.08.2022
# Last Modified: 12.08.2022

# Description:
# Just a simple task for TechMagic Academy that consist of a calculator, the tool for reading files, quering web-sites and getting corresponging responses and running os commands

# Usage:
# ./script.py

# Dependencies:
# pprint, validators

###########################################

RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
WHITE='\033[37m'

###########################################

import re
import os
import requests
import json
import pprint
import validators

def menu():
    print(GREEN, "[*] Please, select the option that you want to run:", sep="")
    print("1. Simple calculator.")
    print("2. Reading files.")
    print("3. Querying websites.")
    print("4. Execute OS commands.")
    print("5. Exit\n")
    option = input("Your choice >> ")
    while (option < '1' or option > '5' or len(option) != 1):
        print(RED, "[!] You have entered incorrect data!", GREEN, sep="")
        option = input("Your choice >> ")
    return option

def calculator():
    print(BLUE, "[*] You are in the CALCULATOR menu", GREEN, sep="")
    print("Please, enter the expression in the following way: ", BLUE, "NUMBER1 OPERATION NUMBER2", GREEN, sep="")
    print("If you want to finish the calculation, please, enter the", BLUE, " # ", GREEN, "sign", sep="")
    print("Examples:")
    print("23 + 54")
    print("123.45 - 0.23")
    print("75 * -237")
    print("-50 / 12")
    
    expression = ""
    flag = True
    while (expression != "#"):
        expression = input("Enter your expression >> ")
        if expression == "#":
            print()
            return
        expression = re.split("\s+", expression)
        if (len(expression) != 3):
            print(RED, "[!] You have entered incorrect data!", GREEN, sep="")
            continue
        number1 = expression[0]
        operation = expression[1]
        number2 = expression[2]
        if (not re.match("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$", number1)):
            print(RED, "[!] You have entered incorrect first number!", GREEN, sep="")
            flag = False
        if (not re.match("^[+-/\*]$", operation)):
            print(RED, "[!] You have entered incorrect operation!", GREEN, sep="")
            flag = False
        if (not re.match("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$", number2)):
            print(RED, "[!] You have entered incorrect second number!", GREEN, sep="")
            flag = False
        if (flag):
            result = 0
            number1 = float(number1)
            number2 = float(number2)
            match operation:
                case '+':
                    result = number1 + number2
                case '-':
                    result = number1 - number2
                case '*':
                    result = number1 * number2
                case '/':
                    result = number1 / number2
            print("The result is: ", result)
        flag = True


def read_files():
    print(BLUE, "[*] You are in the READ_FILE menu", GREEN, sep="")
    print("Please, enter the path to the file the content of which you want to read:")
    print("Enter the", BLUE, " # ", GREEN, "sign to interrupt the input and go back to the main menu", sep="")
    flag = False
    while not flag:
        flag = True
        path = input("Path >> ")
        if path == "#":
            return
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            print(RED, "[!] You have specified incorrect path to the file!", GREEN, sep="")
            flag = False
        elif not os.access(path, os.R_OK):
            print(RED, "[!] The specified file is not readable for the current user!", GREEN, sep="")
            flag = False
    print(YELLOW)
    file = open(path, "r")
    print(file.read())
    print(GREEN)

def query_websites():
    print(BLUE, "[*] You are in the WEBSITES QUERYING menu", GREEN, sep="")
    print("Please, enter the URL of the site you want to query:")
    url = input("URL >> ")
    print(WHITE)
    is_valid = validators.url(url)
    if is_valid != True:
        print(RED, "[!] You have specified incorrect URL!\n", GREEN, sep="")
        return
    response = requests.get(url)
    if response.status_code != 200:
        print(RED, "[!] You have specified incorrect URL!\n", GREEN, sep="")
        return
    header = dict(response.headers)
    print(json.dumps(header, indent=4))
    pprint.pprint(response.text)

def execute_os_commands():
    print(BLUE, "[*] You are in the EXECUTE_OS_COMMANDS menu", GREEN, sep="")
    print("Please, enter the OS command that you want to run:")
    command = input("Command >> ")
    result = os.system(command)
    if result:
        print(RED, "[!] You have specified incorrect command!\n", GREEN, sep="")
    else:
        print("")


option = ""
while (option != '5'):
    option = menu()
    match option:
        case '1':
            calculator()
        case '2':
            read_files()
        case '3':
            query_websites()
        case '4':
            execute_os_commands()
        case '5':
            break
print("[*] Goodbye!")
