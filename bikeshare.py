import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = ''
    day = ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Would you like to see data for Chicago, New York City, or Washington?")
    while(True):
        try:
            select = input('Enter the City name: ').lower().strip()
        except:
            print("This is not a valid city name please re-enter (chicago, new york city and washington)")
        if select in CITY_DATA.keys():
            city = select
            break
        else:
            print("This is not a valid city name please re-enter (chicago, new york city and washington)")

    print("Would you like to filter the data by month, day, or None?")
    while(True):
        try:
            date_filter = input('Enter filter type: ').lower().strip()
        except:
            print("This is not a valid filter type for the date (month, day or None)")
        # get user input for month (all, january, february, ... , june)
        if date_filter == 'month':
            print("Which month - January, February, March, April, May, or June?")
            while(True):
                try:
                    month_filter = input('Enter a month: ').lower().strip()
                except:
                    print("This is not a valid month please re-enter from (january, february, ... , june)")
                if month_filter in months:
                    month = month_filter
                    day = 'all'
                    break
                else:
                    print("This is not a valid month please re-enter from (january, february, ... , june)")
            break
        # get user input for day of week (all, monday, tuesday, ... sunday)
        elif date_filter == 'day':
            print("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?")
            while(True):
                try:
                    day_filter = input('Enter a day: ').lower().strip()
                except:
                    print("This is not a valid day please re-enter from ('sunday', 'monday', ... , saturday)")
                if day_filter in weekdays:
                    day = day_filter
                    month = 'all'
                    break
                else:
                    print("This is not a valid month please re-enter from ('sunday', 'monday', ... , saturday)")
            break
        elif date_filter == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            print("This is not a valid filter, please re-enter (month, day or None)")


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
        Takes df - Pandas dataframe as an argument"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month is: {}'.format(popular_month))
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start Day is: {}'.format(popular_day))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour is: {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
        Takes df - Pandas dataframe as an argument"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station is: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station is:'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    freq_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination is: {} AND {}'.format(freq_combination[0], freq_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total trip duration is: ', total_trip_duration)
    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('Average trip duration is: ', mean_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of user types is: {}'.format(user_types))

    # Display counts of gender
    if 'Gender' in df:
        gender_data = df['Gender'].value_counts()
        print('Counts of genders is: {}'.format(gender_data))
    else:
        print('Washington has no gender data!')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_YOB = df['Birth Year'].min()
        print('The earliest year of birth is: {}'.format(earliest_YOB))
        recent_YOB = df['Birth Year'].max()
        print('The most recent year of birth is: {}'.format(recent_YOB))
        common_YOB = df['Birth Year'].mode()[0]
        print('The most common year of birth is: {}'.format(common_YOB))
    else:
        print('Washington has no birth year data!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_raw_data(df):
    """Prompt the user whether they would like want to see the raw data. If the user answers 'yes,'
    then the script should print 5 rows of the data at a time."""

    limit = 0
    while(True):
        get_inp = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        if get_inp == 'yes':
            print(df[limit : limit+5])
            limit += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
