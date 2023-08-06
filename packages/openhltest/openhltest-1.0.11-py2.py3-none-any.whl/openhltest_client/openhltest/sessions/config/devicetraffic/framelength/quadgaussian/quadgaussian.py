from openhltest_client.base import Base


class QuadGaussian(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/config/device-traffic/frame-length/quad-gaussian resource.
	"""
	YANG_NAME = 'quad-gaussian'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"WidthAtHalf": "width-at-half", "Name": "name", "Weight": "weight", "Center": "center"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(QuadGaussian, self).__init__(parent)

	@property
	def Name(self):
		"""TBD

		Getter Returns:
			string

		Setter Allows:
			string

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('name')

	@property
	def Center(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('center')
	@Center.setter
	def Center(self, value):
		return self._set_value('center', value)

	@property
	def WidthAtHalf(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('width-at-half')
	@WidthAtHalf.setter
	def WidthAtHalf(self, value):
		return self._set_value('width-at-half', value)

	@property
	def Weight(self):
		"""TBD

		Getter Returns:
			int32

		Setter Allows:
			int32

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('weight')
	@Weight.setter
	def Weight(self, value):
		return self._set_value('weight', value)

	def create(self, Name, Center=None, WidthAtHalf=None, Weight=None):
		"""Create an instance of the `quad-gaussian` resource

		Args:
			Name (string): TBD
			Center (int32): TBD
			WidthAtHalf (int32): TBD
			Weight (int32): TBD
		"""
		return self._create(locals())

	def read(self, Name=None):
		"""Get `quad-gaussian` resource(s). Returns all resources from the server if `Name` is not specified

		"""
		return self._read(Name)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `quad-gaussian` resource

		"""
		return self._delete()

	def update(self, Center=None, WidthAtHalf=None, Weight=None):
		"""Update the current instance of the `quad-gaussian` resource

		Args:
			Center (int32): TBD
			WidthAtHalf (int32): TBD
			Weight (int32): TBD
		"""
		return self._update(locals())

