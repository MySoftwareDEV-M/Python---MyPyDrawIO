import xmltodict

import MyFramework.Informations   as Infos
import MyFramework.Data           as Data
    
class ElementDefinition(dict):
    """
    ElementDefinitions werden beim Laden von [Library Objekten](./Library.html#Library) angelegt. Sie repräsentieren die in der DrawIO Bibliothek enthaltenen Definitionen von [Vertices](./Vertex.html#Vertex) und [Edges](./Edge.html#Edge) und dienen als Vorlage für die Erstellung. Hierzu werden sie den Funktionen [Page.createVertex()](./Page.html#Page.createVertex) und [Page.createEdge()](./Page.html#Page.createEdge) übergeben.
    """    
    ###############################################################################################
    # class variables of Element
        
    ###############################################################################################
    # private functions  of Element
            
    ###############################################################################################
    # public functions  of Element        
    #----------------------------------------------------------------------------------------------
    def parse(self, definition : str) -> bool:
        """
        Der übergebene String wird geparst. In diesem String sollte die Definition eines DrawIO Elements enthalten sein.
        """        
        # 1. We only need the "xml entry"
        definition = definition["xml"]

        # 2. This "xml entry" needs to be paresd
        definition = xmltodict.parse(definition)
        
        # 3. Within this content we expect the "object key" to exist.
        try:
            # object_definition = definition["mxGraphModel"]["root"]["object"]
            # Infos.announceDebug("Hier habe ich einen Anpassung gemacht")
            object_definition = definition["mxGraphModel"]["root"]
        except:
            return ""

        # 4. If we made it this far, we can retrieve the relevant information
        # ... get the name
        name = object_definition["object"]["@name"]
        self["name"] = name
        
        # .. check if it is a vertex ...
        try:
            object_definition["object"]["mxCell"]["@vertex"]
            self["vertex"] = "1"
        except:
            pass
        # .. or an edge
        try:
            object_definition["object"]["mxCell"]["@edge"]
            self["edge"] = "1"
        except:
            pass
        
        # ... get the definition
        self["object definition"] = object_definition["object"]
        return name

###################################################################################################
# Public global functions / Helper functions