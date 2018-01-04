import constants
import csv_database
import util

class Attacker(object):
    def __init__(
        self,
        face_database,
        matches_filename=constants.DEFAULT_MATCHES_CSV_NAME,
        attack_size=constants.DEFAULT_ATTACK_SIZE
    ):
        self._face_database = face_database
        self._matches_database = csv_database.CSVDatabase(matches_filename)
        self._attack_size = attack_size

    # attack the database for self._attacks
    def attack(self):
        # generate "attack_size" faces
        faces = self._face_database.generate_faces(self._attack_size)

        # check if there were any matches
        matched_faces = self._face_database.check_for_matches(faces)

        # document if there were matches
        util.plot_points(range(self._attack_size), matched_faces, x_name="Attack number", y_name="Hits")
