import MyFramework.Informations as Infos

import MyPyDrawIO.File          as File
import MyPyDrawIO.Libraries     as Libraries
import MyPyDrawIO.Page          as Page
import MyPyDrawIO.Vertex        as Vertex
import MyPyDrawIO.Geometry      as Geometry
import json
import os

Infos.Informations(verbosity=Infos.Informations.Verbosity.PrintBulky)
fileName = "./TEST Bibliothek in DrawIO nutzen.xml"

libraries = Libraries.Libraries()
libraries.loadLibrary("./Libraries/MainLibrary.xml")
lib = libraries.libraries()[0]
print(lib.vertices())
print(lib.edges())

# def_rect  = lib.vertex("RECTANGLE")
# def_edge  = lib.edge("VERBINDER PFEIL")
        
# file = File.File(fileName)
# page = file.pages()[0]

# vertex_rect1 = page.createVertex(def_rect)
# vertex_rect1["@value"] = "RECT 1"

# vertex_rect2 = page.createVertex(def_rect)
# vertex_rect2["@value"] = "RECT 2"

# edge = page.createEdge(def_edge, vertex_rect1.id(), vertex_rect2.id())
            
# file.save()

