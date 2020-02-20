# Portan
A Python web-crawler and text-analyzer for single webpages. Future versions might include recursive analysis.

# Instructions
Portan can be run from the commandline or an IDE. Whichever you prefer. Portan comes with a built-in help menu which can be run with the following code:
<code>python portan.py --help</code> on linux or <code>python.exe portan.py --help</code> for windows.

Simply follow the commands help menu and normal bash scripting to retrieve the necessary information gathered by Portan. A few examples include


<code>python portan.py [full url] --verbose</code>     -> This shows everything Portan does to retrieve the information
<code>python portan.py [full url] --no-output</code>   -> This displays no output, but can still generate output if --write is specified
<code>python portan.py [full url] --minimal</code>     -> This is the default tag and will only display the necessary information
<code>python portan.py [full url] --emails</code>      -> This displays the normal data, as well as a list of emails gathered from the url
<code>python portan.py [full url] --images</code>      -> This displays a list of hyperlinks that Portan thinks might be images
<code>python portan.py [full url] --hyperlinks</code>  -> This displays a list of hyperlinks that Portan found scanning the website


Note: Portan has only been tested with Wikipedia, Youtube, and a select number of other websites. It might not be entirely accurate for other websites and requires
further testing.

# License
Portan is licensed under [GPLv3](LICENSE).

# Contributions
Code contributions are very welcome at this point.
