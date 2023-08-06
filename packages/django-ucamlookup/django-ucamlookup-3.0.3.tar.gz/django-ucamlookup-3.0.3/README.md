# Introduction

django-ucamlookup is a library which provides useful methods and templates to integrate your 
[Django](https://www.djangoproject.com/) application with the University of Cambridge University 
[Lookup service](https://www.lookup.cam.ac.uk/). 

## Configuration

The following parameters are optional configurations that you can use in your django settings.

* ``UCAMLOOKUP_HOST``. Optional. Default: ``"www.lookup.cam.ac.uk"``. Specifies the hostname used for the 
IbisClientConnection. This is the connection object that will be used to make all API calls related to lookup.
* ``UCAMLOOKUP_PORT``. Optional. Default: ``443``. Specifies the port used for the 
IbisClientConnection. This is the connection object that will be used to make all API calls related to lookup.
* ``UCAMLOOKUP_URL_BASE``. Optional. Default: ``""``. Specifies the URL base used for the 
IbisClientConnection. This is the connection object that will be used to make all API calls related to lookup.
* ``UCAMLOOKUP_CHECK_CERTS``. Optional. Default: ``True``. Indicates if the client should check if the server side
certificates are valid.
* ``UCAMLOOKUP_USERNAME``. Optional. Default: ``None``. Specifies the username used for the 
IbisClientConnection. This is the connection object that will be used to make all API calls related to lookup. We 
recommend the use of Lookup groups for authentication instead of an individual Raven account.
* ``UCAMLOOKUP_PASSWORD``. Optional. Default: ``None``. Specifies the password used for the 
IbisClientConnection. This is the connection object that will be used to make all API calls related to lookup. We 
recommend the use of Lookup groups passwords for authentication instead of an individual Raven account password.

## Use

Install django-ucamlookup using pip:

```bash
pip install django-ucamlookup
```

Add django-ucamlookup to your installed applications in your project configuration settings.py:

```python
    INSTALLED_APPS=(
    ...
        'ucamlookup', 
    ...
    ),
```

and the urls entries in the urls.py file:

```python
    urlpatterns = patterns(
    ...
        # lookup/ibis urls
        url(r'^ucamlookup/', include('ucamlookup.urls')),
    ...
    )
```

## Warning

Lookup contains personal data of University of Cambridge members. Make sure that you are only showing this data to 
users with rights to see this data.

## Networking

If no optional settings are specified, django-ucamlookup will use ``anonymous`` as username and no password when 
setting up an IbisClientConnection and executing Lookup APIs. This type of anonymous conneciton is only available
inside the Cambridge University Network (CUDN). If your application is deployed outside the CUDN you should use the 
optional authentication with ``UCAMLOOKUP_USERNAME`` and  ``UCAMLOOKUP_PASSWORD``.

We do not recommend the use of individual Raven accounts and instead to set up a Lookup group. Users can generate a 
password for the group and use the group short name as a username for authentication.


## Lookup User

django-ucamlookup modifies a User object each time is going to be saved, either new or update, and assigns to its 
*last_name* property the visible name from lookup for that user. The username is used to search for this user in lookup.

## Lookup Group

django-ucamlookup includes a new model called LookupGroup that it is used to cache lookup models. It is used to store
the lookup group id and its name, and therefore used to reduce the number of call to the lookup service. It can also be
used to create relation with other models. For example, let's say we have a model called Secret and we only want to let
access to it to users inside a certain group or groups. We will create a ManyToMany relation from Secrets to 
LookupGroup.

The name of the group is retrieve from the lookup service each time the group is saved (new or updated). The name is
stored in the *name* property of the class and the id of the lookup group is stored in *lookup_id*.

It is important to say that this model is not used to cache relations between lookup users and lookup groups. These 
relations are always queried to the live lookup service. The model is only used to let the developer make relations
between models that include lookup groups and cache the name of the group.

## Template macros

Two macros are available to be used in a template: `ucamlookup_users`, and `ucamlookup_groups`.
These macros have javascript functions that will tranform an html `select` tag into an interactive
selection control which will interact with the lookup service and will let the user use autocomplete
and search for lookup users and groups.

To include a selection control that can search and add a single or list of users, use the
`ucamlookup_users` macro. You should pass the html `select` `id` as a parameter to the macro.
If you want the control to add more than one user you should set the `multiple` parameter.

```html
    <select id="authors_id" name="authors" multiple="multiple"></select>

    {% include 'ucamlookup_users.html' with input_tag_id="authors_id" multiple=true placeholder='Select an author' %}
```

As seen in the example you can set the placeholder text with `placeholder` parameter.

If you want to show existing `User` records in the input tag you should use the `option` tag in
the template as in the following example:

```html
    <select id="authors_id" name="authors" multiple="multiple">
        {% for user in authors %}
            <option selected=selected value="{{ user.username }}">
                {{user.last_name}} ({{ user.username }})
            </option>
        {% endfor %}
    </select>

    {% include 'ucamlookup_users.html' with input_tag_id="authors_id" multiple=true %}
```

You will also have to include the following macro in the html `header` of your template to load
the js and css files  associated. These macros require jquery if you want to include your own 
jquery library or you are already using it in your template use the parameter `jquery` to specify
it.

```html
    {% include 'ucamlookup_headers.html' with jquery=True %}
```

Your `select` tag will be transform into a selection control that allows the user to search for
users with either using their username or complete name. When the form is submitted, a list of
crsids will be sent with the request as with any normal `select` tag.

If you need to customise the style of the control, you can use the `ucamlookup-user-container`
class for the container part and the `ucamlookup-user-dropdown` class for the dropdown parrt of
the control.

The same approach will also work for lookup groups, as in the following example:

```html
    <select id="groups_id" name="groupids" multiple="multiple">
        {% for group in groups %}
            <option selected=selected value="{{ group.lookup_id }}">
                {{group.name}}
            </option>
        {% endfor %}
    </select>
    
    {% include 'ucamlookup_groups.html' with input_tag_id="groups_id" multiple="true" %}
```

## Admin interface

The admin interface is tunned to add managing options for the LookupGroup model. The **add** option will show the same
ajax-lookup-integrated-input as the template macros described above.

It also changes the add form for the user and it also shows an interactive ajax lookup-integrated input form when the
admin wants to add a new user to the app.

These input forms allow to search for name and crsid in the case of a new user and for name in the case of a lookup 
group.


## Available functions

The module also provides some useful functions to use in your app that do all the calls to the lookup service needed.

`get_group_ids_of_a_user_in_lookup(user)`: Returns the list of group ids of a user

`user_in_groups(user, lookup_groups)`: Check in the lookup webservice if the user is member of any of the groups in the 
LookupGroup list passed by parameter. Returns True if the user is in any of the groups or False otherwise

`get_institutions(user=None)`: Returns the list of institutions using the lookup ucam service. The institutions of 
the user passed by parameters will be shown first in the list returned

`validate_crsid_list(crsids)`: It receives a list of crsids (from the `select` tag from the
template macros described previously) and returns a list of `User` objects corresponding to the
crsids passed.

`get_or_create_user_by_crsid(crsid)`: Returns the `User` object corresponding to the `crsid` 
passed. If it does not exists in the database, it is created.

`validate_groupid_list(groupids)`: It receives a list of groupids (from the `select` tag from the
template macros described previously) and returns a list of `LookupGroup` objects corresponding to
the crsids passed.

`get_or_create_group_by_groupid(groupid)`: Returns the `LookupGroup` object corresponding to the
`groupid` passed. If it does not exists in the database, it is created.

`get_institution_name_by_id(institution_id, all_institutions=None)`: Returns the name of an institution by the id 
passed. If all_institutions is passed (the result from get_institutions) then the search is done locally using this 
list instead of a lookup call.

The last two methods can be used to add institutions to a model and show the name instead of the code in the admin 
interface 

```python
class MyModelAdmin(ModelAdmin):
    all_institutions = get_institutions()
    
    model = MyModel
    list_display = ('institution', )
    list_filter = ('institution_id', )

    def institution(self, obj):
        return get_institution_name_by_id(obj.institution_id, self.all_institutions)
        
    institution.admin_order_field = 'institution_id'
```

# Developing

## Run tests

Tox is configured to run on a container with a matrix execution of different versions of python and django combined.
It will also show the coverage and any possible PEP8 violations.

```shell
$ docker-compose up
```
