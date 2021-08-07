import time
import pandas as pd
import numpy as np
# create dictionary to reference csv files for each city
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').strip().lower()
        if city not in (CITY_DATA.keys()):
            print('That is not a valid city. Please try again\n')
        else:
            break
    # get user input for date filter

    while True:
        date_filter = input('\nWould you like to filter the data by month, day, or neither?\n').strip().lower()
        if date_filter == 'month':
            # get user input for month (all, january, february, ... , june)
            while True:
                month = input('Please choose a month from the following: January, February, March, April, May, or June.\n').strip().lower()
                if month in ['january','february','march','april','may','june']:
                    day = 'all'
                    break
                else:
                    print('That is not a valid month, please try again\n')
            break
        elif date_filter == 'day':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                day = input('Please type a day of the week without abbreviations, e.g., Monday, Tuesday, etc.\n').strip().lower()
                if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                    month = 'all'
                    break
                else:
                    print('That is not a valid day of the week, please try again\n')
            break
        elif date_filter == 'neither':
            month = 'all'
            day = 'all'
            break
        else:
            print('This is not a valid input, please try again.\n')

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
    # load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract time data from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Travel Times...\n')
    start_time = time.time()

    # display the most common month
    top_month = df['month'].mode()[0]
    print('\nMost popular month: ',top_month)

    # display the most common day of week
    top_day = df['day_of_week'].mode()[0]
    print('Most popular day of the week: ',top_day)

    # display the most common start hour
    top_start_hour = df['hour'].mode()[0]
    print('Most popular time of day: ',top_start_hour,':00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    top_start_station = df['Start Station'].mode()[0]
    print('\nMost popular start station: ',top_start_station)

    # display most commonly used end station
    top_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ',top_end_station)

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station']+" --> "+df['End Station']
    top_trip =  df['Trip'].mode()[0]
    print('Most popular trip: ',top_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 60 / 60
    print('\nTotal travel time: ',int(total_travel_time),' hours')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('Average travel time: ',round(mean_travel_time,2),' minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()

    # Display counts of gender
    if "Gender" in df.columns:
        gender_count = df['Gender'].value_counts()
    else:
        gender_count = "This city does not capture data on user gender"

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        top_birth_year = int(df['Birth Year'].mode()[0])
    else:
        earliest_birth_year = "This city does not capture data on user birth year"
        latest_birth_year = "This city does not capture data on user birth year"
        top_birth_year = "This city does not capture data on user birth year"
    print('User Statistics:\nType Breakdown:\n',user_type_count,'\n\nGender Breakdown:\n',gender_count,'\n\nBirth Year Breakdown:\nEarliest: ',earliest_birth_year,'\nMost Recent:',latest_birth_year,'\nMost Common:',top_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#Call all of the functions above until restart or exit
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Display 5 rows of raw data at a time
        start_loc = 0
        end_loc = 5
        raw_data = input('\nWould you like to view individual trip data? Please type yes or no.\n').strip().lower()
        while True:
            if raw_data == 'yes':
                print(df.iloc[start_loc:end_loc])
                #Display 5 more rows of data
                while True:
                    more_raw_data = input('\nWould you like to view more data? Please type yes or no.\n').strip().lower()
                    if more_raw_data == 'yes':
                        start_loc += 5
                        end_loc += 5
                        print(df.iloc[start_loc:end_loc])
                    elif more_raw_data == 'no':
                        break
                    else:
                        print('This is not a valid response, please try again.')
                break
            elif raw_data == 'no':
                break
            else:
                print('This is not a valid response, please try again.')
        #Ask user if they want to start again or exit
        restart = input('\nWould you like to view different Bikeshare data? Enter yes to restart or no to exit.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()
