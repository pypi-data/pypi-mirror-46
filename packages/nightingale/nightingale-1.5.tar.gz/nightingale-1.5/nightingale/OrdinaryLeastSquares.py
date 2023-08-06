from pandas import DataFrame
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

class OrdinaryLeastSquares:
	def __init__(self, data, formula):
		"""
		:param DataFrame data: input dataframe
		:param str formula: formula such as "v1 ~ v2 + v3 * v4" where v1 is the dependent variable
		"""
		self._formula = None
		self._data = None
		self.formula = formula
		self.data = data
		model = self.model
		fit = self.fit
		table = self.table

	def reset(self):
		self._model = None
		self._fit = None
		self._table = None


	@property
	def formula(self):
		return self._formula

	@formula.setter
	def formula(self, formula):
		self._formula = formula
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
		self.reset()

	@property
	def model(self):
		if self._model is None:
			self._model = ols(formula=self.formula, data=self.data)
		return self._model

	@property
	def fit(self):
		if self._fit is None:
			self._fit = self.model.fit()
		return self._fit

	@property
	def table2(self):
		"""
		:rtype: DataFrame
		"""
		if self._table is None:
			self._table = anova_lm(self.fit)
		return self._table

	@property
	def r_squared(self):
		return self.fit.rsquared

	@property
	def adjusted_r_squared(self):
		return self.fit.rsquared_adj

	@property
	def degrees_of_freedom(self):
		return self.model.df_model

	@property
	def summary2(self):
		return self.fit.summary2()

	@property
	def summary(self):
		return self.fit.summary()

	@property
	def table(self):
		return self.summary2.tables[1]
