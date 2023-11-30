import sqlite3
from helper import database, execute_from_file, CustomException
from color_terminal import Color, print_color


def create_database():
    conn = sqlite3.connect(database)
    curs = conn.cursor()

    # NOTE: All create SQL statments are using "IF NOT EXISTS"
    try:
        execute_from_file("tables.sql")
    except CustomException as exception:
        print(exception)

    curs.execute("SELECT name FROM sqlite_schema WHERE type='table';")
    tables = curs.fetchall()

    # Check if tables have been populated
    not_empty = True
    for table in tables:
        # Returns a list of 1 that is the length of the table
        cmd = "SELECT 1 FROM " + table[0]
        curs.execute(cmd)
        # Checks each table if they are empty
        if curs.fetchall() == []:
            not_empty = False
            break

    # Generate sample data
    sample_sql_location = "sample_data.sql"
    if not not_empty:
        try:
            print_color("⚙️ Creating Tables", Color.CYAN)
            print_color("⚙️ Inserting sample data", Color.CYAN)
            print_color("✔️ Database Genereated", Color.CYAN)
            execute_from_file(sample_sql_location)
        except CustomException as exception:
            print(exception)

    conn.commit()
    conn.close()
