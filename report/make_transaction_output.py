from datetime import datetime

import jdatetime
from bson import ObjectId

from mongo_conn import get_db


def making_output(mode: str, type_: str, merchant_id: str = None) -> list[dict]:
    db = get_db()

    pipeline = []
    if merchant_id:
        pipeline = [{"$match": {"merchantId": ObjectId(merchant_id)}}]
    if mode == 'daily':
        pipeline += [
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$createdAt"
                        }
                    },
                    "value": {"$sum": "$amount" if type_ == 'amount' else 1}
                }
            },
            {"$sort": {"_id": 1}}
        ]
    elif mode == 'weekly':
        pipeline += [
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$createdAt"},
                        "week": {"$isoWeek": "$createdAt"}
                    },
                    "value": {"$sum": "$amount" if type_ == 'amount' else 1}
                }
            },
            {"$sort": {"_id.year": 1, "_id.week": 1}}
        ]
    elif mode == 'monthly':
        pipeline += [
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$createdAt"},
                        "month": {"$month": "$createdAt"}
                    },
                    "value": {"$sum": "$amount" if type_ == 'amount' else 1}
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1}}
        ]

    results = list(db.transaction.aggregate(pipeline))
    response_data = []

    for result in results:
        if mode == 'daily':
            date = datetime.strptime(result['_id'], '%Y-%m-%d')
            solar_date = jdatetime.datetime.fromgregorian(datetime=date).strftime('%Y/%m/%d')
            response_data.append({"key": solar_date, "value": result['value']})
        elif mode == 'weekly':
            solar_date = (f"هفته {result['_id']['week']} سال "
                          f"{jdatetime.date.fromgregorian(year=result['_id']['year'], month=1, day=1).strftime('%Y')}")
            response_data.append({"key": solar_date, "value": result['value']})
        elif mode == 'monthly':
            solar_date = jdatetime.date.fromgregorian(year=result['_id']['year'], month=result['_id']['month'],
                                                      day=1).strftime('%B %Y')
            response_data.append({"key": solar_date, "value": result['value']})

    return response_data
