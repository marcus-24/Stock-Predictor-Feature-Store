import time
from hsfs.feature_group import FeatureGroup
from hsfs.feature_store import FeatureStore
from hsml.client.exceptions import RestAPIError
from tqdm import tqdm


def delete_existing_feature_group(fs: FeatureStore, fg_name: str) -> None:
    """Deletes existing feature group from Hopsworks AI

    Args:
        fs (FeatureStore): The feature store that hosts the feature group that is being deleted
        fg_name (str): The name of the feature group
    """
    try:
        fg_feature: FeatureGroup = fs.get_feature_group(name=fg_name)
        fg_feature.delete()  # if feature group doesnt exist, AttributeError is raised
        for _ in tqdm(range(60), desc=f'Deleting "{fg_name}" Feature store…'):
            time.sleep(1)
    except (RestAPIError, AttributeError):
        print(f'The "{fg_name}" has not been created yet')
