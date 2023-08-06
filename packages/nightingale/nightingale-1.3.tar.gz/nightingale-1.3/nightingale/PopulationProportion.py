# source: https://onlinecourses.science.psu.edu/stat100/node/56/
# source: http://www.dummies.com/education/math/statistics/how-to-determine-the-confidence-interval-for-a-population-proportion/

# main python libraries
import math

# idin's libraries
import slytherin.numbers as sn

# this library
from .get_z_score import get_z_score

def percent_str(x):
	return f"{round(x*100, ndigits=2)}%"

def get_population_proportion_error(group_n, sample_n, confidence=0.95):
	p = group_n/sample_n
	if p>1 or p<0: raise ValueError(f'p={p} is an invalid value.')
	standard_error = math.sqrt(p*(1-p)/sample_n)
	return standard_error*get_z_score(confidence=confidence)



class PopulationProportion:
	def __init__(self, sample_n, group_n=None, group_proportion=0.5):
		if group_n is None and group_proportion is None:
			raise ValueError('group_n and group_proportion cannot both be None.')

		if group_n is None:
			group_n = sample_n*group_proportion

		self._group_n = group_n
		self._sample_n = sample_n

	@property
	def p(self):
		return self._group_n/self._sample_n

	def get_error(self, confidence=0.95):
		return get_population_proportion_error(group_n=self._group_n, sample_n=self._sample_n, confidence=confidence)

	def get_interval_str(self, confidence=0.95):
		return f'{percent_str(self.p)} ± {percent_str(self.get_error(confidence=confidence))}'
