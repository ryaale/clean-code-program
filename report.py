'''
Report.

Author: Alexander Ryan.

This program reads two csv input files, the result of the
report.py program, and creates a report in html format
which contains the instances of bad programming style
presented in the csv input files. A quality score graph is
also created and inserted into the html code. This graph is
based off the information in the .score.csv file.



Revision History:

16 Oct 2014: Started building report.py
17 Oct 2014: built creat_quality_score_graph function
19 Oct 2014: wrote all documentation for the code



'''
import csv
from utils import plot_graph


def create_quality_score_graph(python_filename):
    '''
    Creates a quality score graph from the information
    in the (python_filename).score.csv file,
    created by the lint function in lint.py.
    
    The (python_filename).score.csv file is first
    opened and the contents stored in the variable
    list_of_scores.
    
    Two empty lists are created to put each element of the
    list of scores. x_axis_ticks will contain the date and
    time values in the csv file, while the each_score
    variable will contain each score from the file.
    
    The for loop is the element that moves this data into
    the respective lists. We only want the last 20 results
    to be put into the graph, so we limit the for loop to
    only go through the last 20 items from the list.
    Hence why we stipulate list_of_scores[-20:].
    
    We next call the function plot_graph from the utils.py
    program.
    
        1.    each_score goes into the y-variable location
    
        2.    x_axis_ticks goes into the x-variable location
           
        3.    we want the y axis max to be 10, since that is the most
              the score can go up to
    
        4.    the x axis title is 'Date and Time'
    
        5.    the y axis title is 'Score (out of 10)'
    
        6.    the title of the whole graph is 'Quality Score Graph'
    
        7.    the filename will be python_filename[:-2] + 'history.svg'
    
    Parameters:
    
    python_filename: The name of the python file you want to create
    a quality score graph for.
    
    Example:
    
    python_filename = 'naughty.py'
    >>>None
    
    creates a svg file called naughty.history.svg
    
    '''
    # Reads the contents of the .score.csv file and puts it into
    # a list
    with open(python_filename[:-2] + 'score.csv', 'rb') as contents:
        reader = csv.reader(contents)
        list_of_scores = list(reader)
    
    x_axis_ticks = []
    each_score = []
    
    # Takes the last 20 scores and appends the contents into
    # the two empty lists x_axis_ticks and each_score
    for each_line in list_of_scores[-20:]:
        x_axis_ticks.append(each_line[0])
        each_score.append(each_line[1])

    # Calls the plot_graph function from utils.py
    plot_graph(each_score, x_axis_ticks, 10, 'Date and Time',
               'Score (out of 10)' , 'Lint score history for ' +
               python_filename, python_filename[:-2] + 'history.svg')
    

def report(python_filename):
    '''
    Reads the output from the lint function in lint.py,
    namely the .lint.csv and .score.csv files, and creates
    a html file and svg file.
    
    Each line of the html file is written into the file.
    
    The for loop cycles through every instance in the
    list_of_instances, and writes each line into the
    html file.
    
    Each individual instance is written to
    the html file differently.
    
    Parameters:
    
        python_filename: The name of the python file you want to create
    
    Result:
    
    A html file and a svg file. The html file contains a report
    of the instances of bad programming style in an input
    python file. The svg file contains a graph of the scores
    contained in the .score.csv file over time.
    
    Example:
    
    python_filename = 'naughty.py'
    >>>None
    
    Creates a html file naughty.report.html
    Creates a svg file called naughty.history.svg
    
    '''
    # Creates the file .report.html file in write mode
    out_filename = python_filename[:-2] + 'report.html'
    out_file = open(out_filename, 'w')
    
    # Opens the .lint.csv file and reads the lines into
    # the variable lines
    with open(python_filename[:-2] + 'lint.csv', 'rb') as contents:
        reader = csv.reader(contents)
        list_of_instances = list(reader)
    
    out_file.write('\n')
    out_file.write('<!DOCTYPE html>\n')
    out_file.write('<html>\n')
    out_file.write('    <head>\n')
    out_file.write('        <title>Lint report</title>\n')
    out_file.write('    </head>\n')
    out_file.write('    <body>\n')
    out_file.write('        <h1>Lint report for ' +
                   python_filename + '</h1>\n')
    out_file.write('        <h2>Errors</h2>\n')
    out_file.write('            <ol>\n')
    
    for line in list_of_instances[1:]:
        if line[0] == "SINGLE_CHAR_VAR":
            out_file.write('                <li>Line: ' + line[1] + ', Col: ' +
                           line[2] + '. Single character variable ' +
                           line[3] + '.<br><pre>&longrightarrow;' +
                           line[4] + '&longleftarrow;</pre></li>\n')
        elif line[0] == "LONG_LINE":
            out_file.write('                <li>Line: ' + line[1] +
                           '. Line too long, length = ' + line[3] +
                           '.<br><pre>&longrightarrow;' + line[4] +
                           '&longleftarrow;</pre></li>\n')
        elif line[0] == "TRAIL_WHITESPACE":
            out_file.write('                <li>Line: ' + line[1] +
                           ', Col: ' + line[2] +
                           '. Trailing whitespace.<br><pre>&longrightarrow;' +
                           line[4] + '&longleftarrow;</pre></li>\n')
        elif line[0] == "BAD_INDENT":
            out_file.write('                <li>Line: ' + line[1] + ', Col: ' +
                           line[2] + '. Bad indent.<br><pre>&longrightarrow;' +
                           line[4] + '&longleftarrow;</pre></li>\n')

    out_file.write('            </ol>\n')
    out_file.write('        <h2>Score history</h2>\n')
    
    # Creates the quality score graph which will be written
    # to the html file in the next line
    create_quality_score_graph(python_filename)
    
    out_file.write('            <img src="' + python_filename[:-2] +
                   'history.svg" alt="Lint score history for ' +
                   python_filename + '">\n')
    out_file.write('    </body>\n')
    out_file.write('</html>\n')
    out_file.close()
