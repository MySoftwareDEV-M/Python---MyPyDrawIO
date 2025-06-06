import json
import xmltodict

import MyFramework.Informations     as Infos
import MyPyDrawIO.ElementDefinition as ElementDefinition
    
class Library(dict):
    """
    Repräsentation einer DrawIO-Bibliothek (xml-Datei). Zu den in den DrawIO Bibliotheken enthaltenen Vertices und Edges werden [ElementDefinition](./ElementDefinition.html#ElementDefinition) erstellt. Diese dienen als Vorlage für die Erstellung von Vertices und Edges, welche den Funktionen [Page.createVertex()](./Page.html#Page.createVertex) und [Page.createEdge()](./Page.html#Page.createEdge) übergeben werden.
    """    
    ###############################################################################################
    # class variables of Library    
    __edges     = dict()
    __vertices  = dict()
        
    ###############################################################################################
    # private functions of Library
    def __init__(self):
        self["name"] = "<no name>"
            
    ###############################################################################################
    # public functions of Library
    #----------------------------------------------------------------------------------------------
    def vertex(self, name : str) -> ElementDefinition.ElementDefinition:
        """
        Gibt eine [ElementDefinition](./ElementDefinition.html#ElementDefinition) für die Erstellung eines [Vertices](./Vertex.html#Vertex) zurück.
        """        
        return self.__vertices[name]
    
    #----------------------------------------------------------------------------------------------
    def edge(self, name : str) -> ElementDefinition.ElementDefinition:
        """
        Gibt eine [ElementDefinition](./ElementDefinition.html#ElementDefinition) für die Erstellung einer [Edge](./Edge.html#Edge) zurück.
        """
        return self.__edges[name]
    
    #----------------------------------------------------------------------------------------------
    def vertices(self) -> list[str]:
        """
        Gibt eine Liste der Namen der [ElementDefinition](./ElementDefinition.html#ElementDefinition) für die Erstellung eines [Vertices](./Vertex.html#Vertex) zurück.
        Über diese Namen können die [ElementDefinitionen](./ElementDefinition.html#ElementDefinition) in der Funktion [edge()](./Library.html#Library.vertex) abgerufen werden.
        """
        return self.__vertices.keys()
        
    #----------------------------------------------------------------------------------------------
    def edges(self) -> list[str]:
        """
        Gibt eine Liste der Namen der [ElementDefinition](./ElementDefinition.html#ElementDefinition) für die Erstellung einer [Edge](./Edge.html#Edge) zurück.
        Über diese Namen können die [ElementDefinitionen](./ElementDefinition.html#ElementDefinition) in der Funktion [edge()](./Library.html#Library.edge) abgerufen werden.
        """
        return self.__edges.keys()
    
    #----------------------------------------------------------------------------------------------
    def load(self, filePath : str) -> bool:
        """
        Lädt die in filePath angegebene DrawIO Bibliothek und legt zu all den in der Bibliothek enthaltenen Elemente [ElementDefinition](./ElementDefinition.html#ElementDefinition) an.
        """        
        # 1. load the file
        try:
            file = open(filePath)
            content = xmltodict.parse(file.read())
            file.close()
        except:
            Infos.announceWarning("Library \"" + filePath + "\"con not be loaded.")
            return False
        
        # 2. get the name
        name = filePath.split("/")
        name = name[len(name)-1]
        index = name.index(".")
        self["name"] = name[:index]
        
        # 3. get the content --> all the elements within the library ...
        content = content["mxlibrary"]
        content = json.loads(content)
        # ... and create an element for each
        for elementDefinition in content:
            element = ElementDefinition.ElementDefinition()
            name = element.parse(elementDefinition)
            if(name == None):
                Infos.announceWarning("An element within the library \"" + self["name"] + "\" could not be parsed")
            else:
                try:
                    element["vertex"]
                    self.__vertices[name] = element
                except:
                    pass

                try:
                    element["edge"]
                    self.__edges[name] = element
                except:
                    pass
        
        return True

###################################################################################################
# Public global functions / Helper functions