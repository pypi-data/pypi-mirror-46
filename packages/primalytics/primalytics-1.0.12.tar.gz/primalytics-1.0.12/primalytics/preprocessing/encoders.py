import numpy
import pandas
from sklearn.feature_extraction import FeatureHasher


class Hasher:
	def __init__(self, categoricals: list, n_min_features: int=2, n_attempt_max: int=3, n_attempt_tot_max: int=30, verbose: bool=False):
		self._categoricals = categoricals
		self._hashing_dict = {}
		self._hashing_cols = {}
		self._n_min_features = n_min_features
		self._n_attempt_max = n_attempt_max
		self._n_attempt_tot_max = n_attempt_tot_max
		self.__fitted = False
		self._verbose = verbose

	def fit(self, df: pandas.DataFrame, return_hashing_cols: bool=False):
		self.__fitted = False

		for variable in self._categoricals:
			if self._verbose:
				print('Fitting', variable)
			self.__get_hashing(df, variable)

		self.__fitted = True
		if return_hashing_cols:
			return self._hashing_cols

	def transform(self, data, array_indices=None):
		if not self.__fitted:
			raise FitError('Hasher class not fitted')

		is_df = isinstance(data, pandas.DataFrame)
		is_series = isinstance(data, pandas.Series)
		is_dict = isinstance(data, dict)
		is_array = isinstance(data, numpy.ndarray)

		if is_df:
			transformed = data[data.columns.difference(self._categoricals)]
			original_columns = list(data.columns)
		elif is_series:
			transformed = data[data.index.difference(self._categoricals)]
			original_columns = list(data.index)
		elif is_dict:
			transformed = data.copy()
			original_columns = list(data.keys())
		elif is_array:
			if array_indices is None:
				raise MissingIndicesError('Missing indices for array transformation')
			transformed = numpy.array([])
			original_columns = []
		else:
			raise TypeError('Type not valid for transformation')

		if is_df or is_series:
			final_columns = []
			for variable in original_columns:
				if variable in self._categoricals:
					final_columns += self._hashing_cols[variable]

					if self._verbose:
						print('Transforming', variable)
					if is_series:
						transformed = transformed.append(pandas.Series(self._hashing_dict[variable][data[variable]], index=self._hashing_cols[variable]))
					else:
						transformed = transformed.join(pandas.DataFrame(list(data[variable].apply(lambda x: self._hashing_dict[variable][x])), index=data.index, columns=self._hashing_cols[variable]))
				else:
					final_columns.append(variable)

			transformed = transformed[final_columns]
			transformed = transformed[final_columns]

		elif is_dict:
			for variable in self._categoricals:
				if self._verbose:
					print('Transforming', variable)

				n_new_columns = len(list(self._hashing_dict[variable].values())[0])
				columns = [variable + '_H' + str(i) for i in range(n_new_columns)]
				value = transformed.pop(variable)
				try:
					hashing_values = self._hashing_dict[variable][value]
				except KeyError:
					raise HashingError('Value \'{}\' not found in hashing dict for variable \'{}\'.'.format(value, variable))

				transformed.update({columns[i]: float(v) for i, v in enumerate(hashing_values)})

		elif is_array:
			for index in range(len(data)):
				if index in array_indices.keys():
					variable = array_indices[index]
					try:
						transformed = numpy.append(transformed, numpy.array(self._hashing_dict[variable][data[index]]))
					except KeyError:
						raise HashingError('Value \'{}\' not found in hashing dict for variable \'{}\'.'.format(data[index], variable))
				else:
					numpy.append(transformed, data[index])
		else:
			raise TypeError('Type not valid for transformation')

		return transformed

	def fit_transform(self, df: pandas.DataFrame):
		self.fit(df)
		return self.transform(df)

	def __get_hashing(self, df: pandas.DataFrame, variable: str):
		n_features = self._n_min_features
		n_attempt = 0
		n_attempt_tot = 0
		lost = -1
		non_trivial = False
		uniques = df.loc[:, variable].unique()
		hashed_matrix = [[]]

		while (lost != 0 or not non_trivial) and n_attempt_tot < self._n_attempt_tot_max:
			non_trivial = False
			feature_hasher = FeatureHasher(input_type='string', n_features=n_features)
			keys_list = list(map(lambda x: str(x) + str(numpy.random.rand())[2:8], uniques))

			hashed_matrix = feature_hasher.fit_transform(keys_list).toarray().astype(int)
			hashed_code = set(map(lambda x: ''.join(x.astype(str)), hashed_matrix))

			lost = len(hashed_code) - len(uniques)

			n_attempt += 1
			n_attempt_tot += 1

			if n_attempt == self._n_attempt_max:
				n_attempt = 0
				n_features += 1

			if min(numpy.var(hashed_matrix, axis=0)) > 0:
				non_trivial = True

		if lost != 0 or not non_trivial:
			raise HashingError('Hashing failed on variable: {}. Lost: {}. Trivial: {}.'.format(variable, lost, not non_trivial))

		else:
			tmp_hashing_dict = dict(zip(uniques, map(list, hashed_matrix)))
			self._hashing_dict.update({variable: tmp_hashing_dict})
			self._hashing_cols.update({variable: ['{}_H{}'.format(variable, i) for i in range(hashed_matrix.shape[1])]})


class HashingError(Exception):
	""":raises Error when hashing is invalid"""


class FitError(Exception):
	""":raises Error when class Hasher is not fitted"""


class MissingIndicesError(Exception):
	""":raises Error when indices are missing"""
