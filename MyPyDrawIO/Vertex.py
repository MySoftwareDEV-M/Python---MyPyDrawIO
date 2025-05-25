import uuid

import MyFramework.Informations     as Infos
import MyFramework.Data             as Data
import MyPyDrawIO.Attributes        as Attributes
import MyPyDrawIO.Geometry          as Geometry
import MyPyDrawIO.Library           as Library
import MyPyDrawIO.ElementDefinition as ElementDefinition

class Vertex(Attributes.Attributes):
    """
    Objekt, das einen Vertex auf einer [Page](./Page.html#Page) repräsentiert.
    """
    ###############################################################################################
    # class variables
    __geometry  : Geometry.Geometry
    __object    = None
    __parent    = None

    ###############################################################################################
    # private functions    
    #----------------------------------------------------------------------------------------------
    def __init__(self, content : dict, parent = None):
        """        
        Wenn ein Dictionary (mit dem Inhalt eines Vertex) übergeben wird, wird ein entsprechendes Vertex Objekt erstellt. Wenn ein [Libraries.Element](./Libraries.html#Element) übergeben wird, wird entsprechend dessen Definition ein Vertex Objekt erstellt.
        """
        self.setProtectedAttributes(["@id", "@parent", "@vertex"])
        if(type(content) == ElementDefinition.ElementDefinition):
            definition = content["object definition"]
            self.__geometry = Geometry.Geometry(definition["mxCell"]["mxGeometry"])
            self.__object = Data.copyArguments(definition)
            dict.__init__(self, Data.copyArguments(definition["mxCell"]))
            self.__object["@id"] = str(uuid.uuid4())
            self["children"] = list[Vertex]()
                            
            if(parent != None):
                parent.addChild(self)
                self["@parent"] = parent["@id"]
        else:
            try:
                self.__geometry = Geometry.Geometry(content["mxCell"]["mxGeometry"])
                del content["mxCell"]["mxGeometry"]
                self.__object = Data.copyArguments(content)
                dict.__init__(self, Data.copyArguments(content["mxCell"]))
                self["children"] = list[Vertex]()
                
            except:
                self.__geometry = Geometry.Geometry(content["mxGeometry"])
                del content["mxGeometry"]
                dict.__init__(self, Data.copyArguments(content))
                self["children"] = list[Vertex]()

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def addChild(self, newChild):
        """
        Fügt diesem Vertex das newChild hinzu. Sollte das newChild bereits einem anderen Vertex als Child zugeordnet sein, wird er dort als Child entfernt. Dieser Vertex wird bei dem newChild als [Parent](./Vertex.html#Parent) gesetzt.
        """        
        children = self["children"]
        for child in children:
            if(child == newChild):
                return
        children.append(newChild)
        self["children"] = children

        parent = newChild.parent()
        if(parent != None):
            parent.removeChild(self)
        newChild.setParent(self)
        
    def content(self) -> list:
        """
        Gibt den Inhalt dieses Vertex zurück, welcher nach der Überführung in XML zum Speichern in der Datei genutzt werden kann.
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
            content = [content]
        else:
            content = Data.copyArguments(self)
            content["mxGeometry"] = self.__geometry.content()
            content = [content]

        children = self["children"]
        for child in children:
            content.extend(child.content())

        return content
    
    def geometry(self) -> Geometry.Geometry:
        """
        Gibt die [Geometry](./Geometry.html#Geometry) dieses Vertex zurück.
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
    
    def removeChild(self, child):
        """
        Entfernt child bei diesem Vertex als child. Bei dem Child wird der [parent()](./Vertex.html#Vertex.parent) auf None gesetzt.
        """        
        children = self["children"]
        children.remove(child)
        self["children"] = children
        child.setParent(None)

    def parent(self):
        """
        Vertex, welcher der Parent dieses Vertex Objekts ist.
        """     
        return self.__parent

    def setParent(self, parent):
        """
        Setzt den Parent Vertex, zu diesem Vertex Objekt.
        """     
        self.__parent = parent

###################################################################################################
# Public global functions / Helper functions
