from difflib import SequenceMatcher
import pandas as pd

"""
This module contains helper functions and dictionaries used in the testing process of the cell culture analysis.
"""

# TODO: Consider moving these dictionaries to a separate configuration file
dict1 = {
    0: 'A human orthogonal IL-2 and IL-2R system enhances\nCAR T cell expansion and antitumor activity in a\nmurine model of leukemia (https://www.notion.so/A-human-orthogonal-IL-2-and-IL-2R-system-enhances-CAR-T-cell-expansion-and-antitumor-activity-in-a-m-c9d7658fe6744a7c94596e5d7359d325?pvs=21)',
    # ... (rest of the dictionary)
}
dict2 = {y: x for x, y in dict1.items()}

def similar(a: str, b: str) -> float:
    """Calculate the similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()

def remove_spaces(l: list) -> list:
    """Remove empty strings from a list."""
    return [i for i in l if i]

def convert_string_to_df(s: str) -> pd.DataFrame:
    """Convert a string representation of a table to a pandas DataFrame."""
    rows = [remove_spaces(row.strip().split("  ")) for row in s.split('\n')]
    return pd.DataFrame(rows[1:], columns=['Index'] + rows[0]).drop('Index', axis=1)