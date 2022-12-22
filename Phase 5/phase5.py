#-----------------------------------------------------------#
# Author: Pratik Antoni Patekar                             #
#-----------------------------------------------------------#
# The University of Texas at Arlington                      #
#-----------------------------------------------------------#
# CSE 5330: Database Systems - Phase 5 Final code           #
#-----------------------------------------------------------#

# Import the required packages
import pandas as pd         # for storing the results obtained from database and printing
import sys                  # for system commands like exiting code if error occurs
import cx_Oracle as cora    # for accessing the Omega Oracle system
import maskpass             # for taking user password as input
from art import *           # for cosmetic effects in the beginning

# Function 1: To execute the business query 1
def exec_query_1(c):
    # SQL query to be executed written as string and values to be passed from front end
    # specified as bindings followed by ":" in the query
    sql = """
    select pid, fname, lname, count(song_id) as song_count
    from fall22_s004_10_songs songs, fall22_s004_10_person person
    where fname = :fname and
            lname = :lname and 
            (songs.song_id, person.pid) in (-- get pid of customers from customers table
                                      select song_id, pid
                                      from fall22_s004_10_avail_songs asong, fall22_s004_10_customer cust
                                      where (asong.avail_song_id, cust.cust_id) in (-- get pruchase song history from buys_rents table
                                                                                    select avail_song_id, cust_id 
                                                                                    from fall22_s004_10_buys_rents
                                                                                    -- 'B' indicates that song is pruchased and not rented
                                                                                    where trans_type = :trans_type)
                                                                                    )
    group by pid, fname, lname
    --having count(song_id) >= 2
    --order by song_count desc
    --fetch first 10 rows only
    """
    # Getting the required inputs from the user for plugging it in the above sql query
    first_name = input("Enter first name of customer: ")
    last_name = input("Enter last name of customer: ")
    trans_typp = input("Enter the transaction type (b - purchase, r - rent): ")
    
    # Input value checks
    if trans_typp.lower() == 'b':
        trans_typp = 'B'
    else:
        trans_typp = 'R'
    
    # Execute the query
    c.execute(sql, [first_name, last_name, trans_typp])

    # Printing the results using the pandas DataFrame
    num_col = 4
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)

    df_sg_count = pd.DataFrame(pd_list, columns = ["PID", "CUST_FNAME", "CUST_LNAME", "SONG COUNT"])
    if df_sg_count.empty:
        print('\n\nError message: Results table is empty.')
    else:
        print(df_sg_count.to_string())

# Function 2: To execute the business query 2
def exec_query_2(c):
    # SQL query to be executed written as string and values to be passed from front end
    # specified as bindings followed by ":" in the query
    sql = """
    select year, year_revenue, sum(year_revenue) over (order by year rows between unbounded preceding and current row) as cum_revenue
    from (
            select year, sum(price) as year_revenue
            from (
                    select substr(trans_date, 7, 4) as year, 
                          (case when trans_type = 'B' then purchase_price else rent_price end) as price
                    from fall22_s004_10_buys_rents buys_rents, fall22_s004_10_avail_songs asongs
                    where buys_rents.avail_song_id = asongs.avail_song_id
                    )
            where year between :start_year and :end_year
            group by year
            order by year
            )
        """
    # write input check statements
    # Getting the required inputs from the user for plugging it in the above sql query
    start_year = input("Enter start year: ")
    end_year = input("Enter end year: ")

    # Execute the query
    c.execute(sql, [start_year, end_year])

    # Printing the results using the pandas DataFrame
    num_col = 3
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)

    df_cumm_rev = pd.DataFrame(pd_list, columns = ["YEAR", "YEAR_REVENUE", "CUMM_REVENUE"])
    if df_cumm_rev.empty:
        print('\n\nError message: Results table is empty.')
    else:
        print(df_cumm_rev.to_string())


def exec_query_3(c):
    # SQL query to be executed written as string and values to be passed from front end
    # specified as bindings followed by ":" in the query
    sql = """select person.fname as singer_fname, person.lname as singer_lname, songs.song_name, count(*) as likes_count
    from fall22_s004_10_likes likes, fall22_s004_10_avail_songs asongs, fall22_s004_10_sings sings, fall22_s004_10_songs songs, 
          fall22_s004_10_artist artist, fall22_s004_10_singer singer, fall22_s004_10_person person
    where likes.avail_song_id = asongs.avail_song_id and
          asongs.song_id = songs.song_id and
        songs.song_id = sings.song_id and
        sings.singer_id = singer.singer_id and
        singer.artist_id = artist.artist_id and 
        artist.pid = person.pid
    group by person.fname, person.lname, sings.singer_id, songs.song_name
    order by likes_count desc
    fetch first :k_num rows only""" 

    # write validation for k_num
    # Getting the required inputs from the user for plugging it in the above sql query
    k_num = int(input("Enter the value of k: "))

    # Execute the query
    c.execute(sql, [k_num])

    # Printing the results using the pandas DataFrame
    num_col = 4
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)

    df_top_k = pd.DataFrame(pd_list, columns = ["SINGER_FNAME", "SINGER_LNAME", "SONG_NAME", "LIKE_COUNT"])
    if df_top_k.empty:
        print('\n\nError message: Results table is empty.')
    else:
        print(df_top_k.to_string())

def exec_query_4(c):
    # SQL query to be executed written as string and values to be passed from front end
    # specified as bindings followed by ":" in the query
    sql = """select status, count(song_id) as song_count
    from  
          (-- get the song ids of available songs and assign 'Available' as status  
          (select songs.song_id, 'Available' as status 
          from fall22_s004_10_avail_songs asongs, fall22_s004_10_songs songs
          where (songs.song_id = asongs.song_id))
          union
          (-- get the song ids of unavailable songs and assign 'Unavailable' as status
          select songs.song_id, 'Unavailable' as status
         from fall22_s004_10_unavail_songs uasongs, fall22_s004_10_songs songs
          where (songs.song_id = uasongs.song_id)))
    -- group by on Status and get song_count
    where status in (:in1, :in2)
    group by status
    order by song_count"""

    # write check statements for in1
    # Getting the required inputs from the user for plugging it in the above sql query
    in1 = input("Enter song type (A/ U/ B): ").upper()

    if in1 == 'A':
        in2 = 'Available'
        in3 = 'Available'
    elif in1 == 'U':
        in2 = 'Unavailable'
        in3 = 'Unavailable'
    else:
        in2 = 'Available'
        in3 = 'Unavailable'

    # Execute the query
    c.execute(sql, [in2, in3])

    # Printing the results using the pandas DataFrame
    num_col = 2
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)
    
    df_song_stat = pd.DataFrame(pd_list, columns = ["Status", "Song_count"])
    if df_song_stat.empty:
        print('\n\nError message: Results table is empty.')
    else:
        print(df_song_stat.to_string())


def modify_person(conn, c):
    # Get inputs from user which needs to be modified
    first_name = input("\nEnter the name that you want to update: ")
    last_name = input("Enter the last name: ")

    # Get the table contents from the server
    df_person = display_person(c, False)

    # Check if the record exists in the table before performing update SQL statement
    if first_name in df_person['FNAME'].values:
        print("\nFirst name present in the database")
    else:
        print("\nERROR: No such first name exists in the database")
        return

    if last_name in df_person['LNAME'].values:
        print("Last name present in the database")
    else:
        print("ERROR: No such last name exists in the database")
        return

    # Print the record(s) if the exists that need to be modified
    df_out = df_person[(df_person['FNAME'] == first_name) & (df_person['LNAME'] == last_name)]
    print('\n\nFollowing are the records that will be affected.\n')
    print(df_out.to_string())

    # SQL query to be executed written as string and values to be passed from front end
    # specified as bindings followed by ":" in the query
    sql = "update fall22_s004_10_person set fname = :fname, lname = :lname where fname = :fname1 and lname = :lname1"

    # Get the details that need to be modified
    new_fname = input("\nEnter the new first name: ")
    new_lname = input("Enter the new last name: ")

    try:
        c.execute(sql, [new_fname, new_lname, first_name, last_name])
        conn.commit()
        c.execute("select * from fall22_s004_10_person where fname = :fname and lname = :lname", [new_fname, new_lname])
        num_col = 6
        pd_list = []
        for row in c:
            x = []
            for i in range(num_col):
                x.append(row[i])
            pd_list.append(x)

        df_person_new = pd.DataFrame(pd_list, columns = ["PID", "FNAME", "MNAME", "LNAME", "GENDER", "DOB"])

        print("\nFollowing are the modified rows of the person table:")
        print(df_person_new.to_string())
    except:
        # Database error
        print("Database error: The entered name combinaton already exists. The fname and lname pair should be unique.")
        return

def modify_songs(conn, c):
    # Get the table contents from the server
    df_songs = display_songs(c, False)
    
    try:
        # Check if the entered song id exists in the table
        song_id = int(input("Enter the song id that you want to delete: "))
        if song_id not in df_songs['SONG_ID'].values:
            print("ERROR: Invalid song id entered.")
            return
    except:
        print("ERROR: Invalid song id entered.")
        return

    # SQL query to be executed written as string and values to be passed from front end
    # specified as bindings followed by ":" in the query
    sql = "delete from fall22_s004_10_songs where song_id = :song_id"
    
    # Execute the sql statement
    c.execute(sql, [song_id])
    conn.commit()
    
    # Display all the records in the songs table after modification
    c.execute('select * from FALL22_S004_10_SONGS')
    num_col = 5
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)

    df_songs = pd.DataFrame(pd_list, columns = ["SONG_ID", "SONG_NAME", "GENRE", "REGION", "RELEASE_DATE"])

    print("\nFollowing are the modified records of the songs table:\n")
    if df_songs.empty:
        print('\n\nError message: The songs table is empty.')
    else:
        print(df_songs.to_string())

# Function to modify the table on basis of the table indicator
def modify_table(table_ind, conn, c):
    if table_ind == 'p':
        modify_person(conn, c)
    elif table_ind == 's':
        modify_songs(conn, c)
    else:
        print("Invalid table indicator entered")
        return

# Function to display buys_rents table
def display_buys_rents(c, display = True):
    c.execute('select * from FALL22_S004_10_BUYS_RENTS')
    num_col = 9
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)
    
    df_buys_rents = pd.DataFrame(pd_list, columns = ["AVAIL_SONG_ID", "CUST_ID", "TRANS_ID", "TRANS_TYPE", "PAY_MODE", "TRANS_DATE", "TRANS_TIME", "BANK_NAME", "DURATION"])

    if display == True:
        if df_buys_rents.empty:
            print('\n\nError message: The buys_rents table is empty.')
        else:
            print(df_buys_rents.to_string())
    return df_buys_rents

# Function to display the songs table
def display_songs(c, display = True):
    c.execute('select * from FALL22_S004_10_SONGS')
    num_col = 5
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)
    
    df_songs = pd.DataFrame(pd_list, columns = ["SONG_ID", "SONG_NAME", "GENRE", "REGION", "RELEASE_DATE"])

    if display == True:
        if df_songs.empty:
            print('\n\nError message: The songs table is empty.')
        else:
            print(df_songs.to_string())
    return df_songs

# Function to display person table
def display_person(c, display = True):
    c.execute('select * from FALL22_S004_10_PERSON')
    num_col = 6
    pd_list = []

    for row in c:
        x = []
        for i in range(num_col):
            x.append(row[i])
        pd_list.append(x)
    
    df_person = pd.DataFrame(pd_list, columns = ["PID", "FNAME", "MNAME", "LNAME", "GENDER", "DOB"])

    if display == True:
        if df_person.empty:
            print('\n\nError message: The persons table is empty.')
        else:
            print(df_person.to_string())
    return df_person

# Function to display table on basis of table indicator
def display_table(table_ind, c):
    if table_ind == 'b':
        return(display_buys_rents(c))
    elif table_ind == 's':
        return(display_songs(c))
    elif table_ind == 'p':
        return(display_person(c))
    else:
        print("Invalid table indicator entered.")
        return

# Main function
def main():
    # Welcome message "Welcome to Chimes Music"
    print("------------------------------------------------------------------------------------")
    tprint("WELCOME   TO")
    tprint("CHIMES MUSIC")
    print("------------------------------------------------------------------------------------")
    
    # Initialise the connection to Omega Oracle client
    print("Initializing connection with Omega Oracle client.")
    try:
        cora.init_oracle_client(lib_dir = "C:/Users/patek/Downloads/Phase5-JDBC/instantclient_21_7")
        username = input("Enter Username: ") # pxp7948
        password = maskpass.askpass(mask="") # Hgd3df7hTdrd8s
        conn = cora.connect(username + '/' + password + '@az6F72ldbp1.az.uta.edu:1523/pcse1p.data.uta.edu')
        print("Connection established...")
        print("Connection version: " + conn.version + "\n\n")
    except:
        print("ERROR: Could not establish connection with the SQL server. Check if the enter credentials are correct.")
        return
    
    # Create cursor to execute the sql statements
    c = conn.cursor()

    # Print all the tables that are present to the current user view
    print("Printing all the tables present for current user: " + username)
    c.execute('select * from cat')
    check_count = 0
    for row in c:
        print(row[0])
        if row[0] in ('FALL22_S004_10_BUYS_RENTS', 'FALL22_S004_10_PERSON', 'FALL22_S004_10_SONGS'):
            check_count += 1
    print("\n\n")

    if check_count != 3:
        print('ERROR: One or more of the following tables is missing in the database view for the current user.')
        print('1. FALL22_S004_10_BUYS_RENTS\n2. FALL22_S004_10_PERSON\n3. FALL22_S004_10_SONGS')
        print('\nTerminating session...')
        conn.close()
        return

    # Start the main menu loop
    while True:
        # Display the main menu
        print("\n\nFollowing are the options that we can be executed from the front end interface:")
        options = [['1', 'Display contents of tables'], 
                    ['2', 'Modification of tables data'],
                    ['3', 'Performing Business goals from front end'],
                    ['4', 'Exit code']]
        df_options = pd.DataFrame(options, columns = ['Option #', 'Description'])
        print(df_options.to_string(index=False))

        # Take user option input
        opt = input("\nEnter option corresponding to the operation that you want to perform: ")
        
        # Validate the input option
        if opt not in ('1', '2', '3', '4'):
            print("\nInvalid option entered. Restarting ...")
            continue
        
        # If the opt is 4 then terminate the session and close the connection
        if opt == '4':
            print("Terminating session.")
            conn.close()
            return

        # If opt is 1 then display the table names to be displayed
        if opt == '1':
            # Display the available options
            options1 = [['1', 'buys_rents'], 
                    ['2', 'songs'],
                    ['3', 'person'],
                    ['4', 'Back to main menu.']]
            df_options1 = pd.DataFrame(options1, columns = ['Option #', 'Table name'])
            print(df_options1.to_string(index=False))
            
            # Get user input option
            opt1 = input("\nEnter option from above: ")

            # Validation
            if opt1 not in ('1', '2', '3', '4'):
                print("\nInvalid option entered. Returning to main menu.")
                continue
            
            # Depending on the option entered display the table using the functions created above main function
            if opt1 == '1':
                display_table('b', c)
            elif opt1 == '2':
                display_table('s', c)
            elif opt1 == '3':
                display_table('p', c)
            else:
                continue
        
        # if option in main menu is 2 then display the database modification options
        elif opt == '2':
            # Display the options
            options2 =  [['1', 'Update name of person from Person table using fname and lname.'],
                        ['2', 'Delete song from Songs table using song_id.'],
                        ['3', 'Back to main menu.']]
            df_options2 = pd.DataFrame(options2, columns = ['Option #', 'Description'])
            print(df_options2.to_string(index=False))

            # get user option input
            opt2 = input('\nEnter option from above: ')

            # Validation
            if opt2 not in ('1', '2', '3'):
                print("\nInvalid option entered. Returning to main menu.")
                continue
            
            # Depending on the user input modify the table using the functions created above main
            if opt2 == '1':
                modify_table('p', conn, c)
            elif opt2 == '2':
                modify_table('s', conn, c)
            elif opt2 == '3':
                continue
        
        # If the option entered in the main menu is 3 then display the queries that can be executed
        elif opt == '3':
            # Display the options available
            options3 = [['1', 'Find the number of songs purchased or rented by a customer.'],
                            ['2', 'Generate cummulative sum revenue report for year range specified.'],
                            ['3', 'Find top k singers with highest number of likes for their songs (k specified by user).'],
                            ['4', 'Find number of songs that are available, unavailable or both as specified by user.'],
                            ['5', 'Back to main menu.']]
            df_options3 = pd.DataFrame(options3, columns = ['Option #', 'Description'])
            print(df_options3.to_string(index=False))

            # Get user input
            opt3 = input('\nEnter option from above: ')

            # Validation
            if opt3 not in ('1', '2', '3', '4', '5'):
                print("\nInvalid option entered. Returning to main menu.")
                continue
            
            # Depending on the option entered execute the required query using functions created above main
            if opt3 == '1':
                exec_query_1(c)
            elif opt3 == '2':
                exec_query_2(c)
            elif opt3 == '3':
                exec_query_3(c)
            elif opt3 == '4':
                exec_query_4(c)
            else:
                continue

if __name__ == "__main__":
    main()

