from openhltest_client.base import Base


class Random(Base):
	"""The repeatable random pattern.
	"""
	YANG_NAME = 'random'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Max": "max", "Step": "step", "Seed": "seed", "Min": "min"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Random, self).__init__(parent)

	@property
	def Min(self):
		"""The minimum random value of the random pattern

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('min')
	@Min.setter
	def Min(self, value):
		return self._set_value('min', value)

	@property
	def Max(self):
		"""The maximum random value of the random pattern

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('max')
	@Max.setter
	def Max(self, value):
		return self._set_value('max', value)

	@property
	def Step(self):
		"""The step value of the random pattern

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('step')
	@Step.setter
	def Step(self, value):
		return self._set_value('step', value)

	@property
	def Seed(self):
		"""The seed value of the random pattern

		Getter Returns:
			uint32

		Setter Allows:
			uint32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('seed')
	@Seed.setter
	def Seed(self, value):
		return self._set_value('seed', value)

