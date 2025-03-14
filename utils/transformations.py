import pandas as pd


WIN_SIZE = 7
N_FUTURE = 7


def feature_engineering(df: pd.DataFrame, win_size: int = WIN_SIZE) -> pd.DataFrame:
    """Generates window features for the stock prediction

    Args:
        df (pd.DataFrame): raw stock prediction data from yahoo finance
        win_size (int, optional): Look back window for features. Defaults to WIN_SIZE.

    Returns:
        pd.DataFrame: features for stock prediction model and ready for hopsworks feature store ingestion
    """
    # https://medium.com/aimonks/improving-stock-price-forecasting-by-feature-engineering-8a5d0be2be96
    _df = df.copy()
    # TODO: Labels use a negative shift in for loop

    return (
        _df.assign(
            daily_var=(_df["High"] - _df["Low"]) / (_df["Open"]),
            sev_day_sma=_df["Close"].rolling(win_size).mean(),
            sev_day_std=_df["Close"].rolling(win_size).std(),
            daily_return=_df["Close"].diff(),
            sma_2std_pos=_df["Close"].rolling(win_size).mean()
            + 2 * _df["Close"].rolling(win_size).std(),
            sma_2std_neg=_df["Close"].rolling(win_size).mean()
            - 2 * _df["Close"].rolling(win_size).std(),
            high_close=(_df["High"] - _df["Close"]) / _df["Open"],
            low_open=(_df["Low"] - _df["Open"]) / _df["Open"],
            cumul_return=_df["Close"] - _df["Close"].iloc[0],
        )
        .dropna()
        .drop(columns=df.columns)
        .reset_index()
        .rename(columns=str.lower)
    )


def create_labels(df: pd.DataFrame, n_future: int = N_FUTURE) -> pd.DataFrame:
    """Generates labels for model training

    Args:
        df (pd.DataFrame): raw stock prediction data from yahoo finance
        n_future (int, optional): The number of time steps ahead of time the model needs to predict. Defaults to N_FUTURE.

    Returns:
        pd.DataFrame: future time steps that the model needs to predict
    """
    _df = df.copy()
    for idx in range(n_future):
        _df[f"label_time_{idx + 1}"] = _df["Close"].shift(-idx - 1)

    return _df.dropna().drop(columns=df.columns).reset_index().rename(columns=str.lower)
