import numpy as np
import time
from functools import reduce

import constants
import csv_database
import util


(
    NO_DEBUG,
    DEBUG_LEVEL,
    PLOT_END_LEVEL,
    PLOT_ALL_LEVEL,
)=range(4)

class Attacker(object):
    LOG_FILE = "logs/attack_log"

    def __init__(
        self,
        training_db,
        testing_db,
        attack_size=constants.DEFAULT_ATTACK_SIZE,
        logfile=LOG_FILE
    ):
        self._training_db = training_db
        self._testing_db = testing_db
        # self._matches_database = csv_database.CSVDatabase(matches_filename)
        self._attack_size = attack_size

        # create log file
        self._log_file = logfile + "_" + time.strftime('%d:%m:%Y_%H:%M:%S')


    # attack the database for self._attacks
    def attack(self, debug_level=PLOT_END_LEVEL):
        with open(self._log_file, "w+") as f:
            if debug_level:
                print("\n~~~~Attack Log~~~~\n")
            f.write(
                """
                \n~~~~Attack Log~~~~\n
                Training database:\t%s
                Testing database:\t%s
                Attack size:\t%d\n
                """ % (
                    self._training_db,
                    self._testing_db,
                    self._attack_size
                )
            )

            all_matches = []
            for i in range(int(self._attack_size / constants.ATTACK_BATCH)):
                # generate "attack_size" faces
                faces = self._training_db.generate_faces(constants.ATTACK_BATCH)

                # check if there were any matches
                matched_faces = self._testing_db.check_for_matches(faces)
                all_matches += reduce(lambda x, y: x + y, matched_faces)

                # document if there were matches
                if debug_level == PLOT_ALL_LEVEL:
                    util.plot_points(range(len(all_matches)), all_matches, x_name="Attack number", y_name="Hits")
                elif debug_level in (DEBUG_LEVEL, PLOT_END_LEVEL):
                    print(
                        "Batch #%d / %d\nFaces Generated:%d\nTotal matches: %d\n"
                        % (
                            i + 1,
                            self._attack_size / constants.ATTACK_BATCH,
                            (i + 1) * constants.ATTACK_BATCH,
                            len(all_matches)
                        )
                    )

            # Document results
            freqs = [0] * self._testing_db._data_len
            for match in all_matches:
                freqs[match] += 1

            f.write(
                """
                Total hits:\t%s
                Frequencies:\t%s\n
                Random seed:\t%s\n
                """ % (
                    len(all_matches),
                    freqs,
                    np.random.get_state()
                )
            )

            # Plot histogram if requested
            if debug_level in (PLOT_END_LEVEL, PLOT_ALL_LEVEL):
                x_new = range(self._testing_db._data_len)
                y_new = freqs
                util.plot_points(x_new, y_new, x_name="Face index", y_name="Hits")

        # return number of attacks
        return len(all_matches)
