TOTAL_PREDICTIONS_PROVIDED = 'total_predictions_provided'
RESULTS = 'results'


class StatsCollector:
    '''
    Class responsible for collecting stats on prediction model
    '''

    def __init__(self):
        self.stats = {
            TOTAL_PREDICTIONS_PROVIDED: 0,
            RESULTS: {

            }
        }

    def total_predictions_provided_inc(self):
        self.stats[TOTAL_PREDICTIONS_PROVIDED] = self.stats[TOTAL_PREDICTIONS_PROVIDED] + 1

    def result_inc(self, result_str):
        if result_str in self.stats[RESULTS]:
            self.stats[RESULTS][result_str] = self.stats[RESULTS][result_str] + 1
            return

        self.stats[RESULTS][result_str] = 1

    def get_total_predictions_provided(self):
        return self.stats[TOTAL_PREDICTIONS_PROVIDED]

    def get_results(self):
        return self.stats[RESULTS]

    def reset(self):
        self.stats[TOTAL_PREDICTIONS_PROVIDED] = 0
        self.stats[RESULTS] = {}
