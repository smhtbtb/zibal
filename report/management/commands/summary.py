from datetime import datetime

from bson import ObjectId
from django.core.management import BaseCommand

from mongo_conn import get_db
from report.make_transaction_output import making_output


class Command(BaseCommand):
    help = "This command makes summary_transaction collection"

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', type=str, help='mode can be daily, weekly or monthly')
        parser.add_argument('-t', '--type', type=str, help='type can be amount or count')

    def handle(self, *args, **kwargs):
        modes = ['daily', 'weekly', 'monthly']
        types = ['amount', 'count']
        if kwargs['mode']:
            if kwargs['mode'] in modes:
                modes = [kwargs['mode']]
            else:
                return 'mode can be daily, weekly or monthly'
        if kwargs['type']:
            if kwargs['type'] in types:
                types = [kwargs['type']]
            else:
                return 'type can be amount or count'
        for mode in modes:
            for type_ in types:
                response_data = making_output(mode, type_)
                db = get_db()
                this_summary_transaction = db.summary_transaction.find_one({"mode": mode, "type": type_}, {"data": 0})
                print('this_summary_transaction=', this_summary_transaction)
                today = datetime.now().strftime("%Y-%m-%d %H:%M")
                if this_summary_transaction:  # update
                    db.summary_transaction.update_one({"_id": ObjectId(this_summary_transaction["_id"])},
                                                      {"$set": {"data": response_data, "updated_at": today}})
                else:  # insert
                    db.summary_transaction.insert_one({
                        "mode": mode,
                        "type": type_,
                        "updated_at": today,
                        "created_at": today,
                        "data": response_data
                    })
