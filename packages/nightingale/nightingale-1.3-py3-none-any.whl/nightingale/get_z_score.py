import scipy.stats as st

# source: https://stackoverflow.com/questions/20864847/probability-to-z-score-and-vice-versa-in-python
def get_z_score(confidence):
	"""
	gets confidence interval (e.g., 0.95) and returns z-score (e.g., 1.96)
	:type confidence: float
	:rtype: float
	"""
	return st.norm.ppf(confidence/2+0.5)