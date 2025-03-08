import hopsworks
from hsfs.feature_store import FeatureStore
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("HOPSWORKS_KEY")

project = hopsworks.login(api_key_value=API_KEY)
fs: FeatureStore = project.get_feature_store(name="stock_predictor_featurestore")
fg = fs.get_or_create_feature_group(
    name="python_api_test",
    version=1,
    description="API test",
    primary_key=["col1"],
    online_enabled=True,
)


df1 = pd.DataFrame(data=np.array([[1, 2], [3, 4]]), columns=["col1", "col2"])

fg.insert(df1)
