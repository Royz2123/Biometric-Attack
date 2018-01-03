import sys

import attacker
import csv_database


def print_usage():
    print """
    Usage: python attack_database.py [(OPTIONAL) FACES_DIR] [(OPTIONAL) INPUT_CSV] [(OPTIONAL) OUTPUT_CSV]

    FACES_DIR - 
    
    """


def main():
    if len(sys.argv) < 2:
        print_usage()


    print("Generating face database from %s" % )
    face_database = csv_database.CSVDatabase()
    database_attacker = attacker.Attacker(face_database)
    database_attacker.attack()


if __name__ == "__main__":
    main()





