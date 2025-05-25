import os
import xmltodict

import MyFramework.Informations     as Infos

import MyPyDrawIO.Page              as Page
import MyPyDrawIO.Attributes        as Attributes

class File(Attributes.Attributes):
    """
    Repräsentation einer gesamten drawIO-Datei.
    Die wichtigsten Eigenschaften dieser Datei sind der Dateipfad und die Seiten der Datei.

    Über [pages()](./File.html#File.pages) werden die aktuell in der Datei enthaltenen [Page Objekte](./Page.html#Page) in der Reiehnfolge, wie sie auch in der DrawIO Datei gespeichert werden, ausgegeben. Die in dieser Liste enthalten [Page Objekte](./Page.html#Page) können direkt zur Bearbeitung und Ansicht des Seiteninhalts genutzt werden.
    """
    ###############################################################################################
    # class variables
    __filePath          : str
    __pages             = list[Page.Page]()

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __createFile(self):
        """
        Private Funktion, um eine DrawIO Datei mit einer Seite zu erstellen.
        """
        newPage = Page.Page("Seite - 1")
        self["mxfile"] = {
            "diagram" : []
        }

        self.__pages = list()
        self.__pages.append(
            newPage
        )

    #----------------------------------------------------------------------------------------------
    def __init__(self, filePath):
        """
        filePath ist der Pfad zu der Datei, die geöffnet oder erstellt werden soll. Wenn die Datei noch nicht besteht, wird eine neue Datei unter dem Dateipfad angelegt.
        """
        self.__infos       = Infos.Informations()
        self.__filePath     = ''
        self.__pages        = list()

        self.open(filePath)

    #----------------------------------------------------------------------------------------------
    def __loadFile(self):
        """
        Private Funktion zum Laden einer bestehenden Datei.
        """
        pages = []
        self.__pages = list[Page.Page]()

        # 1. Die Datei laden
        try:
            file = open(self.__filePath)
            content = xmltodict.parse(file.read())
            file.close()
            dict.__init__(self, content)
            # WICHTIG: Die Zuweisung zu pages muss erfolgen, bevor in der folgenden Zeile
            # im self-Objekt der Eintrag diagram gelöscht wird.
            # Indem zuerst die Pages ihre Teile des Dictionaries referenzieren, scheinen diese Teile nicht vom Löschen betroffen zu sein.
            pages = content["mxfile"]["diagram"]
            self["mxfile"]["diagram"] = []
        except:
            Infos.announceError("Datei \"" + self.__filePath + "\" konnte nicht geladen werden.")
            return
        
        # 2. Die Seiten bestimmen
        if(type(pages) == dict):
            self.__pages.append(
                Page.Page(pages)
            )
        else:
            for page in pages:
                self.__pages.append(
                    Page.Page(page)
                )
        self["mxfile"]["diagram"] = []

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def deletePage(self, position : int):
        """
        Löscht die Seite an der angegebenen Position.
        Wenn mit dem Aufruf die letzte Seite gelöscht wird, wird die leere "Seite - 1" eingefügt.
        """
        page = self.__pages.pop(position)
        page._invalidate()
        if(len(self.__pages) == 0):
            self.insertPage(0, "Seite - 1")

    #----------------------------------------------------------------------------------------------
    def insertPage(self, position : int, name : str) -> Page.Page:
        """
        Erstellt eine neue Seite und fügt sie an der angegebenen Position ein. Das erstellte [Page Objekt](./Page.html#Page) wird zurückgegeben.
        """
        newPage = Page.Page(name)
        self.__pages.insert(position, newPage)
        return newPage

    #----------------------------------------------------------------------------------------------
    def movePage(self, positionOld : int, positionNew : int):
        """
        Verschiebt die Seite von der Position Old auf die Position New.
        """
        page = self.__pages.pop(positionOld)
        self.__pages.insert(positionNew, page)

    #----------------------------------------------------------------------------------------------
    def numOfPages(self):
        """
        Gibt die Anzahl der Seiten in der DrawIO Datei aus.
        """
        return len(self.__pages)

    #----------------------------------------------------------------------------------------------
    def open(self, filePath):
        """
        Wenn aktuell eine Datei geöffnet ist, wird diese gespeichert.
        Wenn die in filePath angegebene Datei besteht, wird diese geöffnet.
        Wenn die in filePath angegebene Datei nicht besteht, wird diese erstellt.
        """
        if(self.__filePath):
            Infos.announceDebug("Aktuell geöfnete Datei wird gespeichert und geschlossen.")
            self.save()

        self.__filePath = filePath
        if(os.path.exists(filePath) == True):
            Infos.announceDebug("Bestehende Datei wird geladen.")
            self.__loadFile()
        else:
            Infos.announceDebug("Neue Datei wird erstellt.")
            self.__createFile()
    
    #----------------------------------------------------------------------------------------------
    def pages(self) -> list [Page.Page]:
        """
        Eine geordnete Liste der [Page Objekte](./Page.html#Page) zu allen Seiten. 
        """
        return self.__pages
            
    #----------------------------------------------------------------------------------------------
    def save(self):
        """
        Speichert den aktuellen Arbeitsstand unter dem zuvor angegebenen Dateipfad.
        """        
        f = open(self.__filePath, "w")

        diagrams = []
        for page in self.__pages:
            diagrams.append(page.content())

        content = self
        content["mxfile"]["diagram"] = diagrams
        
        f.write(xmltodict.unparse(content, pretty = True))
        f.close()

    #----------------------------------------------------------------------------------------------
    def saveAs(self, filePath : str):
        """
        Speichert den aktuellen Arbeitsstand unter dem neu angegebenen Dateipfad. Ein erneuter Aufruf von [save()](./File.html#File.save) speichert den Arbeitsstand dann ebenfalls unter dem neu angegebenen Dateipfad.
        """        
        self.__filePath = filePath
        self.save()

###################################################################################################
# Public global functions / Helper functions
