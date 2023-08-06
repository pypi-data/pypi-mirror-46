import re

from django.conf import settings
from django.core.exceptions import ValidationError
from ucamlookup.ibisclient import PersonMethods, GroupMethods, IbisException, InstitutionMethods, \
    IbisClientConnection


def get_connection():
    UCAMLOOKUP_HOST = getattr(settings, "UCAMLOOKUP_HOST", "www.lookup.cam.ac.uk")
    UCAMLOOKUP_PORT = getattr(settings, 'UCAMLOOKUP_PORT', 443)
    UCAMLOOKUP_URL_BASE = getattr(settings, 'UCAMLOOKUP_URL_BASE', "")
    UCAMLOOKUP_CHECK_CERTS = getattr(settings, 'UCAMLOOKUP_CHECK_CERTS', True)
    UCAMLOOKUP_USERNAME = getattr(settings, 'UCAMLOOKUP_USERNAME', None)
    UCAMLOOKUP_PASSWORD = getattr(settings, 'UCAMLOOKUP_PASSWORD', None)

    conn = IbisClientConnection(UCAMLOOKUP_HOST, UCAMLOOKUP_PORT, UCAMLOOKUP_URL_BASE, UCAMLOOKUP_CHECK_CERTS)

    if UCAMLOOKUP_USERNAME:
        conn.set_username(UCAMLOOKUP_USERNAME)

    if UCAMLOOKUP_PASSWORD:
        conn.set_password(UCAMLOOKUP_PASSWORD)

    return conn


def get_users_from_query(search_string):
    """ Returns the list of people based on the search string using the lookup ucam service
        :param search_string: the search string
    """
    persons = PersonMethods(get_connection()).search(query=search_string)

    return list(map((lambda person: {'crsid': person.identifier.value, 'visibleName': person.visibleName}), persons))


def return_visibleName_by_crsid(crsid):
    person = PersonMethods(get_connection()).getPerson(scheme='crsid', identifier=crsid)
    return person.visibleName if person is not None else ''


def get_groups_from_query(search_string):
    """ Returns the list of groups based on the search string using the lookup ucam service
        :param search_string: the search string
    """
    groups = GroupMethods(get_connection()).search(query=search_string)

    return list(map((lambda group: {'groupid': group.groupid, 'title': group.title}), groups))


def return_title_by_groupid(groupid):
    group = GroupMethods(get_connection()).getGroup(groupid=groupid)
    if group is None:
        raise ValidationError("The group with id %(groupid)s does not exist in Lookup", code='invalid',
                              params={'groupid': groupid},)
    return group.title if group is not None else ''


def get_group_ids_of_a_user_in_lookup(user):
    """ Returns the list of groups of a user in the lookup service
    :param user: the user
    :return: the list of group_ids
    """
    try:
        group_list = PersonMethods(get_connection()).getGroups(scheme="crsid", identifier=user.username)
        return list(map(lambda group: group.groupid, group_list))
    except IbisException:
        return []


def get_or_create_group_by_groupid(groupid):
    """ Returns the django LookupGroup object corresponding to the groupid parameter.
        :param crsid: the groupid of the retrieved group
    """
    from ucamlookup.models import LookupGroup
    groupidstr = str(groupid)
    group = LookupGroup.objects.filter(lookup_id=groupidstr)
    if group.exists():
        group = group.first()
    else:
        group = LookupGroup.objects.create(lookup_id=groupidstr)
    return group


def get_user_lookupgroups(user):
    """ Returns the list of lookup groups of a user
    :param user: the User
    :return: the list of LookupGroups
    """
    try:
        group_list = PersonMethods(get_connection()).getGroups(scheme="crsid", identifier=user.username)
        return list(map(lambda group: get_or_create_group_by_groupid(group.groupid), group_list))
    except IbisException:
        return []


def get_institutions(user=None):
    """ Returns the list of institutions using the lookup ucam service. The institutions of the user doing
    the request will be shown first
        :param user: the user doing the request
    """

    all_institutions = InstitutionMethods(get_connection()).allInsts(includeCancelled=False)
    # filter all the institutions that were created for store year students
    all_institutions = list(filter(lambda institution: re.match(r'.*\d{2}$', institution.instid) is None,
                                   all_institutions))

    if user is not None:
        try:
            all_institutions = PersonMethods(get_connection()).getInsts("crsid", user.username) + all_institutions
        except IbisException:
            pass

    return list(map((lambda institution: (institution.instid, institution.name)), all_institutions))


def get_institution_name_by_id(institution_id, all_institutions=None):
    if all_institutions is not None:
        instname = next((institution[1] for institution in all_institutions if institution[0] == institution_id), None)
    else:
        institution = InstitutionMethods(get_connection()).getInst(instid=institution_id)
        instname = institution.name if institution is not None else None

    return instname if instname is not None else 'This institution no longer exists in the database'


def user_in_groups(user, lookup_groups):
    """ Check in the lookup webservice if the user is member of any of the groups given
    :param user: the User
    :param lookup_groups: the list of LookupGroups
    :return: True if the user belongs to any of the groups or False otherwise
    """

    user_group_list = get_group_ids_of_a_user_in_lookup(user)
    groups = list(filter(lambda group: group.lookup_id in user_group_list, lookup_groups))
    if len(groups) > 0:
        return True
    else:
        return False


def get_or_create_user_by_crsid(crsid):
    """ Returns the django user corresponding to the crsid parameter.
        :param crsid: the crsid of the retrieved user
    """
    from django.contrib.auth.models import User
    user = User.objects.filter(username=crsid)
    if user.exists():
        user = user.first()
    else:
        user = User.objects.create_user(username=crsid)

    return user


def validate_crsids(crsids_text):
    """
    Validates a comma seperated list of crsids returning a list of User objects

    .. deprecated:: 3.0.0

    validate_crsid_list() should now be used in conjunction with the <select> element.

    :param crsids_text: a comma seperated list of crsids
    :return: The list of User objects
    """
    if crsids_text is None:
        return ()

    return validate_crsid_list(crsids_text.split(','))


def validate_crsid_list(crsids):
    """
    Validates the list of crsids returning a list of User objects

    :param crsids: list of crsids
    :return: The list of User objects
    """
    users = ()

    if crsids is None:
        return users

    if len(crsids) == 1 and crsids[0] == '':
        return users

    crsid_re = re.compile(r'^[a-z][a-z0-9]{3,7}$')
    for crsid in crsids:
        if crsid_re.match(crsid):
            users += (get_or_create_user_by_crsid(crsid),)
        else:
            raise ValidationError("The list of users contains an invalid user: {}".format(crsid))

    return users


def get_users_of_a_group(group):
    """ Returns the list of users of a LookupGroup
    :param group: The LookupGroup
    :return: the list of Users
    """

    return list(map(lambda user: get_or_create_user_by_crsid(user.identifier),
                    GroupMethods(get_connection()).getMembers(groupid=group.groupid)))


def validate_groupids(groupids_text):
    """
    Validates a comma seperated list of groupids returning a list of LookupGroup objects

    .. deprecated:: 3.0.0

    validate_groupid_list() should now be used in conjunction with the <select> element.

    :param crsids_text: a comma seperated list of groupids
    :return: The list of LookupGroup objects
    """
    if groupids_text is None:
        return ()

    return validate_groupid_list(groupids_text.split(','))


def validate_groupid_list(groupids):
    """
    Validates a comma seperated list of groupids returning a list of LookupGroup objects

    :param crsids_text: a list of groupids
    :return: The list of LookupGroup objects
    """
    groups = ()

    if groupids is None:
        return groups

    if len(groupids) == 1 and groupids[0] == '':
        return groups

    groupid_re = re.compile(r'^[0-9]{1,6}$')

    for groupid in groupids:
        if groupid_re.match(groupid):
            groups += (get_or_create_group_by_groupid(groupid),)
        else:
            raise ValidationError("The list of groups contains an invalid group")

    return groups
