# Prevoditelj iz jednog programskog jezika u drugi
Projekt iz kolegija Deklarativnog programiranje pod nazivom Prevoditelj iz jednog programskog jezika u drugi. U ovom projektu nalazi se početnički prevoditelj iz Pythona u Prolog.

Aplikacija se pokreće unutar Jupyter Notebooka pokretanjem ```App.ipynb``` datoteke.

Sve potrebe datoteke dobivaju se pokretanjem naredbi  ```antlr4 -Dlanguage=Python3 MiniPythonGramatika.g4``` i ```antlr4 -Dlanguage=Python3 -visitor MiniPythonGramatika.g4``` u terminalu.

Također, za potrebe izrade projekta sve je rađeno unutar posebnog okruženja ```venv``` (u ovom slučaju).
