## YetiForce CRM Python API Wrapper

#### Description

This is a lightweight API Wrapper for YetiForce REST services.

#### Installation:

`pip install yetiforce-python`


#### Usage:

##### Login:
```python
>>> from yetiforce_python import YetiForceAPI
>>> api = YetiForceAPI(
>>>     url='http(s)://<hostname>',  # settings->integration->webservice applications
>>>     ws_user='<webservice name>', 
>>>     ws_pass='<webservice passcode>', 
>>>     ws_key='<webservice API key>', 
>>>     username='<user's name>', 
>>>     password='<user's password>'
>>>     )
>>> api.login()
{'language': True,
 'lastLoginTime': '2019-03-19 12:57:02',
 'lastLogoutTime': None,
 'logged': True,
 'name': None,
 'parentName': None,
 'preferences': {'activity_view': 'This Month',
                 'conv_rate': '1.00000',
                 'currency_code': 'EUR',
                 'currency_decimal_separator': '.',
                 'currency_grouping_pattern': '123,456,789',
                 'currency_grouping_separator': ' ',
                 'currency_id': 1,
                 'currency_name': 'Euro',
                 'currency_symbol': '€',
                 'currency_symbol_placement': '1.0$',
                 'date_format': 'yyyy-mm-dd',
                 'date_format_js': 'Y-m-d',
                 'dayoftheweek': 'Monday',
                 'end_hour': '16:00',
                 'hour_format': '24',
                 'no_of_currency_decimals': 2,
                 'start_hour': '08:00',
                 'time_zone': 'Europe/Warsaw',
                 'truncate_trailing_zeros': 0},
 'type': 1}
```

##### Get modules:
````python
>>> api.list_modules()
{'Accounts': 'Accounts',
 'ActivityRegister': 'Activity Register',
 'Announcements': 'Announcements',
  
  ...
  
}
````

##### Get objects:
```python
>>> api.Leads.get_list(){'count': 1,
 'headers': {'assigned_user_id': 'Assigned To',
             'company': 'Lead name',
             'email': 'Primary email',
             'lastname': 'Short name',
             'phone': 'Primary phone',
             'website': 'Website'},
 'isMorePages': False,
 'records': {'115': {'assigned_user_id': 'Administrator',
                     'company': 'Some Company',
                     'email': 'info@company.com',
                     'phone': '+48 12 234 345',
                     'recordLabel': 'Some Company',
                     'website': 'https://www.company.com'}}}
                     
>>> api.Leads.get(115)
{'data': {'active': 'Yes',
          
          ...
          
          'website': 'http://www.company.com'},
 'fields': {'active': 'Active',
 
            ...
             
            'website': 'Website'},
 'id': 115,
 'inventory': False,
 'name': 'Some Company'}
```