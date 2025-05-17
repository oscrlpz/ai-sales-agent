from typing import Dict

from pandas import DataFrame
from rapidfuzz import fuzz


def _normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize weights to sum to 1.

    Args:
        weights (Dict[str, float]): The weights to normalize.

    Returns:
        Dict[str, float]: The normalized weights.
    """
    total = sum(weights.values())
    for key in weights:
        weights[key] /= total
    return weights


def fuzzy_filter(
    df: DataFrame,
    user_input: Dict[str, str],
    weights: Dict[str, float],
    km_tolerance: float = 0.2,
) -> DataFrame:
    """
    Filter a DataFrame based on user input and weights.

    Args:
        df (DataFrame): The DataFrame to filter.
        user_input (Dict[str, str]): The user input to filter by.
        weights (Dict[str, float]): The weights for each key in user_input.
        km_tolerance (float): Tolerance for km filtering.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    df = df.copy()
    # Set to zero weights for keys not in user_input
    for key, val in user_input.items():
        if val is None:
            weights[key] = 0
    weights = _normalize_weights(weights)

    # Calculate score per key
    for key in weights:
        val = user_input.get(key)
        if val:
            df[f"{key}_score"] = df[key].apply(lambda x: fuzz.ratio(str(val), str(x)))
        else:
            df[f"{key}_score"] = 10

    # Exact or fuzzy match
    for key, val in user_input.items():
        if val is None or key in weights:
            continue
        if key == "km":
            # min_km = val * (1 - km_tolerance)
            max_km = val * (1 + km_tolerance)
            df = df[df["km"].between(0, max_km)]
        else:
            df = df[df[key] == val]

    # Percentage of similarity
    df["similarity_score"] = sum(
        df[f"{k}_score"] * w for k, w in weights.items()
    ) / sum(weights.values())

    df = df.sort_values(by="similarity_score", ascending=False)

    return df.drop(columns=[f"{k}_score" for k in weights]).reset_index(drop=True)
