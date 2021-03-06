import json
import numpy

from my_end_point import EndPoint

# Un EndPoint n'est pas enregistré dans la bibliothèque `json`.
class EP_Encoder(json.JSONEncoder):
    def default(self, o):
        #Comportement basique si ce n'est pas un EndPoint
        if not isinstance(o, EndPoint):
            return super().default(o)
        
        #La sérialisation est simplement un string contenant toutes les infos
        a = o.posture[0]
        res = str(a)
        for a in o.posture[1:]:
            res += ",{}".format(a)
        for row in o.matrix:
            for p in row:
                res += ",{}".format(p)

        return res

# Pour décoder facilement un endpoint, car json.load donnera simplement un string
def decode(str_ep):
    res = []
    for ep in str_ep:
        floats = ep.split(',')
        posture = []
        for i in range(6):
            posture.append(float(floats[i]))
        arr = []
        for i in range(4):
            tmp = []
            for j in range(4):
                tmp.append(float(floats[6+i*4+j]))
            arr.append(tmp)
        matrix = numpy.array(arr)
        res.append(EndPoint(posture, matrix))
    
    return res