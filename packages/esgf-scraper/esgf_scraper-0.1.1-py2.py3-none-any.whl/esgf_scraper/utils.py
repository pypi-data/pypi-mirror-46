import shutil

import pandas as pd


def print_items(items, cols="all", default_term_width=200):
    """
    Pretty prints a list of items to stdout

    Parameters
    ----------
    items: list of dicts
        The items to be printed
    cols: str or list of strs
        The columns to be included in the output
    default_term_width: int
        Fallback terminal width if none is set

    """
    cols = cols.split(",") if isinstance(cols, str) else cols
    excluded_cols = [
        "_timestamp",
        "_version_",
        "access",
        "activity_drs",
        "citation_url",
        "data_specs_version",
        "dataset_id_template_",
        "further_info_url",
        "geo",
        "geo_units",
        "pid",
        "title",
        "variable",
        "url",
    ]
    df = pd.DataFrame(items)
    if "_id" in df.columns:
        df = df.set_index("_id")
    for c in excluded_cols:
        if c in df:
            df.drop(c, axis=1, inplace=True)
    if cols != ["all"]:
        df = df[cols]
    terminal_size = shutil.get_terminal_size((default_term_width, 20))
    with pd.option_context(
        "display.max_rows",
        None,
        "display.max_columns",
        df.shape[1],
        "display.width",
        terminal_size.columns,
        "display.max_colwidth",
        default_term_width,
    ):
        print(df)
