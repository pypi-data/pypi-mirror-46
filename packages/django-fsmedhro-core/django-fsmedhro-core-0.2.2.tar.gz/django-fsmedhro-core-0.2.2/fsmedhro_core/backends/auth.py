import logging
from ldap3 import Server, Connection, ALL_ATTRIBUTES
from django.contrib.auth import get_user_model
from django.contrib import messages

logger = logging.getLogger(__name__)
UserModel = get_user_model()


class LDAPUniRostock:
    HOST = 'ldaps://ldap.uni-rostock.de'
    BASE_DN = 'ou=people,o=uni-rostock,c=de'
    server = Server(HOST)

    def authenticate(self, request, username, password):
        username = username.lower()
        uid_qualifier = 'uid={}'.format(username)
        user_dn = uid_qualifier + ',' + self.BASE_DN

        conn = Connection(self.server, user_dn, password)

        """
        Für die Authentifizierung versuchen wir uns hier an den LDAP-Server
        zu binden. Wenn es hierbei keine Exception gibt, dann ist der
        Benutzer gültig.
        """
        bind_succesful = conn.bind()

        if bind_succesful:
            """
            Wenn wir uns erfolgreich binden konnten, dann holen wir uns vom
            LDAP-Server alle Informationen um unseren eigenen Nutzer zu
            befüllen.
            """
            uid_search_term = '({})'.format(uid_qualifier)
            conn.search(
                self.BASE_DN,
                uid_search_term,
                attributes=ALL_ATTRIBUTES
            )
            ldap_user = conn.entries[0]
        else:
            messages.warning(
                request,
                'Authentifizierung bei der Uni fehlgeschlagen – '
                'bitte überprüfe dein Kürzel und Passwort.'
            )
            return None

        conn.unbind()

        if self.is_valid(ldap_user):
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                """
                Wenn der Benutzer noch nicht existiert, dann erstellen wir
                einen:
                """
                user = UserModel(
                    username=ldap_user.uid.value,
                    password='DummyPassword',
                    is_staff=False,
                    is_superuser=False,
                )

                user.set_unusable_password()

                user.save()

            if user.is_active:
                user.email = ldap_user.mail.value
                user.first_name = ldap_user.givenName.value
                user.last_name = ldap_user.sn.value

                user.save()

            return user
        else:
            messages.warning(
                request,
                'Heute leider nur für <del>Stammgäste</del> '
                'Studenten der med. Faktultät.'
            )
            return None

    def is_valid(self, ldap_user):
        """
        Es werden nur Studenten von der Medizinischen Fakultät akzeptiert.
        """
        ldap_auth_filter = {
            'employeeType': 's',
            'uniRFaculty': '03',
            'gidNumber': '97'
        }

        for key, value in ldap_auth_filter.items():
            if ldap_user[key].value != value:
                return False
        else:
            return True

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
