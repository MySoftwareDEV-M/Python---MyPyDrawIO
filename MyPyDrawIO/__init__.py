"""
MyPyDrawio ermöglicht bestehende DrawIO Dateien zu laden oder neue DrawIO Dateien zu erstellen. Deren Aufbau kann angezeigt und manipuliert werden. Diese Dateien können gespeichert oder in einer Datei mit anderem Namen gespeichert werden.

Eine DrawIO Datei wird durch ein [File](./MyPyDrawIO/File.html#File) repräsentiert.
Die Seiten einer Datei werden durch [Pages](./MyPyDrawIO/Page.html#Page) repräsentiert.
Bei den Shapes auf den Seiten wird zwischen [Vertices](./MyPyDrawIO/Vertex.html#Vertex) (den Objekten) und [Edges](./MyPyDrawIO/Edge.html#Edge) (den Verbindern) unterschieden.

Neue Vertices und Edges werden über DrawIO Bibliotheken definiert. Diese Bibliotheken können über [Libraries](./MyPyDrawIO/Libraries.html#Libraries) geladen werden. Die Elemente in den Bibliotheken, also die Vertices und Edges, sind den Create-Funktionen einer Seite zu übergeben, so dass entsprechend der Voreinstellung des Elements eine konkrete Instanz zu diesem Element erstellt wird.
"""