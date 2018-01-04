import constants
import csv_database
import util

class Attacker(object):
    def __init__(
        self,
        training_db,
        testing_db,
        attack_size=constants.DEFAULT_ATTACK_SIZE
    ):
        self._training_db = training_db
        self._testing_db = testing_db
        # self._matches_database = csv_database.CSVDatabase(matches_filename)
        self._attack_size = attack_size

    # attack the database for self._attacks
    def attack(self):
        # generate "attack_size" faces
        faces = self._training_db.generate_faces(self._attack_size)

        # check if there were any matches
        matched_faces = self._testing_db.check_for_matches(faces)

        # document if there were matches
        util.plot_points(range(self._attack_size), matched_faces, x_name="Attack number", y_name="Hits")
