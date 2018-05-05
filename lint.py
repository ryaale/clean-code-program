'''
Lint.

Author: Alexander Ryan.

This program reads an input python file (.py) identifies instances of bad
programming style in the code, and returns a report in a csv file containing
details on the instances and a csv file file detailing a score out of
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

13 Oct 2014: built functions find_single_char_var and find_long_line
14 Oct 2014: built functions find_trail_whitespace and find_bad_indent
15 Oct 2014: built lint function
16 Oct 2014: built quality score log function
17 Oct 2014: ran code through pep8 online check
19 Oct 2014: wrote all documentation
23 Oct 2014: found way to calculate column for trail_whitespace

'''

import csv
from utils import vars_indents, get_current_date_time


def find_single_char_variable(python_filename, lines):
    '''
    Finds the number of single character variables in the input python file
    and returns a list containing the variables and further information about
    them.

    These variables are retrieved from the function vars_indents in the utils
    program file in the form of a dictionary. The dictionary has keys
    corresponding with line numbers and a 2 tuple of the variable and
    the column that variable appears in.

    An empty list called single_char_var_list is created to store all
    the single character variables that are found in the program file.

    The first for loop involves cycling over every key in the
    dictionary retrieved from vars_indents. Since we are only after
    the first dictionary retrieved in the vars_indents file,
    we designate this by variable_dictionary[0].keys().

    The second for loop, nested in the first one, cycles through
    every variable corresponding with each line number (the key).

    The if statement nested within the second for loop then tests
    to see whether each variable that is found is of length equal to 1.
    A length of 1 would mean the variable contains only a single character,
    which is the bad programming instance we are testing for.

    Every time a variable is found with a length of 1, the variable
    information is stored in the single_char_var_list. The information
    stored includes the title SINGLE_CHAR_VAR, the line number,
    the column number, the single variable itself,
    and the entire contents of the line.

    The list is then returned at the end of the function.

    Parameters:

        python_filename: The python file you want tested to find
                         instances of bad programming style.
        lines: The lines of the program

    Result: A list of all the instances of single variables in the
    input python file, with the information including the title
    SINGLE_CHAR_VAR, the line number, the column number,
    the single variable itself, and the entire contents of the line.

    Example:
    python_filename = 'naughty.py'
    lines = "Edge detection.

         Author: Bernie Pope (bjpope@unimelb.edu.au)....

        ...tester('gradient_threshold', GRADIENT_THRESH_TESTS, exact_equal)
             tester('convolute', CONVOLUTE_TESTS, exact_equal)"

    >>>[[SINGLE_CHAR_VAR,79,25,r,"def gradient_row(image, r, col):"],
    [SINGLE_CHAR_VAR,129,29,r,
                   "    return get_pixel(image, r - 1, col - 1) + \"     ''],
    [SINGLE_CHAR_VAR,130,33,r,
                   "           2 * get_pixel(image, r - 1, col) + \"     ''],
    [SINGLE_CHAR_VAR,131,29,r,
                   "           get_pixel(image, r - 1, col + 1) - \"      ],
    [SINGLE_CHAR_VAR,132,29,r,
                   "           get_pixel(image, r + 1, col - 1) - \"      ],
    [SINGLE_CHAR_VAR,133,33,r,
                   "           2 * get_pixel(image, r + 1, col) - \"      ],
    [SINGLE_CHAR_VAR,134,29,r,
                   "           get_pixel(image, r + 1, col + 1)"],
    [SINGLE_CHAR_VAR,194,7,r,
                   "      r = gradient_row(image, row, col)"],
    [SINGLE_CHAR_VAR,195,7,c,
                   "      c = gradient_col(image, row, col)"],
    [SINGLE_CHAR_VAR,196,24,r,
                          return math.sqrt(r ** 2 + c ** 2)],
    [SINGLE_CHAR_VAR,196,33,c,
                          return math.sqrt(r ** 2 + c ** 2)],
    [SINGLE_CHAR_VAR,314,11,r,"def clamp(v, u, l):"],
    [SINGLE_CHAR_VAR,314,14,u,"def clamp(v, u, l):"],
    [SINGLE_CHAR_VAR,314,17,l,"def clamp(v, u, l):"],
    [SINGLE_CHAR_VAR,315,23,v,"       return max(min(v, u), l)   "],
    [SINGLE_CHAR_VAR,315,26,u,"       return max(min(v, u), l)   "],
    [SINGLE_CHAR_VAR,315,30,l,"       return max(min(v, u), l)   "],
    [SINGLE_CHAR_VAR,352,5,r,"    r = clamp(row, 0, max_row)"],
    [SINGLE_CHAR_VAR,353,5,c,"    c = clamp(col, 0, max_col)"],
    [SINGLE_CHAR_VAR,354,18,r,    return image[r][c]],
    [SINGLE_CHAR_VAR,354,21,c,    return image[r][c]]]
    '''

    variable_dictionary = vars_indents(python_filename)
    single_char_var_list = []

    for each_key in variable_dictionary[0].keys():
        for each_variable in variable_dictionary[0][each_key]:
            if len(each_variable[0]) == 1:
                single_char_var_list.append(["SINGLE_CHAR_VAR",
                                            int(each_key), each_variable[1],
                                            each_variable[0],
                                            lines[each_key-1][:-1]])
    return single_char_var_list


def find_long_line(python_filename, lines):
    '''
    Finds the instances of long lines in an input python file and then returns
    a list containing instances and further information about them.

    An empty list is created called long_line_list which will store all the
    instances of long lines in the input python file. A counter is also
    created to count through each line in the file, which will be used to
    verify the line number when writing into the list.

    The for loop cycles through every line in the parameter lines.
    For each line it performs the following actions:

        1. sums the total number of characters in the line
        2. adds 1 to the line counter
        3. an if statement - if the sum of the line is over 79 characters it
            writes the line information to the long_line_list

    The information stored in the long_line_list includes the title LONG_LINE,
    the line number (obtained from the counter),
    the length of the long line, and the entire contents of the line.

    The long_line_list is returned at the end of the function, once all lines
    have been cycled through.

    Parameters:

        python_filename: The python file you want tested to find
                         instances of bad programming style.
        lines: The lines of the program

    Result: A list of all the instances of long lines in the input python file,
    with the information including the title LONG_LINE, the line number,
    the length of the long line, and the entire contents of the line.

    Example:
    python_filename = 'naughty.py'
    lines = "Edge detection.

            Author: Bernie Pope (bjpope@unimelb.edu.au)...

            ...tester('gradient_threshold', GRADIENT_THRESH_TESTS, exact_equal)
             tester('convolute', CONVOLUTE_TESTS, exact_equal)"

    >>>[[LONG_LINE,187,,86,"    return get_pixel(image, row - 1, col + 1) +
         2 * get_pixel(image, row, col + 1) + \"],
    [LONG_LINE,188,,86,"           get_pixel(image, row + 1, col + 1) -
      get_pixel(image, row - 1, col - 1) - \"],
    [LONG_LINE,203,,120,
    The result is computed by comparing the gradient magnitude at the
    coordinate against the threshold parameter. If the]]
    '''
    long_line_list = []
    line_count = 0

    for each_line in lines:
        line_length = sum(1 for char in each_line)
        line_count += 1
        if line_length >= 80:
            long_line_list.append(["LONG_LINE", int(line_count), "",
                                  (line_length - 1), each_line[:-1]])
    return long_line_list


def find_trail_whitespace(python_filename, lines):
    '''
    Finds the instances of trailing white space in the input python file and
    then returns the instances in the form of a list.

    An empty list is created called trail_whitespace_list which will store all
    the instances of trailing whitespace.

    A counter is also created called line_count which will be used to
    verify the line number when writing into the trail_whitespace_list.

    A for loop is used to cycle through each line in the input python file and
    performs the following actions:

        1. adds 1 to the line counter
        2. an if statement that determines if there is a space
           immediately before the end of the line, represented by '\n'.
           Trailing whitespace is represented by an instance of ' \n'.
           If the instance does occur then it is written to the
           trail_whitespace_list.

    The information stored in the trail_whitespace_list includes
    the title TRAIL_WHITESPACE, the line number (obtained from the counter),
    the column number where the first trailing whitespace occurs,
    and the entire contents of the line.

    The trail_whitespace_list is returned at the end of the function.

    Parameters:

        python_filename: The python file you want tested to find
                         instances of bad programming style.
        lines: The lines of the program

    Result: A list of all the instances of trailing whitespace
    in the input python file, with the information including
    the title TRAIL_WHITESPACE, the line number (obtained from the counter),
    the column number where the first trailing whitespace occurs,
    and the entire contents of the line.

    Example:
    python_filename = 'naughty.py'
    lines = "Edge detection.

            Author: Bernie Pope (bjpope@unimelb.edu.au)...

            ...tester('gradient_threshold', GRADIENT_THRESH_TESTS, exact_equal)
             tester('convolute', CONVOLUTE_TESTS, exact_equal)"

    >>>[[TRAIL_WHITESPACE,4,line_length,,
         Author: Bernie Pope (bjpope@unimelb.edu.au). ],
    [TRAIL_WHITESPACE,51,line_length,,
      and check the output for correctness.      ],
    [TRAIL_WHITESPACE,244,line_length,,        return BLACK_PIXEL  ],
    [TRAIL_WHITESPACE,288,line_length,,
     "     [0,   0,   0,   0,   255, 255, 0,   0,   0,   0  ],            "],
    [TRAIL_WHITESPACE,311,line_length,,    ],
    [TRAIL_WHITESPACE,315,line_length,,"       return max(min(v, u), l)   "],
    [TRAIL_WHITESPACE,385,line_length,,
      "     [0,   0,   0,   0,   255, 255, 0,   0,   0,   0  ],    "],
    [TRAIL_WHITESPACE,406,line_length,,
      # An image with a sharp vertical edge.    ],
    [TRAIL_WHITESPACE,408,line_length,,
      "             [0, 0, 255, 255, 255],  "]]
    '''

    trail_whitespace_list = []
    line_count = 0

    for each_line in lines:
        line_count += 1
        # Strips all the white space on the right side of the line
        # and finds the length of this string.
        # We add 1 because we disignate the column as the position
        # with the first of the trailing whitespace.
        column_num = len(each_line.rstrip()) + 1
        if ' \n' in each_line or '\t\n' in each_line:
            trail_whitespace_list.append(["TRAIL_WHITESPACE", int(line_count),
                                         column_num, '', each_line[:-1]])

    return trail_whitespace_list


def find_bad_indent(python_filename, lines):
    '''
    Finds the instances of bad indents in the input python file and then
    returns the instances in the form of a list.

    The vars_indents from utlis.py is used to find the instances
    of bad indents in the input python file. This information is
    located in the second dictionary.

    A empty list is created called bad_indents_list to hold
    all the instances of bad indents.

    A for loop is used to cycle through every key in the second
    dictionary returned from the vars_indents function.
    Hence the functon stipulates variable_dictionary[1].keys().

    The second for loop, nested in the first for loop,
    then cycles through every indent with the designated key.

    An if statement, nested within the second for loop,
    then tests if the indent, in the form of a string,
    has a multiple of 4 spaces or a tab '\t'. These are the two instances
    of bad indents. If either of these are found then the instance
    is written to the bad_indents_list.

    The information written to the bad_indents_list in the instance
    of a bad indent includes the title BAD_INDENT, the line number
    the instance appears, the column number which is the position
    immediately after the indentation, the entire contents of the line
    containing the instance of the bad indent.

    Parameters:

        python_filename: The python file you want tested to find
                         instances of bad programming style.
        lines: The lines of the program

    Result:
    A list called bad_indents_list containing the information from
    each instance of a bad indent. This information includes
    the title BAD_INDENT, the line number the instance appears,
    the column number which is the position immediately after the indentation,
    the entire contents of the line containing the instance of the bad indent.

    Example:
    python_filename = 'naughty.py'
    lines = "Edge detection.

            Author: Bernie Pope (bjpope@unimelb.edu.au)...

            ...tester('gradient_threshold', GRADIENT_THRESH_TESTS, exact_equal)
             tester('convolute', CONVOLUTE_TESTS, exact_equal)"

    >>>[[BAD_INDENT,194,7,,"      r = gradient_row(image, row, col)"],
    [BAD_INDENT,301,6,,        new_row = []],
    [BAD_INDENT,305,12,,
      "              edge_pixel = gradient_threshold
      (image, row, col, threshold)"],
    [BAD_INDENT,315,8,,"       return max(min(v, u), l)   "],
    [BAD_INDENT,357,2,,    in_image = read_image(in_filename)],
    [BAD_INDENT,559,2,, ''Test for exact equality between two objects.''],
    [BAD_INDENT,581,6,,     ''Run all the test cases.'']]
    '''

    variable_dictionary = vars_indents(python_filename)
    bad_indent_list = []

    for each_key in variable_dictionary[1].keys():
        for indent in variable_dictionary[1][each_key]:
            if (str(indent).count(' ') % 4) > 0 or '\t' in str(indent):
                bad_indent_list.append(["BAD_INDENT", int(each_key),
                                       variable_dictionary[1][each_key][1],
                                       '', lines[each_key-1][:-1]])
    return bad_indent_list


def find_num_instances(list_total):
    '''
    Calculates the number of instances of each type of bad
    programmming instance in a given total list.
    The result is returned as a tuple with 4 numbers.

    1.    SINGLE_CHAR_VAR
    2.    LONG_LINE
    3.    TRAIL_WHITESPACE
    4.    BAD_INDENT

    Number counters for each instance of bad programming style are created,
    which includes the number of trailing whitespace,
    single character variables, bad indents, and long lines.
    These will be used to tally the total number of each instance and
    then used to calculate the total score out of 10.

    A for loop, with nested if and elif statements, are used to tally
    each instance and add to the respective counters.
    The for loop cycles through each list contained in the list_total.
    Each if/elif statement checks if the title matches with a particular
    bad instance, then adds 1 to its respective counter.
    This is done by checking if the first value of each_item is equal
    to the particular title of the bad programming style.
    Hence each_item[0] is used to select the first value.
    '''
    num_trail_whitespace = 0
    num_single_char_var = 0
    num_bad_indent = 0
    num_long_line = 0
    
    for each_item in list_total:
        if each_item[0] == "SINGLE_CHAR_VAR":
            num_single_char_var += 1
        elif each_item[0] == "LONG_LINE":
            num_long_line += 1
        elif each_item[0] == "TRAIL_WHITESPACE":
            num_trail_whitespace += 1
        elif each_item[0] == "BAD_INDENT":
            num_bad_indent += 1
    
    return (num_trail_whitespace, num_single_char_var,
            num_bad_indent, num_long_line)


def write_quality_score_log(python_filename, list_total, lines):
    '''
    Creates a csv file with a score out of 10 representing
    the number of instances of bad programming style are in a particular
    input python file and the date and time of when the function was used.
    
    The csv file, with filename of python_filename[:-2] + 'score.csv',
    is created if it does not exist already. If it already exists,
    the file is opened in append mode, so the contents of the file
    are not over-written. It is important the file is not overwritten
    because we want to create a log of the score and date. This will
    mean we can check if we are removing the bad instances, and
    therefore improving the quality of the code.
    
    The total penalty is calculated by the following:
    
        number of instances of trailing whitespace x 1 +
        number of instances of single character variables x 2 +
        number of instances of bad indents x 4 +
        number of instances of long lines x 5
    
    This intutively indicates the severity of each instance,
    with trailing whitespace being the least severe and long lines
    being the most severe, based on the number multiple.
    
    A variable called score is then used to calculate the value
    from the float of total_penalty and the float of num_lines.
    
    To prevent an error occuring if there are 0 instances of bad
    programming style, or there are 0 lines in the file, we have
    an if statement that makes score equal to 0 if the total_penalty
    is equal to 0. This is so we are not trying to divide 0, which
    will always throw up an error.
    
    The next variable, quality_score, calcuates the quality score based off the
    following equation:

    maximum of (0, 10 - (( total penalty / number of lines ) x 10 ))

    The maximum is used to ensure that the score does not fall below 0.

    Parameters:

        python_filename: The python file you want tested to find
                         instances of bad programming style.
        list_total: A list containing all the instances of
                    bad programming styles.
        lines: The lines of the program

    Result:
    Creates a csv log file with a score out of 10 representing
    how many instances of bad programming style are in a particular
    input python file and the date and time of when the function was used.

    Example:
    python_filename = 'naughty.py'
    list_total = [[TRAIL_WHITESPACE,4,line_length,,
                   Author: Bernie Pope (bjpope@unimelb.edu.au). ],
                  [TRAIL_WHITESPACE,51,line_length,,
                   and check the output for correctness.   ],...

              ...[BAD_INDENT,559,2,, ''
                  Test for exact equality between two objects.''],
                  [BAD_INDENT,581,6,,     ''Run all the test cases.'']]

    lines = "Edge detection.

            Author: Bernie Pope (bjpope@unimelb.edu.au)...
    
            ...tester('gradient_threshold',GRADIENT_THRESH_TESTS, exact_equal)
             tester('convolute', CONVOLUTE_TESTS, exact_equal)"
    
    >>>None
    '''
    quality_filename = python_filename[:-2] + 'score.csv'
    
    # The quality score file is opend in append mode so the
    # existing contents in the file are not over-written
    quality_file = open(quality_filename, 'a')
    writer = csv.writer(quality_file)
    
    total_penalty = find_num_instances(list_total)[0] * 1 +\
                    find_num_instances(list_total)[1] * 2 +\
                    find_num_instances(list_total)[2] * 4 +\
                    find_num_instances(list_total)[3] * 5
    
    # Counts the total number of lines in the input python file
    num_lines = sum(1 for each_line in lines)
    
    # To prevent an error occuring if there are 0 instances of
    if total_penalty == 0:
        score = 0
    else:
        score = float(total_penalty) / float(num_lines)
    
    # The quality score is limited to 2 decimals points
    quality_score = "%.2f" % (max(0, 10 - score * 10))
    
    # Writes the current date and time and the quality score
    # to the csv score file
    writer.writerow([get_current_date_time(), quality_score])
    
    quality_file.close()


def lint(python_filename):
    '''
    Creates a csv which lists a few of the instances of
    bad programming style from the given input python file.
    
    The 4 bad instances of programming style include:

        Single Character Variables - a variable name consisting of only
                                     a single character, such as x.

        Long Line - a line of code that is over 79 characters.

        Trailing Whitespace - a line that contains any space or tab characters
                              immediately before the end of the line.

        Bad Indent - an indent that is not a multiple of 4 single spaces.
                     This includes tabs.
    
    The following functions will also be utlised:
        
        1.    find_single_char_variable
    
        2.    find_long_line
    
        3.    find_trail_whitespace
    
        4.    find_bad_indent
    
        5.    write_quality_score_log
    
    A list total of all the instances of the above bad programming styles
    is created to contain what will be written into the csv file.

    This list of instances is then sorted by the line number, the second value.

    The header is first written into the file:

        ["ERROR_TYPE", "LINE_NUMBER", "COLUMN", "INFO", "SOURCE_LINE"]

    The for loop is used to then write every instance in the list_total
    to the file.

    The last part of the function calls the write_quality_score_log to
    create the csv log of the quality score.


    Parameters:

        python_filename: The python file you want tested to find
                         instances of bad programming style.

    Result:
    Two csv files. One containing every instance of the 4
    bad programming styles. The second, a log of the score out of 10
    for the amount of instances of bad programming styles
    with the date and time.

    Example:
    python_filename = 'naughty.py'

    >>>None
    '''
    in_file = open(python_filename)
    lines = in_file.readlines()
    out_filename = python_filename[:-2] + 'lint.csv'
    out_file = open(out_filename, 'w')
    writer = csv.writer(out_file)

    list_total = []
    
    # Adds all the instances to the list_total.
    list_total += find_single_char_variable(python_filename, lines)
    list_total += find_long_line(python_filename, lines)
    list_total += find_trail_whitespace(python_filename, lines)
    list_total += find_bad_indent(python_filename, lines)

    # Sorts the list_total by the line number each instance appears in.
    list_total.sort(key=lambda tup: tup[1])

    # Header is written to the top of the csv file.
    writer.writerow(["ERROR_TYPE", "LINE_NUMBER",
                    "COLUMN", "INFO", "SOURCE_LINE"])
    
    # Writes every item in the total list to the lint.csv file.
    for each_item in list_total:
        writer.writerow(each_item)

    out_file.close()
    
    # Creates the log quality .csv file.
    write_quality_score_log(python_filename, list_total, lines)
    