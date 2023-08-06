from openhltest_client.base import Base


class Bfdv6Statistics(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/bfdv6-statistics resource.
	"""
	YANG_NAME = 'bfdv6-statistics'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'device-name'
	YANG_PROPERTY_MAP = {"PortName": "port-name", "DeviceName": "device-name", "RxCount": "rx-count", "TxCount": "tx-count"}

	def __init__(self, parent):
		super(Bfdv6Statistics, self).__init__(parent)

	@property
	def DeviceName(self):
		"""Device name

		Getter Returns:
			string
		"""
		return self._get_value('device-name')

	@property
	def PortName(self):
		"""An abstract test port name

		Getter Returns:
			string
		"""
		return self._get_value('port-name')

	@property
	def TxCount(self):
		"""Number of BFD packets sent on this router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-count')

	@property
	def RxCount(self):
		"""Number of BFD packets received on this router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-count')

	def create(self, DeviceName, PortName=None, TxCount=None, RxCount=None):
		"""Create an instance of the `bfdv6-statistics` resource

		Args:
			DeviceName (string): Device name
			PortName (string): An abstract test port name
			TxCount (uint64): Number of BFD packets sent on this router.
			RxCount (uint64): Number of BFD packets received on this router.
		"""
		return self._create(locals())

	def read(self, DeviceName=None):
		"""Get `bfdv6-statistics` resource(s). Returns all resources from the server if `DeviceName` is not specified

		"""
		return self._read(DeviceName)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `bfdv6-statistics` resource

		"""
		return self._delete()

	def update(self, PortName=None, TxCount=None, RxCount=None):
		"""Update the current instance of the `bfdv6-statistics` resource

		Args:
			PortName (string): An abstract test port name
			TxCount (uint64): Number of BFD packets sent on this router.
			RxCount (uint64): Number of BFD packets received on this router.
		"""
		return self._update(locals())

