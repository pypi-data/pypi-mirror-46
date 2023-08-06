from openhltest_client.base import Base


class Increment(Base):
	"""The values that make up the increment pattern
	"""
	YANG_NAME = 'increment'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Start": "start", "Step": "step"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Increment, self).__init__(parent)

	@property
	def Start(self):
		"""The start value of the increment pattern

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('start')
	@Start.setter
	def Start(self, value):
		return self._set_value('start', value)

	@property
	def Step(self):
		"""The step value of the increment pattern

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

