from openhltest_client.base import Base


class Increment(Base):
	"""TBD
	"""
	YANG_NAME = 'increment'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"To": "to", "Step": "step", "From": "from"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Increment, self).__init__(parent)

	@property
	def From(self):
		"""Starting increment value for frame length

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('from')
	@From.setter
	def From(self, value):
		return self._set_value('from', value)

	@property
	def To(self):
		"""Maximum increment value for frame length

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('to')
	@To.setter
	def To(self, value):
		return self._set_value('to', value)

	@property
	def Step(self):
		"""Step increment value for frame length

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('step')
	@Step.setter
	def Step(self, value):
		return self._set_value('step', value)

