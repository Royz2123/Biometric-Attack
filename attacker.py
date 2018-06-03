import constants
import csv_database
import util


(
    NO_DEBUG,
    DEBUG_LEVEL,
    PLOT_LEVEL,
)=range(3)

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
    def attack(self, debug_level=DEBUG_LEVEL):
        if debug_level:
            print("\n~~~~Attack Log~~~~\n")

        all_matches = []
        for i in range(int(self._attack_size / constants.ATTACK_BATCH)):
            # generate "attack_size" faces
            faces = self._training_db.generate_faces(constants.ATTACK_BATCH)

            # check if there were any matches
            matched_faces = self._testing_db.check_for_matches(faces)
            all_matches += matched_faces

            # document if there were matches
            if debug_level == PLOT_LEVEL:
                util.plot_points(range(len(all_matches)), all_matches, x_name="Attack number", y_name="Hits")
            elif debug_level == DEBUG_LEVEL:
                print(
                    "Batch #%d / %d\nFaces Generated:%d\nTotal matches: %d\n"
                    % (
                        i + 1,
                        self._attack_size / constants.ATTACK_BATCH,
                        len(all_matches),
                        sum(all_matches)
                    )
                )

        util.plot_points(range(len(all_matches)), all_matches, x_name="Attack number", y_name="Hits")
        return sum(all_matches)
