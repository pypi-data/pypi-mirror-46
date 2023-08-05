oneplatform-sdk-python
======================

|OnePlatform Mascot|

|PyPI version|

Python SDK สำหรับ API OnePlatform

เกี่ยวกับ OnePlatform API
-------------------------

See the official API documentation for more information.
ติดตามคู่มือการใช้งาน Official API และข้อมูลอื่นๆ ได้ที่ https://api.one.th/docs

การติดตั้ง
----------

.. code:: bash

    $ pip install pyoneplatform

ตัวอย่างการใช้งาน
-----------------

Usage:

.. code:: python

    from oneplatform.oneid import OneIDApi

    one_id_api = OneIDApi(
        client_id="_YOUR_CLIENT_ID_",
        client_secret="_YOUR_CLIENT_SECRET_",
        ref_code="_YOUR_REF_CODE_"
    )

    try:
        r = one_id_api.login("_USERNAME_", "_PASSWORD_")
        for k in r:
            key = "{}".format(k).ljust(50)
            print("{}: {}".format(key, r[k]))
    except Exception as e:
        print("Login failed: ", e)
        exit(1)

Platform service list:
----------------------

* One ID:
    * Login with username and password
    * Get profile
    * Verify authorization code
    * Refresh token
    * Generate login link

API
---

OneIDApi
~~~~~~~~

\_\_init\_\_(self, client\_id, client\_secret, ref\_code, endpoint='https://one.th', timeout=5)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

สร้างตัวแปรสำหรับ OneIDApi

.. code:: python

    one_id_api = OneIDApi('_CLIENT_ID_', '_CLIENT_SECRET_', '_REF_CODE_')

คุณสามารถเปลี่ยนค่า ``endpoint`` และ ``timeout`` ได้ตามค่าที่คุณต้องการ

login(self, username, password)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Login เข้าสู่ระบบโดยใช้ One ID และคืนค่า Token และ Information ของ user มาให้

.. code:: python

    one_id_api.login('_USERNAME_', '_PASSWORD_')

ตัวอย่าง Response

.. code:: json

    {
        "token_type": "Bearer",
        "expires_in": 86400,
        "access_token": "_ACCESS_TOKEN_",
        "refresh_token": "_REFRESH_TOKEN_",
        "account_id": "_ACCOUNT_ID_",
        "result": "Success",
        "username": "_USERNAME_"
    }

refresh\_token(self, refresh\_token)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Renew Access token ใหม่หลังจากที่ Access token หมดอายุ โดยใช้ Refresh token ที่ให้มาตั้งแต่ตอน Login

.. code:: python

    one_id_api.refresh_token('_REFRESH_TOKEN_')

ตัวอย่าง Response

.. code:: json

    {
        "token_type": "Bearer",
        "expires_in": 86400,
        "access_token": "_ACCESS_TOKEN_",
        "refresh_token": "_REFRESH_TOKEN_",
        "account_id": "_ACCOUNT_ID_",
        "result": "Success",
        "username": "_USERNAME_"
    }

verify\_authorize\_code(self, authorize\_code, redirect\_url=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ใช้กับการ Authentication แบบ OAuth2 เป็น API ไว้สำหรับส่ง Authorization code ไปตรวจสอบกับ One ID

.. code:: python

    one_id_api.verify_authorize_code('_AUTHORIZATION_CODE_')

สามารถใส่ค่า ``redirect_url`` ได้ตามต้องการ

ตัวอย่าง Response

.. code:: json

    {
        "token_type": "Bearer",
        "expires_in": 86400,
        "access_token": "_ACCESS_TOKEN_",
        "refresh_token": "_REFRESH_TOKEN_",
        "account_id": "_ACCOUNT_ID_",
        "result": "Success",
        "username": "_USERNAME_"
    }

get\_profile(self, access\_token)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ใช้ในการดึงค่า Profile ของ user นั้นๆ โดยจะต้องใช้ Access token ที่ได้จากการ Login เสมอ

.. code:: python

    one_id_api.get_profile('_ACCESS_TOKEN_')

ตัวอย่าง Response

.. code:: json

    {
        "id": "_ACCOUNT_ID_",
        "first_name_th": null,
        "last_name_th": null,
        "first_name_eng": null,
        "last_name_eng": null,
        "account_title_th": null,
        "account_title_eng": null,
        "id_card_type": "ID_CARD",
        "id_card_num": "DUMMY",
        "hash_id_card_num": "ceec12762e66397b56dad64fd270bb3d694c78fb9cd665354383c0626dbab013",
        "account_category": "Residential",
        "account_sub_category": "Thai",
        "thai_email": "_DEFAULT_THAI_EMAIL_",
        "thai_email2": null,
        "status_cd": "Active",
        "birth_date": null,
        "status_dt": "2019-05-02 16:46:26",
        "register_dt": "2019-05-02 16:46:26",
        "address_id": null,
        "created_at": "2019-05-02 16:46:26",
        "created_by": "OPENID_USR",
        "updated_at": "2019-05-02 16:46:26",
        "updated_by": "OPENID_USR",
        "reason": null,
        "tel_no": null,
        "name_on_document_th": null,
        "name_on_document_eng": null,
        "mobile": [
            {
                "id": "277d6e20-6cbf-11e9-babc-15a0f81e7cb5",
                "mobile_no": "_MOBILE_NUMBER_",
                "created_at": "2019-05-02 16:46:26",
                "created_by": "OPENID_USR",
                "updated_at": "2019-05-02 16:46:26",
                "updated_by": "OPENID_USR",
                "deleted_at": null,
                "pivot": {
                    "account_id": "_ACCOUNT_ID_",
                    "mobile_id": "277d6e20-6cbf-11e9-babc-15a0f81e7cb5",
                    "created_at": "2019-05-02 16:46:26",
                    "updated_at": "2019-05-02 16:46:26",
                    "status_cd": "Active",
                    "primary_flg": "Y",
                    "mobile_confirm_flg": null,
                    "mobile_confirm_dt": null
                }
            }
        ],
        "email": [
            {
                "id": "277793e0-6cbf-11e9-a6f2-55c5066f0181",
                "email": "_DEFAULT_THAI_EMAIL_",
                "created_at": "2019-05-02 16:46:26",
                "created_by": "OPENID_USR",
                "updated_at": "2019-05-02 16:46:26",
                "updated_by": "OPENID_USR",
                "deleted_at": null,
                "pivot": {
                    "account_id": "_ACCOUNT_ID_",
                    "email_id": "277793e0-6cbf-11e9-a6f2-55c5066f0181",
                    "created_at": "2019-05-02 16:46:26",
                    "updated_at": "2019-05-02 16:46:26",
                    "status_cd": "Active",
                    "primary_flg": "Y",
                    "email_confirm_flg": null,
                    "email_confirm_dt": null
                }
            }
        ],
        "address": [],
        "account_attribute": [],
        "status": "data not complete",
        "last_update": "2019-05-02 16:46:26"
    }

get\_login\_link(self)
^^^^^^^^^^^^^^^^^^^^^^

เมื่อต้องการดึงค่า Login url สำหรับใช้ในการ Login

.. code:: python

    one_id_api.get_login_link()

ตัวอย่าง Link URL ที่ได้จากการเรียก Function

.. code:: text

    https://one.th/api/oauth/getcode?client_id=<_CLIENT_ID_>&response_type=code&scope=

สามารถ Return redirect ด้วย code 302 ไปยัง link ที่ได้ generate ออกมา และระบบของ OneID จะ redirect ไปยังหน้าให้กรอก Username/Password

|Login Form|

OneChatApi
^^^^^^^^^^

https://chat-develop.one.th/docs

Requirements
------------

-  Python >= 2.7 or >= 3.4

For SDK developers
------------------

First install for development.

::

    $ pip install -r requirements-dev.txt


Changelog
=========

Version 0.1.1 (2019-05-07)
--------------------------

* Fixed One ID version with main lib
* Clear .idea folder
* Fix http client for support python v2.7 and v3.7
* Fixed incorrect readme

Version 0.1.0 (2019-05-03)
---------------------------

* First release after prepare library
* Platform service compatibility:
    * One ID:
        * Login with username and password
        * Get profile
        * Verify authorization code
        * Refresh token
        * Generate login link

.. |PyPI version| image:: https://badge.fury.io/py/pyoneplatform.svg
   :target: https://badge.fury.io/py/pyoneplatform
.. |Login Form| image:: https://monitor.sdi.one.th/imagik/bj60vbqtpnstbpk7nhs0
.. |OnePlatform Mascot| image:: https://monitor.sdi.one.th/imagik/bj612eatpnstbpk7nhsg
