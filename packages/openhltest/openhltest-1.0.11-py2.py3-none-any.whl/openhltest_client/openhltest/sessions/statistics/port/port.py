from openhltest_client.base import Base


class Port(Base):
	"""TBD

	This class supports iterators and encapsulates 0..n instances of the openhltest:sessions/statistics/port resource.
	"""
	YANG_NAME = 'port'
	YANG_KEYWORD = 'list'
	YANG_KEY = 'name'
	YANG_PROPERTY_MAP = {"FcoeRxFrameCount": "fcoe-rx-frame-count", "TxByteRate": "tx-byte-rate", "OctetTxFrameCount": "octet-tx-frame-count", "MplsRxFrameRate": "mpls-rx-frame-rate", "PfcPriority4RxFrameCount": "pfc-priority4-rx-frame-count", "TxDuration": "tx-duration", "Ipv6RxFrameRate": "ipv6-rx-frame-rate", "PfcTxFrameCount": "pfc-tx-frame-count", "InSequenceRxFrameCount": "in-sequence-rx-frame-count", "Ipv4TxFrameCount": "ipv4-tx-frame-count", "PfcPriority7RxFrameCount": "pfc-priority7-rx-frame-count", "CorrectedRsFecErrorCount": "corrected-rs-fec-error-count", "Ipv6TxTotalFrameCount": "ipv6-tx-total-frame-count", "VlanTxFrameRate": "vlan-tx-frame-rate", "Ipv4ChecksumErrorRxFrameRate": "ipv4-checksum-error-rx-frame-rate", "PfcPriority1TxFrameCount": "pfc-priority1-tx-frame-count", "Ipv6RxFrameCount": "ipv6-rx-frame-count", "Ipv4RxFrameCount": "ipv4-rx-frame-count", "L1TxBitRatePercent": "l1-tx-bit-rate-percent", "MplsTxFrameRate": "mpls-tx-frame-rate", "MinFrameLength": "min-frame-length", "RxBitCount": "rx-bit-count", "CellTxTotalFrameCount": "cell-tx-total-frame-count", "FirstArrivalTimestamp": "first-arrival-timestamp", "L4ChecksumErrorCount": "l4-checksum-error-count", "L1RxBitCount": "l1-rx-bit-count", "CorrectedBaserFecErrorCount": "corrected-baser-fec-error-count", "Ipv6OverIpv4RxFrameRate": "ipv6-over-ipv4-rx-frame-rate", "CrcErrorFrameCount": "crc-error-frame-count", "L4ChecksumErrorRate": "l4-checksum-error-rate", "UndersizeTxFrameRate": "undersize-tx-frame-rate", "JumboTxFrameCount": "jumbo-tx-frame-count", "TxBitCount": "tx-bit-count", "PfcPriority6TxFrameCount": "pfc-priority6-tx-frame-count", "PfcRxFrameCount": "pfc-rx-frame-count", "MplsTxTotalFrameCount": "mpls-tx-total-frame-count", "Ipv4TxFrameRate": "ipv4-tx-frame-rate", "OctetTxTotalFrameRate": "octet-tx-total-frame-rate", "PfcPriority2TxFrameCount": "pfc-priority2-tx-frame-count", "JumboRxFrameCount": "jumbo-rx-frame-count", "OctetTxTotalFrameCount": "octet-tx-total-frame-count", "L3ChecksumErrorRate": "l3-checksum-error-rate", "PfcPriority5TxFrameCount": "pfc-priority5-tx-frame-count", "L1RxBitRate": "l1-rx-bit-rate", "AbortFrameCount": "abort-frame-count", "OctetRxFrameCount": "octet-rx-frame-count", "MplsTxTotalFrameRate": "mpls-tx-total-frame-rate", "Ipv4TxTotalFrameCount": "ipv4-tx-total-frame-count", "PfcPriority3RxFrameCount": "pfc-priority3-rx-frame-count", "PfcPriority0TxFrameCount": "pfc-priority0-tx-frame-count", "SigRxFrameRate": "sig-rx-frame-rate", "Ipv4TxTotalFrameRate": "ipv4-tx-total-frame-rate", "L1TxBitRate": "l1-tx-bit-rate", "IcmpRxFrameRate": "icmp-rx-frame-rate", "CellTxTotalFrameRate": "cell-tx-total-frame-rate", "PfcPriority2RxFrameCount": "pfc-priority2-rx-frame-count", "MaxFrameLength": "max-frame-length", "PfcPriority5RxFrameCount": "pfc-priority5-rx-frame-count", "JumboTxFrameRate": "jumbo-tx-frame-rate", "TxCounterTimestamp": "tx-counter-timestamp", "PfcPriority1RxFrameCount": "pfc-priority1-rx-frame-count", "OversizeRxFrameRate": "oversize-rx-frame-rate", "Ipv4ChecksumErrorRxFrameCount": "ipv4-checksum-error-rx-frame-count", "OctetRxFrameRate": "octet-rx-frame-rate", "L1RxBitRatePercent": "l1-rx-bit-rate-percent", "VlanRxFrameRate": "vlan-rx-frame-rate", "DuplicateFrameCount": "duplicate-frame-count", "PfcPriority4TxFrameCount": "pfc-priority4-tx-frame-count", "PfcPriority0RxFrameCount": "pfc-priority0-rx-frame-count", "JumboRxFrameRate": "jumbo-rx-frame-rate", "L3ChecksumErrorCount": "l3-checksum-error-count", "ComboTriggerCount": "combo-trigger-count", "FcsRxFrameCount": "fcs-rx-frame-count", "TxFrames": "tx-frames", "PfcPriority7TxFrameCount": "pfc-priority7-tx-frame-count", "SigTxFrameRate": "sig-tx-frame-rate", "Ipv6TxFrameCount": "ipv6-tx-frame-count", "RxFrameRate": "rx-frame-rate", "CrcErrorFrameRate": "crc-error-frame-rate", "Ipv6TxFrameRate": "ipv6-tx-frame-rate", "OutSequenceRxFrameCount": "out-sequence-rx-frame-count", "OversizeRxFrameCount": "oversize-rx-frame-count", "VlanTxFrameCount": "vlan-tx-frame-count", "VlanRxFrameCount": "vlan-rx-frame-count", "RxFrames": "rx-frames", "SigTxFrameCount": "sig-tx-frame-count", "PfcPriority3TxFrameCount": "pfc-priority3-tx-frame-count", "DroppedFrames": "dropped-frames", "PfcPriority6RxFrameCount": "pfc-priority6-rx-frame-count", "LateFrameCount": "late-frame-count", "ComboTriggerRate": "combo-trigger-rate", "OversizeTxFrameRate": "oversize-tx-frame-rate", "L1TxBitCount": "l1-tx-bit-count", "PauseRxFrameCount": "pause-rx-frame-count", "RxByteCount": "rx-byte-count", "MplsTxFrameCount": "mpls-tx-frame-count", "RxBitRate": "rx-bit-rate", "UndersizeTxFrameCount": "undersize-tx-frame-count", "FcsRxFrameRate": "fcs-rx-frame-rate", "TxFrameRate": "tx-frame-rate", "UndersizeRxFrameRate": "undersize-rx-frame-rate", "IcmpRxFrameCount": "icmp-rx-frame-count", "FcoeRxFrameRate": "fcoe-rx-frame-rate", "OctetTxFrameRate": "octet-tx-frame-rate", "OversizeTxFrameCount": "oversize-tx-frame-count", "TxBitRate": "tx-bit-rate", "CorrectedRsFecSymbols": "corrected-rs-fec-symbols", "RxByteRate": "rx-byte-rate", "Ipv6OverIpv4RxFrameCount": "ipv6-over-ipv4-rx-frame-count", "UndersizeRxFrameCount": "undersize-rx-frame-count", "RxCounterTimestamp": "rx-counter-timestamp", "Name": "name", "HwRxFrameCount": "hw-rx-frame-count", "TxByteCount": "tx-byte-count", "PauseRxFrameRate": "pause-rx-frame-rate", "Ipv6TxTotalFrameRate": "ipv6-tx-total-frame-rate", "HwTxFrameCount": "hw-tx-frame-count", "MplsRxFrameCount": "mpls-rx-frame-count", "AbortFrameRate": "abort-frame-rate", "LastArrivalTimestamp": "last-arrival-timestamp", "Ipv4RxFrameRate": "ipv4-rx-frame-rate", "SigRxFrameCount": "sig-rx-frame-count"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(Port, self).__init__(parent)

	@property
	def Name(self):
		"""An abstract test port name

		Getter Returns:
			string
		"""
		return self._get_value('name')

	@property
	def TxDuration(self):
		"""Generator on time in seconds.

		Getter Returns:
			decimal64
		"""
		return self._get_value('tx-duration')

	@property
	def TxFrames(self):
		"""The total number of frames transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-frames')

	@property
	def RxFrames(self):
		"""The total number of frames received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-frames')

	@property
	def TxFrameRate(self):
		"""Total number of frames transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-frame-rate')

	@property
	def RxFrameRate(self):
		"""Total number of frames received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-frame-rate')

	@property
	def DroppedFrames(self):
		"""Total Number of dropped frames during transit.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('dropped-frames')

	@property
	def TxBitCount(self):
		"""The total number of bits transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-bit-count')

	@property
	def RxBitCount(self):
		"""The total number of bits received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-bit-count')

	@property
	def TxBitRate(self):
		"""Total number of bits transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-bit-rate')

	@property
	def RxBitRate(self):
		"""Total number of bits received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-bit-rate')

	@property
	def TxByteCount(self):
		"""The total number of bytes transmitted on the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-byte-count')

	@property
	def RxByteCount(self):
		"""The total number of bytes received on the the port.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-byte-count')

	@property
	def TxByteRate(self):
		"""Total number of bytes transmitted over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-byte-rate')

	@property
	def RxByteRate(self):
		"""Total number of bytes received over the last 1-second interval.
		Empty if the abstract port is not connected to a test port.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-byte-rate')

	@property
	def TxCounterTimestamp(self):
		"""Time when the counter was stored. This value is derived from the TestCenter chassis time sync source.
		The unit is 10 nanoseconds.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-counter-timestamp')

	@property
	def AbortFrameCount(self):
		"""Number of abort frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('abort-frame-count')

	@property
	def AbortFrameRate(self):
		"""Number of abort frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('abort-frame-rate')

	@property
	def CrcErrorFrameCount(self):
		"""Number of CRC error frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('crc-error-frame-count')

	@property
	def CrcErrorFrameRate(self):
		"""Number of CRC error frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('crc-error-frame-rate')

	@property
	def Ipv4TxFrameCount(self):
		"""Number of IPv4 frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-tx-frame-count')

	@property
	def Ipv4TxFrameRate(self):
		"""Number of IPv4 frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-tx-frame-rate')

	@property
	def Ipv4RxFrameCount(self):
		"""Number of IPv4 frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-rx-frame-count')

	@property
	def Ipv4RxFrameRate(self):
		"""Number of IPv4 frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-rx-frame-rate')

	@property
	def Ipv4TxTotalFrameCount(self):
		"""Total number of IPv4 frames transmitted.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-tx-total-frame-count')

	@property
	def Ipv4TxTotalFrameRate(self):
		"""Total number of IPv4 frames transmitted over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-tx-total-frame-rate')

	@property
	def Ipv6TxFrameCount(self):
		"""Number of IPv6 frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-tx-frame-count')

	@property
	def Ipv6TxFrameRate(self):
		"""Number of IPv6 frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-tx-frame-rate')

	@property
	def Ipv6RxFrameCount(self):
		"""Number of IPv6 frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-rx-frame-count')

	@property
	def Ipv6RxFrameRate(self):
		"""Number of IPv6 frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-rx-frame-rate')

	@property
	def Ipv6TxTotalFrameCount(self):
		"""Total number of IPv6 frames transmitted.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-tx-total-frame-count')

	@property
	def Ipv6TxTotalFrameRate(self):
		"""Total number of IPv6 frames transmitted over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-tx-total-frame-rate')

	@property
	def JumboTxFrameCount(self):
		"""Number of jumbo frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('jumbo-tx-frame-count')

	@property
	def JumboTxFrameRate(self):
		"""Number of jumbo frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('jumbo-tx-frame-rate')

	@property
	def JumboRxFrameCount(self):
		"""Number of jumbo frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('jumbo-rx-frame-count')

	@property
	def JumboRxFrameRate(self):
		"""Number of jumbo frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('jumbo-rx-frame-rate')

	@property
	def L3ChecksumErrorCount(self):
		"""Number of frames generated with an L3 checksum error.

		Getter Returns:
			uint64
		"""
		return self._get_value('l3-checksum-error-count')

	@property
	def L3ChecksumErrorRate(self):
		"""Number of frames generated with an L3 header checksum, per second.

		Getter Returns:
			uint64
		"""
		return self._get_value('l3-checksum-error-rate')

	@property
	def L4ChecksumErrorCount(self):
		"""Number of frames generated with an L4 checksum error.

		Getter Returns:
			uint64
		"""
		return self._get_value('l4-checksum-error-count')

	@property
	def L4ChecksumErrorRate(self):
		"""Number of frames generated with an L4 header checksum, per second.

		Getter Returns:
			uint64
		"""
		return self._get_value('l4-checksum-error-rate')

	@property
	def MplsTxFrameCount(self):
		"""Number of mpls frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('mpls-tx-frame-count')

	@property
	def MplsTxFrameRate(self):
		"""Number of mpls frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('mpls-tx-frame-rate')

	@property
	def MplsRxFrameCount(self):
		"""Number of mpls frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('mpls-rx-frame-count')

	@property
	def MplsRxFrameRate(self):
		"""Number of mpls frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('mpls-rx-frame-rate')

	@property
	def MplsTxTotalFrameCount(self):
		"""Total number of MPLS frames transmitted.

		Getter Returns:
			uint64
		"""
		return self._get_value('mpls-tx-total-frame-count')

	@property
	def MplsTxTotalFrameRate(self):
		"""Total number of MPLS frames transmitted over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('mpls-tx-total-frame-rate')

	@property
	def OctetTxFrameCount(self):
		"""Number of octet frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('octet-tx-frame-count')

	@property
	def OctetTxFrameRate(self):
		"""Number of octet frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('octet-tx-frame-rate')

	@property
	def OctetRxFrameCount(self):
		"""Number of octet frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('octet-rx-frame-count')

	@property
	def OctetRxFrameRate(self):
		"""Number of octet frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('octet-rx-frame-rate')

	@property
	def OctetTxTotalFrameCount(self):
		"""Total number of octet frames transmitted.

		Getter Returns:
			uint64
		"""
		return self._get_value('octet-tx-total-frame-count')

	@property
	def OctetTxTotalFrameRate(self):
		"""Total number of octet frames transmitted over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('octet-tx-total-frame-rate')

	@property
	def CellTxTotalFrameCount(self):
		"""Count of total cells generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('cell-tx-total-frame-count')

	@property
	def CellTxTotalFrameRate(self):
		"""Total number of bytes generated over last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('cell-tx-total-frame-rate')

	@property
	def OversizeTxFrameCount(self):
		"""Number of oversize frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('oversize-tx-frame-count')

	@property
	def OversizeTxFrameRate(self):
		"""Number of oversize frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('oversize-tx-frame-rate')

	@property
	def OversizeRxFrameCount(self):
		"""Number of oversize frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('oversize-rx-frame-count')

	@property
	def OversizeRxFrameRate(self):
		"""Number of oversize frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('oversize-rx-frame-rate')

	@property
	def UndersizeTxFrameCount(self):
		"""Number of undersize frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('undersize-tx-frame-count')

	@property
	def UndersizeTxFrameRate(self):
		"""Number of undersize frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('undersize-tx-frame-rate')

	@property
	def UndersizeRxFrameCount(self):
		"""Number of undersize frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('undersize-rx-frame-count')

	@property
	def UndersizeRxFrameRate(self):
		"""Number of undersize frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('undersize-rx-frame-rate')

	@property
	def SigTxFrameCount(self):
		"""Number of Spirent Signature frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('sig-tx-frame-count')

	@property
	def SigTxFrameRate(self):
		"""Number of Spirent Signature  frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('sig-tx-frame-rate')

	@property
	def SigRxFrameCount(self):
		"""Number of Spirent Signature  frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('sig-rx-frame-count')

	@property
	def SigRxFrameRate(self):
		"""Number of Spirent Signature  frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('sig-rx-frame-rate')

	@property
	def VlanTxFrameCount(self):
		"""Number of VLAN frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('vlan-tx-frame-count')

	@property
	def VlanTxFrameRate(self):
		"""Number of VLAN frames generated over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('vlan-tx-frame-rate')

	@property
	def VlanRxFrameCount(self):
		"""Number of VLAN frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('vlan-rx-frame-count')

	@property
	def VlanRxFrameRate(self):
		"""Number of VLAN frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('vlan-rx-frame-rate')

	@property
	def HwTxFrameCount(self):
		"""Number of Hardware frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('hw-tx-frame-count')

	@property
	def HwRxFrameCount(self):
		"""Number of Hardware frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('hw-rx-frame-count')

	@property
	def L1TxBitCount(self):
		"""Count of total layer1 bits generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('l1-tx-bit-count')

	@property
	def L1TxBitRate(self):
		"""Total number of layer1 bits transmitted over last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('l1-tx-bit-rate')

	@property
	def L1TxBitRatePercent(self):
		"""Total number of layer 1 bits transmitted in percentage.

		Getter Returns:
			decimal64
		"""
		return self._get_value('l1-tx-bit-rate-percent')

	@property
	def L1RxBitCount(self):
		"""Count of total layer1 bits received.

		Getter Returns:
			uint64
		"""
		return self._get_value('l1-rx-bit-count')

	@property
	def L1RxBitRate(self):
		"""Total number of layer1 bits received over last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('l1-rx-bit-rate')

	@property
	def L1RxBitRatePercent(self):
		"""Total number of layer 1 bits received in percentage.

		Getter Returns:
			decimal64
		"""
		return self._get_value('l1-rx-bit-rate-percent')

	@property
	def PfcTxFrameCount(self):
		"""Number of pause frames transmitted.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-tx-frame-count')

	@property
	def PfcRxFrameCount(self):
		"""Number of pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-rx-frame-count')

	@property
	def PfcPriority0TxFrameCount(self):
		"""Number of priority-0 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority0-tx-frame-count')

	@property
	def PfcPriority1TxFrameCount(self):
		"""Number of priority-1 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority1-tx-frame-count')

	@property
	def PfcPriority2TxFrameCount(self):
		"""Number of priority-2 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority2-tx-frame-count')

	@property
	def PfcPriority3TxFrameCount(self):
		"""Number of priority-3 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority3-tx-frame-count')

	@property
	def PfcPriority4TxFrameCount(self):
		"""Number of priority-4 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority4-tx-frame-count')

	@property
	def PfcPriority5TxFrameCount(self):
		"""Number of priority-5 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority5-tx-frame-count')

	@property
	def PfcPriority6TxFrameCount(self):
		"""Number of priority-6 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority6-tx-frame-count')

	@property
	def PfcPriority7TxFrameCount(self):
		"""Number of priority-7 pause frames generated.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority7-tx-frame-count')

	@property
	def PfcPriority0RxFrameCount(self):
		"""Number of priority-0 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority0-rx-frame-count')

	@property
	def PfcPriority1RxFrameCount(self):
		"""Number of priority-1 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority1-rx-frame-count')

	@property
	def PfcPriority2RxFrameCount(self):
		"""Number of priority-2 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority2-rx-frame-count')

	@property
	def PfcPriority3RxFrameCount(self):
		"""Number of priority-3 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority3-rx-frame-count')

	@property
	def PfcPriority4RxFrameCount(self):
		"""Number of priority-4 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority4-rx-frame-count')

	@property
	def PfcPriority5RxFrameCount(self):
		"""Number of priority-5 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority5-rx-frame-count')

	@property
	def PfcPriority6RxFrameCount(self):
		"""Number of priority-6 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority6-rx-frame-count')

	@property
	def PfcPriority7RxFrameCount(self):
		"""Number of priority-7 pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pfc-priority7-rx-frame-count')

	@property
	def ComboTriggerCount(self):
		"""Number of frames captured by all the triggers.

		Getter Returns:
			uint64
		"""
		return self._get_value('combo-trigger-count')

	@property
	def ComboTriggerRate(self):
		"""Number of frames received by all the triggers over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('combo-trigger-rate')

	@property
	def CorrectedBaserFecErrorCount(self):
		"""Number of Corrected BaseR FEC Errors received.

		Getter Returns:
			uint64
		"""
		return self._get_value('corrected-baser-fec-error-count')

	@property
	def CorrectedRsFecErrorCount(self):
		"""Number of Corrected RS FEC Errors received.

		Getter Returns:
			uint64
		"""
		return self._get_value('corrected-rs-fec-error-count')

	@property
	def CorrectedRsFecSymbols(self):
		"""Number of Corrected RS FEC Symbols received.

		Getter Returns:
			uint64
		"""
		return self._get_value('corrected-rs-fec-symbols')

	@property
	def RxCounterTimestamp(self):
		"""Time when the counter was stored.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-counter-timestamp')

	@property
	def DuplicateFrameCount(self):
		"""Number of duplicate frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('duplicate-frame-count')

	@property
	def FcoeRxFrameCount(self):
		"""Fiber channel over Ethernet frame count.

		Getter Returns:
			uint64
		"""
		return self._get_value('fcoe-rx-frame-count')

	@property
	def FcoeRxFrameRate(self):
		"""Fiber channel over Ethernet frame rate.

		Getter Returns:
			uint64
		"""
		return self._get_value('fcoe-rx-frame-rate')

	@property
	def FcsRxFrameCount(self):
		"""Number of FCS error frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('fcs-rx-frame-count')

	@property
	def FcsRxFrameRate(self):
		"""Number of FCS error frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('fcs-rx-frame-rate')

	@property
	def FirstArrivalTimestamp(self):
		"""Backplane first arrival timestamp received.

		Getter Returns:
			decimal64
		"""
		return self._get_value('first-arrival-timestamp')

	@property
	def LastArrivalTimestamp(self):
		"""Backplane last arrival timestamp received.

		Getter Returns:
			decimal64
		"""
		return self._get_value('last-arrival-timestamp')

	@property
	def LateFrameCount(self):
		"""Number of late frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('late-frame-count')

	@property
	def MaxFrameLength(self):
		"""Maximum frame length received (in bytes).

		Getter Returns:
			uint64
		"""
		return self._get_value('max-frame-length')

	@property
	def MinFrameLength(self):
		"""Minimum frame length received (in bytes).

		Getter Returns:
			uint64
		"""
		return self._get_value('min-frame-length')

	@property
	def IcmpRxFrameCount(self):
		"""Number of ICMP frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('icmp-rx-frame-count')

	@property
	def IcmpRxFrameRate(self):
		"""Number of ICMP frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('icmp-rx-frame-rate')

	@property
	def Ipv4ChecksumErrorRxFrameCount(self):
		"""Number of IPv4 checksum errors received.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-checksum-error-rx-frame-count')

	@property
	def Ipv4ChecksumErrorRxFrameRate(self):
		"""Number of IPv4 checksum errors received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv4-checksum-error-rx-frame-rate')

	@property
	def InSequenceRxFrameCount(self):
		"""Number of frames received in sequence order.

		Getter Returns:
			uint64
		"""
		return self._get_value('in-sequence-rx-frame-count')

	@property
	def OutSequenceRxFrameCount(self):
		"""Number of frames received out of sequence order.

		Getter Returns:
			uint64
		"""
		return self._get_value('out-sequence-rx-frame-count')

	@property
	def Ipv6OverIpv4RxFrameCount(self):
		"""Number of IPv6 over IPv4 frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-over-ipv4-rx-frame-count')

	@property
	def Ipv6OverIpv4RxFrameRate(self):
		"""Number of IPv6 over IPv4 frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('ipv6-over-ipv4-rx-frame-rate')

	@property
	def PauseRxFrameCount(self):
		"""Number of pause frames received.

		Getter Returns:
			uint64
		"""
		return self._get_value('pause-rx-frame-count')

	@property
	def PauseRxFrameRate(self):
		"""Number of pause frames received over the last 1-second interval.

		Getter Returns:
			uint64
		"""
		return self._get_value('pause-rx-frame-rate')

	def create(self, Name, TxDuration=None, TxFrames=None, RxFrames=None, TxFrameRate=None, RxFrameRate=None, DroppedFrames=None, TxBitCount=None, RxBitCount=None, TxBitRate=None, RxBitRate=None, TxByteCount=None, RxByteCount=None, TxByteRate=None, RxByteRate=None, TxCounterTimestamp=None, AbortFrameCount=None, AbortFrameRate=None, CrcErrorFrameCount=None, CrcErrorFrameRate=None, Ipv4TxFrameCount=None, Ipv4TxFrameRate=None, Ipv4RxFrameCount=None, Ipv4RxFrameRate=None, Ipv4TxTotalFrameCount=None, Ipv4TxTotalFrameRate=None, Ipv6TxFrameCount=None, Ipv6TxFrameRate=None, Ipv6RxFrameCount=None, Ipv6RxFrameRate=None, Ipv6TxTotalFrameCount=None, Ipv6TxTotalFrameRate=None, JumboTxFrameCount=None, JumboTxFrameRate=None, JumboRxFrameCount=None, JumboRxFrameRate=None, L3ChecksumErrorCount=None, L3ChecksumErrorRate=None, L4ChecksumErrorCount=None, L4ChecksumErrorRate=None, MplsTxFrameCount=None, MplsTxFrameRate=None, MplsRxFrameCount=None, MplsRxFrameRate=None, MplsTxTotalFrameCount=None, MplsTxTotalFrameRate=None, OctetTxFrameCount=None, OctetTxFrameRate=None, OctetRxFrameCount=None, OctetRxFrameRate=None, OctetTxTotalFrameCount=None, OctetTxTotalFrameRate=None, CellTxTotalFrameCount=None, CellTxTotalFrameRate=None, OversizeTxFrameCount=None, OversizeTxFrameRate=None, OversizeRxFrameCount=None, OversizeRxFrameRate=None, UndersizeTxFrameCount=None, UndersizeTxFrameRate=None, UndersizeRxFrameCount=None, UndersizeRxFrameRate=None, SigTxFrameCount=None, SigTxFrameRate=None, SigRxFrameCount=None, SigRxFrameRate=None, VlanTxFrameCount=None, VlanTxFrameRate=None, VlanRxFrameCount=None, VlanRxFrameRate=None, HwTxFrameCount=None, HwRxFrameCount=None, L1TxBitCount=None, L1TxBitRate=None, L1TxBitRatePercent=None, L1RxBitCount=None, L1RxBitRate=None, L1RxBitRatePercent=None, PfcTxFrameCount=None, PfcRxFrameCount=None, PfcPriority0TxFrameCount=None, PfcPriority1TxFrameCount=None, PfcPriority2TxFrameCount=None, PfcPriority3TxFrameCount=None, PfcPriority4TxFrameCount=None, PfcPriority5TxFrameCount=None, PfcPriority6TxFrameCount=None, PfcPriority7TxFrameCount=None, PfcPriority0RxFrameCount=None, PfcPriority1RxFrameCount=None, PfcPriority2RxFrameCount=None, PfcPriority3RxFrameCount=None, PfcPriority4RxFrameCount=None, PfcPriority5RxFrameCount=None, PfcPriority6RxFrameCount=None, PfcPriority7RxFrameCount=None, ComboTriggerCount=None, ComboTriggerRate=None, CorrectedBaserFecErrorCount=None, CorrectedRsFecErrorCount=None, CorrectedRsFecSymbols=None, RxCounterTimestamp=None, DuplicateFrameCount=None, FcoeRxFrameCount=None, FcoeRxFrameRate=None, FcsRxFrameCount=None, FcsRxFrameRate=None, FirstArrivalTimestamp=None, LastArrivalTimestamp=None, LateFrameCount=None, MaxFrameLength=None, MinFrameLength=None, IcmpRxFrameCount=None, IcmpRxFrameRate=None, Ipv4ChecksumErrorRxFrameCount=None, Ipv4ChecksumErrorRxFrameRate=None, InSequenceRxFrameCount=None, OutSequenceRxFrameCount=None, Ipv6OverIpv4RxFrameCount=None, Ipv6OverIpv4RxFrameRate=None, PauseRxFrameCount=None, PauseRxFrameRate=None):
		"""Create an instance of the `port` resource

		Args:
			Name (string): An abstract test port name
			TxDuration (decimal64): Generator on time in seconds.
			TxFrames (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxFrames (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			TxFrameRate (uint64): Total number of frames transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxFrameRate (uint64): Total number of frames received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			DroppedFrames (uint64): Total Number of dropped frames during transit.Empty if the abstract port is not connected to a test port.
			TxBitCount (uint64): The total number of bits transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxBitCount (uint64): The total number of bits received on the the port.Empty if the abstract port is not connected to a test port.
			TxBitRate (uint64): Total number of bits transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxBitRate (uint64): Total number of bits received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			TxByteCount (uint64): The total number of bytes transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxByteCount (uint64): The total number of bytes received on the the port.Empty if the abstract port is not connected to a test port.
			TxByteRate (uint64): Total number of bytes transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxByteRate (uint64): Total number of bytes received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			TxCounterTimestamp (uint64): Time when the counter was stored. This value is derived from the TestCenter chassis time sync source.The unit is 10 nanoseconds.
			AbortFrameCount (uint64): Number of abort frames generated.
			AbortFrameRate (uint64): Number of abort frames generated over the last 1-second interval.
			CrcErrorFrameCount (uint64): Number of CRC error frames generated.
			CrcErrorFrameRate (uint64): Number of CRC error frames generated over the last 1-second interval.
			Ipv4TxFrameCount (uint64): Number of IPv4 frames generated.
			Ipv4TxFrameRate (uint64): Number of IPv4 frames generated over the last 1-second interval.
			Ipv4RxFrameCount (uint64): Number of IPv4 frames received.
			Ipv4RxFrameRate (uint64): Number of IPv4 frames received over the last 1-second interval.
			Ipv4TxTotalFrameCount (uint64): Total number of IPv4 frames transmitted.
			Ipv4TxTotalFrameRate (uint64): Total number of IPv4 frames transmitted over the last 1-second interval.
			Ipv6TxFrameCount (uint64): Number of IPv6 frames generated.
			Ipv6TxFrameRate (uint64): Number of IPv6 frames generated over the last 1-second interval.
			Ipv6RxFrameCount (uint64): Number of IPv6 frames received.
			Ipv6RxFrameRate (uint64): Number of IPv6 frames received over the last 1-second interval.
			Ipv6TxTotalFrameCount (uint64): Total number of IPv6 frames transmitted.
			Ipv6TxTotalFrameRate (uint64): Total number of IPv6 frames transmitted over the last 1-second interval.
			JumboTxFrameCount (uint64): Number of jumbo frames generated.
			JumboTxFrameRate (uint64): Number of jumbo frames generated over the last 1-second interval.
			JumboRxFrameCount (uint64): Number of jumbo frames received.
			JumboRxFrameRate (uint64): Number of jumbo frames received over the last 1-second interval.
			L3ChecksumErrorCount (uint64): Number of frames generated with an L3 checksum error.
			L3ChecksumErrorRate (uint64): Number of frames generated with an L3 header checksum, per second.
			L4ChecksumErrorCount (uint64): Number of frames generated with an L4 checksum error.
			L4ChecksumErrorRate (uint64): Number of frames generated with an L4 header checksum, per second.
			MplsTxFrameCount (uint64): Number of mpls frames generated.
			MplsTxFrameRate (uint64): Number of mpls frames generated over the last 1-second interval.
			MplsRxFrameCount (uint64): Number of mpls frames received.
			MplsRxFrameRate (uint64): Number of mpls frames received over the last 1-second interval.
			MplsTxTotalFrameCount (uint64): Total number of MPLS frames transmitted.
			MplsTxTotalFrameRate (uint64): Total number of MPLS frames transmitted over the last 1-second interval.
			OctetTxFrameCount (uint64): Number of octet frames generated.
			OctetTxFrameRate (uint64): Number of octet frames generated over the last 1-second interval.
			OctetRxFrameCount (uint64): Number of octet frames received.
			OctetRxFrameRate (uint64): Number of octet frames received over the last 1-second interval.
			OctetTxTotalFrameCount (uint64): Total number of octet frames transmitted.
			OctetTxTotalFrameRate (uint64): Total number of octet frames transmitted over the last 1-second interval.
			CellTxTotalFrameCount (uint64): Count of total cells generated.
			CellTxTotalFrameRate (uint64): Total number of bytes generated over last 1-second interval.
			OversizeTxFrameCount (uint64): Number of oversize frames generated.
			OversizeTxFrameRate (uint64): Number of oversize frames generated over the last 1-second interval.
			OversizeRxFrameCount (uint64): Number of oversize frames received.
			OversizeRxFrameRate (uint64): Number of oversize frames received over the last 1-second interval.
			UndersizeTxFrameCount (uint64): Number of undersize frames generated.
			UndersizeTxFrameRate (uint64): Number of undersize frames generated over the last 1-second interval.
			UndersizeRxFrameCount (uint64): Number of undersize frames received.
			UndersizeRxFrameRate (uint64): Number of undersize frames received over the last 1-second interval.
			SigTxFrameCount (uint64): Number of Spirent Signature frames generated.
			SigTxFrameRate (uint64): Number of Spirent Signature  frames generated over the last 1-second interval.
			SigRxFrameCount (uint64): Number of Spirent Signature  frames received.
			SigRxFrameRate (uint64): Number of Spirent Signature  frames received over the last 1-second interval.
			VlanTxFrameCount (uint64): Number of VLAN frames generated.
			VlanTxFrameRate (uint64): Number of VLAN frames generated over the last 1-second interval.
			VlanRxFrameCount (uint64): Number of VLAN frames received.
			VlanRxFrameRate (uint64): Number of VLAN frames received over the last 1-second interval.
			HwTxFrameCount (uint64): Number of Hardware frames generated.
			HwRxFrameCount (uint64): Number of Hardware frames received.
			L1TxBitCount (uint64): Count of total layer1 bits generated.
			L1TxBitRate (uint64): Total number of layer1 bits transmitted over last 1-second interval.
			L1TxBitRatePercent (decimal64): Total number of layer 1 bits transmitted in percentage.
			L1RxBitCount (uint64): Count of total layer1 bits received.
			L1RxBitRate (uint64): Total number of layer1 bits received over last 1-second interval.
			L1RxBitRatePercent (decimal64): Total number of layer 1 bits received in percentage.
			PfcTxFrameCount (uint64): Number of pause frames transmitted.
			PfcRxFrameCount (uint64): Number of pause frames received.
			PfcPriority0TxFrameCount (uint64): Number of priority-0 pause frames generated.
			PfcPriority1TxFrameCount (uint64): Number of priority-1 pause frames generated.
			PfcPriority2TxFrameCount (uint64): Number of priority-2 pause frames generated.
			PfcPriority3TxFrameCount (uint64): Number of priority-3 pause frames generated.
			PfcPriority4TxFrameCount (uint64): Number of priority-4 pause frames generated.
			PfcPriority5TxFrameCount (uint64): Number of priority-5 pause frames generated.
			PfcPriority6TxFrameCount (uint64): Number of priority-6 pause frames generated.
			PfcPriority7TxFrameCount (uint64): Number of priority-7 pause frames generated.
			PfcPriority0RxFrameCount (uint64): Number of priority-0 pause frames received.
			PfcPriority1RxFrameCount (uint64): Number of priority-1 pause frames received.
			PfcPriority2RxFrameCount (uint64): Number of priority-2 pause frames received.
			PfcPriority3RxFrameCount (uint64): Number of priority-3 pause frames received.
			PfcPriority4RxFrameCount (uint64): Number of priority-4 pause frames received.
			PfcPriority5RxFrameCount (uint64): Number of priority-5 pause frames received.
			PfcPriority6RxFrameCount (uint64): Number of priority-6 pause frames received.
			PfcPriority7RxFrameCount (uint64): Number of priority-7 pause frames received.
			ComboTriggerCount (uint64): Number of frames captured by all the triggers.
			ComboTriggerRate (uint64): Number of frames received by all the triggers over the last 1-second interval.
			CorrectedBaserFecErrorCount (uint64): Number of Corrected BaseR FEC Errors received.
			CorrectedRsFecErrorCount (uint64): Number of Corrected RS FEC Errors received.
			CorrectedRsFecSymbols (uint64): Number of Corrected RS FEC Symbols received.
			RxCounterTimestamp (uint64): Time when the counter was stored.
			DuplicateFrameCount (uint64): Number of duplicate frames received.
			FcoeRxFrameCount (uint64): Fiber channel over Ethernet frame count.
			FcoeRxFrameRate (uint64): Fiber channel over Ethernet frame rate.
			FcsRxFrameCount (uint64): Number of FCS error frames received.
			FcsRxFrameRate (uint64): Number of FCS error frames received over the last 1-second interval.
			FirstArrivalTimestamp (decimal64): Backplane first arrival timestamp received.
			LastArrivalTimestamp (decimal64): Backplane last arrival timestamp received.
			LateFrameCount (uint64): Number of late frames received.
			MaxFrameLength (uint64): Maximum frame length received (in bytes).
			MinFrameLength (uint64): Minimum frame length received (in bytes).
			IcmpRxFrameCount (uint64): Number of ICMP frames received.
			IcmpRxFrameRate (uint64): Number of ICMP frames received over the last 1-second interval.
			Ipv4ChecksumErrorRxFrameCount (uint64): Number of IPv4 checksum errors received.
			Ipv4ChecksumErrorRxFrameRate (uint64): Number of IPv4 checksum errors received over the last 1-second interval.
			InSequenceRxFrameCount (uint64): Number of frames received in sequence order.
			OutSequenceRxFrameCount (uint64): Number of frames received out of sequence order.
			Ipv6OverIpv4RxFrameCount (uint64): Number of IPv6 over IPv4 frames received.
			Ipv6OverIpv4RxFrameRate (uint64): Number of IPv6 over IPv4 frames received over the last 1-second interval.
			PauseRxFrameCount (uint64): Number of pause frames received.
			PauseRxFrameRate (uint64): Number of pause frames received over the last 1-second interval.
		"""
		return self._create(locals())

	def read(self, Name=None):
		"""Get `port` resource(s). Returns all resources from the server if `Name` is not specified

		"""
		return self._read(Name)

	def delete(self):
		"""Delete all the encapsulated instances of the retrieved `port` resource

		"""
		return self._delete()

	def update(self, TxDuration=None, TxFrames=None, RxFrames=None, TxFrameRate=None, RxFrameRate=None, DroppedFrames=None, TxBitCount=None, RxBitCount=None, TxBitRate=None, RxBitRate=None, TxByteCount=None, RxByteCount=None, TxByteRate=None, RxByteRate=None, TxCounterTimestamp=None, AbortFrameCount=None, AbortFrameRate=None, CrcErrorFrameCount=None, CrcErrorFrameRate=None, Ipv4TxFrameCount=None, Ipv4TxFrameRate=None, Ipv4RxFrameCount=None, Ipv4RxFrameRate=None, Ipv4TxTotalFrameCount=None, Ipv4TxTotalFrameRate=None, Ipv6TxFrameCount=None, Ipv6TxFrameRate=None, Ipv6RxFrameCount=None, Ipv6RxFrameRate=None, Ipv6TxTotalFrameCount=None, Ipv6TxTotalFrameRate=None, JumboTxFrameCount=None, JumboTxFrameRate=None, JumboRxFrameCount=None, JumboRxFrameRate=None, L3ChecksumErrorCount=None, L3ChecksumErrorRate=None, L4ChecksumErrorCount=None, L4ChecksumErrorRate=None, MplsTxFrameCount=None, MplsTxFrameRate=None, MplsRxFrameCount=None, MplsRxFrameRate=None, MplsTxTotalFrameCount=None, MplsTxTotalFrameRate=None, OctetTxFrameCount=None, OctetTxFrameRate=None, OctetRxFrameCount=None, OctetRxFrameRate=None, OctetTxTotalFrameCount=None, OctetTxTotalFrameRate=None, CellTxTotalFrameCount=None, CellTxTotalFrameRate=None, OversizeTxFrameCount=None, OversizeTxFrameRate=None, OversizeRxFrameCount=None, OversizeRxFrameRate=None, UndersizeTxFrameCount=None, UndersizeTxFrameRate=None, UndersizeRxFrameCount=None, UndersizeRxFrameRate=None, SigTxFrameCount=None, SigTxFrameRate=None, SigRxFrameCount=None, SigRxFrameRate=None, VlanTxFrameCount=None, VlanTxFrameRate=None, VlanRxFrameCount=None, VlanRxFrameRate=None, HwTxFrameCount=None, HwRxFrameCount=None, L1TxBitCount=None, L1TxBitRate=None, L1TxBitRatePercent=None, L1RxBitCount=None, L1RxBitRate=None, L1RxBitRatePercent=None, PfcTxFrameCount=None, PfcRxFrameCount=None, PfcPriority0TxFrameCount=None, PfcPriority1TxFrameCount=None, PfcPriority2TxFrameCount=None, PfcPriority3TxFrameCount=None, PfcPriority4TxFrameCount=None, PfcPriority5TxFrameCount=None, PfcPriority6TxFrameCount=None, PfcPriority7TxFrameCount=None, PfcPriority0RxFrameCount=None, PfcPriority1RxFrameCount=None, PfcPriority2RxFrameCount=None, PfcPriority3RxFrameCount=None, PfcPriority4RxFrameCount=None, PfcPriority5RxFrameCount=None, PfcPriority6RxFrameCount=None, PfcPriority7RxFrameCount=None, ComboTriggerCount=None, ComboTriggerRate=None, CorrectedBaserFecErrorCount=None, CorrectedRsFecErrorCount=None, CorrectedRsFecSymbols=None, RxCounterTimestamp=None, DuplicateFrameCount=None, FcoeRxFrameCount=None, FcoeRxFrameRate=None, FcsRxFrameCount=None, FcsRxFrameRate=None, FirstArrivalTimestamp=None, LastArrivalTimestamp=None, LateFrameCount=None, MaxFrameLength=None, MinFrameLength=None, IcmpRxFrameCount=None, IcmpRxFrameRate=None, Ipv4ChecksumErrorRxFrameCount=None, Ipv4ChecksumErrorRxFrameRate=None, InSequenceRxFrameCount=None, OutSequenceRxFrameCount=None, Ipv6OverIpv4RxFrameCount=None, Ipv6OverIpv4RxFrameRate=None, PauseRxFrameCount=None, PauseRxFrameRate=None):
		"""Update the current instance of the `port` resource

		Args:
			TxDuration (decimal64): Generator on time in seconds.
			TxFrames (uint64): The total number of frames transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxFrames (uint64): The total number of frames received on the the port.Empty if the abstract port is not connected to a test port.
			TxFrameRate (uint64): Total number of frames transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxFrameRate (uint64): Total number of frames received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			DroppedFrames (uint64): Total Number of dropped frames during transit.Empty if the abstract port is not connected to a test port.
			TxBitCount (uint64): The total number of bits transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxBitCount (uint64): The total number of bits received on the the port.Empty if the abstract port is not connected to a test port.
			TxBitRate (uint64): Total number of bits transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxBitRate (uint64): Total number of bits received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			TxByteCount (uint64): The total number of bytes transmitted on the port.Empty if the abstract port is not connected to a test port.
			RxByteCount (uint64): The total number of bytes received on the the port.Empty if the abstract port is not connected to a test port.
			TxByteRate (uint64): Total number of bytes transmitted over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			RxByteRate (uint64): Total number of bytes received over the last 1-second interval.Empty if the abstract port is not connected to a test port.
			TxCounterTimestamp (uint64): Time when the counter was stored. This value is derived from the TestCenter chassis time sync source.The unit is 10 nanoseconds.
			AbortFrameCount (uint64): Number of abort frames generated.
			AbortFrameRate (uint64): Number of abort frames generated over the last 1-second interval.
			CrcErrorFrameCount (uint64): Number of CRC error frames generated.
			CrcErrorFrameRate (uint64): Number of CRC error frames generated over the last 1-second interval.
			Ipv4TxFrameCount (uint64): Number of IPv4 frames generated.
			Ipv4TxFrameRate (uint64): Number of IPv4 frames generated over the last 1-second interval.
			Ipv4RxFrameCount (uint64): Number of IPv4 frames received.
			Ipv4RxFrameRate (uint64): Number of IPv4 frames received over the last 1-second interval.
			Ipv4TxTotalFrameCount (uint64): Total number of IPv4 frames transmitted.
			Ipv4TxTotalFrameRate (uint64): Total number of IPv4 frames transmitted over the last 1-second interval.
			Ipv6TxFrameCount (uint64): Number of IPv6 frames generated.
			Ipv6TxFrameRate (uint64): Number of IPv6 frames generated over the last 1-second interval.
			Ipv6RxFrameCount (uint64): Number of IPv6 frames received.
			Ipv6RxFrameRate (uint64): Number of IPv6 frames received over the last 1-second interval.
			Ipv6TxTotalFrameCount (uint64): Total number of IPv6 frames transmitted.
			Ipv6TxTotalFrameRate (uint64): Total number of IPv6 frames transmitted over the last 1-second interval.
			JumboTxFrameCount (uint64): Number of jumbo frames generated.
			JumboTxFrameRate (uint64): Number of jumbo frames generated over the last 1-second interval.
			JumboRxFrameCount (uint64): Number of jumbo frames received.
			JumboRxFrameRate (uint64): Number of jumbo frames received over the last 1-second interval.
			L3ChecksumErrorCount (uint64): Number of frames generated with an L3 checksum error.
			L3ChecksumErrorRate (uint64): Number of frames generated with an L3 header checksum, per second.
			L4ChecksumErrorCount (uint64): Number of frames generated with an L4 checksum error.
			L4ChecksumErrorRate (uint64): Number of frames generated with an L4 header checksum, per second.
			MplsTxFrameCount (uint64): Number of mpls frames generated.
			MplsTxFrameRate (uint64): Number of mpls frames generated over the last 1-second interval.
			MplsRxFrameCount (uint64): Number of mpls frames received.
			MplsRxFrameRate (uint64): Number of mpls frames received over the last 1-second interval.
			MplsTxTotalFrameCount (uint64): Total number of MPLS frames transmitted.
			MplsTxTotalFrameRate (uint64): Total number of MPLS frames transmitted over the last 1-second interval.
			OctetTxFrameCount (uint64): Number of octet frames generated.
			OctetTxFrameRate (uint64): Number of octet frames generated over the last 1-second interval.
			OctetRxFrameCount (uint64): Number of octet frames received.
			OctetRxFrameRate (uint64): Number of octet frames received over the last 1-second interval.
			OctetTxTotalFrameCount (uint64): Total number of octet frames transmitted.
			OctetTxTotalFrameRate (uint64): Total number of octet frames transmitted over the last 1-second interval.
			CellTxTotalFrameCount (uint64): Count of total cells generated.
			CellTxTotalFrameRate (uint64): Total number of bytes generated over last 1-second interval.
			OversizeTxFrameCount (uint64): Number of oversize frames generated.
			OversizeTxFrameRate (uint64): Number of oversize frames generated over the last 1-second interval.
			OversizeRxFrameCount (uint64): Number of oversize frames received.
			OversizeRxFrameRate (uint64): Number of oversize frames received over the last 1-second interval.
			UndersizeTxFrameCount (uint64): Number of undersize frames generated.
			UndersizeTxFrameRate (uint64): Number of undersize frames generated over the last 1-second interval.
			UndersizeRxFrameCount (uint64): Number of undersize frames received.
			UndersizeRxFrameRate (uint64): Number of undersize frames received over the last 1-second interval.
			SigTxFrameCount (uint64): Number of Spirent Signature frames generated.
			SigTxFrameRate (uint64): Number of Spirent Signature  frames generated over the last 1-second interval.
			SigRxFrameCount (uint64): Number of Spirent Signature  frames received.
			SigRxFrameRate (uint64): Number of Spirent Signature  frames received over the last 1-second interval.
			VlanTxFrameCount (uint64): Number of VLAN frames generated.
			VlanTxFrameRate (uint64): Number of VLAN frames generated over the last 1-second interval.
			VlanRxFrameCount (uint64): Number of VLAN frames received.
			VlanRxFrameRate (uint64): Number of VLAN frames received over the last 1-second interval.
			HwTxFrameCount (uint64): Number of Hardware frames generated.
			HwRxFrameCount (uint64): Number of Hardware frames received.
			L1TxBitCount (uint64): Count of total layer1 bits generated.
			L1TxBitRate (uint64): Total number of layer1 bits transmitted over last 1-second interval.
			L1TxBitRatePercent (decimal64): Total number of layer 1 bits transmitted in percentage.
			L1RxBitCount (uint64): Count of total layer1 bits received.
			L1RxBitRate (uint64): Total number of layer1 bits received over last 1-second interval.
			L1RxBitRatePercent (decimal64): Total number of layer 1 bits received in percentage.
			PfcTxFrameCount (uint64): Number of pause frames transmitted.
			PfcRxFrameCount (uint64): Number of pause frames received.
			PfcPriority0TxFrameCount (uint64): Number of priority-0 pause frames generated.
			PfcPriority1TxFrameCount (uint64): Number of priority-1 pause frames generated.
			PfcPriority2TxFrameCount (uint64): Number of priority-2 pause frames generated.
			PfcPriority3TxFrameCount (uint64): Number of priority-3 pause frames generated.
			PfcPriority4TxFrameCount (uint64): Number of priority-4 pause frames generated.
			PfcPriority5TxFrameCount (uint64): Number of priority-5 pause frames generated.
			PfcPriority6TxFrameCount (uint64): Number of priority-6 pause frames generated.
			PfcPriority7TxFrameCount (uint64): Number of priority-7 pause frames generated.
			PfcPriority0RxFrameCount (uint64): Number of priority-0 pause frames received.
			PfcPriority1RxFrameCount (uint64): Number of priority-1 pause frames received.
			PfcPriority2RxFrameCount (uint64): Number of priority-2 pause frames received.
			PfcPriority3RxFrameCount (uint64): Number of priority-3 pause frames received.
			PfcPriority4RxFrameCount (uint64): Number of priority-4 pause frames received.
			PfcPriority5RxFrameCount (uint64): Number of priority-5 pause frames received.
			PfcPriority6RxFrameCount (uint64): Number of priority-6 pause frames received.
			PfcPriority7RxFrameCount (uint64): Number of priority-7 pause frames received.
			ComboTriggerCount (uint64): Number of frames captured by all the triggers.
			ComboTriggerRate (uint64): Number of frames received by all the triggers over the last 1-second interval.
			CorrectedBaserFecErrorCount (uint64): Number of Corrected BaseR FEC Errors received.
			CorrectedRsFecErrorCount (uint64): Number of Corrected RS FEC Errors received.
			CorrectedRsFecSymbols (uint64): Number of Corrected RS FEC Symbols received.
			RxCounterTimestamp (uint64): Time when the counter was stored.
			DuplicateFrameCount (uint64): Number of duplicate frames received.
			FcoeRxFrameCount (uint64): Fiber channel over Ethernet frame count.
			FcoeRxFrameRate (uint64): Fiber channel over Ethernet frame rate.
			FcsRxFrameCount (uint64): Number of FCS error frames received.
			FcsRxFrameRate (uint64): Number of FCS error frames received over the last 1-second interval.
			FirstArrivalTimestamp (decimal64): Backplane first arrival timestamp received.
			LastArrivalTimestamp (decimal64): Backplane last arrival timestamp received.
			LateFrameCount (uint64): Number of late frames received.
			MaxFrameLength (uint64): Maximum frame length received (in bytes).
			MinFrameLength (uint64): Minimum frame length received (in bytes).
			IcmpRxFrameCount (uint64): Number of ICMP frames received.
			IcmpRxFrameRate (uint64): Number of ICMP frames received over the last 1-second interval.
			Ipv4ChecksumErrorRxFrameCount (uint64): Number of IPv4 checksum errors received.
			Ipv4ChecksumErrorRxFrameRate (uint64): Number of IPv4 checksum errors received over the last 1-second interval.
			InSequenceRxFrameCount (uint64): Number of frames received in sequence order.
			OutSequenceRxFrameCount (uint64): Number of frames received out of sequence order.
			Ipv6OverIpv4RxFrameCount (uint64): Number of IPv6 over IPv4 frames received.
			Ipv6OverIpv4RxFrameRate (uint64): Number of IPv6 over IPv4 frames received over the last 1-second interval.
			PauseRxFrameCount (uint64): Number of pause frames received.
			PauseRxFrameRate (uint64): Number of pause frames received over the last 1-second interval.
		"""
		return self._update(locals())

