import json
import string
from shapely.geometry import shape
from shapely.strtree import STRtree

polygons = []
polygon_dict = {}
f = open("MD_precincts.json")
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

    precinct_node["whitePop"] = properties["NH_WHITE"]
    precinct_node["blackPop"] = properties["NH_BLACK"]
    precinct_node["asianPop"] = properties["NH_ASIAN"]
    precinct_node["hispanicPop"] = properties["HISP"]
    precinct_node["population"] = properties["TOTPOP"]
    precinct_node["whiteVap"] = properties["WVAP"]
    precinct_node["blackVap"] = properties["BVAP"]
    precinct_node["asianVap"] = properties["ASIANVAP"]
    precinct_node["hispanicVap"] = properties["HVAP"]
    precinct_node["totalVap"] = properties["VAP"]
    precinct_node["district"] = string.ascii_uppercase[int(properties["CD"][1]) - 1]
    if properties["PRES16R"] > properties["PRES16D"]:
        precinct_node["voting_history"] = "R"
    else:
        precinct_node["voting_history"] = "D"

    output_json[str(count)] = precinct_node

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


output_file = open("maryland_graph.json", 'w')
output_file.write(json.dumps(output_json))
output_file.close()


