import constants
import csv_database

class Attacker(object):
    def __init__(
        self, 
        face_database, 
        matches_filename=constants.DEFAULT_MATCHES_CSV_NAME, 
        attacks=constants.DEFAULT_ATTACK_SIZE
    ):
        self._face_database = database
        self._matches_database = csv_database.CSVDatabase(matches_filename)
        self._attacks = attacks
        
    # attack the database for self._attacks
    def attack(self):
        for i in xrange(self._attacks):
            # generate a face 
            face = self._database.generate_face()
            
            # check if there were any matches
            matched_faces = self._database.check_for_match(face)
        
            # document if there were matches
            if not len(matched_faces):
                self._matches_database.append_item(np.array([i] + matched_faces))
    
