#! python3
#! /usr/bin/python3
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

# Program Process (adopted by the class)
#   1)  Download the html text document corrsponding to the provided URL
#       - If no URL provided, output error message
#       - If URL provided, show status message
#   2)  Check the downloaded text for any hyperlinks and emails.
#       - If no hyperlinks present, output "None" accordingly
#       - If no emails present, output "None" accordingly 
#       - Always output the number of Hyperlinks and Emails found
#   3)  Get the main body of text in the html document
#   4)  Get the reduced body of text (no articles and no prepositions)
#   5)  Conclude the process 

import re
import os
import sys
import urllib.request, urllib.error

import pprint

# Class defition
class Portan:
    # Text Numbers
    __int_num_emails = 0
    __int_num_hyperlinks = 0
    __int_num_text = 0
    __int_num_html_tags = 0

    # Provided link
    __string_provided_url = "N/A"

    # Downloaded html data
    __string_returned_webpage = "N/A"
    __string_status_code = "N/A"
    __string_header_information = "N/A"

    # Webpage Information
    __string_last_modified = "N/A"
    __string_content_language = "N/A"
    __string_current_date = "N/A"
    __string_content_type = "N/A"
    __string_content_length_bytes = "N/A"

    # Lists [and strings] of data retrieved
    __list_emails = ["None"]            # Contains the found emails
    __list_hyperlinks = ["None"]        # Contains the found hyperlinks
    __list_html_tags = ["None"]         # Contains all the html tags found in the website
    __string_webpage_plain_text = ""    # Contains the normal plaintext based on the html document without tags, comments, or javascript

    # Constructor taking arguments
    def __init__(self, list_arguments):
        return None

    # Constructor not requiring arguments
    def __init__(self):
        return None


    def get(self, string_received_url):
        # Retrieve the data from the web
        file_object = urllib.request.urlopen(string_received_url)

        # Set the webpage data
        self.__string_provided_url = string_received_url
        self.__string_status_code = file_object.getcode()
        self.__string_returned_webpage = file_object.read().decode().replace("\n", "", -1)    # Remove all newlines as well, gets a few more tags
        
        # Extract the necessary header information
        self.__dict_header_info = file_object.info()
        self._get_webpage_information()

        # Get all html tags
        self._find_all_tags()

        # Get normal text
        self._find_all_text()

        # Get all hyperlinks
        self._find_all_hyperlinks()

        # Get all emails
        self._find_all_emails()

        # Print the data retrieved
        self.print_details()
        
        return None


    # Not supposed to be called
    def _get_webpage_information(self):
        # Parse the webpage information into the required variables
        self.__string_last_modified = self.__dict_header_info["Last-Modified"]
        self.__string_content_language = self.__dict_header_info["Content-language"]
        self.__string_current_date = self.__dict_header_info["Date"]
        self.__string_content_type = self.__dict_header_info["Content-Type"]
        self.__string_content_length_bytes = self.__dict_header_info["Content-Length"]

        return None


    # print the details to the screen
    def print_details(self):
        # Print the required data to the screen

        # Print the License and Version information of Portan
        # TODO
        print("<LICENSE & VERSION INFO GOES HERE>")

        # Print the URL Accessed & Header information
        print("\n\nACCESSED: \t\t%s\nSTATUS CODE: \t\t%s\nLAST MODIFIED: \t\t%s\nDATE ACCESSED: \t\t%s\nCONTENT TYPE: \t\t%s\nCONTENT LANGUAGE: \t%s\nRECEIVED BYTES: \t%s\n\n" \
            % (self.__string_provided_url, self.__string_status_code, self.__string_last_modified, self.__string_current_date, self.__string_content_type, self.__string_content_language,self.__string_content_length_bytes))

        # Print the status information on found emails and hyperlinks TODO (Add in text size, reduced text_size, image links)
        print("EMAILS: \t\t%s\nHYPERLINKS: \t\t%s\nSEARCHABLE TEXT: \t%s BYTES" \
            % (self.__int_num_emails, self.__int_num_hyperlinks, self.__int_num_text))

        return None


    # Find all the emails in the text
    def _find_all_emails(self):
        # Create the regex to identify nearly all email addresses
        email_regex = re.compile("""(?P<full_email>
        (?![@.,%&#\-\/*{}])                                             # To avoid false positives, such as }@font-face, avoid certain special characters 
        ([a-zA-Z0-9\u00a1-\uffff.!#$%&’*+\/=?\^_`\{\|\}~\-]+)           # Character class that matches most nicknames
        @                                                               # The @ sign
        ([a-zA-Z0-9\u00a1-\uffff\-]+)                                   # Character class that matches most mail-servers
        (\.[a-zA-Z0-9\-]+)+                                             # Character class that matches most top-level domains                                                     
	    )""", re.VERBOSE)

        # Search the member variable for emails
        list_found_emails = self._from_tuple_to_list(email_regex.findall(self.__string_returned_webpage))

        # Remove any duplicates
        list_found_emails = self._remove_list_duplicates(list_found_emails)

        # With some creative (&& Repetive coding - should improve this later)
        # it is possible to remove any urls that were incorrectly recognized as emails
        # thanks to the existence of sets. Not implemented here, though

        # Determine whether any information was found
        if (len(list_found_emails) > 0):
            self.__list_emails = list_found_emails

        # Set the email information
        self.__int_num_emails = len(list_found_emails)

        return None


    # Find all the hyperlinks in the text
    def _find_all_hyperlinks(self):
        # Create a regex to identify nearly all hyperlinks
        hyperlink_regex = re.compile("""(?P<full_url>
            # URLS are very peculiar and quite a few have been made. We can't just match www.google.com, as github.com also exits.
            # Additionally there are protocosl and ports sometimes specified as well, for example https://www.google.com, or localhost:8080.
            # Urls can also not start with special characters, such as @.,%&#-
            # This regex will try and find all of them given these conditions.

            (?![@.,%&#\-]+)                                                  # Match only if it doesn't match with a special character
            (?P<protocol>(http|https)\://)                                    # Optional schemes that indicate protocols and "://"; matches minimally   ;removed \w{2,10}
            ([a-zA-Z0-9\u00a1-\uffff?\-=#:;%@&.,$+_~]+?)                     # Host names must be at least one character long, but will be separated by periods
            (\.[a-zA-Z0-9\u00a1-\uffff?\-=#:;%@&.,$+_~]+?)                     # Host names must be at least one character long, but will be separated by periods
            (\.[a-zA-Z0-9\u00a1-\uffff?\-=#:;%@&.,$+_~]+?)                     # Host names must be at least one character long, but will be separated by periods             
            (?![@])                                                          # Matches only if the next character is not @; prevent recognizing emails
            (?(protocol)((:\d)+))?                                           # Port matching only if there was a protocol
            ([a-zA-Z0-9\u00a1-\uffff?\-=#:;%@&.,\/$+_~]+)                   # The path of the url can contain any number of special characters
            (?![.,?!\-])                                                     # The path cannot end on .,?!-            
        )""", re.VERBOSE | re.UNICODE)

        # Search the member variable for hyperlinks
        list_found_hyperlinks = self._from_tuple_to_list(hyperlink_regex.findall(self.__string_returned_webpage))

        # Remove duplicates
        list_found_hyperlinks = self._remove_list_duplicates(list_found_hyperlinks)

        # Determine whether any hyperlinks were found and update the member variables accordingly
        if (len(list_found_hyperlinks)):
            self.__list_hyperlinks = list_found_hyperlinks

        # Set the hyperlink information
        self.__int_num_hyperlinks = len(list_found_hyperlinks)

        return None


    # Separate the html tags from the normal text
    def _find_html_tags(self):
        # This function will take in the member variable containing the body of the html text
        # and return all the tags. These can be searched for links later

        list_html_tags = []

        # Create the regex to find all self-closing tags
        html_self_closing_tag_regex = re.compile("""(?P<self_closing_tag>
            (<.+?\/>)                         # Look for self-closing tags
        )""", re.VERBOSE)

        # Create the regex to find all normal tags
        html_tag_regex = re.compile("""(?P<pair_tags>
            </?                                                             # Opening tag and possible / to close it
            \w+                                                             # Immediately followed by any normal text
            ((\s+\w+(\s*=\s*(?:".*?"|'.*?'|[\^'">\s]+))?)+\s*|\s*)          # Any number of tag attributes and values separated by any number of spaces
            /?>                                                             # the ending of the tag - accouting for possible self-closing tags
        )""", re.VERBOSE)

        html_comment_regex = re.compile("""(?P<comment_tags>
            (<!DOCTYPE(\s\S)?>)|                                            # Look for html document information
            (<!--[\\s\\S]*?-->)                                              # Find only comments, but they may not be terminated as per HTML 5 spec
        )""", re.VERBOSE)

        javascript_html_regex = re.compile("""(?P<javascript_or_css_tags>
            # Find javascript tags
            (?P<script_tag>(<script[\s\S]*?>)                                 # Find script opening tag
            ([\s\S]*?)                                                        # Find data witin the script tag
            (<\/script>))?                                                    # Find the ending of the script tag
            # Find noscript tags
            (?P<noscript_tag>(<noscript[\s\S]*?>)                             # Find noscript openign tag
            ([\s\S]*?)                                                        # Find the data between
            (<\/noscript>))?                                                  # Find the ending noscript tag
            # Find style tags
            (?P<css_tags>(<style[\s\S]*?\/>))?                                # Find the css tag opening style which is likely self-terminating
        )""", re.VERBOSE)

        # Find all self-closing tag occurrences and return them
        list_html_self_closing_tags = self._from_tuple_to_list(html_self_closing_tag_regex.findall(self.__string_returned_webpage))
        list_html_tags = self._from_tuple_to_list(html_tag_regex.findall(self.__string_returned_webpage))
        list_comment_tags = self._from_tuple_to_list(html_comment_regex.findall(self.__string_returned_webpage))
        list_extra_tags = self._from_tuple_to_list(javascript_html_regex.findall(self.__string_returned_webpage))                       # Javascript and CSS tags


        # Find all normal tag occurences and return them
        list_html_tags = list_extra_tags + list_html_tags + list_html_self_closing_tags + list_comment_tags

        return list_html_tags

    
    # Separate the normal text from the html tags
    def _find_html_text(self):
        # This function will take in the member variable containing the body of the html text
        # and return all the normal text. This bundle of text will be reduced and can be searched for links later

        # Find all the tags
        list_found_html_tags = self._find_html_tags()

        # Cycle through all of the tags, and replace them with "" in the string
        string_new_html_text = self.__string_returned_webpage

        # Additional information
        file = open("string_html_text", 'w')
        file.write(string_new_html_text)
        file.close()

        for element in list_found_html_tags:
            string_new_html_text = string_new_html_text.replace(str(element), "", -1) # replace all

        # Additional information
        file = open("string_new_html_text", 'w')
        file.write(string_new_html_text)
        file.close()

        return string_new_html_text


    # Find a list of all tags
    def _find_all_tags(self):
        # This function uses the _find_html_tags function to return a list of html tags that 
        # can be perused and scanned to add more hyperlinks and emails which weren't previously found
        self.__list_html_tags = self._find_html_tags()
        self.__int_num_html_tags = len(self.__list_html_tags)

        return None


    # Find the html text reduced to normal plain text
    def _find_all_text(self):
        # This function uses the _find_html_text function to return a string of plain website text
        # that can be perused and scanned for information.
        self.__string_webpage_plain_text = self._find_html_text()
        self.__int_num_text = len(self.__string_webpage_plain_text)

        return None


    # Convert the regex tuple obtained with ".findall()" to a list with the required information
    def _from_tuple_to_list(self, tuple_input):
        # This function knows that the input tuple will have the complete information as the first element
        # as such it will retrieve only first elment and return the list
        list_to_return = []

        # Get each tuple
        for tuple_element in tuple_input:
            # Change it to a list element and append it
            list_to_return.append(tuple_element[0])

        return list_to_return
    

    # Remove any duplicates from a passed list. It will use sets to accomplish this
    def _remove_list_duplicates(self, list_input):
        # This function uses python's ability to change between sets and lists.
        # With a set, duplicate information is automatically removed using approved
        # methods which thus cut down time to improve efficiency. Downside is, this 
        # method will take a bit of memory to do
        list_to_return = []

        # convert the list to a set, and return it immediately
        list_to_return = list(set(list_input))

        return list_to_return


    # Displays the Portan Version
    def _version(self):
        print("Portan v1.0.0\n")
        return None



    
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


def argument_search(list_arguments):
    # Based on the passed system arguments different information will be displayed.
    # Basic Outline: require at least one argument, the url. If not, display help
    # Tags Outline: --version, --help, --minimal, --no-output, --license, --show-emails,
    # --show-hyperlinks, --show-text

    # Erase the first argument form the list. Why? It only contains the name of the program
    #list_arguments.pop(0)
    
    string_help_data = """Portan requires a number of arguments. See the list below.
    
     --verbose              Shows all steps Portan takes. 
     --version              Displays the version of Portan. 
     --help                 Displays help information. 
     --minimal              Shows basic information. Used 
                            by default. 
     --no-output            Displays nothing except success 
                            or failure. 
     --license              Displays the license under which 
                            Portan was published together with
                            any additional information.
     --write [path]         Creates files containing the 
                            information found in the designated
                            path. If no path is provided, 
                            places the files in application 
                            directory.
     --emails               Displays the emails found
     --hyperlinks           Displays the hyperlinks found
     --plain-text           Displays the obtained plaintext"""

    return None

# Main function which controls the execution of the program
def main():
    # TODO: Get arguments passed && possible switched that define behaviour, e.g. --version, --help, --minimal, --no-output, --license
    argument_search(sys.argv)  # Convert the item to a set and back to remove multiple arguments    


    # Create the portan object, and pass the relevant switches
    portan = Portan()
    #portan.get(r"https://www.youtube.com/watch?v=rei5vMQmD4Q")                                                  # EMAILS: 0; URLS: 48  # Excludes local links found in href="" tags
    #portan.get(r"https://www.ohayosensei.com/current-edition.html")                                             # EMAILS: 113; URLS: 106
    portan.get(r"https://en.wikipedia.org/wiki/Linus")                                                          # EMAILS: 0; URLS: 26 
    #portan.get(r"https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string")  # EMAILS: 2; URLS: 192  # !Error, recognizes a url with an @ in it as email.
    #portan.get(r"https://en.wikipedia.org/wiki/Cat")                                                            # EMAILS: 0; URLS: 472  

    return None


# Run the main function
main()


# TODO:
# Get the links from the tags and add them to the hyperlinks by making sure that all relative links are changed to proper URLS
# Remove the URLS from the email list
# 
# Add in the "command-line arguments that will allow different information, including searching the page
#
# Add in the urllib error checking for urls that do not exist