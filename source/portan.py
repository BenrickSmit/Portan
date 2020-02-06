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
    __list_possible_arguments = []                  # Used to check the consistency of the arguments passed

    # Text Numbers
    __int_num_emails = 0                            # Contains the number of email links found
    __int_num_hyperlinks = 0                        # Contains the number of hyperlinks found
    __int_num_text = 0                              # Contains the number of textual characers found - that are human readable by non-programmers
    __int_num_html_tags = 0                         # Displays the number of html tags found within the text

    # Provided link
    __string_provided_url = "N/A"                   # Contains the url provided

    # Downloaded html data
    __string_returned_webpage = "N/A"               # Contains the text retured by urllib
    __string_status_code = "N/A"                    # Displays codes such as 200 - successful, 404 - page not found, etc
    __dict_header_info = "N/A"                      # Contains the webpage header info in a dictionary 

    # Webpage Information
    __string_last_modified = "N/A"                  # Displays when the website was last modified
    __string_content_language = "N/A"               # Displays the language of the website
    __string_current_date = "N/A"                   # Displays the current date of access
    __string_content_type = "N/A"                   # Displays the website type of content
    __string_content_length_bytes = "N/A"           # Contains how many bytes are available

    # Lists [and strings] of data retrieved
    __list_emails = ["None"]                        # Contains the found emails
    __list_hyperlinks = ["None"]                    # Contains the found hyperlinks
    __list_html_tags = ["None"]                     # Contains all the html tags found in the website
    __string_webpage_plain_text = ""                # Contains the normal plaintext based on the html document without tags, comments, or javascript

    # Set program flags for use
    #   NOTE: certain flags override output, such as --help, --license, and --version
    __flag_verbose = False
    __flag_minimal = False
    __flag_license = False
    __flag_version = False
    __flag_minimal = False
    __flag_no_output = False
    __flag_write = False
    __flag_emails = False
    __flag_hyperlinks = False
    __flag_plaintext = False
    __flag_search = False


    # Constructor taking arguments from the commandline
    def __init__(self, list_arguments):
        # Dictate and set the arguments that are supported by portan - Remember to delete this later
        self.__list_possible_arguments = ["--verbose", "--version", "--help", "--minimal", "--no-output",\
             "--license", "--emails", "--hyperlinks", "--write", "--plaintext", "--search"]

        # Remove the first part of the list, as this will always be the current file path
        list_arguments.pop(0)

        
        # Check which flags are active in the list, but only those which override processing the url
        # and require no url to be present.
        if (self._find_argument(list_arguments, "--version")):
            self._version_menu()
            return None
        elif (self._find_argument(list_arguments, "--help")):
            self._help_menu()
            return None
        elif (self._find_argument(list_arguments, "--license")):
            self._license_menu()
            return None


        # Eliminate the arguments from the list, and set the required flags
        if (self._find_argument(list_arguments, "--verbose")):
            self.__flag_verbose = True
        if (self._find_argument(list_arguments, "--minimal")):
            self.__flag_minimal = True
        if (self._find_argument(list_arguments, "--no-output")):
            self.__flag_no_output = True
        if (self._find_argument(list_arguments, "--emails")):
            self.__flag_emails = True
        if (self._find_argument(list_arguments, "--hyperlinks")):
            self.__flag_hyperlinks = True
        if (self._find_argument(list_arguments, "--write")):
            self.__flag_write = True
        if (self._find_argument(list_arguments, "--plaintext")):
            self.__flag_plaintext = True
        if (self._find_argument(list_arguments, "--search")):
            self.__flag_search = True

        # Determine whether the program has any mutually exclusive arguments active
        if (int(self.__flag_verbose) + int(self.__flag_minimal) + int(self.__flag_no_output)) > 1:
            print("Error: Cannot contain more than one mutually exclusive tags. \nChoose one: --verbose, --minimal, or --no_output")
            return None     # To exit the program

        # Should --minimal be set, don't display any message, should --verbose be set, display all messages
        # PS, the first argument should be the url, if not, some errors will occur
        self.get(list_arguments[0], self.__flag_verbose)

        # Should --no-output be set, get the information, but display nothing
        self.print_details(self.__flag_no_output)

        return None


    def get(self, string_received_url, bool_is_verbose = False):
        # Retrieve the data from the web
        self.__log("Retrieve Server Data...", bool_is_verbose)
        file_object = urllib.request.urlopen(string_received_url)

        # Set the webpage data
        self.__log("Extract Website Data...", bool_is_verbose)
        self.__string_provided_url = string_received_url
        self.__string_status_code = file_object.getcode()
        self.__string_returned_webpage = file_object.read().decode().replace("\n", "", -1)    # Remove all newlines as well, gets a few more tags later on
        
        # Extract the necessary header information
        self.__log("Extract Header Data...", bool_is_verbose)
        self.__dict_header_info = file_object.info()
        self._get_webpage_information()

        # Get all html tags
        self.__log("Extract HTML, CSS, JavaScript Data...", bool_is_verbose)
        self._find_all_tags()

        # Get normal text
        self.__log("Extract Plaintext...", bool_is_verbose)
        self._find_all_text()

        # Get all hyperlinks
        self.__log("Extract Hyperlinks...", bool_is_verbose)
        self._find_all_hyperlinks()

        # Get all emails
        self.__log("Extract Emails...\n", bool_is_verbose)
        self._find_all_emails()

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
    def print_details(self, bool_no_output = False):
        # Print the required data to the screen if allowed
        if(bool_no_output):
            return None

        # Print the License and Version information of Portan
        # TODO
        self._license_menu()

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


    # Find an argument in a list of arguments passed to the program
    def _find_argument(self, list_arguments, string_item_to_find):
        # This function takes a list of arguments passed to the program and looks to find a specified
        # argument. Returns true if it is found, and false if not
        bool_argument_found = False
        
        # Look for the argument
        try:
            if (list_arguments.index(string_item_to_find)):
                bool_argument_found = True
        except ValueError:
            bool_argument_found = False

        return bool_argument_found


    # Displays the help menu
    def _help_menu(self):
        # Create the string to display
        string_help_data = """Portan requires a number of arguments. See the list and example below.
    Portan will require a URL to search. Should none be present
    Portan will cease to execute and display an error.

        >> portan.py [url] [arguments]
    
     --verbose                  Shows all steps Portan takes. 
     --version                  Displays the version of Portan. 
     --help                     Displays help information. 
     --minimal                  Shows basic information. Used 
                                by default. 
     --no-output                Displays nothing except success 
                                or failure. 
     --license                  Displays the license under which 
                                Portan was published together with
                                any additional information.
     --write [path]             Creates files containing the 
                                information found in the designated
                                path. If no path is provided, 
                                places the files in application 
                                directory.
     --emails                   Displays the emails found
     --hyperlinks               Displays the hyperlinks found
     --plain-text               Displays the obtained plaintext
     --search ["to_search"]     Searches for the text "to_search" in 
                                the plaintext found on the website. 
                                Should the text be more than one word
                                enclose it in double quotes, i.e. 
                                --search "words to search" """

        # Remember to add in recursive searching

        # Display the help string
        print(string_help_data)
        return None


    # Displays the Portan Version
    def _version_menu(self):
        print("Portan v1.0.0\n")
        return None


    # Display the license under which Portan is published
    def _license_menu(self):
        string_license = """# Copyright (C) 2020 Benrick Smit <metatronicprogramming@hotmail.com>
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
# with this program.  If not, see <http://www.gnu.org/licenses/>."""

        print(string_license)

    
    # Displays a message for use when using the flag --verbose
    def __log(self, string_to_display, bool_display_condition):
        # This function will only display a message should bool_display_condition is ture
        if (bool_display_condition):
            print("<<verbose>> " + string_to_display)

        return None



# Main function which controls the execution of the program
def main():
    # Create the portan object, and pass the relevant switches
    list_to_pass = list(sys.argv)
    # To account for building the program in an IDE
    #list_to_pass.append(r"https://en.wikipedia.org/wiki/Linus")
    #list_to_pass.append(r"https://www.youtube.com/watch?v=rei5vMQmD4Q")
    #list_to_pass.append(r"https://www.ohayosensei.com/current-edition.html")
    #list_to_pass.append(r"https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string")
    list_to_pass.append(r"https://en.wikipedia.org/wiki/Cat")
    list_to_pass.append("--verbose")
    #list_to_pass.append("--minimal")

    portan = Portan(list_to_pass)
    
    # Check the actual links
    #portan.get(r"https://www.youtube.com/watch?v=rei5vMQmD4Q")                                                  # EMAILS: 0; URLS: 48  # Excludes local links found in href="" tags
    #portan.get(r"https://www.ohayosensei.com/current-edition.html")                                             # EMAILS: 113; URLS: 106
    #portan.get(r"https://en.wikipedia.org/wiki/Linus")                                                          # EMAILS: 0; URLS: 26 
    #portan.get(r"https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string")  # EMAILS: 2; URLS: 192  # !Error, recognizes a url with an @ in it as email.
    #portan.get(r"https://en.wikipedia.org/wiki/Cat")                                                            # EMAILS: 0; URLS: 472  

    return None


# Run the main function
main()


# TODO:
# Get the links from the tags and add them to the hyperlinks by making sure that all relative links are changed to proper URLS
# Remove the URLS from the email list
# 
# Add in the urllib error checking for urls that do not exist