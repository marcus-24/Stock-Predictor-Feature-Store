# standard imports
import os
from datetime import date
import hopsworks
import holidays
from hsfs.feature_group import FeatureGroup
from hsfs.feature_store import FeatureStore
import yfinance as yf
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

# local imports
from utils.dates import correct_start_date
from utils.transformations import feature_engineering, create_labels

load_dotenv(override=True)

API_KEY = os.getenv("HOPSWORKS_KEY")
PROJECT = hopsworks.login(api_key_value=API_KEY)

nyse_holidays = holidays.financial_holidays("NYSE")
today = date.today()

if today not in nyse_holidays:  # if today is not a financial holiday

    """Create features and labels"""
    start_date = today - relativedelta(years=2)
    new_start_date = correct_start_date(start_date, nyse_holidays)
    df = yf.Ticker("AAPL").history(interval="1d", start=new_start_date)
    feature_df = feature_engineering(df)
    labels_df = create_labels(df)

    """A single feature group is feature constructed from data of the same source"""
    # Reference: https://github.com/logicalclocks/hopsworks-tutorials/blob/master/batch-ai-systems/credit_scores/1_credit_scores_feature_backfill.ipynb
    fs: FeatureStore = PROJECT.get_feature_store(name="stock_predictor_featurestore")

    """Ingest features in feature store"""
    # Feature groups will be offline since I dont need fast real-time predictions
    fg_feature: FeatureGroup = fs.get_or_create_feature_group(
        name="stock_features",
        version=1,
        description="stores windowed features of stock",
        primary_key=["date"],
        event_time="date",
        online_enabled=False,
    )

    fg_feature.insert(feature_df, overwrite=True)

    """Insert labels into feature store"""
    fg_labels: FeatureGroup = fs.get_or_create_feature_group(
        name="stock_labels",
        version=1,  # TODO: try to auto increment versions and check if all data is overwritten
        description="stores stock prediction labels",
        primary_key=["date"],
        event_time="date",
        online_enabled=False,
    )

    fg_labels.insert(labels_df, overwrite=True)
