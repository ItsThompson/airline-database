from color_terminal import Color, print_color
from helper import int_input_validation, string_input_validation, select_query, commit_query, iso8601_to_datetime, return_to_main
from prettytable import PrettyTable


def list_of_destinations():
    cmd = "SELECT departure_airport_code FROM flight \
UNION SELECT arrival_airport_code FROM flight;"

    records = select_query(cmd)

    out = "🛫 Our current list of destinations are: "

    for index, rows in enumerate(records):
        if index == len(records) - 1:
            out += "and "
            out += rows[0]
        else:
            out += rows[0]
            out += ", "

    print(out)
    return_to_main()


def flight_search():
    prompts = [
        ("Please enter the designator or press enter if you are unsure (Ex. BA0185):",
         6, "flight_designator"),
        ("Please enter the 3 letter airport code for your departure airport \
or press enter if you are unsure (Ex. LHR):", 3, "departure_airport_code"),
        ("Please enter the 3 letter airport code for your arrival airport \
or press enter if you are unsure (Ex. EWR):", 3, "arrival_airport_code")
    ]
    choices = []
    for prompt in prompts:
        string = prompt[0]
        minimum = maximum = prompt[1]
        user_input = string_input_validation(string, minimum, maximum)
        choices.append((user_input.upper(), prompt[2]))

    choices = [tup for tup in choices if tup[0] != '']

    cmd = "SELECT flight.flight_designator, flight.departure, flight.arrival, \
flight.departure_airport_code, flight.arrival_airport_code, \
flight.passengers, aircraft.manufacturer, aircraft.aircraft_model, \
aircraft_type.maximum_capacity FROM flight \
INNER JOIN aircraft ON flight.aircraft_id = aircraft.aircraft_id \
INNER JOIN aircraft_type ON \
aircraft_type.aircraft_model = aircraft.aircraft_model \
AND aircraft_type.manufacturer = aircraft.manufacturer"

    args = []
    if len(choices) == 0:
        cmd += ";"
    elif len(choices) == 1:
        choice = choices[0]
        cmd += " WHERE "
        cmd += choice[1] + " = ?"
        args = [choice[0]]
        cmd += ";"
    else:
        temp = ""
        cmd += " WHERE "
        for index, choice in enumerate(choices):
            if index == len(choices) - 1:
                temp += choice[1] + " = ?"
            else:
                temp += choice[1] + " = ? AND "
            args.append(choice[0])
        cmd += temp
        cmd += ";"
    args = tuple(args)

    print_color("⚙️ Generating Results", Color.CYAN)

    records = select_query(cmd, args)

    if records == []:
        print_color("🛫 No Flights Found, Please Try Again!", Color.CYAN)
        return flight_search()

    table = PrettyTable()
    table.field_names = [
        "Designator", "Departure", "Arrival", "Departure Airport",
        "Arrival Airport", "Airplane", "Capacity Percentage"
    ]
    print_color("⚙️ Formating Results", Color.CYAN)
    for rows in records:
        airplane = str(rows[6]) + " " + str(rows[7])
        capacity_percentage = str("%.2f" % round(
            (float(rows[5]) / float(rows[8])) * 100, 2)) + "%"
        departure = iso8601_to_datetime(str(rows[1]))
        arrival = iso8601_to_datetime(str(rows[2]))

        table.add_row([
            rows[0], departure, arrival, rows[3], rows[4], airplane,
            capacity_percentage
        ])
    print(table)

    return_to_main()


def book_flight():
    def print_table(records):
        opts = []
        cap = []
        table = PrettyTable()
        table.field_names = [
            "ID", "Designator", "Departure", "Arrival", "Departure Airport",
            "Arrival Airport", "Capacity Percentage"
        ]
        print_color("⚙️ Formating Results", Color.CYAN)
        for rows in records:
            opts.append(int(rows[0]))
            cap.append((float(rows[6]), float(rows[7])))
            capacity_percentage = str("%.2f" % round(
                (float(rows[6]) / float(rows[7])) * 100, 2)) + "%"
            departure = iso8601_to_datetime(str(rows[2]))
            arrival = iso8601_to_datetime(str(rows[3]))

            table.add_row([
                rows[0], rows[1], departure, arrival, rows[4], rows[5],
                capacity_percentage
            ])
        print(table)
        return (opts, cap)

    prompts = [
        ("Please enter the 3 letter airport code for your departure airport \
or press enter if you are unsure (Ex. LHR):", 3, "departure_airport_code"),
        ("Please enter the 3 letter airport code for your arrival airport \
or press enter if you are unsure (Ex. HKG):", 3, "arrival_airport_code")
    ]
    choices = []
    for prompt in prompts:
        string = prompt[0]
        minimum = maximum = prompt[1]
        user_input = string_input_validation(string, minimum, maximum)
        choices.append((user_input.upper(), prompt[2]))

    choices = [tup for tup in choices if tup[0] != '']

    cmd = "SELECT flight.flight_id, flight.flight_designator, flight.departure, \
flight.arrival, flight.departure_airport_code, flight.arrival_airport_code, \
flight.passengers, aircraft_type.maximum_capacity FROM flight \
INNER JOIN aircraft ON flight.aircraft_id = aircraft.aircraft_id \
INNER JOIN aircraft_type ON \
aircraft_type.aircraft_model = aircraft.aircraft_model \
AND aircraft_type.manufacturer = aircraft.manufacturer"

    args = []
    if len(choices) == 0:
        cmd += ";"
    elif len(choices) == 1:
        choice = choices[0]
        cmd += " WHERE "
        cmd += choice[1] + " = ?"
        args = [choice[0]]
        cmd += ";"
    else:
        temp = ""
        cmd += " WHERE "
        for index, choice in enumerate(choices):
            if index == len(choices) - 1:
                temp += choice[1] + " = ?"
            else:
                temp += choice[1] + " = ? AND "
            args.append(choice[0])
        cmd += temp
        cmd += ";"
    args = tuple(args)

    print_color("⚙️ Generating Results", Color.CYAN)

    query_output = select_query(cmd, args)
    if query_output == []:
        print_color("🛫 No Flights Found, Please Try Again!", Color.CYAN)
        return book_flight()

    print_table_output = print_table(query_output)

    options = print_table_output[0]
    capacity = print_table_output[1]

    prompt_id_from_table = "Please type the flight id you would like to book:"

    flag = True

    first_time = True

    while flag:
        user_input = int_input_validation(prompt_id_from_table, min(options),
                                          max(options), options, first_time)

        index = options.index(user_input)

        new_passenger_total = float(capacity[index][0] + 1)
        maximum_capacity = float(capacity[index][1])

        if new_passenger_total / maximum_capacity > 1:
            print(
                "🚨 Apologize for the inconvenience, but this flight is full. Please select a new flight:"
            )
            first_time = False
            continue
        else:
            flag = False

    print("✈️ Excellent Choice! You have selected flight id: " +
          str(user_input))
    print_color("⚙️ Updating Database", Color.CYAN)
    cmd = "UPDATE flight SET passengers = passengers + 1 \
            WHERE flight_id = ?"

    commit_query(cmd, (user_input, ))
    print_color("⚙️ Passenger Added", Color.CYAN)
    cmd = "SELECT flight.flight_id, flight.flight_designator, flight.departure, \
flight.arrival, flight.departure_airport_code, flight.arrival_airport_code, \
flight.passengers, aircraft_type.maximum_capacity FROM flight \
INNER JOIN aircraft ON flight.aircraft_id = aircraft.aircraft_id \
INNER JOIN aircraft_type ON \
aircraft_type.aircraft_model = aircraft.aircraft_model \
AND aircraft_type.manufacturer = aircraft.manufacturer \
WHERE flight.flight_id = ?"

    query_output = select_query(cmd, (user_input, ))
    print_table(query_output)

    return_to_main()
