
class EndPoint():
    def __init__(self, posture : list, rotation_matrix):
        #Liste d'angle
        self.posture = posture
        #Matrice de rotation du End Point
        self.matrix = rotation_matrix
    
    def get_pos(self):
        """Retourne la position 3D dans un tuple de cet end_point."""
        return (self.matrix[0][3], self.matrix[1][3], self.matrix[2][3])
    
    def get_rot(self):
        """Retourne la partie 3x3 concernant la rotation dans la matrice de rotation"""
        return (
            (self.matrix[0][0], self.matrix[0][1], self.matrix[0][2]),
            (self.matrix[1][0], self.matrix[1][1], self.matrix[1][2]),
            (self.matrix[2][0], self.matrix[2][1], self.matrix[2][2])
        )
    
    def get_posture(self):
        """Retourne la liste d'angle utilisée pour atteindre cet end_point"""
        return self.posture

    #Pour la serialisation pickle
    def __getstate__(self):
        res = (self.posture, self.matrix)
        return res
    
    def __setstate__(self, d):
        self.posture = d[0]
        self.matrix = d[1]

    
    #Pour la comparaison entre les nearest neighbor (my_nn_test)
    def __eq__(self, other):
        if isinstance(other, self.__class__) and len(self.posture) == len(other.posture):
            # Si la posture est la meme alors le resultat (position) et le meme.
            for i in range(len(self.posture)):
                if not self.posture[i] == other.posture[i]:
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)