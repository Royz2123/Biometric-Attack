import numpy as np
import time
from functools import reduce
import matplotlib.pyplot as plt

import constants
import csv_database
import util


(
    NO_DEBUG,
    DEBUG_LEVEL,
    PLOT_END_LEVEL,
    PLOT_VIZ_LEVEL,
    PLOT_ALL_LEVEL,
)=range(5)

class Attacker(object):
    LOG_FILE = "logs/general/attack_log"
    SEED_FILE = "logs/seeds/seed_file"

    def __init__(
        self,
        training_db,
        testing_db,
        attack_size=constants.DEFAULT_ATTACK_SIZE,
        recover_time=None
    ):
        self._training_db = training_db
        self._testing_db = testing_db
        # self._matches_database = csv_database.CSVDatabase(matches_filename)
        self._attack_size = attack_size

        # create log file
        self._timestamp = time.strftime('%d:%m:%Y_%H:%M:%S')
        self._log_file = Attacker.LOG_FILE + "_" + self._timestamp
        self._seed_file = Attacker.SEED_FILE + "_" + self._timestamp

        # load random state if requested
        if recover_time is not None:
            self.load_state(Attacker.SEED_FILE + "_" + recover_time)


    def save_state(self):
        with open(self._seed_file, "w+") as f:
            rand_state = list(np.random.get_state())
            # handle annoying numpy array
            rand_state[1] = rand_state[1].tolist()
            f.write(str(tuple(rand_state)))


    def load_state(self, filename):
        with open(filename, "r+") as f:
            rand_state = list(eval(f.read()))
            # handle annoying numpy array
            rand_state[1] = np.array(rand_state[1])
            np.random.set_state(tuple(rand_state))

    # attack the database for self._attacks
    def attack(self, debug_level=PLOT_VIZ_LEVEL):
        # First save the random seed
        self.save_state()

        with open(self._log_file, "w+") as f:
            if debug_level:
                print("\n~~~~Attack Log~~~~\n")
            f.write(
                """
                \n~~~~Attack Log~~~~\n
                Timestamp:\t%s
                Training database:\t%s
                Testing database:\t%s
                Attack size:\t%d\n
                """ % (
                    self._timestamp,
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
                elif debug_level == PLOT_VIZ_LEVEL:
                    for gen_features in faces:
                        gen_face_im = self._training_db.approx_by_faces(gen_features)
                        plt.imshow(gen_face_im)
                        plt.show()
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

            distrib = {}
            for face_index, freq in enumerate(freqs):
                #print((freq, face_index))
                if freq not in distrib.keys():
                    distrib[freq] = []
                distrib[freq].append(face_index)

            f.write(
                """
                Total hits:\t%s
                Random seed:\t%s\n
                Distribution:\n\t\t\t\t\t\t\t\t\t%s\n
                """ % (
                    len(all_matches),
                    self._seed_file,
                    "\n\t\t\t\t\t\t\t\t\t".join([
                        "%d Hits\t# of faces:%d\tFace indexes: %s" %
                        (hits, len(indexes), indexes)
                        for hits, indexes in distrib.items()
                    ]),
                )
            )

            # Plot histogram if requested
            if debug_level in (PLOT_END_LEVEL, PLOT_ALL_LEVEL):
                x_new = range(self._testing_db._data_len)
                y_new = freqs
                util.plot_points(x_new, y_new, x_name="Face index", y_name="Hits")

        # return number of attacks
        return len(all_matches)
