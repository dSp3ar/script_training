#!/bin/bash

# Author: Denys Spys
# Created: 11.08.2022
# Last Modified: 12.08.2022

# Description:
# Just a simple task for TechMagic Academy that consist of a calculator, the tool for reading files, quering web-sites and getting corresponging responses

# Usage:
# ./script.sh

# Dependencies:
# bc, curl

###########################################

RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
WHITE='\033[37m'

###########################################

function menu {
	echo -e ${GREEN}
	options=("Simple calculator." "Reading files." "Querying websites." "Exit.")
	echo "[*] Please, select the option that you want to run:"
	PS3="Your choice >> "
	select option in "${options[@]}"; do
		if [[ -z ${option} ]]; then
			echo -e ${RED} "[!] You have entered incorrect data!" ${GREEN}
		else
		break
	fi
	done
	for i in "${!options[@]}"; do
		if [[ "${option}" = "${options[${i}]}" ]]; then
			return $((${i} + 1))
		fi
	done
}

function calculator {
	echo -e ${BLUE} "[*] You are in the CALCULATOR menu" ${GREEN}
	echo -e "Please, enter the expression in the following way: ${BLUE} NUMBER1 OPERATION NUMBER2" ${GREEN}
	echo -e "If you want to finish the calculation, please, enter the ${BLUE}#${GREEN} sign"
	echo "Examples:"
	echo "23 + 54"
	echo "123.45 - 0.23"
	echo "75 * -237"
	echo "-50 / 12"
	
	local expression=''
	local flag="true"
	while [[ "${expression}" != "#" ]]; do
		read -p "Enter your expression >> " expression
		if [[ "${expression}" = "#" ]]; then
			continue
		fi
		number1=$(echo "${expression}" | awk '{print $1}')
		operation=$(echo "${expression}" | awk '{print $2}')
		number2=$(echo "${expression}" | awk '{print $3}')
		if [[ ! "${number1}" =~ ^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$ ]]; then
			echo -e ${RED} "[!] You have entered incorrect first number!" ${GREEN}
			flag="false"
		fi
		if [[ ! "${operation}" =~ ^[+-/\*]$ ]]; then
			echo -e ${RED} "[!] You have entered incorrect operation!" ${GREEN}
			flag="false"
		fi
		if [[ ! "${number2}" =~ ^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$ ]]; then
			echo -e ${RED} "[!] You have entered incorrect second number!" ${GREEN}
			flag="false"
		fi
		if [[ "${flag}" = "true" ]]; then
			local result=$(bc <<< "scale=2; ${number1} ${operation} ${number2}")
			echo "The result is: ${result}"
		fi
		flag="true"
	done
}

function read_files {
	echo -e ${BLUE} "[*] You are in the READ_FILE menu" ${GREEN}
	echo "Please, enter the path to the file the content of which you want to read:"
	echo -e "Enter the ${BLUE}#${GREEN} sign to interrupt the input and go back to the main menu"
	flag="false"
	while [[ "${flag}" != "true" ]]; do
		flag="true"
		read -p "Path >> " path
		if [[ "${path}" = "#" ]]; then
			return
		fi
		path=$(echo "${path}" | sed "s|~|${HOME}|")
		if [[ ! -f "${path}" ]]; then
			echo -e ${RED} "[!] You have specified incorrect path to the file!" ${GREEN}
			flag="false"
		elif [[ ! -r "${path}" ]]; then
			echo -e ${RED} "[!] The specified file is not readable for the current user!" ${GREEN}
			flag="false"
		fi
	done
	echo -e ${YELLOW}
	while read line; do
		echo "${line}"
	done < ${path}
	echo -e ${GREEN}
}

function query_websites {
	echo -e ${BLUE} "[*] You are in the WEBSITES QUERYING menu" ${GREEN}
	echo "Please, enter the URL of the site you want to query:"
	read -p "URL >> " url
	echo -e ${WHITE}
	curl -i "${url}" 2>/dev/null
	if [[ $? != 0 ]]; then
		echo -e ${RED} "[!] You have specified incorrect URL!" ${GREEN}
	fi
}

while [[ "${option}" -ne 4 ]]; do
	menu
	option=$?
	case "${option}" in
		1) calculator;;
		2) read_files;;
		3) query_websites;;
		4) ;;
	esac
done
echo "[*] Goodbye!"
