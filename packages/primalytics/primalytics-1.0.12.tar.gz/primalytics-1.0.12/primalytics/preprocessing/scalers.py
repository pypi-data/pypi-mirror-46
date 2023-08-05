import numpy
import pandas


class Scaler:
	def __init__(self, scaler):
		self.__scaler = scaler
		self.__fitted = False
		self.__fit_variables = None

	def fit(self, df: pandas.DataFrame, variables):
		self.__fit_variables = variables
		self.__scaler.fit(df[self.__fit_variables])
		self.__fitted = True

	def transform(self, df):
		if self.__fitted:
			if isinstance(df, dict):
				transformed = dict(zip(self.__fit_variables, self.__scaler.transform([[df[variable] for variable in self.__fit_variables]])[0]))
				transformed.update({variable: value for variable, value in df.items() if variable not in self.__fit_variables})
				transformed = {variable: transformed[variable] for variable in df.keys()}

			elif isinstance(df, pandas.DataFrame):
				original_variables = list(df.columns)
				other_variables = list(df.columns.difference(self.__fit_variables))
				transformed = self.__scaler.transform(df[self.__fit_variables])
				transformed = df[other_variables].join(pandas.DataFrame(transformed, index=df.index, columns=self.__fit_variables))[original_variables]

			elif isinstance(df, numpy.ndarray):
				transformed = self.__scaler.transform(df)

			else:
				raise Exception('Type {} is invalid for scaling transformation'.format(type(df)))

		else:
			raise Exception('Scaler not fitted')

		return transformed

	def fit_transform(self, df, variables):
		self.fit(df, variables)
		return self.transform(df)


class MultiDimStandardScaler:
	def __init__(self):
		self._mean = None
		self._var = None
		self._std = None
		self.__fitted = None

	def fit(self, df):
		if isinstance(df, pandas.DataFrame):
			data = df.values
		else:
			data = df.copy()

		self._mean = numpy.mean(data, axis=0)
		self._var = numpy.var(data, axis=0)
		self._std = numpy.sqrt(self._var)
		self.__fitted = True

	def transform(self, df):
		if self.__fitted:
			sample_len = len(df)
			scaled = df - numpy.array([self._mean for _ in range(sample_len)])
			scaled = scaled / numpy.array([self._std for _ in range(sample_len)])
		else:
			raise Exception('Scaler not fitted.')

		return scaled

	def fit_transform(self, df):
		self.fit(df)
		return self.transform(df)
