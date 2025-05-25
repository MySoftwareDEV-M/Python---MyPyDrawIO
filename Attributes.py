class Attributes(dict):
    """
    Abstrakte Klasse, über die die XML-Attribute eines Elements generisch zugänglich gemacht werden. Die XML-Attribute sind durch ein @ gekennzeichnet.
    """
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self):
        self.__protectedAttributes = []

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def addAttribute(self, attribute : str, value):
        """
        Wenn das Attribute bereits besteht, wird dessen Wert gesetzt, solange es nicht geschützt ist.
        Wenn das Attribute nicht besteht, wird es ergänzt, solange es nicht geschützt ist.
        """
        if(attribute in self.__protectedAttributes):
            return
        self[attribute] = value

    #----------------------------------------------------------------------------------------------
    def attributes(self) -> list:
        """
        Liste der Attribute, die von diesem Objekt bereitgestellt werden.
        """
        keys = self.keys()
        keys = list(filter(lambda x: x.startswith("@"), keys))
        return keys
        
    #----------------------------------------------------------------------------------------------
    def attribute(self, attribute : str):
        """
        Gibt den Wert des Attributes zurück, wenn dieses existiert. Ansonsten wird None zurückgegeben.
        """
        try:
            return self[attribute]
        except:
            return None
        
    #----------------------------------------------------------------------------------------------
    def setAttribute(self, attribute : str, value):
        """
        Setzt den Wert des Attributes, wenn dieses existiert und nicht geschützt ist.
        (Wenn es nicht existiert, wird es nicht erstellt und auch nicht gesetzt.)
        """
        if(attribute in self.__protectedAttributes):
            return
        
        attributes = self.attributes()
        if attribute in attributes:
            self[attribute] = value
        
    #----------------------------------------------------------------------------------------------
    def setProtectedAttributes(self, attributes : list):
        """
        Setzt eine Liste von Attributen, die nicht über `MyPyDrawIO.Attributes.Attributes.addAttribute` und `MyPyDrawIO.Attributes.Attributes.setAttribute` geändert werden können.
        """
        self.__protectedAttributes = attributes

###################################################################################################
# Public global functions / Helper functions
    def getValue(aDict : dict, attribute : str):
        """
            Öffentliche Funktion, die das Auslesen von Key-Value-Paaren in einem Dictionary kapselt und Abbrüche durch Fehler vermeidet.
        """        
        try:
            return aDict[attribute]
        except:
            return None
