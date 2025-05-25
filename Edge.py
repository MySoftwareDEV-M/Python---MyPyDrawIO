import uuid

import MyFramework.Data             as Data
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
    __object    = None

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, content : dict, sourceID : str = None, targetID : str = None):
        """        
        Wenn ein Dictionary (mit dem Inhalt einer Edge) übergeben wird, wird ein entsprechendes Edge Objekt erstellt. Wenn ein [Libraries.Element](./Libraries.html#Element) übergeben wird, wird entsprechend dessen Definition ein Edge Objekt erstellt.
        """
        self.setProtectedAttributes(["@id", "@edge", "@parent"])
        if(type(content) == ElementDefinition.ElementDefinition):
            definition = content["object definition"]
            self.__geometry = Geometry.Geometry(definition["mxCell"]["mxGeometry"])
            self.__object = Data.copyArguments(definition)
            self.__object["@id"] = str(uuid.uuid4())
            dict.__init__(self, Data.copyArguments(definition["mxCell"]))
            self["@parent"] = "1"
            self["@source"] = sourceID
            self["@target"] = targetID
            
        else:
            try:
                self.__geometry = Geometry.Geometry(content["mxCell"]["mxGeometry"])
                del content["mxCell"]["mxGeometry"]
                self.__object = Data.copyArguments(content)
                dict.__init__(self, Data.copyArguments(content["mxCell"]))
                
            except:
                self.__geometry = Geometry.Geometry(content["mxGeometry"])
                del content["mxGeometry"]
                dict.__init__(self, Data.copyArguments(content))

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def content(self) -> dict:
        """
        Gibt den Inhalt dieser edge zurück, welcher nach der Überführung in XML zum Speichern in der Datei genutzt werden kann.
        """
        content = None
        if(self.__object):
            content = Data.copyArguments(self.__object)
            content["mxCell"] = Data.copyArguments(self)
            
            value = Attributes.Attributes.getValue(content["mxCell"], "@value")
            if(value):
                content["@label"] = value
                del content["mxCell"]["@value"]
            
            content["mxCell"]["mxGeometry"] = self.__geometry.content()
        else:
            content = Data.copyArguments(self)
            content["mxGeometry"] = self.__geometry.content()
            
        return content

    #----------------------------------------------------------------------------------------------
    def geometry(self) -> Geometry.Geometry:
        """
        Gibt die [Geometry](./Geometry.html#Geometry) dieser Edge zurück.
        """        
        return self.__geometry

    def id(self) -> str:
        """
        Gibt das Attribut id des Vertex zurück.
        <br>
        <br>Technischer Hintergrund:
        <br>Je nachdem, ob ein Vertex als Object oder als einfacher Vertex realisiert ist, wird dessen ID 
        entweder im Object oder halt im einfachen Vertex hinterlegt. Diese Funktion führt die entsprechende
        Prüfung durch und gibt die id zurück.
        """
        if (self.isObject()):
            return self.__object["@id"]
        return self["@id"]
    
    def isObject(self) -> bool:
        """
        Gibt zurück, ob dieser Vertex ein Object ist.
        <br> true -> Vertex ist ein Object
        <br> false -> Vertex ist kein Object, sondern ein einfacher Vertex.
        """
        return (self.__object != None)
###################################################################################################
# Public global functions / Helper functions
