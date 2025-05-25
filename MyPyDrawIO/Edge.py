import Framework.Data               as Data
import MyPyDrawIO.Attributes        as Attributes
import MyPyDrawIO.Library           as Library
import MyPyDrawIO.ElementDefinition as ElementDefinition
import MyPyDrawIO.Geometry          as Geometry

class Edge(Attributes.Attributes):
    """
    Objekt, das eine Edge auf einer [Page](./Page.html#Page) repräsentiert.
    """
    ###############################################################################################
    # class variables
    __geometry  : Geometry.Geometry

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, content : dict, sourceID : str = None, targetID : str = None):
        """        
        Wenn ein Dictionary (mit dem Inhalt einer Edge) übergeben wird, wird ein entsprechendes Edge Objekt erstellt. Wenn ein [Libraries.Element](./Libraries.html#Element) übergeben wird, wird entsprechend dessen Definition ein Edge Objekt erstellt.
        """
        self.setProtectedAttributes(["@id", "@edge", "@parent"])
        if(type(content) == ElementDefinition.ElementDefinition):
            definition = content["definition"]
            self.__geometry = Geometry.Geometry(definition["mxGeometry"])
            dict.__init__(self, Data.copyArguments(definition))
            self["@parent"] = "1"
            self["@source"] = sourceID
            self["@target"] = targetID
        else:
            dict.__init__(self, Data.copyArguments(content))
            self.__geometry = Geometry.Geometry(content["mxGeometry"])

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def content(self) -> dict:
        """
        Gibt den Inhalt dieser edge zurück, welcher nach der Überführung in XML zum Speichern in der Datei genutzt werden kann.
        """
        content = Data.copyArguments(self)
        content["mxGeometry"] = self.__geometry.content()
        return content

    #----------------------------------------------------------------------------------------------
    def geometry(self) -> Geometry.Geometry:
        """
        Gibt die [Geometry](./Geometry.html#Geometry) dieser Edge zurück.
        """        
        return self.__geometry

###################################################################################################
# Public global functions / Helper functions
