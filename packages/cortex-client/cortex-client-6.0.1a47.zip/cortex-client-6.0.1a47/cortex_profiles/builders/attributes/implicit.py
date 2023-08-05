from typing import List, Union

import pandas as pd

from cortex_profiles.builders.attributes.utils import implicit_attribute_builder_utils
from cortex_profiles import utils
from cortex_profiles.schemas.schemas import UNIVERSAL_ATTRIBUTES, TIMEFRAMES, PROFILE_TYPES
from cortex_profiles.types.attribute_values import ListAttributeValue
from cortex_profiles.types.attributes import ProfileAttribute, AssignedProfileAttribute, ObservedProfileAttribute

from cortex_profiles.builders.attributes.utils.attribute_builder_utils import state_modifier


def derive_implicit_attributes(insights_df: pd.DataFrame, interactions_df: pd.DataFrame, sessions_df: pd.DataFrame, conceptToMakeInstancesFor:List[str], days_considered_recent:int=3) -> List[ProfileAttribute]:
    recent_insights_df, recent_interactions_df, recent_sessions_df = (
        implicit_attribute_builder_utils.filter_recent_insights(insights_df, days_considered_recent),
        implicit_attribute_builder_utils.filter_recent_interactions(interactions_df, days_considered_recent),
        implicit_attribute_builder_utils.filter_recent_sessions(sessions_df, days_considered_recent)
    )
    eternal_attributes = implicit_attribute_builder_utils.derive_implicit_attributes_from_timeranged_dataframes(
        TIMEFRAMES.HISTORIC, insights_df, interactions_df, sessions_df, conceptToMakeInstancesFor
    )
    recent_attributes = implicit_attribute_builder_utils.derive_implicit_attributes_from_timeranged_dataframes(
        TIMEFRAMES.RECENT, recent_insights_df, recent_interactions_df, recent_sessions_df, conceptToMakeInstancesFor
    )
    return utils.flatten_list_recursively([eternal_attributes] + [recent_attributes])


def derive_implicit_profile_type_attribute(profileId:str, profileTypes:List[str]=[PROFILE_TYPES.END_USER]) -> AssignedProfileAttribute:
    return AssignedProfileAttribute(
        profileId = profileId,
        attributeKey = UNIVERSAL_ATTRIBUTES.TYPES,
        attributeValue = ListAttributeValue(profileTypes)
    )


class ImplicitAttributesBuilder(object):

    def __init__(self):
        self.attributes = [ ]

    @state_modifier(derive_implicit_attributes, (lambda self, results: self.attributes.extend(results)))
    def append_implicit_attributes(self, *args, **kwargs):
        """
        See :func:`.derive_declared_attributes_from_key_value_df` for input argument instructions.
        :return: The builder itself, after its state has been modified with the appended attributes ...
        """
        return self

    @state_modifier(derive_implicit_profile_type_attribute, (lambda self, results: self.attributes.append(results)))
    def append_implicit_type_attribute(self, *args, **kwargs):
        """
        See :func:`.derive_declared_attributes_from_value_only_df` for input argument instructions.
        :return: The builder itself, after its state has been modified with the appended attributes ...
        """
        return self


    def get(self) -> List[Union[AssignedProfileAttribute, ObservedProfileAttribute]]:
        return self.attributes


if __name__ == '__main__':
    from cortex_profiles import create_profile_synthesizer
    synth = create_profile_synthesizer()
    profileId, sessions_df, insights_df, interactions_df = synth.dfs_to_build_single_profile()
    attributes = (
        ImplicitAttributesBuilder()
            .append_implicit_attributes(insights_df, interactions_df, sessions_df)
            .append_implicit_type_attribute(profileId)
            .get()
    )
    for attribute in attributes:
        print(attribute)