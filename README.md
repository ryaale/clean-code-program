# Code cleaning program
Lint.

Author: Alexander Ryan.

This program reads an input python file (.py) identifies instances of bad
programming style in the code, and returns a report in a csv file containing
details on the instances and a csv file detailing a score out of
10 for how many bad instances appear in the code.

The 4 bad instances of programming style that will be tested for:

    Single Character Variables - a variable name consisting of only a single
    character, such as x.

    Long Line - a line of code that is over 79 characters.

    Trailing Whitespace - a line that contains any space or tab characters
    immediately before the end of the line.

    Bad Indent - an indent that is not a multiple of 4 single spaces. This
    includes tabs.

The two functions vars_indents and get_current_date_time from the program
file utils.py will be imported and used in the proceeding functions.

Revision history:

13 Oct 2014: built functions find_single_char_var and find_long_line . 
14 Oct 2014: built functions find_trail_whitespace and find_bad_indent . 
15 Oct 2014: built lint function . 
16 Oct 2014: built quality score log function . 
17 Oct 2014: ran code through pep8 online check . 
19 Oct 2014: wrote all documentation . 
23 Oct 2014: found way to calculate column for trail_whitespace . 
