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
# 	-	Remove all spaces from the retrieved text

import re
import os
import pyperclip
import pprint


# Write the data to a file in a folder called retrieved_data
def write_files(list_emails, list_urls, list_text, list_reduced_text):
	if not os.path.exists("retrieved_data"):
		os.mkdir("retrieved_data")

    # Create the file paths
	string_email_file_path = os.path.join("retrieved_data", "emails.txt")
	string_url_file_path = os.path.join("retrieved_data", "urls.txt")
	string_text_file_path = os.path.join("retrieved_data", "text.txt")
	string_reduced_file_path = os.path.join("retrieved_data", "reduced_text.txt")
	
	# Write the file
	email_file_object = open(string_email_file_path, "w")
	url_file_object = open(string_url_file_path, "w")
	text_file_object = open(string_text_file_path, "w")
	reduced_file_object = open(string_reduced_file_path, "w")

	email_file_object.write("\n".join(list_emails))
	url_file_object.write("\n".join(list_urls))
	text_file_object.write("\n".join(list_text))
	reduced_file_object.write("\n".join(list_reduced_text))

    # Close the files
	email_file_object.close()
	url_file_object.close()
	text_file_object.close()
	reduced_file_object.close()


# Use regex to find all the email links identifiable in the passed text
def get_emails(string_input_text):
    email_regex = re.compile("""(
		([a-zA-Z.0-9\+\-\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+)		# Create a character class
		@																# The @ sign
		([a-zA-Z.0-9\+\-\!\#\$\%\&\'\*\+\-\/\=\?\^\_\`\{\|\}\~]+)		# Create a character class
	)""", re.VERBOSE)
    list_emails = email_regex.findall(string_input_text)
    return list_emails


# Use regex to find all the hyperlinks identifiable in the passed text
def get_hyperlinks(string_input_text):
    hyperlinks_regex = re.compile("""(
		(http:|https|www)   					    			    # The basic indicator of most URLs
		([a-zA-Z0-9.\!\*\'\(\)\;\:\@\&\=\+\$\,\/\?\#\[\]\_\-\%\~]+)	# Create a new character class that should return all the input urls
	)""", re.VERBOSE)
    list_hyperlinks = hyperlinks_regex.findall(string_input_text)
    return list_hyperlinks


# Determine whetherthe list is empty as a clean list from a Regex will
# return None
def is_empty_list(list_input):
    bool_conditions = False

    if (list_input is None):
        bool_conditions = True

    return bool_conditions


# Write the recieved data to a file in CSV format
def write_file():
    return None


# Main function which controls the execution of the program
def main():
    # Get the input from the clipboard
    string_input = pyperclip.paste()

    # Create the empty lists
    list_emails = []
    list_hyperlinks = []

    # Determine if the returned lists are empty, if they aren't then find the
    # complete information found
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

    # Write the output to the files
    write_files(
        list_emails,
        list_hyperlinks,
        list("No Normal Text"),
        list("No Reduced Text"))

    print("Data Written")
    return None


# Run the main function
main()
