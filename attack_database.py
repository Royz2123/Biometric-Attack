import matplotlib.pyplot as plt
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



def attack_base(training, testing, attack_size):
    print("Generating training database:")
    training_database = csv_database.CSVDatabase(
        training["folder"],
        training["csv"]
    )
    print("Training dataset initialized. Total samples = %d" % len(training_database._data))

    print("Generating testing database: ")
    testing_database = csv_database.CSVDatabase(
        testing["folder"],
        testing["csv"]
    )
    print("Testing dataset initialized. Total samples = %d" % len(testing_database._data))

    print("Attacking... Attack size is %d." % (attack_size))
    database_attacker = attacker.Attacker(training_database, testing_database, attack_size)
    return database_attacker.attack()


def thresh_test_attack(training, testing):
    xnew = []
    ynew = []

    orig_dist = constants.MIN_DISTANCE
    for thresh in range(0, 10):
        constants.MIN_DISTANCE = orig_dist + thresh * 0.01
        xnew.append(orig_dist + thresh * 0.01)
        ynew.append(attack_base(training, testing, 100000))

    plt.plot(xnew, ynew)
    plt.ylabel("Hits for 100000 attacks")
    plt.xlabel("Threshhold")
    plt.show()



def main():
    if constants.HELP_ARGUMENT in sys.argv:
        print_usage()
        return

    args = sys.argv[1:] + DEFAULT_ARGS[len(sys.argv)-1:]

    # Database info
    training = {
        "folder" : args[0],
        "csv" : args[2],
    }
    testing = {
        "folder" : args[1],
        "csv" : args[3]
    }
    attack_size = args[4]

    # print("\nFirst attacking the training_database\n")
    # attack_self(args)

    print("\nNow attacking the testing_database\n")

    attack_base(training, testing, attack_size)

    # thresh_test_attack(training, testing)



if __name__ == "__main__":
    main()
