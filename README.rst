Ord-en Ley
==========

Resume
------
Desktop program to manage lawyer's office

This project has been made to allow mainly new lawyers who wants to start her law office, 
who want have an alternative base on open source to manage their's clients, 
appointments and files.

Resumen
-------
Programa de escritorio destinado a la organización de despachos de abogados
Está orientado a cualquier abogado o despacho de abogados que quiera montar su propio 
despacho pueda tener una aplicación para la gestión de su despacho, basado en software 
libre y no viendose obligado a usar soluciones profesionales que aunque puedan ser más 
completas impliquen un gasto inicial muy elevado.

Maintenance
-----------
Author: Oscar Ramirez Jimenez

Email: tuxskar<at>gmail.com

Installation on Linux
---------------------
Using PyPI:

::

$> pip install ordenley

Alternative installation
........................
As normal python application:

::

$> python setup.py install

Run
---
As the program script is stored into bin you can run it using:

::

> ordenley

Actual version 0.2.1dev Alpha
-----------------------------
This is an improved version and let you manage more complex clients and many to many address and clients

Features
........
- Insert/Modify/Delete clients
- Insert/Modify/Delete address
- Installation easy from PyPI using "pip install ordenley"
- Identifiers for clients and address using id
- No force to use not empty DNI for clients
- Many clients could same address or more than one each one (many to many relation)

Change-log
----------
from 0.1.7dev
    - Clients now could have address
    - Clients identifiers by Id instead of by DNI
    - New client_view GUI with address
    - Reimplemented almos from scratch the code
    - Better structure to add more features as modules
    - New menu in main_view to add and delete client
From 0.1.6dev
    - Renamed package test to tests to run the binary
    - Fixed main_window plot
