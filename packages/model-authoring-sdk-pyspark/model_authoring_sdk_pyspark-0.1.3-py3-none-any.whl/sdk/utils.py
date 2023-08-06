'''
 * ADOBE CONFIDENTIAL
 * ___________________
 *
 *  Copyright 2017 Adobe Systems Incorporated
 *  All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Adobe Systems Incorporated and its suppliers,
 * if any.  The intellectual and technical concepts contained
 * herein are proprietary to Adobe Systems Incorporated and its
 * suppliers and are protected by all applicable intellectual property
 * laws, including trade secret and copyright laws.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Adobe Systems Incorporated.
'''

from .exceptions import MLRuntimeException

def create_instance(module, map, class_name_key, clazz):
    specified_class = map.get(class_name_key)
    found_clazz_ = getattr(module, specified_class)

    if not issubclass(found_clazz_, clazz):
        raise MLRuntimeException(
            "{subclass} is not a subclass of {parent}".format(
                subclass=found_clazz_, parent=clazz))

    instance = found_clazz_()
    return instance
