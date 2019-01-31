import logging
import shutil
from . import charthelper
import ntpath

logger = logging.getLogger(__name__)

extension_csv = '.csv'
extension_json = '.json'
extension_png = '.png'

def generate_file_names(output_dir,symbol,file_name):
    csv_file_name = output_dir + ntpath.basename(symbol) + '_' + file_name + extension_csv
    png_file_name = output_dir + ntpath.basename(symbol) + '_' + file_name + extension_png
    json_file_name = output_dir + ntpath.basename(symbol) + '_' + file_name + extension_json

    file_names = [csv_file_name, png_file_name, json_file_name]
    return [*file_names]

def save_output(pivot_df, csv_file_name, png_file_name, json_file_name):
    # write to csv and json files and create charts
    pivot_df.to_csv(csv_file_name, sep=',', encoding='utf-8')
    charthelper.plot_chart_pivots(pivot_df, png_file_name)
    with open(json_file_name, 'w') as f:
        f.write(pivot_df.to_json(orient='records', lines=True))
    return


def print_output(df):
    # convert DataFrame to string
    df_string = df.to_string()
    df_split = df_string.split('\n')

    columns = shutil.get_terminal_size().columns
    for i in range(len(df)):
        logger.debug(df_split[i].center(columns))
    return