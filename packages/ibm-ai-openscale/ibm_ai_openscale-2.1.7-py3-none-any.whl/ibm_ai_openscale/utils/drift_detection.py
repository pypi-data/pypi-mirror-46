# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2019
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import io
import os
import pickle
import tarfile
import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import LabelEncoder
from enum import Enum

from ibm_ai_openscale.utils import install_package


class DriftDetection():
    """
        Class to generate information needed for error model generation
        :param training_data_frame: Dataframe comprising of input training data
        :type training_data_frame: DataFrame

        :param score: Customized score function to get prediction and probability array
        :type training_data_frame: function

        :param payload_analytics_input: Input parameters needed for error model creation
        :type payload_analytics_input:dict

        Example:
        drift_detection_input = {
            "feature_columns":<list of feature columns>
            "categorical_columns": <list of categorical columns>
            "label_column": <label column>
            "problem_type": <problem_type>
        }

    """
    RANDOM_STATE = 111

    def __init__(self, training_dataframe, drift_detection_input):
        initial_level = logging.getLogger().getEffectiveLevel()

        updated_level = logging.getLogger().getEffectiveLevel()

        if initial_level != updated_level:
            logging.basicConfig(level=initial_level)

        self.training_data_frame = training_dataframe
        self.drift_detection_input = drift_detection_input
        self.ddm_features = []
        self.dd_model = None
        self.base_client_accuracy = 0
        self.base_predicted_accuracy = 0
        self.__validate_drift_input()

    def __validate_drift_input(self):
        problem_type = self.drift_detection_input.get("problem_type")
        drift_supported_problem_types = ["binary", "multiclass"]
        if problem_type not in drift_supported_problem_types:
            raise Exception(
                "Drift detection is not supported for {}. Supported types are:{}".format(problem_type, drift_supported_problem_types))

        columns_from_data_frame = list(self.training_data_frame.columns.values)
        self.label_column = self.drift_detection_input.get("label_column")
        if self.label_column not in columns_from_data_frame:
            raise Exception(
                "'label_column':{} missing in training data".format(self.label_column))

        self.feature_columns = self.drift_detection_input.get(
            "feature_columns")
        if self.feature_columns is None or type(self.feature_columns) is not list or len(self.feature_columns) == 0:
            raise Exception("'feature_columns should be a non empty list")

        check_feature_column_existence = list(
            set(self.feature_columns) - set(columns_from_data_frame))
        if len(check_feature_column_existence) > 0:
            raise Exception("Feature columns missing in training data.Details:{}".format(
                check_feature_column_existence))

        self.categorical_columns = self.drift_detection_input.get(
            "categorical_columns")

        if self.categorical_columns is not None and type(self.categorical_columns) is not list:
            raise Exception(
                "'categorical_columns' should be a list of values")

        # Verify existence of  categorical columns in feature columns
        if self.categorical_columns is not None and len(self.categorical_columns) > 0:
            check_cat_col_existence = list(
                set(self.categorical_columns) - set(self.feature_columns))
            if len(check_cat_col_existence) > 0:
                raise Exception("'categorical_columns' should be subset of feature columns.Details:{}".format(
                    check_cat_col_existence))

    def __get_probability_dataframe(self, probabilities):

        # Add probabilities of the classes as columns to the dataframe
        prob_df = pd.DataFrame(probabilities, columns=["probability_{}".format(
            idx) for idx in range(0, probabilities.shape[1])])
        sorted_probs = np.sort(probabilities)

        # Also add difference between highest probability and second highest probability
        prob_df["probability_diff"] = sorted_probs[:, -1:] - \
            sorted_probs[:, -2:-1]
        return prob_df

    def balance_data(self, train, train_y):
        num_correct_predictions = len(train_y[train_y == 1])
        num_incorrect_predictions = len(train_y[train_y == 0])

        if num_correct_predictions > num_incorrect_predictions:
            supplemental_set = train.iloc[train_y[train_y == 0].index]
            supplemental_set_y = pd.Series([0] * len(supplemental_set))
            repeat_num = int(num_correct_predictions /
                             num_incorrect_predictions)
            remaining_num = num_correct_predictions - \
                num_incorrect_predictions * repeat_num
        else:
            supplemental_set = train.iloc[train_y[train_y == 1].index]
            supplemental_set_y = pd.Series([1] * len(supplemental_set))
            repeat_num = int(num_incorrect_predictions /
                             num_correct_predictions)
            remaining_num = num_incorrect_predictions - num_correct_predictions * repeat_num

        new_train = train.append(
            [supplemental_set] * (repeat_num-1), ignore_index=True)
        new_train_y = train_y.append(
            [supplemental_set_y] * (repeat_num-1), ignore_index=True)
        new_train = new_train.append(
            supplemental_set.sample(remaining_num), ignore_index=True)
        new_train_y = new_train_y.append(
            supplemental_set_y.sample(remaining_num), ignore_index=True)
        return new_train, new_train_y

    def generate_drift_detection_model(self, score, optimise=True, verbose=1):
        """
        Generates the drift detection model.

        Arguments:
            score {function} -- A function that accepts a dataframe with features as columns and returns a tuple of numpy array
                of probabilities array of shape `(n_samples,n_classes)` and numpy array of prediction vector of shape `(n_samples,)`
            input_df {pandas.DataFrame} -- a pandas dataframe containing the training data.

        Keyword Arguments:
            optimise {bool} -- If True, does hyperparameter optimisation for the drift detection model (default: {False})
            verbose {int} -- Controls the logging output (default: {1})
        """

        # Split 80 20
        input_df = self.training_data_frame
        train_df = input_df[self.feature_columns]
        train_y_df = input_df[self.label_column]
        train_df, test_df, train_y_df, test_y_df = train_test_split(
            train_df, train_y_df, test_size=0.2, stratify=train_y_df, random_state=DriftDetection.RANDOM_STATE)
        train_df.reset_index(drop=True, inplace=True)
        test_df.reset_index(drop=True, inplace=True)
        train_y_df.reset_index(drop=True, inplace=True)
        test_y_df.reset_index(drop=True, inplace=True)

        # Score the training subset
        train_probabilities, train_predictions = score(train_df)

        # Prepare training data for drift detection model.
        ddm_train = pd.concat(
            [train_df, self.__get_probability_dataframe(train_probabilities)], axis=1)
        self.ddm_features = list(ddm_train.columns)
        ddm_train_y = pd.Series(train_predictions == train_y_df).replace(
            to_replace={True: 1, False: 0})

        # Balance the training data
        ddm_train, ddm_train_y = self.balance_data(ddm_train, ddm_train_y)

        features = [(feature, ColumnSelector(
            key=feature, is_categorical=feature in self.categorical_columns)) for feature in ddm_train.columns]

        if optimise:
            self.model_stage = DriftModelStage.OPTIMIZE_DRIFT_MODEL.value
            parameters = {
                "classifier__loss": ["deviance"],
                "classifier__learning_rate": [0.1, 0.15, 0.2],
                "classifier__min_samples_split": np.linspace(0.005, 0.01, 5),
                "classifier__min_samples_leaf": np.linspace(0.0005, 0.001, 5),
                "classifier__max_leaf_nodes": list(range(3, 12, 2)),
                "classifier__max_features": ["log2", "sqrt"],
                "classifier__subsample": np.linspace(0.3, 0.9, 6),
                "classifier__n_estimators": range(100, 401, 50)
            }

            model_params = {
                "random_state": DriftDetection.RANDOM_STATE,
                "verbose": 0
            }

            randomized_params = {
                "n_iter": 40,
                "scoring": "f1",
                "n_jobs": -1,
                "verbose": 4,
                "random_state": DriftDetection.RANDOM_STATE,
                "return_train_score": True
            }

            classifier = GradientBoostingClassifier(**model_params)
            pipeline = Pipeline([
                ("features", FeatureUnion(features)),
                ("classifier", classifier)
            ])

            clf = RandomizedSearchCV(pipeline, parameters, **randomized_params)
            clf.fit(ddm_train, ddm_train_y)
            self.dd_model = clf.best_estimator_
        else:
            # If total elements are less than 1M, use 0.05 as learning rate else 0.1
            learning_rate = 0.05 if ddm_train.shape[0] * \
                ddm_train.shape[1] < 1000000 else 0.1

            initial_parameters = {
                "random_state": DriftDetection.RANDOM_STATE,
                "learning_rate": learning_rate,
                "n_estimators": 1500,
                "verbose": verbose,
                "n_iter_no_change": 5,
                "min_samples_split": 0.005,
                "min_samples_leaf": 0.0005,
                "max_leaf_nodes": 10
            }

            self.model_stage = DriftModelStage.CREATE_DRIFT_MODEL.value
            classifier = GradientBoostingClassifier(**initial_parameters)
            self.dd_model = Pipeline([
                ("features", FeatureUnion(features)),
                ("classifier", classifier)
            ])

            self.dd_model.fit(ddm_train, ddm_train_y)

        # Score the test subset
        test_probabilities, test_predictions = score(test_df)

        # Calculate base client model accuracy
        self.base_client_accuracy = accuracy_score(test_y_df, test_predictions)

        # Prepare the test data to score against drift detection model
        ddm_test = pd.concat(
            [test_df, self.__get_probability_dataframe(test_probabilities)], axis=1)
        ddm_test_predictions = self.dd_model.predict(ddm_test)

        # Calculate base predicted accuracy
        self.base_predicted_accuracy = sum(
            ddm_test_predictions)/len(ddm_test_predictions)

        print("base_client_accuracy:{} and base_predicted_accuracy:{}".format(
            self.base_client_accuracy, self.base_predicted_accuracy))

    @staticmethod
    def create_model_tar(drift_detection_model, path_prefix=".", file_name="drift_detection_model.tar.gz"):
        """Creates a tar file for the drift detection model

        Arguments:
            drift_detection_model {DriftDetectionModel} -- the drift detection model to save

        Keyword Arguments:
            path_prefix {str} -- path of the directory to save the file (default: {"."})
            file_name {str} -- name of the tar file (default: {"drift_detection_model.tar.gz"})

        Raises:
            Exception: If there is an issue while creating directory, pickling the model or creating the tar file
        """
        try:
            os.makedirs(path_prefix, exist_ok=True)

            model_pkl = io.BytesIO(pickle.dumps(drift_detection_model))

            with tarfile.open(file_name, mode="w:gz") as model_tar:
                tarinfo = tarfile.TarInfo("drift_detection_model.pkl")
                tarinfo.size = len(model_pkl.getvalue())
                model_tar.addfile(tarinfo=tarinfo, fileobj=model_pkl)
        except (OSError, pickle.PickleError, tarfile.TarError):
            raise Exception(
                "There was a problem creating tar file for drift detection model.")


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Selects a column out of a dataframe. If it's a categorical column, this class also does label encoding on it.
    """

    def __init__(self, key, is_categorical=False):
        """Init Constructor

        Arguments:
            key {str} -- Key on which to select the column

        Keyword Arguments:
            categorical {bool} -- True if the column is a categorical feature (default: {False})
        """
        self.key = key
        self.is_categorical = is_categorical
        self.encoder = LabelEncoder()
        self.classes = []

    def fit(self, X, y=None):
        if self.is_categorical:
            self.encoder.fit(X[self.key])
            self.classes = self.encoder.classes_
        return self

    def transform(self, X):
        result = self.encoder.transform(
            X[self.key]) if self.is_categorical else X[self.key]
        return np.expand_dims(result, axis=1)

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class DriftModelStage(Enum):
    """Enumerated type for different stages involved in drift model creation."""
    READ_TRN_DATA = "READ_TRN_DATA"
    SCORE_TRN_DATA = "SCORE_TRN_DATA"
    CREATE_DRIFT_MODEL = "CREATE_DRIFT_MODEL"
    OPTIMIZE_DRIFT_MODEL = "OPTIMIZE_DRIFT_MODEL"
    STORE_DRIFT_MODEL = "STORE_DRIFT_MODEL"
    DRIFT_MODEL_COMPLETE = "DRIFT_MODEL_COMPLETE"
