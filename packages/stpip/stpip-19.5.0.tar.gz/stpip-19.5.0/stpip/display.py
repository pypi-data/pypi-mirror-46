'''
---stpip---
This file contains the code that display the results

@R. Thomas
@Santiago, Chile
@2019
'''


def indiv(number,  display_type, package):
    '''
    This function go scrap pepy.tech

    Parameters
    -----------
    number
            int, number of downloads
    display_type
            str, type of display
    package
            str, name of the package

    Returns
    -------
    '''

    url = 'https://pepy.tech/project/' + package

    print('\033[1m\n###############################################\033[0m')
    print('\033[1m      Download counts for %s \033[0m'%package)
    
    if display_type == 'total':
        print('\033[1m Total all time:' + '\033[94m %s\033[0m'%number)

    else:
        print('\033[1m Total last %s:'%display_type + '\033[94m %s\033[0m'%number)

    print('\033[1m--> visit %s \033[0m'%url) 
    print('\033[1m\033[91m##############################################\n\033[0;0m') 
 

def full(total, month, day, yest, yest_down, ndays, package):
    '''
    Display all the download informations

    Parameters
    ----------
    total
            int, total number of downloads, all time
    month
            int, number of downloads in last month
    day
            int, number of downloads in the last week
    ndays
            int, total nu,ber of days in the webpage
    pacakge
            int, name of the package

    '''
    if yest_down == '0 0 0':
        url = 'No package found on pepy.tech with name %s'%package

    else:
        url = 'visit https://pepy.tech/project/' + package
    print('\033[1m\n###############################################\033[0m')
    print('\033[1m      Download counts for %s \033[0m'%package)
    print('\033[1m Total all time:' + '\033[94m %s\033[0m'%total)
    print('\033[1m Total last %s days:'%(ndays) + '\033[94m %s\033[0m'%month)
    print('\033[1m Total last 7 days:' + '\033[94m %s\033[0m'%day)
    print('\033[1m last day %s:'%yest_down + '\033[94m %s\033[0m'%yest)
    print('\033[1m--> %s \033[0;0m'%url) 
    print('\033[1m\033[91m##############################################\n\033[0m') 
    

