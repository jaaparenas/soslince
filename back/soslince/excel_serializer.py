from rest_framework import serializers
from openpyxl import Workbook


class ExcelSerializer(serializers.Serializer):
    data = serializers.ListField(child=serializers.DictField())

    def to_excel(self, map_headers=None, map_datas=None):
        workbook = Workbook()
        worksheet = workbook.active

        headers = list(self.validated_data['data'][0].keys())
        headers_titles = headers

        if map_headers:
            _headers = headers
            headers = []
            headers_titles = []
            for header in map_headers:
                if header in _headers:
                    headers.append(header)
                    headers_titles.append(map_headers[header])

        worksheet.append(headers_titles)

        for item in self.validated_data['data']:
            row = []
            for header in headers:
                try:
                    if map_datas and header in map_datas:
                        if map_datas[header] == "boolean":
                            row.append("Si" if item[header] else "No")
                        elif map_datas[header] == "currency":
                            row.append(float(item[header]))
                        else:
                            row.append(map_datas[header][item[header]])
                    else:
                        row.append(item[header])
                except KeyError:
                    row.append(item[header])
            worksheet.append(row)

        return workbook