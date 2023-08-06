from .get_z_score import get_z_score
def get_sample_size(population_size, confidence=0.95, error_margin=0.05, group_proportion=0.5):
	# group_proportion = group_n/sample_n # 0.5 is the worst case scenario
	p = group_proportion
	sample_size = p*(1-p)/((error_margin/get_z_score(confidence=confidence))**2)
	true_sample = (sample_size*population_size)/(sample_size + population_size - 1)
	return true_sample




