'''
Utility code for COMP10001 Project 3, Semester 2 2014.

Author: Bernie Pope (bjpope@unimelb.edu.au).

This module contains utility code which is helpful for implementing
COMP10001 Project 3, a Python style checking program.

It contains the following three functions:

    - vars_indents: collects variable names and indentation
          information from a Python file. The results are returned in a
          2-tuple of dictionaries, one for variables and one for indentation.
          The dictionaries are indexed by line number.

    - get_current_date_time: returns the current date and time at the
          point when the function is called. The result is returned as a
          string in the format: <year>-<month>-<day> <hour>:<min>:<sec>

    - plot_graph: plots a line graph from an input data set and saves the
          result to a SVG file.

Revision history:

22 Sep 2014: Initial version.
1  Oct 2014: Added get_current_date_time.
4  Oct 2014: Added comments, changed graph file output to SVG from PNG.
'''

VERSION = 1.0

from tokenize import generate_tokens
from token import NAME, INDENT
from keyword import iskeyword
from datetime import datetime
import matplotlib
# Generate output graphs in SVG format and turn off warnings which
# are normally generated when the module is reloaded.
matplotlib.use('svg', warn=False)
import matplotlib.pyplot as plt


def vars_indents(python_filename):
    '''Read the contents of a Python file and find all variables and all
    indents. The results are returned as a pair of dictionaries which are
    indexed by line number. Line numbers start at 1. Multiple variables can
    appear on the same line, but only one indent can appear on a line. The
    variables and indents are found by tokenizing the Python file using the
    standard library tokenize.

    Parameters:

        python_filename: a string, the name of the input Python file.

    Result:

        A 2-tuple of dictionaries. The first dictionary represents all
        variables in the Python file. The second dictionary represents all
        indents in the Python file. The keys of each dictionary are integer
        line numbers, such that the first line number is 1.

        Each variable is represented in the output by a 2-tuple containing
        the name of the variable as a string, and the integer column number
        of the first character in the variable name.

        Each indent is represented by in the output by a 2-tuple containing
        the text of the indent, and the integer column number of the first
        character immediately following the indent.

        Multiple variables can appear on the same line in a Python file.
        Therefore, each value in the variable dictionary is a list of
        2-tuples. Each 2-tuple in the list describes a single variable
        occurrence on the given line in the format described above.

        A maximum of one indent can occur per line. Therefore, each value
        in the indent dictionary is a single 2-tuple containing information
        about that indent in the format described above.

    Notes:

        Only one indentation token is generated for an entire indented block
        of Python code. So we get just one indent for the whole block rather
        than one for each line. This is sufficient for the purposes of the
        project, but may be surprising if you were expecting to see an indent
        for every line of code in the input file.

        This function does no error checking. It assumes that the input file
        exists and can be read by the program. It also assumes that the input
        is syntactically correct Python code.

        Missing files, files that cannot be read, or files that do not contain
        Python code may cause this function to raise exceptions.

    Example (truncated for brevity):

        >>> vars_indents("utils.py")
        ({129: [('variables', 17), ('line_number', 27),
                ('token_info', 43)], ... },
         {129: ('                ', 17), 163: ('    ', 5), ... })
    '''

    python_file = open(python_filename)
    # Obtain a generator for all lexical tokens for the input Python file.
    token_gen = generate_tokens(python_file.readline)
    variables = {}
    indents = {}
    # Iterate over all tokens in the file and collect those corresponding to
    # variables (a subset of NAME tokens) and indents (the INDENT token).
    for (token_type, token_text, start_pos, end_pos, _src_line) in token_gen:
        # Check for variables.
        if token_type == NAME and not iskeyword(token_text):
            # Variables are NAME tokens which are not keywords.
            line_number, start_col = start_pos
            # We record the variable name as a string, plus the column
            # coordinate of the first character in the name. The tokenizer
            # starts columns at 0, but we prefer columns to start at 1, so we
            # adjust accordingly by adding 1. Most text editors report column
            # numbers starting from 1.
            token_info = (token_text, start_col + 1)
            # We record all variables occurring on the same line in a list.
            # The variables dictionary is indexed by line number.
            if line_number in variables:
                # We've seen this line number before, extend its existing
                # list of variables.
                variables[line_number].append(token_info)
            else:
                # We have not seen this line number before, record this
                # as the first variable for the line as a singleton list.
                variables[line_number] = [token_info]
        # Check for indents.
        elif token_type == INDENT:
            # There can only be one indent at most per line. We record the
            # coordinate of the character immediately after the indent.
            line_number, end_col = end_pos
            token_info = (token_text, end_col + 1)
            indents[line_number] = token_info
    python_file.close()
    return variables, indents


def get_current_date_time():
    '''Return the current local date and time and return as a string the
    format:

    <year>-<month>-<day> <hour>:<min>:<sec>

    Months, days, hours, minutes and seconds and shown in a field width of two
    characters padded with leading zeros where necessary. Hours are recorded in
    24-hour format.

    Example:

        >>> get_current_date_time()
        '2014-09-04 09:15:43'
    '''
    now = datetime.now()
    return "%d-%02d-%02d %02d:%02d:%02d" % \
           (now.year, now.month, now.day,
               now.hour, now.minute, now.second)


def plot_graph(data, x_axis_ticks, max_y_val, xlabel, ylabel, title, filename):
    '''Plot a line graph of a numerical data set. The graph is saved in SVG
    format to a file named by the filename parameter. The ticks on the x-axis
    are rotated 270 degrees to display vertically. Each data point on the
    line is indicated with a solid dot.

    Arguments:

        data: A list of numbers (either integers or floating point).
        x_axis_ticks: A list of strings for labeling the x-axis ticks. The
            length of data and x_axis_ticks should be the same.
        max_y_val: The maximum y value to display on the y axis, as an integer.
            The y axis ticks will be labeled by integers in
                range(max_y_val + 1).
            This number should be greater than or equal to the largest value
            in data.
        xlabel: A string to label the entire x axis.
        ylabel: A string to label the entire y axis.
        title: A string providing the title for the graph.
        filename: A string naming the file into which the graph will be saved.
            If the file already exists it will be overwritten. The filename
            must end in a ".svg" suffix.

    Result:

        None

    Example:

        >>> plot_graph([6.3, 5.2, 9.75], ["2012", "2013", "2014"], 10, \
               "Widgets", "Price", "Widget price 2012-2014", "widgets.svg")
    '''
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    # Plot the data as a line, and show each data point with a solid dot
    # on the line.
    plt.plot(data, '-o')
    # Label the x-axis ticks, and rotate the labels 270 degrees so that
    # they display vertically.
    plt.xticks(range(len(x_axis_ticks)), x_axis_ticks, rotation=270)
    # Plot the ticks on the y axis and ensure that they go up to
    # max_y_val.
    plt.yticks(range(max_y_val + 1))
    # Save the graph to a file and ensure that the bounding box fits
    # tightly around the figure (including the rotated x axis ticks).
    plt.savefig(filename, bbox_inches='tight')
    # It is necessary to close the plot, so that new graphs appear in
    # separate figures.
    plt.close()
