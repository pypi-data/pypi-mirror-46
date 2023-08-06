"""
This module parses the Excel file and transforms it to JSON object.
"""


import pandas as pd
import json


def read_xl(filename):
    """

    :param filename: File path of the excel file
    :return: return pandas Dataframe
    """
    return pd.read_excel(filename, sheet_name=None)


def convert_data_to_list(data):
    """

    :param data: "," separated string
    :return: returns a list of values
    """
    temp = (list(map(lambda x: x.strip(), data['Value'].split(','))) if data['IsArray'] == 1 else data['Value'])
    return temp


def parse_tools(df):
    """
    :param df: Pandas Dataframe
    :return: List of dictionaries
    """
    return df.to_dict('records')


def parse_others(df):
    """
    :param df: Pandas Dataframe
    :return: Processed pandas Dataframe containing only useful data
    """
    df['Data'] = df.apply(convert_data_to_list, axis=1)
    temp_df = df[['Type', 'Data']]
    temp_df.set_index('Type', inplace=True)
    return temp_df


def parse_xl(excel_df):
    """
    :param excel_df: pandas Dataframe containing Excel file's data
    :return: dictionary of excel file's data.
        This Dictionary is an intermediate data which gets converted to json.
    """
    dict_data = {}
    #dict_data['sub'] = []
    for key in excel_df.keys():
        excel_df[key].fillna(value=" ", inplace=True)
        if key.find('sub') != -1:
            dict_data['sub'] += parse_tools(excel_df[key])
        else:
            temp_df = parse_others(excel_df[key])
            if key == 'Main':
                dict_data.update(temp_df.to_dict()['Data'])
            else:
                dict_data[key] = temp_df.to_dict()['Data']
    return dict_data


def translate_excel_to_json(xl_file_path, json_file_path):
    """
    :param xl_file_path: Input Excel file path
    :param json_file_path: Resulting JSON file path
    :return: Nothing
    """
    try:
        df = read_xl(xl_file_path)
        dict_data = parse_xl(df)
        json_data = json.dumps(dict_data)
        handle = open(json_file_path, "w")
        handle.write(json_data)
        handle.close()
        return 0

    except Exception as e:
        print("Error while transforming Excel to JSON. Is the Excel file in correct format?")
        raise e
