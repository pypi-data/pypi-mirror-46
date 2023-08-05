import re
import logging

from datetime import datetime

from connexion import NoContent
from mongoengine import ValidationError

from tmlib.models import TradeLog

logger = logging.getLogger()



def get_trade_logs(ticket=None, account_number=None, since_date=None,  include_expired=False):
    """
    Get trade logs by ticket ID;
    Return all the logs if no ticket id is specified
    :param ticket:
    :return:
    """
    order_type_filters = ['OP_BUY', 'OP_SELL']
    if include_expired:
        order_type_filters += ['OP_BUYSTOP', 'OP_BUYLIMIT', 'OP_SELLSTOP', 'OP_SELLLIMIT']

    mongo_filter = {
        "order_type__in": order_type_filters
    }
    if ticket:
        mongo_filter['ticket'] = ticket
    if account_number:
        mongo_filter['account'] = account_number
    if since_date:
        close_time = datetime.strptime(since_date, '%Y.%m.%d')
        mongo_filter['order_close_time__gte'] = close_time

    trade_logs: TradeLog = TradeLog.objects_without_id(**mongo_filter)
    return [t.to_mongo() for t in trade_logs], 200


def post_trade_logs(tradelogs_body):
    """
    Add a new trade log. Proxy function for the put method
    :param tradelogs_body:
    :return:
    """
    return put_trade_logs(tradelogs_body)


def put_trade_logs(tradelogs_body):
    """
    Add a new trade log.
    :param tradelogs_body:
    :return:
    """
    account = tradelogs_body.get('account')
    ticket = tradelogs_body.get('ticket')
    try:
        date_format = '%Y.%m.%d %H.%M'
        for element in ('order_close_time', 'order_open_time', 'order_place_time'):
            try:
                tradelogs_body[element] = datetime.strptime(tradelogs_body[element], date_format)
            except Exception:
                tradelogs_body[element] = None
        trade_log = TradeLog.objects(account=account, ticket=ticket).update(
            upsert=True, full_result=True, **{f'set__{k}': v for k, v in tradelogs_body.items()}
        )
        if trade_log.matched_count == 1:
            status = 200
        else:
            status = 201
        res = TradeLog.objects.get(account=account, ticket=ticket).to_dict()
    except (ValidationError, ValueError) as e:
        status = 400
        res = {
            "detail": str(e),
            "status": status,
            "title": "Bad Request",
            "type": "about:blank"
        }
    return res, status

def delete_trade_logs(account_number, minion_name, symbol, ticket):
    trade_logs = TradeLog.objects(account=account_number, minion_name=minion_name, symbol=symbol, ticket=ticket)
    if len(trade_logs):
        status = 204
        trade_logs.delete()
    else:
        status = 404
    return NoContent, status

def migrate_tradelogs_dates():
    pipeline = [
        {
            "$project": {
            "_id": 1,
            "account": 1,
            "ticket": 1,
            "account_balance": 1,
            "close_notes": 1,
            "magic_number": 1,
            "minion_name": 1,
            "order_close_price": 1,
            "order_close_time": {
                "$dateFromString": {
                    "dateString": '$order_close_time',
                    "format": '%Y.%m.%d %H.%M'
                }
            },
            "order_comment": 1,
            "order_direction": 1,
            "order_open_price": 1,
            "order_open_time": {
                "$dateFromString": {
                    "dateString": '$order_open_time',
                    "format": '%Y.%m.%d %H.%M'
                }
            },
            "order_place_time": {
                "$dateFromString": {
                    "dateString": '$order_place_time',
                    "format": '%Y.%m.%d %H.%M'
                }
            },
            "order_profit": 1,
            "order_profit_r": 1,
            "order_qty": 1,
            "order_type": 1,
            "parameters": 1,
            "period": 1,
            "symbol": 1,
            }
        },
        {"$out": "tradelogs"}
    ]
    try:
        TradeLog.objects.aggregate(*pipeline)
    except Exception as e:
        logger.warning(str(e))
