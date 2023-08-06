from openhltest_client.base import Base


class AutoNegotiationCapabilities(Base):
	"""When auto negotiation is enabled the following speeds and duplex can be advertised
	"""
	YANG_NAME = 'auto-negotiation-capabilities'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"Advertise100mFd": "advertise-100m-fd", "Advertise1000g": "advertise-1000g", "Advertise10mHd": "advertise-10m-hd", "Advertise100mHd": "advertise-100m-hd", "Advertise10mFd": "advertise-10m-fd"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(AutoNegotiationCapabilities, self).__init__(parent)

	@property
	def Advertise1000g(self):
		"""TBD

		Getter Returns:
			boolean

		Setter Allows:
			boolean

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('advertise-1000g')
	@Advertise1000g.setter
	def Advertise1000g(self, value):
		return self._set_value('advertise-1000g', value)

	@property
	def Advertise100mFd(self):
		"""TBD

		Getter Returns:
			boolean

		Setter Allows:
			boolean

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('advertise-100m-fd')
	@Advertise100mFd.setter
	def Advertise100mFd(self, value):
		return self._set_value('advertise-100m-fd', value)

	@property
	def Advertise100mHd(self):
		"""TBD

		Getter Returns:
			boolean

		Setter Allows:
			boolean

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('advertise-100m-hd')
	@Advertise100mHd.setter
	def Advertise100mHd(self, value):
		return self._set_value('advertise-100m-hd', value)

	@property
	def Advertise10mFd(self):
		"""TBD

		Getter Returns:
			boolean

		Setter Allows:
			boolean

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('advertise-10m-fd')
	@Advertise10mFd.setter
	def Advertise10mFd(self, value):
		return self._set_value('advertise-10m-fd', value)

	@property
	def Advertise10mHd(self):
		"""TBD

		Getter Returns:
			boolean

		Setter Allows:
			boolean

		Setter Raises:
			ValueError
			InvalidValueError
		"""
		return self._get_value('advertise-10m-hd')
	@Advertise10mHd.setter
	def Advertise10mHd(self, value):
		return self._set_value('advertise-10m-hd', value)

	def update(self, Advertise1000g=None, Advertise100mFd=None, Advertise100mHd=None, Advertise10mFd=None, Advertise10mHd=None):
		"""Update the current instance of the `auto-negotiation-capabilities` resource

		Args:
			Advertise1000g (boolean): TBD
			Advertise100mFd (boolean): TBD
			Advertise100mHd (boolean): TBD
			Advertise10mFd (boolean): TBD
			Advertise10mHd (boolean): TBD
		"""
		return self._update(locals())

