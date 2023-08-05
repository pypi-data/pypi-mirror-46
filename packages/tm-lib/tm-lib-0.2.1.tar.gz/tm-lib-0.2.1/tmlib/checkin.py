"""
Function _update_last_checkin(string minion_name, string symbol, string broker, number account_number):
# Update the appropriate mongodb node with the current timestamp.
# if the node exists – update it – if not, create it.

return true/false (success/fail)
Notes:
The combination of Broker Name + account number is unique, and can be used to identify the document.

"""
import logging
from datetime import datetime

from connexion import NoContent
from mongoengine import Q

from tmlib.models import Checkin, Customer, License, Registration

logger = logging.getLogger()


def update_last_checkin_view(account_number, broker_name, minion_name, symbol, computer_name=None,
                             minion_version=None, minion_edition=None, current_lots=None, live_trading_status=None):
    """
        Update the appropriate mongodb node with the current timestamp.
        if the node exists – update it – if not, create it.
        :param minion_name:
        :param symbol:
        :param broker_name:
        :param account_number:
        :param computer_name:
        :param minion_version:
        :param minion_edition:
        :param current_lots:
        :param live_trading_status:
        :return: true/false (success/fail)
    """
    status = 404
    try:
        customer: Customer = Customer.objects.get(
            (Q(licenses__account_registrations__account_number=account_number) &
             Q(licenses__account_registrations__broker=broker_name))
        )
    except Customer.DoesNotExist:
        return NoContent, status  # item not found

    except Customer.MultipleObjectsReturned:
        logger.error(
            'Multiple object is returned for the account_number: %s and broker: %s',
            account_number, broker_name
        )
        return NoContent, status
    account_license: License = next(
        (l for l in customer.licenses if l.minion_name == minion_name),
    )
    # license doesn't exist
    if not account_license:
        return NoContent, status

    account_registration: Registration = next(
        (r for r in account_license.account_registrations if r.account_number == account_number),
        None
    )
    # account doesn't exist
    if not account_registration:
        return NoContent, status

    checkin: Checkin = next(
        (c for c in account_registration.checkins if c.broker == broker_name and c.symbol == symbol), None
    )
    if checkin:
        # update query
        status = 200
        checkin.last_checkin = datetime.now()
        checkin.computer_name = computer_name
        checkin.minion_version = minion_version
        checkin.minion_edition = minion_edition
        checkin.current_lots = current_lots
        checkin.live_trading_status = live_trading_status
    else:
        # add query
        status = 201
        account_registration.checkins.append(
            Checkin(
                symbol=symbol, broker=broker_name, last_checkin=datetime.now(),
                computer_name=computer_name, minion_version=minion_version,
                minion_edition=minion_edition, live_trading_status=live_trading_status,
                current_lots=current_lots
            )
        )
    customer.save()
    return NoContent, status


def get_last_checkins_json_view():
    """
        Get users with the last checkin information.
        :return: a generator with dicts.
    """
    # prepare response

    status = 200  # only 200 status is possible
    # response structure
    pipeline = [
        # pre filter values
        {"$match": {"licenses.account_registrations.checkins": {"$exists": True}}},
        # extract embedded docs
        {"$unwind": "$licenses"},
        {"$unwind": "$licenses.account_registrations"},
        {"$unwind": "$licenses.account_registrations.checkins"},
        # sort data to get the last checkin first
        {"$sort": {"licenses.account_registrations.checkins.last_checkin": -1}},
        # group by data and get only last one
        {
            "$group":
                {
                    "_id": "$_id",
                    "given_name": {"$first": "$given_name"},
                    "surname": {"$first": "$surname"},
                    "login": {"$first": "$login"},
                    "account": {"$first": "$licenses.account_registrations.account_number"},
                    "broker_name": {"$first": "$licenses.account_registrations.broker"},
                    "minion_name": {"$first": "$licenses.minion_name"},
                    "last_checkin": {"$first": "$licenses.account_registrations.checkins.last_checkin"},
                    "computer_name": {"$first": "$licenses.account_registrations.checkins.computer_name"},
                    "minion_edition": {"$first": "$licenses.account_registrations.checkins.minion_edition"},
                    "minion_version": {"$first": "$licenses.account_registrations.checkins.minion_version"},
                    "current_lots": {"$first": "$licenses.account_registrations.checkins.current_lots"},
                    "live_trading_status": {"$first": "$licenses.account_registrations.checkins.live_trading_status"},
                }
        },
        # configure fields for the response
        {"$project": {
            "_id": 0,
            "given_name": 1,
            "surname": 1,
            "login": 1,
            "account": 1,
            "minion_name": 1,
            "last_checkin": 1,
            "computer_name": 1,
            "minion_edition": 1,
            "minion_version": 1,
            "current_lots": 1,
            "live_trading_status": 1,
            "broker_name": 1,
        }},
        # sort final data
        {"$sort": {"login": -1}}
    ]
    data = list(Customer.objects.aggregate(*pipeline))
    return data, status


def get_last_checkin_detail_json_view(customer_login):
    """
        Get detailed information about user's checkins
        :param customer_login: login of the user
        :return: a dict with information
        """
    try:
        Customer.objects.get(login=customer_login)
    except Customer.DoesNotExist:
        return NoContent, 404

    pipeline = [
        # pre filter values
        {"$match": {"login": customer_login}},
        # extract embedded docs
        {"$unwind": "$licenses"},
        {"$unwind": "$licenses.account_registrations"},
        {"$unwind": "$licenses.account_registrations.checkins"},
        # select data to show
        {
            "$project":
                {
                    "_id": 0,
                    "minion_name": "$licenses.minion_name",
                    "account": "$licenses.account_registrations.account_number",
                    "broker_name": "$licenses.account_registrations.broker",
                    "symbol": "$licenses.account_registrations.checkins.symbol",
                    "last_checkin": "$licenses.account_registrations.checkins.last_checkin",
                    "computer_name": {
                        "$ifNull": ["$licenses.account_registrations.checkins.computer_name", None]
                    },
                    "minion_version": {
                        "$ifNull": ["$licenses.account_registrations.checkins.minion_version", None]
                    },
                    "minion_edition": {
                        "$ifNull": ["$licenses.account_registrations.checkins.minion_edition", None]
                    },
                    "current_lots": {
                        "$ifNull": ["$licenses.account_registrations.checkins.current_lots", None]
                    },
                    "live_trading_status": {
                        "$ifNull": ["$licenses.account_registrations.checkins.live_trading_status", None]
                    },
                }
        },
        # sort by date
        {"$sort": {"last_checkin": -1}}
    ]
    data = list(Customer.objects.aggregate(*pipeline))

    return data, 200


def delete_checkin(account_number, broker_name, minion_name, symbol):
    customers = Customer.objects(
        licenses__minion_name=minion_name,
        licenses__account_registrations__account_number=account_number,
        licenses__account_registrations__checkins__broker=broker_name,
        licenses__account_registrations__checkins__symbol=symbol
    )
    if not customers:
        return NoContent, 404
    for customer in customers:
        for license in customer.licenses:
            if license.minion_name != minion_name:
                continue
            for registration in license.account_registrations:
                if registration.account_number != account_number:
                    continue
                checkins = []
                for checkin in registration.checkins:
                    if checkin.broker == broker_name and checkin.symbol == symbol:
                        pass
                    else:
                        checkins.append(checkin)
                registration.checkins = checkins
        customer.save()
    return NoContent, 204
