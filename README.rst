Project Short Description

    Build a solution to demonstrate your ability to use a Web Framework.  This task must be developed in Python and
    should have sufficient documentation to understand your answer without asking you.

    This solution makes use of the Reahl Framework (reahl.org).  Reahl comprises a number of projects that help with the development
    of interactive web applications.

    ``Reahl-web`` is a web application framework that allows a programmer to work in terms of useful abstractions – using
    a single programming language. The details of how those abstractions are implemented using several different web
    technologies are hidden and dealt with for the programmer.

    ``Reahl-component`` provides infrastructure for components in any application that can also have their own database
    schemas, configuration, internationalisation and more.

=============
Prerequisites
=============

1.  Python 3.8
2.  Reahl 6.0

============
Installation
============


This project is configured to run in a virtual environment.  For more installation Follow the following steps to install teh environment:

1. Go to the directory where you wnt to clone the project i.e. ~./myprojects and clone the project.

.. code-block:: bash

    $ cd ~./myprojects
    $ git clone https://github.com/hendrikdutoit/reahlbalancesheet.git


2. Create a virtual environment.  Ensure you have the latest pip with wheel support and install a virtualenv using wheels:

.. code-block:: bash

    $ python -m pip install -U pip
    $ pip install -U virtualenv
    $ python -m venv ./reahl_env
    $ source ./reahl_env/bin/activate


3. Install Reahl in the virtualenv.  With your virtualenv activated, install Reahl:

.. code-block:: bash

    $ pip install --upgrade -r requirements.txt
    $ pip install reahl[declarative,sqlite,dev,doc]


4. Initialize the database.  Make sure you are in the ~./myprojects/reaahlbalancesheet directory:

.. code-block:: bash

    $ pip install --no-deps -e .
    $ reahl createdbuser etc
    $ reahl createdb etc
    $ reahl createdbtables etc


5. Start the Reahl local server and browse to http://localhost:8000

.. code-block:: bash

    $ reahl serve etc


=====
Usage
=====

1. Use the Navigation Bar at the top to select the action you want to take:

    - ``Show`` - Show all the customers in the database
    - ``Add`` - Add a customer
    - ``Graph`` - Show the graph of the last person that was added to the database.

2. ``Show`` menu option

    - Display the current users in the database

3. ``Add`` menu option

    - Enter Surname, Name and Date of Birth for the user.
    - Choose a file that contains the income and expenditure for the customer.
    - Click on ``Save`` to save the customer detail.
    - There is asample data file in the ./data directory.
    - All fields are mandatory.

4. ``Graph`` menu option

    - The graph of the income and expenditure of the last person added to the database will be displayed.
    - Use the browser ``<back>`` button to go back to the previous screen or select an option form the Navigation Bar.

===============================
Considerations and Constraints
===============================

1. The data file must be an Excel file.
2. The Excel file must have the following headers on row 1

    - Column A: ``Month``
    - Column B: ``Income``
    - Column C: ``Expences``

3. The data in the sheet must be in the ranges as in 2 above.
4. The data file is not checked and assume a, Excel file.  Loading a non-Excel file will have unexpected results.
