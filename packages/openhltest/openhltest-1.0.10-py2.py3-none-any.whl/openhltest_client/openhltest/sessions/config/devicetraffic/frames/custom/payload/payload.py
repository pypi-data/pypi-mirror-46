from openhltest_client.base import Base


class Payload(Base):
	"""TBD
	"""
	YANG_NAME = 'payload'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Length": "length", "Repeat": "repeat", "Data": "data"}

	def __init__(self, parent):
		super(Payload, self).__init__(parent)

	@property
	def Data(self):
		"""TBD

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('data')
	@Data.setter
	def Data(self, value):
		return self._set_value('data', value)

	@property
	def Repeat(self):
		"""Repeat the payload data to fill the length specified

		Getter Returns:
			boolean

		Setter Allows:
			boolean

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('repeat')
	@Repeat.setter
	def Repeat(self, value):
		return self._set_value('repeat', value)

	@property
	def Length(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('length')
	@Length.setter
	def Length(self, value):
		return self._set_value('length', value)

	def update(self, Data=None, Repeat=None, Length=None):
		"""Update the current instance of the `payload` resource

		Args:
			Data (string): TBD
			Repeat (boolean): Repeat the payload data to fill the length specified
			Length (int32): TBD
		"""
		return self._update(locals())

