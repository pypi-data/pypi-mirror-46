from openhltest_client.base import Base


class ExtendedLsaCounters(Base):
	"""Extended LSA counters.
	"""
	YANG_NAME = 'extended-lsa-counters'
	YANG_KEYWORD = 'container'
	YANG_KEY = None
	YANG_PROPERTY_MAP = {"TxLinkLsa": "tx-link-lsa", "TxInterAreaRouterLsa": "tx-inter-area-router-lsa", "RxLinkLsa": "rx-link-lsa", "TxNssaLsa": "tx-nssa-lsa", "TxNetworkLsa": "tx-network-lsa", "RxInterAreaRouterLsa": "rx-inter-area-router-lsa", "TxAsExternalLsa": "tx-as-external-lsa", "RxNetworkLsa": "rx-network-lsa", "TxInterAreaPrefixLsa": "tx-inter-area-prefix-lsa", "RxIntraAreaPrefixLsa": "rx-intra-area-prefix-lsa", "RxNssaLsa": "rx-nssa-lsa", "RxInterAreaPrefixLsa": "rx-inter-area-prefix-lsa", "RxAsExternalLsa": "rx-as-external-lsa", "RxRouterLsa": "rx-router-lsa", "TxIntraAreaPrefixLsa": "tx-intra-area-prefix-lsa", "TxRouterLsa": "tx-router-lsa"}
	YANG_ACTIONS = []

	def __init__(self, parent):
		super(ExtendedLsaCounters, self).__init__(parent)

	@property
	def RxAsExternalLsa(self):
		"""Received external-LSAs. The number of external LSAs received by theemulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-as-external-lsa')

	@property
	def RxInterAreaPrefixLsa(self):
		"""Received inter-area-prefix LSAs. The number of inter-area-prefix LSAsreceived by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-inter-area-prefix-lsa')

	@property
	def RxInterAreaRouterLsa(self):
		"""Received inter-area-router LSAs. The number of inter-area-router LSAsreceived by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-inter-area-router-lsa')

	@property
	def RxIntraAreaPrefixLsa(self):
		"""Received Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs receivedby the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-intra-area-prefix-lsa')

	@property
	def RxLinkLsa(self):
		"""Received link-LSAs. The number of link LSAs received by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-link-lsa')

	@property
	def RxNetworkLsa(self):
		"""Received Network-LSAs - Number of Network LSAs received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-network-lsa')

	@property
	def RxNssaLsa(self):
		"""Received Link-LSAs. The number of Link LSAs received by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-nssa-lsa')

	@property
	def RxRouterLsa(self):
		"""Received Router-LSAs - Number of Router LSAs received by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('rx-router-lsa')

	@property
	def TxAsExternalLsa(self):
		"""Sent external-LSAs. The number of external LSAs sent by the emulatedrouter.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-as-external-lsa')

	@property
	def TxInterAreaPrefixLsa(self):
		"""Sent inter-area-prefix LSAs. The number of inter-area-prefix LSAs sent bythe emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-inter-area-prefix-lsa')

	@property
	def TxInterAreaRouterLsa(self):
		"""Sent inter-area-router LSAs. The number of inter-area-router LSAs sent bythe emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-inter-area-router-lsa')

	@property
	def TxIntraAreaPrefixLsa(self):
		"""Sent Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs sent by theemulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-intra-area-prefix-lsa')

	@property
	def TxLinkLsa(self):
		"""Sent link-LSAs. The number of link LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-link-lsa')

	@property
	def TxNetworkLsa(self):
		"""Sent Network-LSAs - Number of Network LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-network-lsa')

	@property
	def TxNssaLsa(self):
		"""Sent NSSA-LSAs. The number of NSSA LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-nssa-lsa')

	@property
	def TxRouterLsa(self):
		"""Sent Router-LSAs - Number of Router LSAs sent by the emulated router.

		Getter Returns:
			uint64
		"""
		return self._get_value('tx-router-lsa')

	def update(self, RxAsExternalLsa=None, RxInterAreaPrefixLsa=None, RxInterAreaRouterLsa=None, RxIntraAreaPrefixLsa=None, RxLinkLsa=None, RxNetworkLsa=None, RxNssaLsa=None, RxRouterLsa=None, TxAsExternalLsa=None, TxInterAreaPrefixLsa=None, TxInterAreaRouterLsa=None, TxIntraAreaPrefixLsa=None, TxLinkLsa=None, TxNetworkLsa=None, TxNssaLsa=None, TxRouterLsa=None):
		"""Update the current instance of the `extended-lsa-counters` resource

		Args:
			RxAsExternalLsa (uint64): Received external-LSAs. The number of external LSAs received by theemulated router.
			RxInterAreaPrefixLsa (uint64): Received inter-area-prefix LSAs. The number of inter-area-prefix LSAsreceived by the emulated router.
			RxInterAreaRouterLsa (uint64): Received inter-area-router LSAs. The number of inter-area-router LSAsreceived by the emulated router.
			RxIntraAreaPrefixLsa (uint64): Received Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs receivedby the emulated router.
			RxLinkLsa (uint64): Received link-LSAs. The number of link LSAs received by the emulatedrouter.
			RxNetworkLsa (uint64): Received Network-LSAs - Number of Network LSAs received by the emulated router.
			RxNssaLsa (uint64): Received Link-LSAs. The number of Link LSAs received by the emulatedrouter.
			RxRouterLsa (uint64): Received Router-LSAs - Number of Router LSAs received by the emulated router.
			TxAsExternalLsa (uint64): Sent external-LSAs. The number of external LSAs sent by the emulatedrouter.
			TxInterAreaPrefixLsa (uint64): Sent inter-area-prefix LSAs. The number of inter-area-prefix LSAs sent bythe emulated router.
			TxInterAreaRouterLsa (uint64): Sent inter-area-router LSAs. The number of inter-area-router LSAs sent bythe emulated router.
			TxIntraAreaPrefixLsa (uint64): Sent Intra-Area-Prefix-LSAs - Number of Intra-Area-Prefix LSAs sent by theemulated router.
			TxLinkLsa (uint64): Sent link-LSAs. The number of link LSAs sent by the emulated router.
			TxNetworkLsa (uint64): Sent Network-LSAs - Number of Network LSAs sent by the emulated router.
			TxNssaLsa (uint64): Sent NSSA-LSAs. The number of NSSA LSAs sent by the emulated router.
			TxRouterLsa (uint64): Sent Router-LSAs - Number of Router LSAs sent by the emulated router.
		"""
		return self._update(locals())

