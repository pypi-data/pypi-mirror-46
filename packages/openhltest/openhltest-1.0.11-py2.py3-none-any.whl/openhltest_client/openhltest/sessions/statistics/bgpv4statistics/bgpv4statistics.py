from openhltest_client.base import Base


class Bgpv4Statistics(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/bgpv4-statistics resource.
	"""
	YANG_NAME = 'bgpv4-statistics'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'device-name'
	YANG_PROPERTY_MAP = {"TxNotifyCode": "tx-notify-code", "TxWithdrawnUpdateCount": "tx-withdrawn-update-count", "RxAdvertiseRouteCount": "rx-advertise-route-count", "TxRtConstraintCount": "tx-rt-constraint-count", "TxNotifySubCode": "tx-notify-sub-code", "RxOpenCount": "rx-open-count", "TxOpenCount": "tx-open-count", "TxKeepaliveCount": "tx-keepalive-count", "RxRouteRefreshCount": "rx-route-refresh-count", "DeviceName": "device-name", "TxWithdrawRouteCount": "tx-withdraw-route-count", "RxNotifySubCode": "rx-notify-sub-code", "RxAdvertiseUpdateCount": "rx-advertise-update-count", "RxNotifyCode": "rx-notify-code", "TxAdvertiseUpdateCount": "tx-advertise-update-count", "LastRxUpdateRouteCount": "last-rx-update-route-count", "OutstandingRouteCount": "outstanding-route-count", "SessionUpCount": "session-up-count", "TxAdvertiseRouteCount": "tx-advertise-route-count", "RxWithdrawRouteCount": "rx-withdraw-route-count", "TxRouteRefreshCount": "tx-route-refresh-count", "TxNotificationCount": "tx-notification-count", "RouterState": "router-state", "RxNotificationCount": "rx-notification-count", "RxKeepaliveCount": "rx-keepalive-count", "PortName": "port-name", "RxRtConstraintCount": "rx-rt-constraint-count"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Bgpv4Statistics, self).__init__(parent)

	@property
	def DeviceName(self):
		"""Abstract emulated bgpv4 device name

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
	def RouterState(self):
		"""The state of the connection to the physical hardware
		test port or virtual machine test port
		 NONE	No state.
		 IDLE	Prior to invoking Open_BgpSession or Start_Router, an emulated router is in the Idle state.
		 CONNECT	Connecting.
		 ACTIVE	Active.
		 OPEN_SENT	Open is sent.
		 OPEN_CONFIRM	Open is confirmed.
		 ESTABLISHED	Session is confirmed by the peer. The router state is Established.

		Getter Returns:
			IDLE | CONNECTING | ESTABLISHED | NONE | CONNECT | OPEN_SENT | OPEN_CONFIRM | ACTIVE
		"""
		return self._get_value('router-state')

	@property
	def TxAdvertiseRouteCount(self):
		"""The total number of frames transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-advertise-route-count')

	@property
	def RxAdvertiseRouteCount(self):
		"""The total number of frames received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-advertise-route-count')

	@property
	def TxWithdrawRouteCount(self):
		"""The total number of frames transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-withdraw-route-count')

	@property
	def RxWithdrawRouteCount(self):
		"""The total number of frames received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-withdraw-route-count')

	@property
	def LastRxUpdateRouteCount(self):
		"""Number of routes in the last-received UPDATE message.

		Getter Returns:
			uint64
		"""
		return self._get_value('last-rx-update-route-count')

	@property
	def OutstandingRouteCount(self):
		"""Number of routes that should be in the DUT'scurrent route table.

		Getter Returns:
			uint64
		"""
		return self._get_value('outstanding-route-count')

	@property
	def RxAdvertiseUpdateCount(self):
		"""Received update packet count. Number of Update packets received fromDUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-advertise-update-count')

	@property
	def RxKeepaliveCount(self):
		"""BGP KeepAlive count received. Total number of KeepAlive packets receivedfrom
		the DUT during the test. 

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-keepalive-count')

	@property
	def RxNotificationCount(self):
		"""BGP Notification count received. Number of Notification packets received by
		the emulated router during the test.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-notification-count')

	@property
	def RxNotifyCode(self):
		"""BGP Notify code received. The last NOTIFICATION code the emulated routerreceived from the DUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-notify-code')

	@property
	def RxNotifySubCode(self):
		"""BGP Notify subcode received. Each NOTIFICATION code has a sub-code. 

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-notify-sub-code')

	@property
	def RxOpenCount(self):
		"""BGP Open message count received. Opens received from DUT. In stable BGP
		scenarios, this should match the value in the previous field. 

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-open-count')

	@property
	def RxRouteRefreshCount(self):
		"""Number of advertised route refresh message received.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-route-refresh-count')

	@property
	def RxRtConstraintCount(self):
		"""Number of RT-Constraint routes received for this router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-rt-constraint-count')

	@property
	def SessionUpCount(self):
		"""Number of router sessions within the router block in the Establishedstate.

		Getter Returns:
			uint64
		"""
		return self._get_value('session-up-count')

	@property
	def TxAdvertiseUpdateCount(self):
		"""Advertised update route count transmitted. Total number of UPDATE packetswith
		feasible routes sent to the DUT. 

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-advertise-update-count')

	@property
	def TxKeepaliveCount(self):
		"""BGP KeepAlive count transmitted. Total number of KEEPALIVE packets sent to
		the DUT during test. 

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-keepalive-count')

	@property
	def TxNotificationCount(self):
		"""BGP Notification count transmitted. Number of Notification packets sent
		from the emulated router. 

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-notification-count')

	@property
	def TxNotifyCode(self):
		"""BGP Notify code transmitted. Last Notification code the emulated router
		sent to the DUT.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-notify-code')

	@property
	def TxNotifySubCode(self):
		"""BGP Notify subcode received. Each NOTIFICATION code has a sub-code. 

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-notify-sub-code')

	@property
	def TxOpenCount(self):
		"""BGP Open message count transmitted. Total number of OPEN packets sent tothe DUT.
		Initial one, plus number of times the emulated router re-establishessessions. 

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-open-count')

	@property
	def TxRouteRefreshCount(self):
		""" Number of advertised route refresh message transmitted.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-route-refresh-count')

	@property
	def TxRtConstraintCount(self):
		"""Number of RT-Constraint routes transmitted for this router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-rt-constraint-count')

	@property
	def TxWithdrawnUpdateCount(self):
		"""Withdrawn update route count transmitted. Total number of UPDATE packetswith unfeasible
		routes sent to the DUT (route flapping).  

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-withdrawn-update-count')

	def create(self, DeviceName, PortName=None, RouterState=None, TxAdvertiseRouteCount=None, RxAdvertiseRouteCount=None, TxWithdrawRouteCount=None, RxWithdrawRouteCount=None, LastRxUpdateRouteCount=None, OutstandingRouteCount=None, RxAdvertiseUpdateCount=None, RxKeepaliveCount=None, RxNotificationCount=None, RxNotifyCode=None, RxNotifySubCode=None, RxOpenCount=None, RxRouteRefreshCount=None, RxRtConstraintCount=None, SessionUpCount=None, TxAdvertiseUpdateCount=None, TxKeepaliveCount=None, TxNotificationCount=None, TxNotifyCode=None, TxNotifySubCode=None, TxOpenCount=None, TxRouteRefreshCount=None, TxRtConstraintCount=None, TxWithdrawnUpdateCount=None):
		"""Create an instance of the `bgpv4-statistics` resource

		Args:
			DeviceName (string): Abstract emulated bgpv4 device name
			PortName (string): An abstract test port name
			RouterState (enumeration): The state of the connection to the physical hardwaretest port or virtual machine test port NONENo state. IDLEPrior to invoking Open_BgpSession or Start_Router, an emulated router is in the Idle state. CONNECTConnecting. ACTIVEActive. OPEN_SENTOpen is sent. OPEN_CONFIRMOpen is confirmed. ESTABLISHEDSession is confirmed by the peer. The router state is Established.
			TxAdvertiseRouteCount (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxAdvertiseRouteCount (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			TxWithdrawRouteCount (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxWithdrawRouteCount (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			LastRxUpdateRouteCount (uint64): Number of routes in the last-received UPDATE message.
			OutstandingRouteCount (uint64): Number of routes that should be in the DUT'scurrent route table.
			RxAdvertiseUpdateCount (uint64): Received update packet count. Number of Update packets received fromDUT.
			RxKeepaliveCount (uint64): BGP KeepAlive count received. Total number of KeepAlive packets receivedfromthe DUT during the test. 
			RxNotificationCount (uint64): BGP Notification count received. Number of Notification packets received bythe emulated router during the test.
			RxNotifyCode (uint64): BGP Notify code received. The last NOTIFICATION code the emulated routerreceived from the DUT.
			RxNotifySubCode (uint64): BGP Notify subcode received. Each NOTIFICATION code has a sub-code. 
			RxOpenCount (uint64): BGP Open message count received. Opens received from DUT. In stable BGPscenarios, this should match the value in the previous field. 
			RxRouteRefreshCount (uint64): Number of advertised route refresh message received.
			RxRtConstraintCount (uint64): Number of RT-Constraint routes received for this router.
			SessionUpCount (uint64): Number of router sessions within the router block in the Establishedstate.
			TxAdvertiseUpdateCount (uint64): Advertised update route count transmitted. Total number of UPDATE packetswithfeasible routes sent to the DUT. 
			TxKeepaliveCount (uint64): BGP KeepAlive count transmitted. Total number of KEEPALIVE packets sent tothe DUT during test. 
			TxNotificationCount (uint64): BGP Notification count transmitted. Number of Notification packets sentfrom the emulated router. 
			TxNotifyCode (uint64): BGP Notify code transmitted. Last Notification code the emulated routersent to the DUT.
			TxNotifySubCode (uint64): BGP Notify subcode received. Each NOTIFICATION code has a sub-code. 
			TxOpenCount (uint64): BGP Open message count transmitted. Total number of OPEN packets sent tothe DUT.Initial one, plus number of times the emulated router re-establishessessions. 
			TxRouteRefreshCount (uint64):  Number of advertised route refresh message transmitted.
			TxRtConstraintCount (uint64): Number of RT-Constraint routes transmitted for this router.
			TxWithdrawnUpdateCount (uint64): Withdrawn update route count transmitted. Total number of UPDATE packetswith unfeasibleroutes sent to the DUT (route flapping).  
		"""
		return self._create(locals())

	def read(self, DeviceName=None):
		"""Get `bgpv4-statistics` resource(s). Returns all resources from the server if `DeviceName` is not specified

		"""
		return self._read(DeviceName)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `bgpv4-statistics` resource

		"""
		return self._delete()

	def update(self, PortName=None, RouterState=None, TxAdvertiseRouteCount=None, RxAdvertiseRouteCount=None, TxWithdrawRouteCount=None, RxWithdrawRouteCount=None, LastRxUpdateRouteCount=None, OutstandingRouteCount=None, RxAdvertiseUpdateCount=None, RxKeepaliveCount=None, RxNotificationCount=None, RxNotifyCode=None, RxNotifySubCode=None, RxOpenCount=None, RxRouteRefreshCount=None, RxRtConstraintCount=None, SessionUpCount=None, TxAdvertiseUpdateCount=None, TxKeepaliveCount=None, TxNotificationCount=None, TxNotifyCode=None, TxNotifySubCode=None, TxOpenCount=None, TxRouteRefreshCount=None, TxRtConstraintCount=None, TxWithdrawnUpdateCount=None):
		"""Update the current instance of the `bgpv4-statistics` resource

		Args:
			PortName (string): An abstract test port name
			RouterState (enumeration): The state of the connection to the physical hardwaretest port or virtual machine test port NONENo state. IDLEPrior to invoking Open_BgpSession or Start_Router, an emulated router is in the Idle state. CONNECTConnecting. ACTIVEActive. OPEN_SENTOpen is sent. OPEN_CONFIRMOpen is confirmed. ESTABLISHEDSession is confirmed by the peer. The router state is Established.
			TxAdvertiseRouteCount (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxAdvertiseRouteCount (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			TxWithdrawRouteCount (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxWithdrawRouteCount (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			LastRxUpdateRouteCount (uint64): Number of routes in the last-received UPDATE message.
			OutstandingRouteCount (uint64): Number of routes that should be in the DUT'scurrent route table.
			RxAdvertiseUpdateCount (uint64): Received update packet count. Number of Update packets received fromDUT.
			RxKeepaliveCount (uint64): BGP KeepAlive count received. Total number of KeepAlive packets receivedfromthe DUT during the test. 
			RxNotificationCount (uint64): BGP Notification count received. Number of Notification packets received bythe emulated router during the test.
			RxNotifyCode (uint64): BGP Notify code received. The last NOTIFICATION code the emulated routerreceived from the DUT.
			RxNotifySubCode (uint64): BGP Notify subcode received. Each NOTIFICATION code has a sub-code. 
			RxOpenCount (uint64): BGP Open message count received. Opens received from DUT. In stable BGPscenarios, this should match the value in the previous field. 
			RxRouteRefreshCount (uint64): Number of advertised route refresh message received.
			RxRtConstraintCount (uint64): Number of RT-Constraint routes received for this router.
			SessionUpCount (uint64): Number of router sessions within the router block in the Establishedstate.
			TxAdvertiseUpdateCount (uint64): Advertised update route count transmitted. Total number of UPDATE packetswithfeasible routes sent to the DUT. 
			TxKeepaliveCount (uint64): BGP KeepAlive count transmitted. Total number of KEEPALIVE packets sent tothe DUT during test. 
			TxNotificationCount (uint64): BGP Notification count transmitted. Number of Notification packets sentfrom the emulated router. 
			TxNotifyCode (uint64): BGP Notify code transmitted. Last Notification code the emulated routersent to the DUT.
			TxNotifySubCode (uint64): BGP Notify subcode received. Each NOTIFICATION code has a sub-code. 
			TxOpenCount (uint64): BGP Open message count transmitted. Total number of OPEN packets sent tothe DUT.Initial one, plus number of times the emulated router re-establishessessions. 
			TxRouteRefreshCount (uint64):  Number of advertised route refresh message transmitted.
			TxRtConstraintCount (uint64): Number of RT-Constraint routes transmitted for this router.
			TxWithdrawnUpdateCount (uint64): Withdrawn update route count transmitted. Total number of UPDATE packetswith unfeasibleroutes sent to the DUT (route flapping).  
		"""
		return self._update(locals())

