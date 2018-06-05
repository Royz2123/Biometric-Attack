import argparse
import matplotlib.pyplot as plt
import sys

import attacker
import constants
import csv_database



def parse_args():
    parser = argparse.ArgumentParser(description='Brute force attack on a database')
    parser.add_argument('--training-dir', default=constants.DEFAULT_TRAINING_DIR,
                       help='directory of all the training faces')
    parser.add_argument('--testing-dir', default=constants.DEFAULT_TESTING_DIR,
                       help='directory of all the training faces')
    parser.add_argument('--training-csv', default=constants.DEFAULT_TRAINING_CSV_NAME,
                       help='training csv of face features')
    parser.add_argument('--testing-csv', default=constants.DEFAULT_TESTING_CSV_NAME,
                       help='testing csv of face features')
    parser.add_argument('--attack-size', default=constants.DEFAULT_ATTACK_SIZE, type=int,
                       help='number of faces to be generated')
    parser.add_argument('--recover-time', default=None, type=str,
                       help='recover from previous run')
    parser.add_argument('--threshhold', default=constants.MIN_DISTANCE, type=float,
                       help='threshhold where to faces are considered identical')
    args = parser.parse_args()
    return args


def attack_base(args):
    print("Generating training database:")
    training_database = csv_database.CSVDatabase(
        args.training_dir,
        args.training_csv
    )
    print("Training dataset initialized. Total samples = %d" % len(training_database._data))

    print("Generating testing database: ")
    testing_database = csv_database.CSVDatabase(
        args.testing_dir,
        args.testing_csv
    )
    print("Testing dataset initialized. Total samples = %d" % len(testing_database._data))

    print("Attacking... Attack size is %d." % (args.attack_size))
    database_attacker = attacker.Attacker(
        training_database,
        testing_database,
        args.attack_size,
        recover_time=args.recover_time
    )
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
    args = parse_args()
    constants.MIN_DISTANCE = args.threshhold

    print("\nNow attacking the testing_database\n")

    attack_base(args)

    # thresh_test_attack(training, testing)



if __name__ == "__main__":
    main()
