import sys

import attacker
import constants
import csv_database

DEFAULT_ARGS = [
    constants.DEFAULT_FACE_DIR,
    constants.DEFAULT_FACES_CSV_NAME,
    constants.DEFAULT_MATCHES_CSV_NAME,
    constants.DEFAULT_ATTACK_SIZE
]


def print_usage():
    print """
    Usage: python attack_database.py [(OPTIONAL) FACES_DIR] [(OPTIONAL) INPUT_CSV] [(OPTIONAL) OUTPUT_CSV] [(OPTIONAL) ATTACKS]

    FACES_DIR - directory of all the faces. default is %s.
    INPUT_CSV - csv of face features. default is %s. If the filename doesn't exist, it will be created 
    OUTPUT_CSV - matches of attack on database. default is %s. 
    ATTACKS - number of attacks on the database. default is %s.
    
    """ % (
        constants.DEFAULT_FACE_DIR,
        constants.DEFAULT_FACES_CSV_NAME,
        constants.DEFAULT_MATCHES_CSV_NAME,
        constants.DEFAULT_ATTACK_SIZE
    )


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == constants.HELP_ARGUMENT:
        print_usage()
        return
    
    args = sys.argv[1:] + DEFAULT_ARGS[len(sys.argv)-1:]
    print("Generating face database from %s. Saving in %s. " % (args[0], args[1]))
    face_database = csv_database.CSVDatabase(args[0], args[1])
    database_attacker = attacker.Attacker(face_database, args[2])

    print("Attcaking the %s database. Saving in %s. " % (args[1], args[2], args[3]))
    database_attacker.attack()


if __name__ == "__main__":
    main()





