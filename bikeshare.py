import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

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
    while True:
        city = input("Would you like to see data for Chicago, New York City,or Washington\n").lower()
        # check the city name if it's one of supported cities (chicago, new york city, washington)
        if city in CITY_DATA.keys():
            break
        else:
            print('Please enter valid city.')

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        choice = input("Would you like to filter the data by month, day, both, or not at all? Type \"none\" for no time filter.\n").lower()
        # handle month choice
        if choice == 'month' or choice == 'both':
            month = input("Which month? All, January, February, March, April, May, June\n").lower()
            if month not in MONTHS:
                print('Please enter a valid month.')
                continue
            else:
                if choice == 'month':
                    day = 'all'
                    break
        # handle day or both choice        
        if choice == 'day' or choice == 'both':
            day = input("Which day? All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()
            if choice == 'day':
                month = 'all'
            if day not in DAYS:
                print('Please enter a valid day')
                continue
            else:
                break
        # handle none choice
        if choice == 'none':
            month = 'all'
            day = 'all'
            break

    # return the user input if it's valid
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

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all': 
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month: ', MONTHS[popular_month - 1])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0] 
    print('Most Common Day of the Week: ', popular_day) 


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    # format the hour in 12-hour clock fromat 
    if popular_hour < 12:
        print('Most Common Start Hour: ', popular_hour, ' AM')
    elif popular_hour >= 12:
        if popular_hour > 12:
            popular_hour -= 12
        print('Most Common Start Hour: ', popular_hour, ' PM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    combo_station = df['Start Station'] + " to " +  df['End Station']
    common_combo_station = combo_station.mode()[0]
    print("Most Common Trip from Start to End:\n {}".format(common_combo_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("The Total Travel Time is {} Hours, {} Minutes, and {} Seconds.".format(hour, minute, second))

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    minute, second = divmod(average_duration, 60)
    if minute> 60:
        hour, minute = divmod(minute, 60)
        print('The Average Travel Time is {} Hours, {} Minutes, and {} seconds.'.format(hour, minute, second))
    else:
        print('The Average Trip Duration is {} Minutes and {} Seconds.'.format(minute, second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of Each User Type: \n", user_types)

    # Display counts of gender
    if(city == 'washington'):
        print('Sorry, no gender data available for {} City'.format(city.title()))
    else:
        gender = df['Gender'].value_counts()
        print(' ' * 40)
        print('Counts of Each User Gender:')
        print(gender)
        

    # Display earliest, most recent, and most common year of birth
    if(city == 'washington'):
        print('Sorry, no birth year data available for {} City'.format(city.title()))
    else:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()
        print(' ' * 40)
        print('Counts of User Birth Year:')
        print('Oldest User(s) Birth Year: ', int(earliest))
        print('Youngest User(s) Birth Year: ', int(recent))
        print('Most Common Birth Year: ', int(common))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def chunker(iterable, size):
    """Yield successive chunks from iterable of length size."""
    for i in range(0, len(iterable), size):
        yield iterable.iloc[i:i + size]


def individual_data(df):
    # Ask user if they want to see individual trip data.
    for chunk in chunker(df, 5):
        raw_data = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'? ").lower()
        if raw_data.lower() == 'yes':
            print("\nDisplaying only 5 rows of data.\n")
            print(chunk)
        else:
            break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
