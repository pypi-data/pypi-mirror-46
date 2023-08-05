from enum import auto, unique
from typing import List, Optional

import pydash

from cortex_profiles.implicit.schema.implicit_tags import expand_tags_for_profile_attribute, ImplicitAttributeSubjects, \
    ImplicitTags, ImplicitTagTemplates
from cortex_profiles.implicit.schema.implicit_templates import CONCEPT, attr_template, attr_name_template
from cortex_profiles.implicit.schema.utils import prepare_template_candidates_from_schema_fields
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.schemas.schemas import UNIVERSAL_ATTRIBUTES
from cortex_profiles.types.attribute_values import DimensionalAttributeValue, CounterAttributeValue, \
    TotalAttributeValue, EntityAttributeValue
from cortex_profiles.types.attribute_values import ListAttributeValue, StatisticalSummaryAttributeValue
from cortex_profiles.types.schema import ProfileValueTypeSummary, ProfileAttributeSchema
from cortex_profiles.types.schema_config import SchemaConfig, CONCEPT_SPECIFIC_INTERACTION_FIELDS, \
    CONCEPT_SPECIFIC_DURATION_FIELDS, APP_SPECIFIC_FIELDS, INTERACTION_FIELDS, TIMEFRAME_FIELDS
from cortex_profiles.utils import AttrsAsDict
from cortex_profiles.utils import EnumWithNamesAsDefaultValue


@unique
class Patterns(EnumWithNamesAsDefaultValue):
    TYPE = auto()
    COUNT_OF_INSIGHT_INTERACTIONS = auto()
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = auto()
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = auto()
    COUNT_OF_APP_SPECIFIC_LOGINS = auto()
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = auto()
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = auto()
    STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS = auto()
    STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS = auto()
    ENTITY_INTERACTION_INSTANCE = auto()


class Metrics(AttrsAsDict):
    STAT_SUMMARY = pydash.strings.camel_case("STAT_SUMMARY")
    COUNT_OF = pydash.strings.camel_case("COUNT_OF")
    TOTAL_DURATION = pydash.strings.camel_case("TOTAL_DURATION")
    DURATION_OF = pydash.strings.camel_case("DURATION_OF")
    AVERAGE_COUNT_OF = pydash.strings.camel_case("AVERAGE_COUNT_OF")
    AVERAGE_DURATION_OF = pydash.strings.camel_case("AVERAGE_DURATION_OF")
    INSTANCE_OF = pydash.strings.camel_case("INSTANCE_OF")


class AttributeSections(AttrsAsDict):
    INSIGHTS            = attr_name_template("insights[{{{insight_type}}}]")
    INTERACTION         = attr_name_template("interaction")
    INTERACTED_WITH     = attr_name_template("interactedWith[{{{interaction_type}}}]")
    INPUT_TIMEFRAME     = attr_name_template("inputTimeframe[{{{timeframe}}}]")
    RELATED_TO_CONCEPT  = attr_name_template("relatedToConcept[{{{concept_title}}}]")
    LOGINS              = attr_name_template("logins[{{{app_id}}}]")
    DAILY_LOGINS        = attr_name_template("dailyLogins[{{{app_id}}}]")
    DAILY_APP_DURATION  = attr_name_template("dailyAppDuration[{{{app_id}}}]")


class NameTemplates(AttrsAsDict):
    TYPE = UNIVERSAL_ATTRIBUTES.TYPES
    COUNT_OF_INSIGHT_INTERACTIONS = ".".join([Metrics.COUNT_OF, AttributeSections.INSIGHTS, AttributeSections.INTERACTED_WITH, AttributeSections.INPUT_TIMEFRAME])
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = ".".join([Metrics.COUNT_OF, AttributeSections.INSIGHTS,  AttributeSections.INTERACTED_WITH, AttributeSections.RELATED_TO_CONCEPT, AttributeSections.INPUT_TIMEFRAME])
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = ".".join([Metrics.TOTAL_DURATION, AttributeSections.INSIGHTS,  AttributeSections.INTERACTED_WITH, AttributeSections.RELATED_TO_CONCEPT, AttributeSections.INPUT_TIMEFRAME])
    COUNT_OF_APP_SPECIFIC_LOGINS = ".".join([Metrics.COUNT_OF, AttributeSections.LOGINS, AttributeSections.INPUT_TIMEFRAME])
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = ".".join([Metrics.DURATION_OF, AttributeSections.LOGINS, AttributeSections.INPUT_TIMEFRAME])
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = ".".join([Metrics.COUNT_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = ".".join([Metrics.DURATION_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = ".".join([Metrics.AVERAGE_COUNT_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = ".".join([Metrics.AVERAGE_DURATION_OF, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS = ".".join([Metrics.STAT_SUMMARY, AttributeSections.DAILY_LOGINS, AttributeSections.INPUT_TIMEFRAME])
    STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS = ".".join([Metrics.STAT_SUMMARY, AttributeSections.DAILY_APP_DURATION, AttributeSections.INPUT_TIMEFRAME])
    ENTITY_INTERACTION_INSTANCE = ".".join([Metrics.INSTANCE_OF, AttributeSections.INTERACTION, AttributeSections.INPUT_TIMEFRAME])


class QuestionTemplates(AttrsAsDict):
    TYPE = "What are the different roles the profile adheres to?"
    COUNT_OF_INSIGHT_INTERACTIONS = attr_template("How many {{{insight_type}}} have been {{{optional_timeframe_adverb}}} {{{interaction_type}}} the profile?")
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = attr_template("How many {{{insight_type}}} related to a specific {{{singular_concept_title}}} have been {{{optional_timeframe_adverb}}} {{{interaction_type}}} the profile?")
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = attr_template("How much time did the profile {{{optional_timeframe_adverb}}} spend on {{{insight_type}}} insights related to a specific {{{singular_concept_title}}}?")
    COUNT_OF_APP_SPECIFIC_LOGINS = attr_template("How many times did the profile {{{optional_timeframe_adverb}}} log into the {{{app_title}}} app?")
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = attr_template("How much time did the profile {{{optional_timeframe_adverb}}} spend logged into the {{{app_title}}} app?")
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("On a daily basis, how many times did the profile {{{optional_timeframe_adverb}}} log into the {{{app_title}}} App?")
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("On a daily basis, how much time did the profile {{{optional_timeframe_adverb}}} spend logged into the {{{app_title}}} app?")
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("On average, how many daily logins into the the {{{app_title}}} App did the profile {{{optional_timeframe_adverb}}} initiate?")
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("On average, how much time did the profile {{{optional_timeframe_adverb}}} spend daily logged into the {{{app_title}}} App?")
    STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS = attr_template("How can we summarize the profile's count of {{{optional_timeframe_adjective}}} daily logins into the the {{{app_title}}} App?")
    STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS = attr_template("How can we summarize the time the profile {{{optional_timeframe_adverb}}} spent on the {{{app_title}}} App on a daily basis?")
    ENTITY_INTERACTION_INSTANCE = attr_template("What interactions with entities has the profile {{{optional_timeframe_adverb}}} initiated?")

class DescriptionTemplates(AttrsAsDict):
    TYPE = "Different Types Profile Adheres to."
    COUNT_OF_INSIGHT_INTERACTIONS = attr_template("Total {{{insight_type}}} insights {{{optional_timeframe_adverb}}} {{{interaction_type}}} profile.")
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = attr_template("Total {{{insight_type}}} insights related to {{{plural_concept_title}}} {{{optional_timeframe_adverb}}} {{{interaction_type}}} profile.")
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = attr_template("Total time {{{optional_timeframe_adverb}}} spent by profile on {{{insight_type}}} insights related to {{{plural_concept_title}}}.")
    COUNT_OF_APP_SPECIFIC_LOGINS = attr_template("Total times profile {{{optional_timeframe_adverb}}} logged into {{{app_title}}} app.")
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = attr_template("Total time profile {{{optional_timeframe_adverb}}} spent logged into {{{app_title}}} app")
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("Total times per day profile {{{optional_timeframe_adverb}}} logged into {{{app_title}}} app")
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("Total time per day profile {{{optional_timeframe_adverb}}} spent logged into {{{app_title}}} app")
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("Daily average of {{{optional_timeframe_adjective}}} logins for profile on {{{app_title}}} app.")
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = attr_template("Daily average time profile {{{optional_timeframe_adverb}}} spent logged into {{{app_title}}} app ")
    STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS = attr_template("Summary of the profile's count of {{{optional_timeframe_adjective}}} daily logins into the the {{{app_title}}} App?")
    STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS = attr_template("Summary of the time the profile {{{optional_timeframe_adverb}}} spent on the {{{app_title}}} App on a daily basis?")
    ENTITY_INTERACTION_INSTANCE = attr_template("Instances of the profiles {{{optional_timeframe_adjective}}} interactions with entities.")

class TitleTemplates(AttrsAsDict):
    TYPE = "Profile Types"
    COUNT_OF_INSIGHT_INTERACTIONS = attr_template("Insights {{{interaction_type}}}")
    COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS = attr_template("{{{plural_concept_title}}} {{{interaction_type}}}")
    TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT = attr_template("Duration on {{{plural_concept_title}}}")
    COUNT_OF_APP_SPECIFIC_LOGINS = "Total Logins"
    TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS = "Duration of Logins"
    COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "Daily Login Count"
    TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "Daily Login Durations"
    AVERAGE_COUNT_OF_DAILY_APP_SPECIFIC_LOGINS = "Average Daily Logins"
    AVERAGE_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS = "Average Login Duration"
    STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS = "Daily Login Summary"
    STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS = "Daily Duration Summary"
    ENTITY_INTERACTION_INSTANCE = "Entity Interactions"

# So do I want the tags and groups to be driven by the ones that appear in attributes ...
# If a tag or group does not appear in an attribute then its not part of the schema ... dont think that is what we are going for!
# Should expand the potential tags!
# Should have validation code to validate that attributes are not tagged with tags that dont exist ...
# And that all tags belong to a group


def all_attribute_names_for_candidates(pattern: Patterns, candidates: list) -> List[str]:
    return [
        NameTemplates[pattern.name].format(**{k: v.id for k, v in cand.items()})
        for cand in candidates
    ]


def expand_profile_attribute_schema(
            attribute_pattern: Patterns,
            attribute_filers:dict,
            valueType:ProfileValueTypeSummary,
            subject:str=None,
            attributeContext:str=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags:bool=True,
            additional_tags:Optional[List[str]]=None
        ) -> ProfileAttributeSchema:
    tags_to_add = additional_tags if additional_tags is not None else []
    return ProfileAttributeSchema(
        name=NameTemplates[attribute_pattern.name].format(**{k: v.id for k, v in attribute_filers.items()}),
        type=attributeContext,
        valueType=valueType,
        label=TitleTemplates[attribute_pattern.name].format(**attribute_filers),
        description=DescriptionTemplates[attribute_pattern.name].format(**attribute_filers),
        questions=[QuestionTemplates[attribute_pattern.name].format(**attribute_filers)],
        tags=expand_tags_for_profile_attribute(attribute_filers, attributeContext, subject) + tags_to_add if include_tags else []
    )

def schema_for_interaction_instances(schema_config:SchemaConfig, include_tags:bool=True) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, TIMEFRAME_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.ENTITY_INTERACTION_INSTANCE, cand,
            EntityAttributeValue.detailed_schema_type(),
            subject=ImplicitAttributeSubjects.INTERACTIONS,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[ImplicitTags.CONCEPT_SPECIFIC.id, ImplicitTags.INSIGHT_INTERACTIONS.id]
        ) for cand in candidates
    ]

def schema_for_concept_specific_interaction_attributes(schema_config:SchemaConfig, include_tags:bool=True) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, CONCEPT_SPECIFIC_INTERACTION_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.COUNT_OF_CONCEPT_SPECIFIC_INSIGHT_INTERACTIONS, cand,
            DimensionalAttributeValue.detailed_schema_type(cand[CONCEPT].id, CounterAttributeValue),
            subject=ImplicitAttributeSubjects.INSIGHT_INTERACTIONS,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[ImplicitTags.CONCEPT_SPECIFIC.id]
        )
        for cand in candidates
    ]


def schema_for_concept_specific_duration_attributes(schema_config: SchemaConfig, include_tags:bool=True) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, CONCEPT_SPECIFIC_DURATION_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.TOTAL_DURATION_ON_CONCEPT_SPECIFIC_INSIGHT, cand,
            DimensionalAttributeValue.detailed_schema_type(cand[CONCEPT].id, TotalAttributeValue),
            subject=ImplicitAttributeSubjects.INSIGHT_INTERACTIONS,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[ImplicitTags.CONCEPT_SPECIFIC.id]
        )
        for cand in candidates
    ]


def schema_for_interaction_attributes(schema_config: SchemaConfig, include_tags:bool=True) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, INTERACTION_FIELDS)
    return [
        expand_profile_attribute_schema(
            Patterns.COUNT_OF_INSIGHT_INTERACTIONS, cand,
            CounterAttributeValue.detailed_schema_type(),
            subject=ImplicitAttributeSubjects.INSIGHT_INTERACTIONS,
            attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
            include_tags=include_tags,
            additional_tags=[ImplicitTags.INSIGHT_INTERACTIONS.id,]
        )
        for cand in candidates
    ]


def schema_for_app_specific_attributes(schema_config:SchemaConfig, include_tags:bool=True) -> List[ProfileAttributeSchema]:
    candidates = prepare_template_candidates_from_schema_fields(schema_config, APP_SPECIFIC_FIELDS)
    return (
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                CounterAttributeValue.detailed_schema_type(),
                subject=ImplicitAttributeSubjects.APP_USAGE,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.id, ImplicitTags.APP_SPECIFIC.id,]
            )
            for attribute_pattern in [Patterns.COUNT_OF_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                DimensionalAttributeValue.detailed_schema_type("cortex/day", CounterAttributeValue),
                subject=ImplicitAttributeSubjects.APP_USAGE,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.id, ImplicitTags.APP_SPECIFIC.id,]
            )
            for attribute_pattern in [Patterns.COUNT_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                TotalAttributeValue.detailed_schema_type(),
                subject=ImplicitAttributeSubjects.APP_USAGE,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.id, ImplicitTags.APP_SPECIFIC.id,]
            )
            for attribute_pattern in [Patterns.TOTAL_DURATION_OF_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                DimensionalAttributeValue.detailed_schema_type("cortex/day", TotalAttributeValue),
                subject=ImplicitAttributeSubjects.APP_USAGE,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.id, ImplicitTags.APP_SPECIFIC.id,]
            )
            for attribute_pattern in [Patterns.TOTAL_DURATION_OF_DAILY_APP_SPECIFIC_LOGINS] for cand in candidates
        ]
        +
        [
            expand_profile_attribute_schema(
                attribute_pattern, cand,
                StatisticalSummaryAttributeValue.detailed_schema_type(),
                subject=ImplicitAttributeSubjects.APP_USAGE,
                attributeContext=CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE,
                include_tags=include_tags,
                additional_tags=[ImplicitTags.APP_USAGE.id, ImplicitTags.APP_SPECIFIC.id,]
            )
            for attribute_pattern in [Patterns.STAT_SUMMARY_DAILY_APP_SPECIFIC_LOGINS, Patterns.STAT_SUMMARY_DAILY_APP_SPECIFIC_DURATIONS] for cand in candidates
        ]

    )


def schemas_for_universal_attributes(include_tags:bool=True) -> List[ProfileAttributeSchema]:
    return [
        ProfileAttributeSchema(
            name=UNIVERSAL_ATTRIBUTES.TYPES,
            type=CONTEXTS.ASSIGNED_PROFILE_ATTRIBUTE,
            valueType=ListAttributeValue.detailed_schema_type("str"),
            label=TitleTemplates.TYPE,
            description=DescriptionTemplates.TYPE,
            questions=[QuestionTemplates.TYPE],
            tags=[ImplicitTags.ASSIGNED.id] if include_tags else []
        )
    ]