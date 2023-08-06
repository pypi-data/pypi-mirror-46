from openhltest_client.base import Base


class Random(Base):
	"""Random frame size options
	"""
	YANG_NAME = 'random'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Max": "max", "Min": "min"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Random, self).__init__(parent)

	@property
	def Max(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('max')
	@Max.setter
	def Max(self, value):
		return self._set_value('max', value)

	@property
	def Min(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('min')
	@Min.setter
	def Min(self, value):
		return self._set_value('min', value)

	def update(self, Max=None, Min=None):
		"""Update the current instance of the `random` resource

		Args:
			Max (int32): TBD
			Min (int32): TBD
		"""
		return self._update(locals())

