import json
import sys
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from mock import patch, Mock

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.test import TestCase, override_settings
from ucamlookup.models import LookupGroup
from ucamlookup.utils import user_in_groups, get_users_from_query, return_visibleName_by_crsid, get_groups_from_query, \
    return_title_by_groupid, get_group_ids_of_a_user_in_lookup, get_institutions, get_institution_name_by_id, \
    validate_crsid_list, validate_groupid_list, get_connection, get_user_lookupgroups, get_users_of_a_group


class UcamLookupOptionsTests(TestCase):

    @override_settings(UCAMLOOKUP_HOST="mock_host", UCAMLOOKUP_PORT=80, UCAMLOOKUP_URL_BASE="/mock",
                       UCAMLOOKUP_CHECK_CERTS=False, UCAMLOOKUP_USERNAME="mock_username",
                       UCAMLOOKUP_PASSWORD="mock_password")
    def test_optional_settings(self):
            conn = get_connection()
            self.assertEqual(conn.host, "mock_host")
            self.assertEqual(conn.port, 80)
            self.assertEqual(conn.url_base, "/mock/")
            self.assertIsNone(conn.ca_certs)
            self.assertEqual(conn.username, "mock_username")
            self.assertEqual(conn.password, "mock_password")


class UcamLookupTests(TestCase):

    def setUp(self):
        # fixture for group 101888
        self.mock_101888 = Mock(groupid='101888', title='CS Information Systems team')
        # fixture for institution UIS
        mock_uis = Mock(instid='UIS')
        mock_uis.name = 'University Information Services'
        # fixture for institution CL
        mock_cl = Mock(instid='CL')
        mock_cl.name = 'Department of Computer Science and Technology'

        # patch the lookup get_connection()
        self.patcher = patch('ucamlookup.utils.get_connection')
        mock_get_connection = self.patcher.start()

        # a mock result returned by invoke_method()
        mock_result = Mock(error=None)

        def side_effect(_, path, path_params, __, ___):
            """
            Side effect method that mocks the lookup connection's invoke_method() and returns a
            mock result.
            """
            try:
                path = path % path_params
            except KeyError:
                pass

            if path == 'api/v1/person/crsid/amc203':
                mock_result.person.visibleName = 'Dr Abraham Martin'
            elif path == 'api/v1/person/crsid/jw35':
                mock_result.person.visibleName = 'John Warbrick'
            elif path == 'api/v1/person/crsid/test0001':
                mock_result.person.visibleName = 'Test User 1'
            elif path == 'api/v1/person/crsid/amc20311':
                mock_result.person = None
            elif path == 'api/v1/group/101888':
                mock_result.group.title = 'CS Information Systems team'
            elif path == 'api/v1/group/101923':
                mock_result.group.title = 'UIS Finance team'
            elif path == 'api/v1/group/001161':
                mock_result.group.title = 'Members of "Magdalene College".'
            elif path == 'api/v1/group/203840928304982':
                mock_result.group = None
            elif path == 'api/v1/person/search':
                mock_result.people = [
                    Mock(visibleName='Dr Abraham Martin', **{'identifier.value': 'amc203'})
                ]
            elif path == 'api/v1/person/crsid/test0001/insts':
                mock_result.institutions = []
            elif path == 'api/v1/person/crsid/amc203/insts':
                mock_result.institutions = [mock_cl]
            elif path == 'api/v1/inst/all-insts':
                mock_result.institutions = [mock_uis, mock_cl]
            elif path == 'api/v1/inst/UIS':
                mock_result.institution.name = mock_uis.name
            elif path == 'api/v1/group/search':
                mock_result.groups = [self.mock_101888]
            elif path == 'api/v1/person/crsid/amc203/groups':
                mock_result.groups = [self.mock_101888]
            elif path == 'api/v1/group/101888/members':
                mock_result.people = [Mock(visibleName='Dr Abraham Martin', identifier='amc203')]
            else:
                self.fail("%s hasn't been mocked" % path)
            return mock_result

        # mock connection returned by get_connectgion()
        mock_connection = Mock()
        mock_connection.invoke_method.side_effect = side_effect

        mock_get_connection.return_value = mock_connection

    def test_add_name_to_user_and_add_title_to_group(self):
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="amc203")
        user1 = User.objects.create_user(username="amc203")
        user2 = User.objects.get(username="amc203")
        self.assertEqual(user1.id, user2.id)
        self.assertEqual(user2.last_name, "Dr Abraham Martin")

        with self.assertRaises(LookupGroup.DoesNotExist):
            LookupGroup.objects.get(lookup_id="101888")
        group1 = LookupGroup.objects.create(lookup_id="101888")
        group2 = LookupGroup.objects.get(lookup_id="101888")
        self.assertEqual(group1.id, group2.id)
        self.assertEqual(group2.name, "CS Information Systems team")
        self.assertEqual(str(group2), "CS Information Systems team (101888)")

    def test_user_in_groups(self):
        amc203 = User.objects.create_user(username="amc203")
        information_systems_group = LookupGroup.objects.create(lookup_id="101888")
        self.assertTrue(user_in_groups(amc203, [information_systems_group]))
        finance_group = LookupGroup.objects.create(lookup_id="101923")
        self.assertFalse(user_in_groups(amc203, [finance_group]))

    def test_get_users_from_query(self):
        results = get_users_from_query("amc203")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['crsid'], "amc203")
        self.assertEqual(results[0]['visibleName'], "Dr Abraham Martin")

        results = get_users_from_query("Abraham Martin")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['crsid'], "amc203")
        self.assertEqual(results[0]['visibleName'], "Dr Abraham Martin")

    def test_return_visibleName_by_crsid(self):
        result = return_visibleName_by_crsid("amc203")
        self.assertEqual(result, "Dr Abraham Martin")
        result = return_visibleName_by_crsid("amc20311")
        self.assertEqual(result, '')

    def test_get_groups_from_query(self):
        results = get_groups_from_query("Information Systems")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['groupid'], "101888")
        self.assertEqual(results[0]['title'], "CS Information Systems team")

    def test_return_title_by_groupid(self):
        result = return_title_by_groupid("101888")
        self.assertEqual(result, "CS Information Systems team")

        with self.assertRaises(ValidationError):
            return_title_by_groupid("203840928304982")

    def test_get_groups_of_a_user_in_lookup(self):
        amc203 = User.objects.create_user(username="amc203")
        information_systems_group = LookupGroup.objects.create(lookup_id="101888")
        amc203_groups = get_group_ids_of_a_user_in_lookup(amc203)
        self.assertIn(information_systems_group.lookup_id, amc203_groups)

    def test_get_institutions(self):
        results = get_institutions()
        self.assertIn(("UIS", "University Information Services"), results)

    def test_get_institutions_with_user(self):
        amc203 = User.objects.create_user(username="amc203")
        results = get_institutions(user=amc203)
        self.assertEquals(("CL", "Department of Computer Science and Technology"), results[0])
        self.assertIn(("UIS", "University Information Services"), results)

    def test_get_institutions_with_non_existant_user(self):
        all_institutions = get_institutions()
        test0001 = User.objects.create_user(username="test0001")
        results = get_institutions(user=test0001)
        self.assertEqual(all_institutions, results)

    def test_get_institution_name_by_id(self):
        result = get_institution_name_by_id(institution_id="UIS")
        self.assertEqual("University Information Services", result)

    def test_get_institution_name_by_id_with_cache(self):
        all_institutions = get_institutions()
        result = get_institution_name_by_id(institution_id="UIS", all_institutions=all_institutions)
        self.assertEqual("University Information Services", result)

    def test_views_without_login(self):
        response = self.client.get(reverse('ucamlookup_find_people'), {'query': 'amc203', 'searchId_u': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        response = self.client.get(reverse('ucamlookup_find_groups'), {'query': 'Information Systems',
                                                                       'searchId_g': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_findpeople_view(self):
        User.objects.create_user(username="amc203", password="test")
        self.assertTrue(self.client.login(username='amc203', password="test"))
        response = self.client.get(reverse('ucamlookup_find_people'), {'query': 'amc203', 'searchId_u': '1'})
        if sys.version_info >= (3, 0):
            jsonresponse = json.loads(response.content.decode('utf-8'))
        else:
            jsonresponse = json.loads(response.content)
        self.assertIn('persons', jsonresponse)
        self.assertIn('searchId_u', jsonresponse)
        self.assertEqual(jsonresponse['searchId_u'], "1")
        self.assertEqual(len(jsonresponse['persons']), 1)
        self.assertEqual(jsonresponse['persons'][0]['visibleName'], "Dr Abraham Martin")
        self.assertEqual(jsonresponse['persons'][0]['crsid'], "amc203")

    def test_findgroups_view(self):
        User.objects.create_user(username="amc203", password="test")
        self.assertTrue(self.client.login(username='amc203', password="test"))
        response = self.client.get(reverse('ucamlookup_find_groups'), {'query': 'Information Systems',
                                                                       'searchId_g': '1'})
        if sys.version_info >= (3, 0):
            jsonresponse = json.loads(response.content.decode('utf-8'))
        else:
            jsonresponse = json.loads(response.content)
        self.assertIn('groups', jsonresponse)
        self.assertIn('searchId_g', jsonresponse)
        self.assertEqual(jsonresponse['searchId_g'], "1")
        self.assertEqual(len(jsonresponse['groups']), 1)
        self.assertEqual(jsonresponse['groups'][0]['groupid'], "101888")
        self.assertEqual(jsonresponse['groups'][0]['title'], "CS Information Systems team")

    def test_validate_crsid_list(self):
        # users do not exist in the DB
        crsid_list = ["amc203", "jw35"]
        user_list = validate_crsid_list(crsid_list)
        self.assertEqual(user_list[0].username, "amc203")
        self.assertEqual(user_list[1].username, "jw35")

        # users exist in the DB
        user_list = validate_crsid_list(crsid_list)
        self.assertEqual(user_list[0].username, "amc203")
        self.assertEqual(user_list[1].username, "jw35")

        user_list = validate_crsid_list([""])
        self.assertEqual(len(user_list), 0)

        user_list = validate_crsid_list(None)
        self.assertEqual(len(user_list), 0)

        with self.assertRaises(ValidationError):
            validate_crsid_list(["kaskvdkam20e9mciasmdimadf"])

    def test_validate_groupid_list(self):
        # users do not exist in the DB
        groupid_list = ["101888", "101923"]
        user_list = validate_groupid_list(groupid_list)
        self.assertEqual(user_list[0].lookup_id, "101888")
        self.assertEqual(user_list[1].lookup_id, "101923")

        # users exist in the DB
        user_list = validate_groupid_list(groupid_list)
        self.assertEqual(user_list[0].lookup_id, "101888")
        self.assertEqual(user_list[1].lookup_id, "101923")

        user_list = validate_groupid_list([""])
        self.assertEqual(len(user_list), 0)

        user_list = validate_groupid_list(None)
        self.assertEqual(len(user_list), 0)

        with self.assertRaises(ValidationError):
            validate_groupid_list(["kaskvdkam20e9mciasmdimadf"])

    def test_validate_groupid_list_leading_zeroes(self):
        """Check that group ids with leading zeroes are correctly validated"""
        user_list = validate_groupid_list(['001161'])
        self.assertEqual(user_list[0].lookup_id, '001161')
        self.assertEqual(user_list[0].name, 'Members of "Magdalene College".')

    def test_get_user_lookupgroups(self):
        amc203 = User.objects.create_user(username="amc203")
        groups = get_user_lookupgroups(amc203)
        # check
        group = next(group for group in groups if group.lookup_id == '101888')
        self.assertEqual(group.name, 'CS Information Systems team')

    def test_get_users_of_a_group(self):
        users = get_users_of_a_group(self.mock_101888)
        # check
        user = next(user for user in users if user.username == 'amc203')
        self.assertEqual(user.last_name, 'Dr Abraham Martin')

    def tearDown(self):
        self.patcher.stop()
