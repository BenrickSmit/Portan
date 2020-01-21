#! python3
#! /usr/bin python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# portan.py
# Copyright (C) 2020 Benrick Smit <metatronicprogramming@hotmail.com>
# 
# Portan is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Portan is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# GOALS
#	-	Find emails
#	- 	Find Hyperlinks
#	-	Find all normal text

import re
import pyperclip
import pprint

def get_emails(string_input_text):
	email_regex = re.compile("""(
		([\-a-zA-Z.0-9]+)		# Create a character class
		@						# The @ sign
		([\-a-zA-Z.0-9]+)		# Create a character class
	)""", re.VERBOSE)
	list_emails = email_regex.findall(string_input_text)
	return list_emails

def get_hyperlinks(string_input_text):
	hyperlinks_regex = re.compile("""(
		(http:|https|www)   					    # The basic indicator of most URLs
		([a-zA-Z0-9.:\&\?_=\-\/]+)					# Create a new character class that should return all the input urls
	)""", re.VERBOSE)
	list_hyperlinks = hyperlinks_regex.findall(string_input_text)
	return list_hyperlinks

def is_empty_list(list_input):
	bool_conditions = False

	if (list_input == None):
		bool_conditions = True		

	return bool_conditions

def main():
	# Get the input from the clipboard
	string_input = pyperclip.paste()
	
	# Create the empty lists
	list_emails = []
	list_hyperlinks = []

	# Determine if the returned lists are empty, if they aren't then find the complete information found
	list_tuple_emails = get_emails(string_input)
	list_tuple_hyperlinks = get_hyperlinks(string_input)

	if(not is_empty_list(list_tuple_emails)):
		for index in list_tuple_emails:
			list_emails.append(index[0])
	else:
		list_emails.append("No Emails Found.")


	if(not is_empty_list(list_tuple_hyperlinks)):	
		for index in list_tuple_hyperlinks:
			list_hyperlinks.append(index[0])
	else:
		list_hyperlinks.append("No Hyperlinks Found.")


	pprint.pprint("List of Emails:")
	pprint.pprint("===============")
	pprint.pprint(list_emails)
	pprint.pprint("List of found Hyperlinks:")
	pprint.pprint("=========================")
	pprint.pprint(list_hyperlinks)

# Run the main function
main()