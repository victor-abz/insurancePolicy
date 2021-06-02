# -*- coding: utf-8 -*-
# Copyright (c) 2021, Abizeyimana Victor and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from requests import request


@frappe.whitelist(allow_guest=True)
def get_insurance_policy():
    responseString = request(
        'GET', 'https://ratingqa.itcdataservices.com/Webservices/ITCRateEngineAPI/api/objectsamples/ITCRateEngineRequest?useacord=true', verify=False)

    res = responseString.json()
    print(res, res.keys())

    new_policy = frappe.new_doc('insurancePolicyTemplate')
    new_policy.data = json.dumps(res)
    new_policy.insert(ignore_permissions=True)

    frappe.db.commit()

    return f'Succesful created policy>>>> {new_policy.name}'
