import sys

import attacker
import constants
import csv_database

DEFAULT_ARGS = [
    constants.DEFAULT_TRAINING_DIR,
    constants.DEFAULT_TESTING_DIR,
    constants.DEFAULT_TRAINING_CSV_NAME,
    constants.DEFAULT_TESTING_CSV_NAME,
    constants.DEFAULT_ATTACK_SIZE
]

def print_usage():
    print (
        """
        Usage: python attack_database.py [TRAINING_DIR] [TESTING_DIR] [TRAINING_CSV] [TESTING_CSV] [ATTACKS]

        TRAINING_DIR - directory of all the training faces. default is %s.
        TESTING_DIR - directory of all the testing faces. default is %s.
        TRAINING_CSV - training csv of face features. default is %s.
        TESTING_CSV - matches of attack on database. default is %s.
        ATTACKS - number of attacks on the database. default is %s.

        """ % tuple(DEFAULT_ARGS)
    )



def attack_self(args):
    print("Generating training database from %s. Saving in %s. " % (args[0], args[2]))
    training_database = csv_database.CSVDatabase(args[0], args[2])
    print("Training dataset initialized. Total samples = %d" % len(training_database._data))

    print("Attacking the %s database. Attack size is %d." % (args[0], int(args[4])))
    database_attacker = attacker.Attacker(training_database, training_database, int(args[4]))
    database_attacker.attack()

def attack_other(args):
    print("Generating training database from %s. Saving in %s. " % (args[0], args[2]))
    training_database = csv_database.CSVDatabase(args[0], args[2])
    print("Training dataset initialized. Total samples = %d" % len(training_database._data))

    print("Generating testing database from %s. Saving in %s. " % (args[1], args[3]))
    testing_database = csv_database.CSVDatabase(args[1], args[3])
    print("Testing dataset initialized. Total samples = %d" % len(testing_database._data))

    print("Attacking the %s database. Attack size is %d." % (args[1], int(args[4])))
    database_attacker = attacker.Attacker(training_database, testing_database, int(args[4]))
    database_attacker.attack()

def main():
    if constants.HELP_ARGUMENT in sys.argv:
        print_usage()
        return

    args = sys.argv[1:] + DEFAULT_ARGS[len(sys.argv)-1:]

    print("\nFirst attacking the training_database\n")
    attack_self(args)

    print("\nNow attacking the testing_database\n")
    attack_other(args)



if __name__ == "__main__":
    main()
