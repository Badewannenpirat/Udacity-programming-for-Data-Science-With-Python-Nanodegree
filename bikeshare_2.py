import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name = ''
    while city_name.lower() not in CITY_DATA:
        city_name = input("\nBy what city would you like to analyze: Chicago, New York City, Washington?\n")
        if city_name.lower() in CITY_DATA:
            city = CITY_DATA[city_name.lower()]
        else:
            print("Sorry you might have had a mistype. Try again!\n")

    # get user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input("\nBy what month would you like to analyze? Pick any month between January, June or even all!\n")
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            print("Sorry you might have had a mistype. Try again!\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input("\nBy what day of the week would you like to analyze? Pick any day between monday, sunday or even all!\n")
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else:
            print("Sorry you might have had a mistype. Try again!\n")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
      print('The most common month is: ', df['month'].mode()[0])
    except KeyError:
      print("\nThe most common month is:\nNo data available...")

    # display the most common day of week
    try:
        print('The most common day of the week is:', df['day_of_week'].value_counts().idxmax())
    except KeyError:
        print("\nThe most common day of the week is:\nNo data available...")

    # display the most common start hour
    try: 
      df['hour'] = df['Start Time'].dt.hour
      popular_hour = df['hour'].mode()[0]
      print('The most common hour is:', popular_hour)
    except KeyError:
      print("\nThe most common hour is:\nNo data available...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station from the given fitered data is: " + common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station from the given fitered data is: " + common_end_station)

    # display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is : " + str(frequent_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', sum(df['Trip Duration'])/86400, "Days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', df['Trip Duration'].mean()/60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types from the given fitered data is: \n" + str(user_types))
    
    # display counts of gender
    if "Gender" in (df.columns):
       print(str(df['Gender'].value_counts()))

    else:
       print("\nGender Types:\nNo data available for this month.")


    # display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("The earliest birth year is: ",int(df['Birth Year'].min()),
        "\nThe most recent birth year is: \n",int(df['Birth Year'].max()),
        "\nand The most common year of birth is: \n",int(df['Birth Year'].value_counts().idxmax()))
    else:
        print("\nDisplay earliest, most recent, and most common year of birth:\nNo data available for this month.")   
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    raw = input('\nWould you like to display the raw data?\n')
    if raw.lower() == 'yes':
        count = 0
        while True:
            pd.set_option("display.max_columns",200)
            print(df.iloc[count: count + 5])
            count =+ 5
            ask = input('\nWould you like to see the following 5 rows of raw data?\n')
            if ask.lower() != 'yes':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #added "display_raw_data(df)" for implementing query
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
