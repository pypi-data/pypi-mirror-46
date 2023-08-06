from openhltest_client.base import Base


class PhysicalPort(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/physical-port resource.
	"""
	YANG_NAME = 'physical-port'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'port-name'
	YANG_PROPERTY_MAP = {"ConnectedTestPortId": "connected-test-port-id", "ConnectionStateDetails": "connection-state-details", "ConnectedTestPortDescription": "connected-test-port-description", "ConnectionState": "connection-state", "PortName": "port-name", "Speed": "speed"}

	def __init__(self, parent):
		super(PhysicalPort, self).__init__(parent)

	@property
	def PortName(self):
		"""An abstract test port name

		Getter Returns:
			string
		"""
		return self._get_value('port-name')

	@property
	def ConnectedTestPortId(self):
		"""The id of the connected test port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			string
		"""
		return self._get_value('connected-test-port-id')

	@property
	def ConnectedTestPortDescription(self):
		"""Free form vendor specific description of the connected test port.
		Can include details such as make/model/productId of the underlying hardware.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			string
		"""
		return self._get_value('connected-test-port-description')

	@property
	def ConnectionState(self):
		"""The state of the connection to the physical hardware
		test port or virtual machine test port

		Getter Returns:
			CONNECTING | CONNECTED_LINK_UP | CONNECTED_LINK_DOWN | DISCONNECTING | DISCONNECTED
		"""
		return self._get_value('connection-state')

	@property
	def ConnectionStateDetails(self):
		"""Free form vendor specific information about the state of the connection to
		the physical hardware test port or virtual machine test port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			string
		"""
		return self._get_value('connection-state-details')

	@property
	def Speed(self):
		"""The actual speed of the test port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			string
		"""
		return self._get_value('speed')

	def create(self, PortName, ConnectedTestPortId=None, ConnectedTestPortDescription=None, ConnectionState=None, ConnectionStateDetails=None, Speed=None):
		"""Create an instance of the `physical-port` resource

		Args:
			PortName (string): An abstract test port name
			ConnectedTestPortId (string): The id of the connected test port.Empty if the abstract port is not connected to a test port.
			ConnectedTestPortDescription (string): Free form vendor specific description of the connected test port.Can include details such as make/model/productId of the underlying hardware.Empty if the abstract port is not connected to a test port.
			ConnectionState (enumeration): The state of the connection to the physical hardwaretest port or virtual machine test port
			ConnectionStateDetails (string): Free form vendor specific information about the state of the connection tothe physical hardware test port or virtual machine test port.Empty if the abstract port is not connected to a test port.
			Speed (string): The actual speed of the test port.Empty if the abstract port is not connected to a test port.
		"""
		return self._create(locals())

	def read(self, PortName=None):
		"""Get `physical-port` resource(s). Returns all resources from the server if `PortName` is not specified

		"""
		return self._read(PortName)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `physical-port` resource

		"""
		return self._delete()

	def update(self, ConnectedTestPortId=None, ConnectedTestPortDescription=None, ConnectionState=None, ConnectionStateDetails=None, Speed=None):
		"""Update the current instance of the `physical-port` resource

		Args:
			ConnectedTestPortId (string): The id of the connected test port.Empty if the abstract port is not connected to a test port.
			ConnectedTestPortDescription (string): Free form vendor specific description of the connected test port.Can include details such as make/model/productId of the underlying hardware.Empty if the abstract port is not connected to a test port.
			ConnectionState (enumeration): The state of the connection to the physical hardwaretest port or virtual machine test port
			ConnectionStateDetails (string): Free form vendor specific information about the state of the connection tothe physical hardware test port or virtual machine test port.Empty if the abstract port is not connected to a test port.
			Speed (string): The actual speed of the test port.Empty if the abstract port is not connected to a test port.
		"""
		return self._update(locals())

