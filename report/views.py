from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mongo_conn import get_db
from report.make_transaction_output import making_output


class ReportTransactions(APIView):
    def get(self, request, *args, **kwargs):
        mode = request.query_params.get('mode')
        type_ = request.query_params.get('type')
        merchant_id = request.query_params.get('merchant_id')

        if mode not in ['daily', 'weekly', 'monthly'] or type_ not in ['amount', 'count']:
            return Response({"error": "Invalid mode or type"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = making_output(mode, type_, merchant_id)
        # print('response_data=', response_data)
        return Response(response_data, status=status.HTTP_200_OK)


class SummaryReportTransactions(APIView):
    def get(self, request, *args, **kwargs):
        mode = request.query_params.get('mode')
        type_ = request.query_params.get('type')
        merchant_id = request.query_params.get('merchant_id')

        if merchant_id:
            return Response({"error": "Passing this param 'merchant_id' is not developed yet"},
                            status=status.HTTP_400_BAD_REQUEST)
        if mode not in ['daily', 'weekly', 'monthly'] or type_ not in ['amount', 'count']:
            return Response({"error": "Invalid mode or type"}, status=status.HTTP_400_BAD_REQUEST)

        db = get_db()
        results = db.summary_transaction.find_one({"mode": mode, "type": type_})
        # print('results=', results)
        data = results.get("data", [])
        return Response(data, status=status.HTTP_200_OK)
