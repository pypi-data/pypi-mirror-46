import pathlib

import numpy as np
import pandas as pd
import yaml

CSV_MAX_ROWS = 1000

TYPE_MAP = {
    'i': 'int',
    'f': 'float',
    'O': 'str',
    'b': 'bool',
}

YAML_INDENT = 4


# disable YAML ordering
def unordered_dict_representer(self, data):
    return yaml.representer.SafeRepresenter.represent_dict(self, data.items())
yaml.add_representer(dict, unordered_dict_representer)    # noqa: E305


def get_type_string(dtype_obj):
    try:
        return TYPE_MAP.get(dtype_obj.kind)
    # default to treating unknown types as strings
    except KeyError:
        return 'str'


def is_likely_category(series):
    """Simple heuristic for guessing if a series of strings should be treated
    as a categorical variable."""
    return series.nunique() < 0.5 * series.shape[0]


def infer_yaml(csv_paths, yaml_path=None):
    """Infers dataset propoerties and generates a YAML description.

    :param csv_paths: list of filepaths to CSV files (only the first is
        checked, but all are used to infer categorical levels)
    :param yaml_path: optional filepath to write the YAML to
    :return: if yaml_path is not given, returns the YAML as a string
    """
    # TODO: verify schema matches across csv files (FV-104)
    csv_paths = [pathlib.Path(csv) for csv in csv_paths]
    first_csv = csv_paths[0].resolve()
    df = pd.read_csv(first_csv, nrows=CSV_MAX_ROWS)

    # get column info
    columns = []
    for column_name, column_series in df.iteritems():
        column_dtype = get_type_string(column_series.dtype)
        if column_dtype == 'str' and is_likely_category(column_series):
            column_dtype = 'category'
        columns.append({'column-name': column_name,
                        'data-type': column_dtype,
                        'column-type': 'feature'})

    # search for all levels of categorical features
    # and add this info to columns
    cat_features = [col['column-name'] for col in columns
                    if col['data-type'] == 'category']
    if len(cat_features) > 0:
        cat_levels = get_categorical_levels(csv_paths, cat_features)
        for col in columns:
            if col['data-type'] == 'category':
                col['possible-values'] = list(cat_levels[col['column-name']])

    # build the yaml obj
    dataset_yaml_obj = {
        'dataset': {
            'name': str(first_csv.parent.stem),
            'files': [pathlib.Path(csv).name for csv in csv_paths],
            'columns': columns
        }
    }

    if yaml_path is None:
        return yaml.dump(dataset_yaml_obj, indent=YAML_INDENT)
    with open(yaml_path, 'w') as outfile:
        yaml.dump(dataset_yaml_obj, outfile, indent=YAML_INDENT)


def get_categorical_levels(csv_paths, variable_names):
    """Returns a dictionary mapping each categorical variable name to a set of
    all unique values of that variable found in the entire dataset."""
    unique_vals = {name: set() for name in variable_names}
    for csv in csv_paths:
        csv_iterator = pd.read_csv(csv, usecols=variable_names,
                                   chunksize=CSV_MAX_ROWS)
        for chunk in csv_iterator:
            chunk_unique_values = (chunk
                                   .apply(lambda series: set(series.unique()))
                                   .to_dict())
            for col_name, uniques in chunk_unique_values.items():
                unique_vals[col_name] = unique_vals[col_name].union(uniques)

    # remove NaNs
    for col_name, uniques in unique_vals.items():
        unique_vals[col_name] = uniques.difference({np.nan})
    return unique_vals
