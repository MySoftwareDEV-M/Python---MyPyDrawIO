import functools
import json

import Framework.Informations       as Infos
import Framework.Data               as Data
import MyPyDrawIO.Attributes        as Attributes

class Geometry(Attributes.Attributes):
    """
    Klasse, die eine Geometry eines Nodes oder einer Edge repräesntiert.
    """
    ###############################################################################################
    # class variables
    __infos    = Infos.Informations()

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------
    def __init__(self, geometryContent : dict):
        """
        Konstruktor, dem ein Dictionary mit dem Inhalt einer bestehenden Geometry zu übergeben ist.

        Args:
            geometryContent {dict} Dictionary mit dem Content der Geometry
        """
        self.setProtectedAttributes([])
        dict.__init__(self, geometryContent)

    ###############################################################################################
    # Public functions
    def content(self) -> dict:
        return self

###################################################################################################
# Public global functions / Helper functions
