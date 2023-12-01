from helper import CustomException, User, int_input_validation, string_input_validation, option_output, string_to_iso8601_date, quit_terminal
from color_terminal import Color, print_color
from passenger import flight_search, book_flight, list_of_destinations
from employee import add_new_flight, add_new_pilot, add_new_aircraft, remove_flight, list_of_pilots, pilots_on_flight, pilot_schedule, generate_stats
from generate_database import create_database
import os

date = None


def start(d=None):
    os.system('clear')
    print_color("--Thompson Airline Information Terminal--", Color.GREEN)
    create_database()
    if d is None:
        date_prompt = """
      Please initialize the program with a date (YYYY-MM-DD)

      For testing, please use 2023-11-30\n"""

        flag = True
        first_time = True
        while flag:
            date_input = string_input_validation(
                date_prompt, 10, 10, [], first_time)

            iso8601_date = string_to_iso8601_date(date_input)
            if iso8601_date[0]:
                global date
                date = iso8601_date[1]
                flag = False
                os.system('clear')
                print_color("--Thompson Airline Information Terminal--", Color.GREEN)
            else:
                first_time = False
                continue

    welcome = """
  Please identify who you are from the following options:
      1. Passenger
      2. Employee
      0. Exit Program\n"""
    choice = int_input_validation(welcome, 0, 2)

    match choice:
        case 1:
            option_output("Passenger")
            passenger_home_page()
        case 2:
            option_output("Employee")
            employee_home_page()
        case 0:
            quit_terminal()
        case _:
            raise CustomException("ERROR", "invalid int")


def passenger_home_page():
    os.system('clear')

    print_color("--Thompson Airline Customer Terminal--", Color.YELLOW)
    welcome = """
  Select an option:
      1. List of Destinations
      2. Flight Search
      3. Book Flight
      0. Change User\n"""
    choice = int_input_validation(welcome, 0, 3)

    match choice:
        case 0:
            option_output("Change User")
            return start(date)
        case 1:
            option_output("List of Destinations", User.PASSENGER)
            list_of_destinations()
        case 2:
            option_output("Flight Search", User.PASSENGER)
            flight_search()
        case 3:
            option_output("Book Flight", User.PASSENGER)
            book_flight()
        case _:
            raise CustomException("ERROR", "invalid int")
    return passenger_home_page()


def employee_home_page():
    os.system('clear')

    print_color("--Thompson Airline Internal Terminal--", Color.RED)
    welcome = """
  Select an option:
      1. List of Destinations
      2. Add New Flight
      3. New Pilot
      4. New Aircraft
      5. Remove Flight
      6. List of Pilots
      7. Pilots on Flight
      8. Pilot Schedule
      9. Statistics Dashboard
      0. Change User\n"""
    choice = int_input_validation(welcome, 0, 9)

    match choice:
        case 0:
            option_output("Change User", User.EMPLOYEE)
            return start(date)
        case 1:
            option_output("List of Destinations", User.EMPLOYEE)
            list_of_destinations()
        case 2:
            option_output("Add New Flight", User.EMPLOYEE)
            add_new_flight()
        case 3:
            option_output("New Pilot", User.EMPLOYEE)
            add_new_pilot()
        case 4:
            option_output("New Aircraft", User.EMPLOYEE)
            add_new_aircraft()
        case 5:
            option_output("Remove Flight", User.EMPLOYEE)
            remove_flight()
        case 6:
            option_output("List of Pilots", User.EMPLOYEE)
            list_of_pilots()
        case 7:
            option_output("Pilots on Flight", User.EMPLOYEE)
            pilots_on_flight()
        case 8:
            option_output("Pilot Schedule", User.EMPLOYEE)
            pilot_schedule()
        case 9:
            option_output("Statistics Dashboard", User.EMPLOYEE)
            generate_stats(date)
        case _:
            raise CustomException("ERROR", "invalid int")
    return employee_home_page()


start()
