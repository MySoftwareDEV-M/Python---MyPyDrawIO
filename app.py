import Framework.Informations as Infos

import MyPyDrawIO.File      as File
import MyPyDrawIO.Libraries as Libraries
import MyPyDrawIO.Page      as Page
import MyPyDrawIO.Vertex    as Vertex
import MyPyDrawIO.Geometry  as Geometry
import json
import os

Infos.Informations(verbosity=Infos.Informations.Verbosity.PrintBulky)
fileName = "./TEST Bibliothek in DrawIO nutzen.xml"

libraries = Libraries.Libraries()
libraries.loadLibrary("./Libraries/MainLibrary.xml")
lib = libraries.libraries()[0]
# print(lib.vertices())

def_rect  = lib.vertex("RECTANGLE")
        
file = File.File(fileName)
page = file.pages()[0]

# vertex_rect = page.createVertex(def_rect)
# vertex_rect["@value"] = "GESETZT IN PYTHON"

# for vertex in page.vertices():
#     print(json.dumps(vertex, indent = 3))
            
file.save()

