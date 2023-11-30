import random
from prettytable import PrettyTable
from helper import int_input_validation, string_input_validation, select_query, commit_query, string_to_iso8601_time, is_between_iso8601, iso8601_to_datetime, yes_no_prompt, return_to_main, get_month, get_week
from color_terminal import Color, print_color


def add_new_flight():
    # INFO: Input Validation: Asks for input until valid ISO8601 Time
    def get_date_time():
        prompt = "Enter a date and time (YYYY-MM-DD HH:MM): "
        flag = True
        first_time = True
        while flag:
            user_input = string_input_validation(prompt, 16, 16, [],
                                                 first_time)
            output = string_to_iso8601_time(user_input)
            first_time = False
            if output[0]:
                flag = False
                return output[1]

    # INFO: Flight Designator: Autogenerated 4 Digit Code
    flight_designator = "BA" + str(random.randint(1000, 9999))

    print("📅 Enter Departure Date and Time:")
    departure_iso8601 = get_date_time()

    departure_airport_code = string_input_validation(
        "🛫 Departure Airport Code: ", 3, 3)

    print("📅 Enter Arrival Date and Time: ")
    arrival_iso8601 = get_date_time()

    arrival_airport_code = string_input_validation(
        "🛫 Departure Airport Code: ", 3, 3)

    # INFO: Generate table for the aircraft type options
    cmd = "SELECT * FROM aircraft_type"
    aircraft_type_records = select_query(cmd)

    table = PrettyTable()
    table.field_names = [
        "ID", "Manufacturer", "Aircraft Model", "Maximum Capacity",
        "Maximum Range"
    ]
    print_color("⚙️ Finding Aircraft Types", Color.CYAN)
    for index, rows in enumerate(aircraft_type_records):
        table.add_row([index, rows[0], rows[1], rows[2], rows[3]])
    print(table)

    prompt_id_from_table = "Please type the id for the desired aircraft type:"

    flag = True
    first_time = True

    # INFO: Algorithm to check if aircraft type is available
    #       and selects airplane.

    possible_aircraft = []

    def update_possible_aircraft(aircraft_list, id, boolean):
        in_list = (0, False)
        for index, aircraft in enumerate(aircraft_list):
            if aircraft[0] == id:
                in_list = (index, True)

        if in_list[1]:
            # aircraft id is in list
            index = in_list[0]
            aircraft_list[index][1] = boolean
        else:
            # aircraft id not in list
            aircraft_list.append([id, boolean])

        return aircraft_list

    while flag:
        user_input = int_input_validation(prompt_id_from_table, 0,
                                          (len(aircraft_type_records) - 1), [],
                                          first_time)

        manufacturer = aircraft_type_records[user_input][0]
        model = aircraft_type_records[user_input][1]

        # INFO: Loads flights for aircraft with selected type
        cmd = "SELECT flight.aircraft_id, flight.departure, flight.arrival \
FROM flight INNER JOIN aircraft ON flight.aircraft_id = aircraft.aircraft_id \
WHERE aircraft.manufacturer = ? AND aircraft.aircraft_model = ?"

        flights_with_aircraft_type = select_query(cmd, (manufacturer, model))

        for rows in flights_with_aircraft_type:
            aircraft_id = rows[0]
            row_departure = rows[1]
            row_arrival = rows[2]
            # INFO: Checks if both chosen departure or arrival are between
            #       current row's departure and arrival.
            if is_between_iso8601(departure_iso8601, row_departure,
                                  row_arrival) or is_between_iso8601(
                                      arrival_iso8601, row_departure,
                                      row_arrival):
                possible_aircraft = update_possible_aircraft(
                    possible_aircraft, aircraft_id, False)
            # INFO: Checks if both row's departure or arrival are between
            #       chosen departure or arrival.
            elif is_between_iso8601(row_departure, departure_iso8601,
                                    arrival_iso8601) or is_between_iso8601(
                                        row_arrival, departure_iso8601,
                                        row_arrival):
                possible_aircraft = update_possible_aircraft(
                    possible_aircraft, aircraft_id, False)
            else:
                possible_aircraft = update_possible_aircraft(
                    possible_aircraft, aircraft_id, True)
                pass

        has_possible_aircraft = False
        for aircraft in possible_aircraft:
            if aircraft[1]:
                has_possible_aircraft = True
                aircraft_id = aircraft[0]

        if has_possible_aircraft:
            flag = False
        else:
            print("🛫 No available aircraft of desired type.")
            first_time = False

            if yes_no_prompt(
                    "Select a new plane or return to main menu (y/n):"):
                continue
            else:
                return

    print_color(
        "✈️ The " + manufacturer + " " + model +
        " with aircraft_id of " + str(aircraft_id) + " is available.",
        Color.CYAN)

    # INFO: Insert to Database
    insert_statement = "INSERT INTO flight \
(flight_designator, aircraft_id, departure, arrival, \
departure_airport_code, arrival_airport_code, passengers) \
VALUES (?, ?, ?, ?, ?, ?, 0)"

    insert_args = (flight_designator, aircraft_id, departure_iso8601,
                   arrival_iso8601, departure_airport_code,
                   arrival_airport_code)

    print_color("⚙️ Inserting Into Database", Color.CYAN)
    new_row_id = commit_query(insert_statement, insert_args)

    select_statement = "SELECT * FROM flight WHERE flight_id = ?"
    new_flight_row = select_query(select_statement, (new_row_id, ))

    table = PrettyTable()
    table.field_names = [
        "ID", "Designator", "Aircraft ID", "Departure Time", "Arrival Time",
        "Departure Airport Code", "Arrival Airport Code", "Passengers"
    ]
    print_color("⚙️ Formating New Row", Color.CYAN)
    for rows in new_flight_row:
        departure = iso8601_to_datetime(str(rows[3]))
        arrival = iso8601_to_datetime(str(rows[4]))

        table.add_row([
            rows[0], rows[1], rows[2], departure, arrival, rows[5], rows[6],
            rows[7]
        ])
    print(table)

    return_to_main()


def add_new_pilot():
    first_name = string_input_validation("Please enter first name: ", 1, 50)
    last_name = string_input_validation("Please enter last name: ", 1, 50)
    nationality_prompt = "Please enter nationality or press enter: "
    nationality_input = string_input_validation(nationality_prompt, 0, 50)
    if nationality_input == '':
        nationality = None
    else:
        nationality = nationality_input
    license_number_prompt = "Please enter your EU license number (EU-#####): "
    license_number = string_input_validation(license_number_prompt, 1, 8)
    license_expiry_date_prompt = "Please enter when license expiry date \
(YYYY-MM-DD): "

    license_expiry_date = string_input_validation(license_expiry_date_prompt,
                                                  10, 10)

    # INFO: Insert to Database
    insert_statement = "INSERT INTO pilot (first_name, last_name, \
nationality, license_number, license_expirydate, flight_hours) VALUES\
(?, ?, ?, ?, ?, ?)"

    insert_args = (first_name, last_name, nationality, license_number,
                   license_expiry_date, 0)

    print_color("⚙️ Inserting Into Database", Color.CYAN)
    new_row_id = commit_query(insert_statement, insert_args)

    select_statement = "SELECT * FROM pilot WHERE pilot_id = ?"
    new_pilot_row = select_query(select_statement, (new_row_id, ))

    table = PrettyTable()
    table.field_names = [
        "ID", "First Name", "Last Name", "Nationality", "License Number",
        "License Expiry Date", "Flight Hours"
    ]
    print_color("⚙️ Formating New Row", Color.CYAN)
    for rows in new_pilot_row:
        table.add_row(
            [rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6]])
    print(table)
    return_to_main()


def add_new_aircraft():
    aircraft_type_statement = "SELECT * FROM aircraft_type"
    aircraft_type_records = select_query(aircraft_type_statement)

    table = PrettyTable()
    table.field_names = [
        "ID", "Manufacturer", "Aircraft Model", "Maximum Capacity",
        "Maximum Range"
    ]
    print_color("⚙️ Formating Results", Color.CYAN)
    for index, rows in enumerate(aircraft_type_records):
        table.add_row([index, rows[0], rows[1], rows[2], rows[3]])
    print(table)
    aircraft_type_prompt = "Please select a aircraft type"
    index = int_input_validation(aircraft_type_prompt, 0,
                                 len(aircraft_type_records) - 1)

    manufacturer = aircraft_type_records[index][1]
    aircraft_model = aircraft_type_records[index][2]

    aircraft_registration_prompt = """Please enter the aircraft registration:
United Kingdom: G-AAAA to G-ZZZZ
United States: N00001 to N99999
Singapore: 9V-AAA to 9V-ZZZ"""
    aircraft_registration = string_input_validation(
        aircraft_registration_prompt, 0, 10)

    # INFO: Insert to Database
    insert_statement = "INSERT INTO aircraft (manufacturer, aircraft_model, \
aircraft_registration) VALUES (?,?,?)"

    insert_args = (manufacturer, aircraft_model, aircraft_registration)

    print_color("⚙️ Inserting Into Database", Color.CYAN)
    new_row_id = commit_query(insert_statement, insert_args)

    select_statement = "SELECT * FROM aircraft WHERE aircraft_id = ?"
    new_pilot_row = select_query(select_statement, (new_row_id, ))

    table = PrettyTable()
    table.field_names = [
        "ID", "Manufacturer", "Aircraft Model", "Aircraft Registration"
    ]
    print_color("⚙️ Formating New Row", Color.CYAN)
    for rows in new_pilot_row:
        table.add_row([rows[0], rows[1], rows[2], rows[3]])
    print(table)
    return_to_main()


def remove_flight():
    # INFO: print_table: Prints and returns the list of possible flight_ids
    def print_table():
        select_statement = "SELECT * FROM flight"
        new_flight_row = select_query(select_statement)

        table = PrettyTable()
        table.field_names = [
            "ID", "Designator", "Aircraft ID", "Departure Time",
            "Arrival Time", "Departure Airport Code", "Arrival Airport Code",
            "Passengers"
        ]
        print_color("⚙️ Formatting Table", Color.CYAN)
        possible_ids = []
        for rows in new_flight_row:
            possible_ids.append(rows[0])
            departure = iso8601_to_datetime(str(rows[3]))
            arrival = iso8601_to_datetime(str(rows[4]))

            table.add_row([
                rows[0], rows[1], rows[2], departure, arrival, rows[5],
                rows[6], rows[7]
            ])
        print(table)
        return possible_ids

    possible_ids = print_table()

    prompt_remove_id = "Please type the flight id you would like to remove:"

    user_input = int_input_validation(prompt_remove_id, min(possible_ids),
                                      max(possible_ids), possible_ids)

    print("✈️ You have selected flight id: " + str(user_input))
    print_color("⚙️ Removing Row", Color.CYAN)

    delete_statement = "DELETE FROM flight WHERE flight_id = ?"
    commit_query(delete_statement, (user_input, ))

    print_table()
    return_to_main()


def list_of_pilots():
    select_statement = "SELECT * FROM pilot"
    records = select_query(select_statement)

    table = PrettyTable()
    table.field_names = [
        "ID", "Name", "Nationality", "License Number", "License Expiry",
        "Flight Hours"
    ]
    print_color("⚙️ Formatting Table", Color.CYAN)
    for rows in records:
        name = rows[1] + " " + rows[2]
        table.add_row([rows[0], name, rows[3], rows[4], rows[5], rows[6]])
    print(table)
    return_to_main()


def pilot_schedule():
    print_color("⚙️ Loading Pilot Information", Color.CYAN)
    pilot_id_length = select_query("SELECT COUNT(*) FROM pilot")[0][0]
    pilots = select_query("SELECT pilot_id, first_name, last_name FROM pilot")
    pilot_ids = [item[0] for item in pilots]
    selected_pilot_id = int_input_validation("Enter your pilot id:", 1,
                                             pilot_id_length, pilot_ids)
    index = pilot_ids.index(selected_pilot_id)
    first_name = pilots[index][1]
    last_name = pilots[index][2]
    print(selected_pilot_id)
    print_color("⚙️ Checking Flight Schedule", Color.CYAN)
    flight_schedule_statement = "SELECT flight.flight_id, \
flight.flight_designator, aircraft.manufacturer,aircraft.aircraft_model, \
flight.departure, flight.arrival, flight.departure_airport_code, \
flight.arrival_airport_code FROM flight \
INNER JOIN flight_pilot_link_table \
ON flight.flight_id=flight_pilot_link_table.flight_id \
INNER JOIN aircraft ON flight.aircraft_id=aircraft.aircraft_id \
WHERE flight_pilot_link_table.pilot_id = ?"

    print_color("⚙️ Generating Results", Color.CYAN)
    flight_schedule = select_query(flight_schedule_statement,
                                   (selected_pilot_id, ))

    if len(flight_schedule) == 0:
        print("You have no scheduled flights")
    else:
        table = PrettyTable()
        table.field_names = [
            "ID", "Designator", "Airplane", "Departure", "Arrival",
            "Departure Airport Code", "Arrival Airport Code"
        ]
        print_color("⚙️ Formating Results", Color.CYAN)
        for rows in flight_schedule:
            airplane = str(rows[2]) + " " + str(rows[3])
            departure = iso8601_to_datetime(str(rows[4]))
            arrival = iso8601_to_datetime(str(rows[5]))

            table.add_row([
                rows[0], rows[1], airplane, departure, arrival, rows[6],
                rows[7]
            ])
        print("Hello " + first_name + " " + last_name +
              ", here is your schedule:")
        print(table)
    return_to_main()


def generate_stats(date):
    # INFO: Number of flights (All Time):
    all_time_statement = "SELECT COUNT(*) FROM flight"
    flights_all_time = select_query(all_time_statement)[0][0]

    # INFO: Number of flights (Monthly):
    monthly_statement = "SELECT COUNT(*) FROM flight \
WHERE strftime('%m', flight.departure) = ?"

    month = get_month(date)

    # INFO: Number of flights (Weekly):
    weekly_statement = "SELECT COUNT(*) FROM flight \
WHERE strftime('%W', flight.departure) = ?"

    week = get_week(date)

    # INFO: Fleet Info
    fleet_statement = "SELECT manufacturer, aircraft_model, COUNT(*) \
FROM aircraft GROUP BY manufacturer, aircraft_model"

    fleet_result = select_query(fleet_statement)

    fleet_table = PrettyTable()
    fleet_table.field_names = ["Aircraft Type", "Quantity"]
    print_color("⚙️ Formatting Fleet Table", Color.CYAN)
    for rows in fleet_result:
        aircraft_type = rows[0] + " " + rows[1]

        fleet_table.add_row([aircraft_type, str(rows[2])])

    # INFO: Pilot Info
    pilot_statement = "SELECT first_name, last_name, nationality, \
license_number, license_expirydate, flight_hours FROM pilot"

    pilot_result = select_query(pilot_statement)

    pilot_table = PrettyTable()
    pilot_table.field_names = [
        "License Number", "Name", "Nationality", "License Expiry",
        "Flight Hours"
    ]
    print_color("⚙️ Formatting Pilot Table", Color.CYAN)
    for rows in pilot_result:
        name = rows[0] + " " + rows[1]
        if rows[2] is None:
            nationality = "Undisclosed"
        else:
            nationality = rows[2]
        pilot_table.add_row([rows[3], name, nationality, rows[4], rows[5]])

    # INFO: Output Data
    print("\n\n")

    print("> All Time Total Flights: " + str(flights_all_time))
    if month is not None:
        flights_monthly = select_query(monthly_statement, (str(month), ))
        monthly_result = flights_monthly[0][0]
        print("> This Month's Total Flights: " + str(monthly_result))
    if week is not None:
        flights_weekly = select_query(weekly_statement, (str(week), ))
        weekly_result = flights_weekly[0][0]
        print("> This Week's Total Flights: " + str(weekly_result))
    print("\n")
    print(fleet_table)
    print(pilot_table)
    return_to_main()
