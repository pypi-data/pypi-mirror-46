=============
FSMEDHRO Core
=============

Dies ist die Grundlage für Webseite des Fachschaftsrates der medizinischen
Fakultät der Uni Rostock. Hier wird definiert, was ein ``FachschaftsUser``, ein
``Studiengang``, ein ``Studienabschnitt`` und was ein ``Gender`` ist.

Installation
------------

1. Füge ``fsmedhro_core`` wie folgt zu deinen ``INSTALLED_APPS`` hinzu::

    INSTALLED_APPS = [
        ...
        'fsmedhro_core.apps.FachschaftConfig',
    ]

2. Erzeuge die Models mittels ``python manage.py migrate``

3. Füge das LDAP-Backend zu ``AUTHENTICATION_BACKENDS`` hinzu::

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'fsmedhro_core.backends.auth.LDAPUniRostock',
    ]
