#####################################################################################################
#####################################################################################################
#################   _____ ____________ ______ ______          _                     #################
#################  |  ___|___  /| ___ \___  / | ___ \        | |                    #################
#################  | |__    / / | |_/ /  / /  | |_/ /_ _  ___| | ____ _  __ _  ___  #################
#################  |  __|  / /  |  __/  / /   |  __/ _` |/ __| |/ / _` |/ _` |/ _ \ #################
#################  | |___./ /___| |   ./ /___ | | | (_| | (__|   < (_| | (_| |  __/ #################
#################  \____/\_____/\_|   \_____/ \_|  \__,_|\___|_|\_\__,_|\__, |\___| #################
#################                                                        __/ |      #################
#################                                                       |___/       #################
#################                                                                   #################
#################                                        Author: Jacob Brehm (2019) #################
#####################################################################################################
#####################################################################################################

#####################################################################################################
#################                            CSV-RELATED                            #################
#####################################################################################################

def ReadCSV(filepath, columns, sort=False, condense=True):
    '''
    Reads the user-specified columns from a given .csv file.

    Parameters:
        filepath         (str)   --  filepath to the .csv file
        columns          (list)  --  integer list of columns to store
        sort             (bool)  --  toggles whether to sort the columns list
                                     (optional, default is False)
        condense         (bool)  --  toggles whether to remove duplicates from the columns list
                                     (optional, default is True)
    '''

    # Verify that each item of the columns list is an integer
    for column in columns:
        if type(column) != int:
            column_string = str(column) if type(column) == float else ( '\'' + str(column) + '\'' )
            message = column_string + ' is not an integer, so it cannot be used as a column index.'
            raise ValueError(message)

    # Import relevant packages
    import csv
    from collections import OrderedDict

    # Remove duplicates if desired
    if condense:
        columns = list(OrderedDict.fromkeys(columns))

    # Sort if desired
    if sort:
        columns.sort()

    # Create a list with a sublist for each column
    data = []
    [data.append([]) for i in range(len(columns))]

    # Iterate through the .csv file and add them to the appropriate sublist
    reader = csv.reader(open(filepath, 'r'), delimiter=',')
    for row in reader:
        for i, item in enumerate(row, start=1):
            for c, column in enumerate(columns, start=0):
                if i == column:
                    try:
                        data[c].append(float(item) if ('.' in item) else int(item))
                    except:
                        data[c].append(item if item else None)

    # Return the relevant information as a list of lists
    return data


def WriteCSV(filepath, data):
    '''
    Writes a list of lists to a .csv file.

    Parameters:
        filepath         (str)   --  destination of the .csv file
        data             (list)  --  list of lists to write
    '''

    # Import relevant packages
    import csv

    #
    index = None
    longest = None
    for i, sublist in enumerate(data):
        length = len(sublist)
        if ( not index ) or ( length > longest ):
            index = i
            longest = length

    #
    write = []
    [write.append([]) for i in range(longest)]

    #
    for i in range(longest):
        for sublist in data:
            write[i].append(sublist[i])

    #
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(write)


def SeparateData(data, header_rows=None):
    '''
    Separates data in the form of a list of lists (intended to be created by the ReadCSV function)
    into header data and body data.

    Parameters:
        data             (list)  --  list of lists to separate
        header_rows      (int)   --  number of header rows in the data (default is None)
    '''

    header, body = [], []
    if header_rows is not None:
        for c in range(len(data)):
            header.append( data[c][0:header_rows] )
            body.append( data[c][header_rows:] )
    else: body = data

    return header, body


def CombineData(header, body):
    '''
    Combines header and body information (intended to be created by the SeparateData function)
    into data in the form of a list of lists.

    Parameters:
        header           (list)  --  header list of lists
        body             (list)  --  body list of lists
    '''

    data = []
    for c, column in enumerate(header):
        data.append( header[c] + body[c] )

    return data


#####################################################################################################
#####################################################################################################
##############################  ______ _       _     _              _  ##############################
##############################  |  ___(_)     (_)   | |            | | ##############################
##############################  | |_   _ _ __  _ ___| |__   ___  __| | ##############################
##############################  |  _| | | '_ \| / __| '_ \ / _ \/ _` | ##############################
##############################  | |   | | | | | \__ \ | | |  __/ (_| | ##############################
##############################  \_|   |_|_| |_|_|___/_| |_|\___|\__,_| ##############################
##############################                                         ##############################
#####################################################################################################
#####################################################################################################