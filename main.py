import hopsworks
from hsfs.feature_group import FeatureGroup
from hsfs.feature_store import FeatureStore
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)
WIN_SIZE = 7
N_FUTURE = 7
API_KEY = os.getenv("HOPSWORKS_KEY")


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


def main() -> None:
    start_date = date.today() - relativedelta(years=2)
    df = yf.Ticker("AAPL").history(interval="1d", start=start_date)
    feature_df = feature_engineering(df)
    labels_df = create_labels(df)

    project = hopsworks.login(api_key_value=API_KEY)

    """A single feature group is feature constructed from data of the same source"""
    # Reference: https://github.com/logicalclocks/hopsworks-tutorials/blob/master/batch-ai-systems/credit_scores/1_credit_scores_feature_backfill.ipynb
    fs: FeatureStore = project.get_feature_store(name="stock_predictor_featurestore")

    # Feature groups will be offline since I dont need fast real-time predictions

    fg_feature: FeatureGroup = fs.get_or_create_feature_group(
        name="stock_features",
        version=1,
        description="stores windowed features of stock",
        primary_key=["date"],
        event_time="date",
        online_enabled=False,
    )

    fg_feature.insert(feature_df)

    fg_labels: FeatureGroup = fs.get_or_create_feature_group(
        name="stock_labels",
        version=1,  # TODO: try to auto increment versions and check if all data is overwritten
        description="stores stock prediction labels",
        primary_key=["date"],
        event_time="date",
        online_enabled=False,
    )

    fg_labels.insert(labels_df)


if __name__ == "__main__":
    main()
