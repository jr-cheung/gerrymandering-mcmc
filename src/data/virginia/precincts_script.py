# ,"geometry".*\},"properties -> ,"properties
import re
import json
import string
from shapely.geometry import Polygon, shape, MultiPolygon
from shapely.strtree import STRtree


# def remove_geometry(string):
#     return re.sub(r',"geometry".*\},"properties', ',"properties', string)[:-2]

# def generatePolygon(coordinates):
#     coordinates = [tuple(c) for c in coordinates]
#     return Polygon(coordinates)

polygons = []
polygon_dict = {}
f = open("vaPrecincts.json")
f.readline()
f.readline()
f.readline()
f.readline()
f.readline()

output_json = json.loads("{}")

count = 1
for line in f:
    line = line[:-2]

    precinct_node = json.loads('{"adjacent_nodes":[]}')
    precinct_json = json.loads(line)

    geometry = precinct_json["geometry"]
    polygon = shape(geometry)
    polygons.append(polygon)
    polygon_dict[id(polygon)] = str(count)
    precinct_node["geometry"] = geometry

    properties = precinct_json["properties"]

    precinct_node["whitePop"] = int(round(properties["NH_WHITE"]))
    precinct_node["blackPop"] = int(round(properties["NH_BLACK"]))
    precinct_node["asianPop"] = int(round(properties["NH_ASIAN"]))
    precinct_node["hispanicPop"] = int(round(properties["HISP"]))
    precinct_node["population"] = int(round(properties["TOTPOP"]))
    precinct_node["whiteVap"] = int(round(properties["WVAP"]))
    precinct_node["blackVap"] = int(round(properties["BVAP"]))
    precinct_node["asianVap"] = int(round(properties["ASIANVAP"]))
    precinct_node["hispanicVap"] = int(round(properties["HVAP"]))
    precinct_node["totalVap"] = int(round(properties["VAP"]))
    precinct_node["district"] = string.ascii_uppercase[int(re.search(r'\d+', properties["district"])[0]) - 1]
    if properties["G16RPRS"] > properties["G16DPRS"]:
        precinct_node["voting_history"] = "R"
    else:
        precinct_node["voting_history"] = "D"

    output_json[str(count)] = precinct_node

    # if count == 1:
    #     break

    count += 1

f.close()

# StrTree stuff
tree = STRtree(polygons)
for p in polygons:
    i = polygon_dict[id(p)]
    query = tree.query(p.buffer(0))
    if len(query) == 0:
        print(i)
    for neighbor in query:
        j = polygon_dict[id(neighbor)]
        if i != j:
            output_json[i]["adjacent_nodes"].append(j)

output_file = open("virginia_graph.json", 'w')
output_file.write(json.dumps(output_json))
output_file.close()


