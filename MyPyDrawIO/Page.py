import uuid

import MyFramework.Informations     as Infos
import MyFramework.Data             as Data
import MyPyDrawIO.Attributes        as Attributes
import MyPyDrawIO.Edge              as Edge
import MyPyDrawIO.Library           as Library
import MyPyDrawIO.ElementDefinition as ElementDefinition
import MyPyDrawIO.Vertex            as Vertex

class Page(Attributes.Attributes):
    """
    Repräsentation einer Seite in einer drawIO-Datei.
    """
    ###############################################################################################
    # class variables
    __vertices          = list[Vertex.Vertex]()
    __edges             = list[Edge.Edge]()

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __rootContent(self) -> dict:
        """
        Private Funktion, die das Dictionary mit den Informationen zu den Vertices und Edges erzeugt, wie sie in der DrawIO Datei gespeichert werden können.
        """
        mxCells = []
        mxCells.append(
            {
                "@id": "0"
            }
        )
        mxCells.append(
            {
                "@id": "1",
                    "@parent": "0"
            }
        )
        
        objects = []

        for vertex in self.__vertices:
            if(vertex.isObject()):
                objects.extend(vertex.content())
            else:
                mxCells.extend(vertex.content())

        for edge in self.__edges:
            if(edge.isObject()):
                objects.append(edge.content())
            else:
                mxCells.append(edge.content())

        root = {
            "mxCell": mxCells,
            "object": objects
        }
        return root

    #----------------------------------------------------------------------------------------------
    def __init__(self, input): #name : str = None, content : dict = None):
        """
        Wenn ein Dictionary (mit dem Inhalt zu einer Seite) übergeben wird, wird dieser Inhalt interpretiert und eine Seite mit entsprechendem Inhalt erstellt. Wenn ein String übergeben wird, wird eine leere Seite mit dem String als Namen erstellt.
        """
        self.setProtectedAttributes(["@id", "@parent"])
        if( type(input) == str ):
            self["@name"]    = input
            self["@id"]      = str(uuid.uuid4())
            self["mxGraphModel"] = {
                    "@dx": "780",
                    "@dy": "542",
                    "@grid": "1",
                    "@gridSize": "10",
                    "@guides": "1",
                    "@page": "1",
                    "@pageScale": "1",
                    "@pageWidth": "1169",
                    "@pageHeight": "1654",
                    "@math": "0",
                    "@shadow": "0",
                    "root": {}
                }
        elif( type(input) == dict ):
            self.setProtectedAttributes(["@id", "@parent"])
            dict.__init__(self, input)
            self.__evaluateElements(input["mxGraphModel"])
            self["mxGraphModel"]["root"] = {}
        else:
            Infos.announceError("Unsupported data type")

    #----------------------------------------------------------------------------------------------
    def __evaluateElements(self, mxGraphModel):
        """
        Wertet die Elemente (mxCell & object) in _theDict["mxGraphModel"]["root"] aus und überführt diese in 
        a) ein Dictionary, dass die Vertices in einer Parent-Child-Struktur repräsentiert.
        b) eine Liste, der Edges.
        """
        self.__vertices = []
        self.__edges    = []
        allVertices     = []
        childVertices   = []
        
        elements = mxGraphModel["root"]["mxCell"]
        
        try:
            objects = mxGraphModel["root"]["object"]
            if type(objects) == dict:
                elements.append(objects)
            elif type(objects) == list:
                elements.extend(objects)
        except:
            pass
        
        for cell in elements:
            try:
                vertex = Attributes.Attributes.getValue(cell["mxCell"], "@vertex")
                edge   = Attributes.Attributes.getValue(cell["mxCell"], "@edge")
                
            except:
                vertex = Attributes.Attributes.getValue(cell, "@vertex")
                edge   = Attributes.Attributes.getValue(cell, "@edge")

            if(edge):
                self.__edges.append(Edge.Edge(cell))
                continue

            if(vertex):
                vertex = Vertex.Vertex(cell)
                allVertices.append(vertex)
                if(vertex.attribute("@parent") == "0"):
                    pass
                elif(vertex.attribute("@parent") == "1"):
                    self.__vertices.append(vertex)
                else:
                    childVertices.append(vertex)

        for child in childVertices:
            parentID = child["@parent"]
            parent = self.__getParent(allVertices, parentID)
            parent.addChild(child)
    
    def __getParent(self, allVertices : list, parentID : str) -> Vertex.Vertex:
        """
        Hilfsfunktion, um aus der übergebenen Liste einen Eintrag mit der übergebenen ID zurückzugeben. (Dies wird genutzt, um den Parent zu bestimmen.)
        """
        for vertex in allVertices:
            if( vertex.id() == parentID):
                return vertex
        return None
    
    #----------------------------------------------------------------------------------------------
    def _invalidate(self) -> str:
        """
        Da zu Page-Objekten beliebig viele Referenzen bestehen können, welche auch nachdem das eigentliche Page-Objekt gelöscht wurde, wird die weitere Bearbeitung unterbunden, indem beim Löschen das Page-Objekt zurückgesetzt wird.
        """
        self._theDict           = {}
        self["@name"]           = ""
        self["@id"]             = ""
        self["mxGraphModel"]    = ""
        self.__vertices         = []
        self.__edges            = []

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def createVertex(self, element : ElementDefinition.ElementDefinition, parent : Vertex.Vertex = None) -> Vertex.Vertex:
        """
        Entsprechend der mit [Element](./Libraries.html#Element) vorgegebenen Definition wird ein [Vertex](./Vertex.html#Vertex) für diese Seite erstellt. Wenn ein Parent [Vertex](./Vertex.html#Vertex) übergeben wird, wird der erstellte [Vertex](./Vertex.html#Vertex) diesem Parent als Child zugeordnet. Der erstellte [Vertex](./Vertex.html#Vertex) wird zurückgegeben.
        """
        vertex = Vertex.Vertex(element, parent)
        if parent == None:
            self.__vertices.append(vertex)
        
        return vertex
    #----------------------------------------------------------------------------------------------
    def createEdge(self, element : ElementDefinition.ElementDefinition, sourceID : str = None, targetID : str = None) -> Edge.Edge:
        """
        Entsprechend der mit [Element](./Libraries.html#Element) vorgegebenen Definition wird eine [Edge](./Edge.html#Edge) für diese Seite erstellt. Die erstellte [Edge](./Edge.html#Edge) wird zurückgegeben.
        """
        edge = Edge.Edge(element, sourceID, targetID)
        self.__edges.append(edge)
        return edge
    
    #----------------------------------------------------------------------------------------------
    def edges(self) -> list[Edge.Edge]:
        """
        Gibt eine Liste der [Edges](./Edge.html#Edge) dieser Seite zurück.
        """
        return self.__edges
    
    #----------------------------------------------------------------------------------------------
    def id(self) -> str:
        """
        Gibt die id dieser Page zurück.
        """
        return self["@id"]
    
    #----------------------------------------------------------------------------------------------
    def name(self) -> str:
        """
        Gibt den Namen dieser Page zurück.
        """
        return self["@name"]
    
    #----------------------------------------------------------------------------------------------
    def vertices(self) -> list[Vertex.Vertex]:
        """
        Gibt eine Liste aller Top Level [Vertices](./Vertex.html#Vertex) der Page zurück. Die Children dieser [Vertices](./Vertex.html#Vertex) werden unter jedem Parent [Vertex](./Vertex.html#Vertex) angegeben. Den Children sind wiederum die ihnen zugehörigen Children zugeordnet und so weiter.
        """
        return self.__vertices
    
    #----------------------------------------------------------------------------------------------
    def content(self) -> dict:
        """
        Gibt den Inhalt dieser Seite zurück, welcher nach der Überführung in XML zum Speichern in der Datei genutzt werden kann.
        """
        mxGraphModel = dict(self["mxGraphModel"])
        mxGraphModel["root"] = self.__rootContent()
        pageDict = {
            "@name"         : str(self["@name"]),
            "@id"           : str(self["@id"]),
            "mxGraphModel"  : mxGraphModel
        }
        return pageDict
    
    #----------------------------------------------------------------------------------------------
    def setName(self, name : str):
        """
        Setzt den Namen dieser Page.
        """
        self["@name"] = name

###################################################################################################
# Public global functions / Helper functions
