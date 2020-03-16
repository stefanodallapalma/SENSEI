from enum import Enum


class ExperimentationType(Enum):
    SCALING = "scaling"
    THREE_CLASSES = "three-classes"
    OVERSAMPLING = "oversampling"
    FEATURE_SELECTION = "feature-selection"


class ExperimentationList(Enum):
    EXP_1 = ExperimentationType.SCALING.value
    EXP_2 = ExperimentationType.OVERSAMPLING.value
    EXP_3 = ExperimentationType.THREE_CLASSES.value
    EXP_4 = ", ".join([ExperimentationType.SCALING.value, ExperimentationType.OVERSAMPLING.value])
    EXP_5 = ", ".join([ExperimentationType.THREE_CLASSES.value, ExperimentationType.OVERSAMPLING.value])
    EXP_6 = ", ".join([ExperimentationType.THREE_CLASSES.value, ExperimentationType.SCALING.value])
    EXP_7 = ", ".join([ExperimentationType.THREE_CLASSES.value, ExperimentationType.SCALING.value,
                      ExperimentationType.OVERSAMPLING.value])
    EXP_8 = ", ".join([ExperimentationType.THREE_CLASSES.value, ExperimentationType.SCALING.value,
                      ExperimentationType.OVERSAMPLING.value, ExperimentationType.FEATURE_SELECTION.value])

