from pandas import DataFrame
import statsmodels.stats.multicomp as multicomp
from scipy import stats

class MultipleComparisons:
	def __init__(self, data, dependent_variable_column, independent_group_column):
		"""
		:param DataFrame data: input dataframe
		:param str dependent_variable_column: name of the column representing the dependent variable
		:param str independent_group_column: name of the column Comparison test should be run on
		"""
		self._independent_group_column = None
		self._dependent_variable_column = dependent_variable_column
		self._data = None
		self.independent_group_column = independent_group_column
		self.data = data


	def reset(self):
		self._comparisons = None
		self._table = None

	@property
	def dependent_variable_column(self):
		return self._dependent_variable_column

	@dependent_variable_column.setter
	def dependent_variable_column(self, dependent_variable_column):
		self._dependent_variable_column = dependent_variable_column
		self.reset()

	@property
	def independent_group_column(self):
		return self._independent_group_column

	@independent_group_column.setter
	def independent_group_column(self, group_column):
		self._independent_group_column = group_column
		self.reset()

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return self._data

	@data.setter
	def data(self, data):
		self._data = data.copy()

	@property
	def comparisons(self):
		if self._comparisons is None:
			self._comparisons = multicomp.MultiComparison(
				self.data[self.dependent_variable_column],
				self.data[self.independent_group_column]
			)
		return self._comparisons

	def get_tukey_results(self, as_dataframe=True, **kwargs):
		results = self.comparisons.tukeyhsd(**kwargs)
		if not as_dataframe:
			return results
		else:
			return DataFrame(data=results._results_table.data[1:], columns=results._results_table.data[0])

	def get_bonferroni_results(self, as_dataframe=True, **kwargs):
		results = self.comparisons.allpairtest(stats.ttest_rel, method='Holm', **kwargs)
		if not as_dataframe:
			return results
		else:
			return DataFrame(data=results._results_table.data[1:], columns=results._results_table.data[0])

