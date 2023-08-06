**REINDEER**
-
Reindeer ist Python Bibliothek um durch Verwendung des DEER-Frameworks, 
CSV-Datensätzen mit zusätzlichen Informationen aus LinkedData anzureichern.

Dazu wird die Funktion `enriche([input_file/s], output_file, script)` bereitgestellt. 
Dieser werden dann eine Liste mit einem oder mehrere Input-Files, ein Path in dem das Resultat 
gespeichert werden soll sowie ein Skript für das DEER-Framework übergeben. Um die Anwendung zu erleichtern 
stehen darüber hinaus auch verschiedene bouild-in Skripts zur Verfügung. Diese können durch die übergäbe 
eines entsprechenden Strings ausgewählt werden.   
  

Installation
-
1.) Deer wie auf GitHub (https://github.com/dice-group/deer) beschrieben installieren. 
Es muss Version 2.0.0 oder 2.0.1 verwendet werden. 
    
    Achtung: Deer kann nur unter Java 9 kompiliert werden. 
    Außerdem musste in der pom.xml `<maven.compiler.target>9</maven.compiler.target>` 
    zu `<maven.compiler.target>1.9</maven.compiler.target>` geändert werden.
    
2.) In `enricher.py` den Path von `Deer-Jar-File` angepassen

3.) Python Bibliothek RDFlib installieren (https://github.com/RDFLib/rdflib) 
    `pip install rdflib`
    `pip install rdflib-jsonld`
    
 Demo
 -
