JCLI
====

Joshua Chin's Lisp Interpreter is a Lisp interpreter, written in python2, for the [frozen syntax project](https://github.com/Shriken/frozen-syntax).

Features
--------

* **Paused Execution** - JCLI can pause the execution of a program and restart it at a later time
* **First Class Function** - In JCLI, function are first class values, just like integers and strings
* **Python Interoperability** - JCLI programs can call python functions
* **Garbage Collection** - JCLI uses the python garbage collector to handle memory management
* **Tail Call Optimization** - JCLI implements full TCO, allowing space efficient recursive function
* **Documentation** - JCLI's runtime is [documented](https://github.com/Joshua-Chin/jcli/blob/frozen-syntax/documentation.md)
* **Debug Information** - JCLI includes the line number if an exception occurs
