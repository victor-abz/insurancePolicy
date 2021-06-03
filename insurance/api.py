# -*- coding: utf-8 -*-
# Copyright (c) 2021, Abizeyimana Victor and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from xmltodict import unparse, parse
from requests import request
from xml.etree import ElementTree as ET


@frappe.whitelist(allow_guest=True)
def get_insurance_policy():
    responseString = request(
        'GET', 'https://ratingqa.itcdataservices.com/Webservices/ITCRateEngineAPI/api/objectsamples/ITCRateEngineRequest?type=xml&useacord=true', verify=False)

    # res = responseString.json()
    # print(res, res.keys())

    xml_parsed_response = json.dumps(parse(responseString.text), indent=4)
    json_response = json.loads(xml_parsed_response)

    # xml_parsed_response = xml_to_dict(responseString.text)

    # json_response = ET.XML(responseString.text)
    # xmldict = XmlDictConfig(json_response)

    new_policy = frappe.new_doc('insurancePolicyTemplate')
    new_policy.data = xml_parsed_response
    new_policy.insert(ignore_permissions=True)

    frappe.db.commit()

    return json_response


# class XmlListConfig(list):
#     def __init__(self, aList):
#         for element in aList:
#             if element:
#                 # treat like dict
#                 if len(element) == 1 or element[0].tag != element[1].tag:
#                     self.append(XmlDictConfig(element))
#                 # treat like list
#                 elif element[0].tag == element[1].tag:
#                     self.append(XmlListConfig(element))
#             elif element.text:
#                 text = element.text.strip()
#                 if text:
#                     self.append(text)

# # from: http://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary-in-python

# class XmlDictConfig(dict):
#     def __init__(self, parent_element):
#         if parent_element.items():
#             self.update(dict(parent_element.items()))
#         for element in parent_element:
#             if element:
#                 if len(element) == 1 or element[0].tag != element[1].tag:
#                     aDict = XmlDictConfig(element)
#                 else:
#                     aDict = {element[0].tag: XmlListConfig(element)}
#                 if element.items():
#                     aDict.update(dict(element.items()))
#                 self.update({element.tag: aDict})
#             elif element.items():
#                 self.update({element.tag: dict(element.items())})
#             else:
#                 self.update({element.tag: element.text})


# def xml_to_dict(xml):

#     if len(xml) == 0:
#         if xml.text:
#             return xml.text.strip()
#         else:
#             return None
#     else:
#         return_dict = dict()
#         for i in range(0, len(xml)):
#             if return_dict.get(xml[i].tag, False):
#                 if isinstance(return_dict[xml[i].tag], list):
#                     return_dict[xml[i].tag].append(xml_to_dict(xml[i]))
#                 else:
#                     temp = return_dict[xml[i].tag]
#                     return_dict[xml[i].tag] = []
#                     return_dict[xml[i].tag].append(temp)
#                     return_dict[xml[i].tag].append(xml_to_dict(xml[i]))
#             else:
#                 return_dict[xml[i].tag] = xml_to_dict(xml[i])
#         return return_dict
