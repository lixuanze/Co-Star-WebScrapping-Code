import pandas as pd

df_result_list = []
df_data_list = []
df_row_path = ''
df_data_index = -1

filename = "./source.csv"

df = pd.read_csv(filename)

df_columns = list(df.columns.values)

class DfJounry:
    def __init__(self, ip, data):
        self.ip = str(ip)
        self.data = []
        self.data.append(data)

class DfJounryResult:
    def __init__(self, path, total_conversions, total_conversion_value, total_null):
        self.path = path
        self.total_conversions = total_conversions
        self.total_conversion_value = total_conversion_value
        self.total_null = total_null

def checkDfJounry(ip):
    for obj_index, obj in enumerate(df_data_list):
        if obj.ip == ip:
            return obj_index
    return False

def checkDfJounryResult(path):
    for obj_index, obj in enumerate(df_result_list):
        if obj.path == path:
            return obj_index
    return False

def checkDfJournyPaths(data):
    for data_row_count in range(1, len(data) + 1):
        checkDfJournyPath(data, 0, data_row_count)

def checkDfJournyPath(data, data_row_index, data_row_count, path = ""):
    data_row_index = data_row_index + 1
    if path != "":
        path += " > "
    data_row_len = len(data[data_row_index - 1])
    for data_row_field_index in range(1, data_row_len - 2):
        if data[data_row_index - 1][data_row_field_index]:
            check_path = path + df_columns[data_row_field_index]
            if data_row_index == data_row_count:
                df_result_list_index = checkDfJounryResult(check_path)
                if df_result_list_index == False:
                    if data[data_row_index - 1][data_row_len - 1]:
                        dj = DfJounryResult(check_path, 1, data[data_row_index - 1][data_row_len - 2], 0)
                    else:
                        dj = DfJounryResult(check_path, 0, 0, 1)
                    df_result_list.append(dj)
                else:
                    if data[data_row_index - 1][data_row_len - 1]:
                        df_result_list[df_result_list_index].total_conversions = df_result_list[df_result_list_index].total_conversions + 1
                        df_result_list[df_result_list_index].total_conversion_value = df_result_list[df_result_list_index].total_conversion_value + data[data_row_index - 1][data_row_len - 2]
                    else:
                        df_result_list[df_result_list_index].total_null = df_result_list[df_result_list_index].total_null + 1
            else:
                checkDfJournyPath(data, data_row_index, data_row_count, check_path)

for df_index, df_row in df.iterrows():
    if df_row_path != str(df_row[0]):
        if df_row_path != '':
            checkDfJournyPaths(df_data_list)
            df_data_list = []
    df_data_list.append(df_row)
    df_row_path = str(df_row[0])

df_result_fields = []
for df_result in df_result_list:
    df_result_field = []
    df_result_field.append(df_result.path)
    df_result_field.append(df_result.total_conversions)
    df_result_field.append(df_result.total_conversion_value)
    df_result_field.append(df_result.total_null)
    df_result_fields.append(df_result_field)

df_result = pd.DataFrame(df_result_fields, columns=['path', 'total_conversions', 'total_conversion_value', 'total_null'])
df_result.to_csv('./journy.csv', index=False)
