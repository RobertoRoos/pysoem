from typing import List, Optional, NamedTuple

class Master:
    """Representing a logical EtherCAT master device.

    For each network interface you can have a Master instance.

    Attributes:
        slaves: Gets a list of the slaves found during config_init. The slave instances are of type :class:`CdefSlave`.
        sdo_read_timeout: timeout for SDO read access for all slaves connected
        sdo_write_timeout: timeout for SDO write access for all slaves connected
    """

    slaves: List["CdefSlave"]
    sdo_read_timeout: int
    sdo_write_timeout: int

    def close(self) -> None:
        """Close the network interface."""

    def config_dc(self) -> bool:
        """Locate DC slaves, measure propagation delays.

        Returns:
            If slaves are found with DC
        """

    def config_init(self, usetable: bool = False) -> int:
        """Enumerate and init all slaves.

        Args:
            usetable: True when using configtable to init slaves, False otherwise

        Returns:
            Working counter of slave discover datagram = number of slaves found, -1 when no slave is connected
        """

    def config_map(self) -> int:
        """Map all slaves PDOs in IO map.

        Returns:
            IO map size (sum of all PDO in an out data)
        """

    def config_overlap_map(self) -> int:
        """Map all slaves PDOs to overlapping IO map.

        Returns:
            IO map size (sum of all PDO in an out data)
        """

    @property
    def dc_time(self) -> int: ...
    @property
    def expected_wkc(self) -> int: ...
    def open(self, ifname: str, ifname_red: Optional[str] = None) -> None:
        """Initialize and open network interface.

        On Linux the name of the interface is the same as usd by the system, e.g. ``eth0``, and as displayed by
        ``ip addr``.

        On Windows the names of the interfaces look like ``\\Device\\NPF_{1D123456-1E12-1C12-12F1-1234E123453B}``.
        Finding the kind of name that SOEM expects is not straightforward. The most practical way is to use the
        :func:`~find_adapters` method to find your available interfaces.

        Args:
            ifname: Interface name.
            ifname_red: Interface name of the second network interface card for redundancy.
                Put to ``None`` if not used.

        Raises:
            ConnectionError: When the specified interface dose not exist or
                you have no permission to open the interface
        """

    def read_state(self) -> int:
        """Read all slaves states.

        Returns:
            Lowest state found
        """

    def receive_processdata(self, timeout: int = 2000) -> int:
        """Receive processdata from slaves.

        Second part from send_processdata().
        Received datagrams are recombined with the processdata with help from the stack.
        If a datagram contains input processdata it copies it to the processdata structure.

        Args:
            timeout: Timeout in us.
        Returns
            Working Counter
        """

    def send_overlap_processdata(self) -> int:
        """Transmit overlap processdata to slaves.

        Returns:
            >0 if processdata is transmitted, might only by 0 if config map is not configured properly
        """

    def send_processdata(self) -> int:
        """Transmit processdata to slaves.

        Uses LRW, or LRD/LWR if LRW is not allowed (blockLRW).
        Both the input and output processdata are transmitted.
        The outputs with the actual data, the inputs have a placeholder.
        The inputs are gathered with the receive processdata function.
        In contrast to the base LRW function this function is non-blocking.
        If the processdata does not fit in one datagram, multiple are used.
        In order to recombine the slave response, a stack is used.

        Returns:
            >0 if processdata is transmitted, might only by 0 if config map is not configured properly
        """

    @property
    def state(self) -> int: ...
    def state_check(self, expected_state: int, timeout: int = 50000) -> int:
        """Check actual slave state.

        This is a blocking function.
        To refresh the state of all slaves read_state() should be called

        Args:
            expected_state: Requested state
            timeout: Timeout value in us

        Returns:
            Requested state, or found state after timeout
        """

    def write_state(self) -> int:
        """Write all slaves state.

        The function does not check if the actual state is changed.

        Returns:
            Working counter or EC_NOFRAME
        """

class CdefSlave:
    config_func: Optional[callable]
    name: str
    id: int
    man: int
    rev: int

    def dc_sync(
        self,
        act: bool,
        sync0_cycle_time: int,
        sync0_shift_time: int = 0,
        sync1_cycle_time: Optional[int] = None,
    ) -> None: ...
    def eeprom_read(self, word_address: int, timeout: int = 20000) -> bytes: ...
    def eeprom_write(
        self, word_address: int, data: bytes, timeout: int = 20000
    ) -> None: ...
    def foe_read(
        self, filename: str, password: int, size: int, timeout: int = 200000
    ) -> bytes: ...
    def foe_write(
        self, filename: str, password: int, data: bytes, timeout: int = 200000
    ) -> None: ...
    def mbx_receive(self) -> int: ...
    def reconfig(self, timeout: int = 500) -> int: ...
    def recover(self, timeout: int = 500) -> int: ...
    def sdo_read(
        self, index: int, subindex: int, size: int = 0, ca: bool = False
    ) -> bytes: ...
    def sdo_write(
        self, index: int, subindex: int, data: bytes, ca: bool = False
    ) -> None: ...

# Additional helper functions
def find_adapters() -> List["Adapter"]:
    """Create a list of available network adapters.

    Returns:
        Each element of the list has a name an desc attribute.

    """

def al_status_code_to_string(code: int) -> str:
    """Look up text string that belongs to AL status code.

    Args:
        code: AL status code as defined in EtherCAT protocol.

    Returns:
        A verbal description of status code

    """

class Adapter(NamedTuple):
    name: str
    desc: str
