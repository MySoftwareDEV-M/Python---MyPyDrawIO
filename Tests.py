import unittest

import MyFramework.Informations as Infos

import MyPyDrawIO.File          as File
import MyPyDrawIO.Page          as Page
import MyPyDrawIO.Vertex        as Vertex
import MyPyDrawIO.Geometry      as Geometry
import json
import os

# Gibt vor, wie ausführlich die Ausgaben von
# a) den UnitTests
# b) meinem Info-Modul
# sind.
testVerbosity = 2

Infos.Informations(verbosity=Infos.Informations.Verbosity.PrintBulky)

class TestFileAndPageLevel(unittest.TestCase):
    """
    Diese Tests umfassen:
    a) Das Erstellen über File.File
    b) Das Hinzufügen von Pages über File.File
    c) Das Verschieben von Pages über File.File
    d) Das Löschen von Pages über File.File
    """    
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        if(testVerbosity == 2):
            Infos.Informations(verbosity = 1)
        else:
            Infos.Informations(verbosity = 0)

    def setUp(self):
        """
        Diese Funktion wird zu Beginn eines jeden Tests aufgerufen und erstellt,
        beziehungsweise lädt die drawio-Datei, mit der die Tests durchgeführt werden.
        Indem in dieser Funktion die Datei gespeichert wird, werden die Manipulationen in den
        einzelnen Tests beibehalten.
        (Durch den Aufruf von test_fileDelete() wird die Datei wieder gelöscht.)
        """
        print()
        self.__fileName = "./TEST erstellt.drawio"
        self.file = File.File(self.__fileName)
        self.file.save()

    def test_fileCreate_runTime(self):
        """
        a) Prüfen, ob in der neu erstellten Datei die Inhalte wie erwartet enthalten sind.
        """
        self.assertEqual(1, len(self.file.pages()), "In der neu erstellten Datei sollte nur eine Seite enthalten sein. (Wurde \"test_fileDelete()\" zum Ende des letzten Testdurchlaufs aufgerufen?)")
        firstPage = self.file.pages()[0]
        self.assertIn("@id",        firstPage.attributes(), "Page hat kein Attribute \"@id\"")
        self.assertIn("@name",      firstPage.attributes(), "Page hat kein Attribute \"@name\"")
        self.assertIn("Seite - 1",  firstPage["@name"],     "Der Name der neu erstellten Seite sollte \"Seite - 1\" sein. (Wurde \"test_fileDelete()\" zum Ende des letzten Testdurchlaufs aufgerufen?)")

    def test_fileCreate_storage(self):
        """
        a) Prüfen, ob in der neu erstellten Datei die Inhalte nach dem Speichern und dem erneuten Laden weiterhin wie erwartet enthalten sind.
        """
        self.assertEqual(1, len(self.file.pages()), "In der neu erstellten Datei sollte nur eine Seite enthalten sein. (Wurde \"test_fileDelete()\" zum Ende des letzten Testdurchlaufs aufgerufen?)")
        firstPage = self.file.pages()[0]
        self.assertIn("@id",        firstPage.attributes(), "Page hat kein Attribute \"@id\"")
        self.assertIn("@name",      firstPage.attributes(), "Page hat kein Attribute \"@name\"")
        self.assertIn("Seite - 1",  firstPage["@name"],     "Der Name der neu erstellten Seite sollte \"Seite - 1\" sein. (Wurde \"test_fileDelete()\" zum Ende des letzten Testdurchlaufs aufgerufen?)")

    def test_pageAdd_runtTime(self):
        """
        b) Prüfen, ob Seiten hinzugefügt werden können.
        """
        self.file.insertPage(1, "NEUE SEITE 3")
        self.file.insertPage(1, "NEUE SEITE 1")
        self.file.insertPage(2, "NEUE SEITE 2")
        self.assertEqual(4, len(self.file.pages()), "Nach dem Hinzufügen sollten vier Seiten enthalten sein.")
        self.assertIn("Seite - 1",    self.file.pages()[0]["@name"], 'Ursprüngliche Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 1", self.file.pages()[1]["@name"], 'Neue Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 2", self.file.pages()[2]["@name"], 'Neue Seite 2 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 3", self.file.pages()[3]["@name"], 'Neue Seite 3 nicht an der erwarteten Position.')
        self.file.save()

    def test_pageAdd_storage(self):
        """
        b) Prüfen, ob die hinzugefügten Seiten nach dem Speichern und dem erneuten Laden weiterhin hinzugefügt sind.
        """
        self.assertEqual(4, len(self.file.pages()), "Nach dem Hinzufügen sollten vier Seiten enthalten sein.")
        self.assertIn("Seite - 1",    self.file.pages()[0]["@name"], 'Ursprüngliche Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 1", self.file.pages()[1]["@name"], 'Neue Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 2", self.file.pages()[2]["@name"], 'Neue Seite 2 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 3", self.file.pages()[3]["@name"], 'Neue Seite 3 nicht an der erwarteten Position.')

    def test_movePage_runTime(self):
        """
        c) Prüfen, ob eine Seite verschoben werden kann.
        """        
        self.file.movePage(1, 2)
        self.assertEqual(4, len(self.file.pages()), "Nach dem Verschieben sollten vier Seiten enthalten sein.")
        self.assertIn("Seite - 1",    self.file.pages()[0]["@name"], 'Ursprüngliche Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 2", self.file.pages()[1]["@name"], 'Neue Seite 2 nicht an der erwarteten (verschobenen) Position.')
        self.assertIn("NEUE SEITE 1", self.file.pages()[2]["@name"], 'Neue Seite 1 nicht an der erwarteten (verschobenen) Position.')
        self.assertIn("NEUE SEITE 3", self.file.pages()[3]["@name"], 'Neue Seite 3 nicht an der erwarteten Position.')
        self.file.save()

    def test_movePage_storage(self):
        """
        c) Prüfen, ob das Verschieben der Seite nach dem Speichern und dem erneuten Laden beibehalten wurde.
        """
        self.assertEqual(4, len(self.file.pages()), "Nach dem Verschieben sollten vier Seiten enthalten sein.")
        self.assertIn("Seite - 1",    self.file.pages()[0]["@name"], 'Ursprüngliche Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 2", self.file.pages()[1]["@name"], 'Neue Seite 2 nicht an der erwarteten (verschobenen) Position.')
        self.assertIn("NEUE SEITE 1", self.file.pages()[2]["@name"], 'Neue Seite 1 nicht an der erwarteten (verschobenen) Position.')
        self.assertIn("NEUE SEITE 3", self.file.pages()[3]["@name"], 'Neue Seite 3 nicht an der erwarteten Position.')
    
    def test_deletePage_runTime(self):
        """
        d) Prüfen, ob eine Seite gelöscht werden kann.
        """        
        self.file.deletePage(2)
        self.assertEqual(3, len(self.file.pages()), "Nach dem Verschieben sollten vier Seiten enthalten sein.")
        self.assertIn("Seite - 1",    self.file.pages()[0]["@name"], 'Ursprüngliche Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 2", self.file.pages()[1]["@name"], 'Neue Seite 2 nicht an der erwarteten (verschobenen) Position.')
        self.assertIn("NEUE SEITE 3", self.file.pages()[2]["@name"], 'Neue Seite 3 nicht an der erwarteten Position.')
        self.file.save()

    def test_deletePage_storage(self):
        """
        d) Prüfen, ob das Löschen der Seite nach dem Speichern und dem erneuten Laden beibehalten wurde.
        """
        self.assertEqual(3, len(self.file.pages()), "Nach dem Verschieben sollten vier Seiten enthalten sein.")
        self.assertIn("Seite - 1",    self.file.pages()[0]["@name"], 'Ursprüngliche Seite 1 nicht an der erwarteten Position.')
        self.assertIn("NEUE SEITE 2", self.file.pages()[1]["@name"], 'Neue Seite 2 nicht an der erwarteten (verschobenen) Position.')
        self.assertIn("NEUE SEITE 3", self.file.pages()[2]["@name"], 'Neue Seite 3 nicht an der erwarteten Position.')

    def test_fileDelete(self):
        """
        Die Datei löschen, damit im Testdurchlauf eine neu erstellte Datei verwendet wird.
        """
        try:
            os.remove(self.__fileName)
        except:
            pass

def suiteFileAndPageLevel():
    suite = unittest.TestSuite()
    suite.addTest(TestFileAndPageLevel('test_fileDelete'))
    suite.addTest(TestFileAndPageLevel('test_fileCreate_runTime'))
    suite.addTest(TestFileAndPageLevel('test_fileCreate_storage'))
    suite.addTest(TestFileAndPageLevel('test_pageAdd_runtTime'))
    suite.addTest(TestFileAndPageLevel('test_pageAdd_storage'))
    suite.addTest(TestFileAndPageLevel('test_movePage_runTime'))
    suite.addTest(TestFileAndPageLevel('test_movePage_storage'))
    suite.addTest(TestFileAndPageLevel('test_deletePage_runTime'))
    suite.addTest(TestFileAndPageLevel('test_deletePage_storage'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity = testVerbosity, failfast = True)
    runner.run(suiteFileAndPageLevel())

    for entry in Infos.entries(Infos.Informations.Types.ERROR):
        entry.printSimple()
