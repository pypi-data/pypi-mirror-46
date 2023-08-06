from mindsdb.libs.helpers.general_helpers import evaluate_accuracy, get_value_bucket
from mindsdb.libs.phases.stats_generator.stats_generator import StatsGenerator
from mindsdb.libs.data_types.transaction_data import TransactionData
from mindsdb.libs.constants.mindsdb import *

class ColumnEvaluator():
    """
    # The Hypothesis Executor is responsible for testing out various scenarios
    regarding the model, in order to determine things such as the importance of
    input variables or the variability of output values
    """

    def __init__(self, transaction):
        self.normal_predictions = None
        self.transaction = transaction

    def get_column_importance(self, model, output_columns, input_columns, full_dataset, stats):
        columnless_prediction_distribution = {}
        all_columns_prediction_distribution = {}

        self.normal_predictions = model.predict('validate')
        normal_accuracy = evaluate_accuracy(self.normal_predictions, full_dataset, stats, output_columns)
        column_importance_dict = {}
        buckets_stats = {}

        # Histogram for when all columns are present, in order to plot the force vectors
        for output_column in output_columns:
            stats_generator = StatsGenerator(session=None, transaction=self.transaction)
            input_data = TransactionData()
            input_data.data_array = list(map(lambda x: [x], list(self.normal_predictions[output_column])))
            input_data.columns = [output_column]
            validation_set_output_stats = stats_generator.run(input_data=input_data, modify_light_metadata=False)

            if validation_set_output_stats is None:
                pass
            elif 'histogram' in validation_set_output_stats[output_column]:
                all_columns_prediction_distribution[output_column] = validation_set_output_stats[output_column]['histogram']

        ignorable_input_columns = []
        for input_column in input_columns:
            if stats[input_column]['data_type'] != DATA_TYPES.FILE_PATH:
                ignorable_input_columns.append(input_column)

        for input_column in ignorable_input_columns:
            # See what happens with the accuracy of the outputs if only this column is present
            ignore_columns = [col for col in ignorable_input_columns if col != input_column]
            col_only_predictions = model.predict('validate', ignore_columns)
            col_only_accuracy = evaluate_accuracy(col_only_predictions, full_dataset, stats, output_columns)

            col_only_normalized_accuracy = col_only_accuracy/normal_accuracy

            # See what happens with the accuracy if all columns but this one are present
            ignore_columns = [input_column]
            col_missing_predictions = model.predict('validate', ignore_columns)

            col_missing_accuracy = evaluate_accuracy(col_missing_predictions, full_dataset, stats, output_columns)

            col_missing_reverse_accuracy = (normal_accuracy - col_missing_accuracy)/normal_accuracy
            column_importance = (col_only_normalized_accuracy + col_missing_reverse_accuracy)/2
            column_importance_dict[input_column] = column_importance

            # Histogram for when the column is missing, in order to plot the force vectors
            for output_column in output_columns:
                if output_column not in columnless_prediction_distribution:
                    columnless_prediction_distribution[output_column] = {}
                stats_generator = StatsGenerator(session=None, transaction=self.transaction)
                input_data = TransactionData()
                input_data.data_array = list(map(lambda x: [x], list(col_missing_predictions[output_column])))
                input_data.columns = [output_column]
                col_missing_output_stats = stats_generator.run(input_data=input_data, modify_light_metadata=False)

                if col_missing_output_stats is None:
                    pass
                elif 'histogram' in col_missing_output_stats[output_column]:
                    columnless_prediction_distribution[output_column][input_column] = col_missing_output_stats[output_column]['histogram']

            # If this coulmn is either very important or not important at all, compute stats for each of the buckets (in the validation data)
            if column_importance > 0.8 or column_importance < 0.2:
                split_data = {}
                for value in full_dataset[input_column]:

                    if 'percentage_buckets' in stats[input_column]:
                        bucket = stats[input_column]['percentage_buckets']
                    else:
                        bucket = None

                    vb = get_value_bucket(value, bucket, stats[input_column])
                    if f'{input_column}_bucket_{vb}' not in split_data:
                        split_data[f'{input_column}_bucket_{vb}'] = []

                    split_data[f'{input_column}_bucket_{vb}'].append(value)

                row_wise_data = []
                max_length = max(list(map(len, split_data.values())))

                columns = []
                for i in range(max_length):
                    row_wise_data.append([])
                    for k in split_data.keys():
                        # If the sub bucket has less than 6 values, it's no relevant
                        if len(split_data[k]) > 6:
                            columns.append(k)
                            if len(split_data[k]) > i:
                                row_wise_data[-1].append(split_data[k][i])
                            else:
                                row_wise_data[-1].append(None)

                input_data = TransactionData()
                input_data.data_array = row_wise_data
                input_data.columns = columns

                stats_generator = StatsGenerator(session=None, transaction=self.transaction)
                col_buckets_stats = stats_generator.run(input_data=input_data, modify_light_metadata=False)

                buckets_stats.update(col_buckets_stats)

        return column_importance_dict, buckets_stats, columnless_prediction_distribution, all_columns_prediction_distribution

    def get_column_influence(self):
        pass









#
