import parser
class read_kml:
    def read_kml(kml_file):
        f = open(kml_file, "r")
        docs = parser.parse(f)
        try:
            doc = docs.getroot().Document.Folder
    
        except:
            try:
                doc = docs.getroot().Document
            except Exception as e:
                # print(e)
                return
        # ===================================== Load KML and append the Data in variable ============================
    
        coords = []
        for place in doc.Placemark:
            try:
    
                x = str(place.Polygon.outerBoundaryIs.LinearRing.coordinates)
            except:
                try:
                    x = str(place.LineString.coordinates)
                except Exception as e:
                    # print(e)
                    return
    
            if '\n' in x:
                x = x.replace('\n', ',')
                x = x.replace(' ', '')
                x = x[1:]
            else:
                x = x.replace(' ', ',')
            v = x.split(",")
            line = []
            for i in range(len(v)):
                try:
                    if float(v[i]) > 1:
                        line.append(v[i])
                except:
                    pass
    
            temp = []
            for i in range(0, len(line), 2):
                temp.append((float(line[i]), float(line[i + 1])))
            coords.append(temp)
    
        # print('number of Coordinates Extracted from KML is',len(coords))
    
        return coords
