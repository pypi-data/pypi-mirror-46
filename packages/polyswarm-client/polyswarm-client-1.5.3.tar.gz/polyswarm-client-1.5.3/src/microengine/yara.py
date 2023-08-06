import logging
import os
import yara

from polyswarmclient.abstractmicroengine import AbstractMicroengine
from polyswarmclient.abstractscanner import AbstractScanner, ScanResult

logger = logging.getLogger(__name__)  # Initialize logger
RULES_DIR = os.getenv('RULES_DIR', 'docker/yara-rules')


class Scanner(AbstractScanner):
    def __init__(self):
        self.rules = yara.compile(os.path.join(RULES_DIR, "malware/MALW_Eicar"))

    async def scan(self, guid, content, chain):
        """Scan an artifact with Yara.

        Args:
            guid (str): GUID of the bounty under analysis, use to track artifacts in the same bounty
            content (bytes): Content of the artifact to be scan
            chain (str): Chain we are operating on

        Returns:
            ScanResult: Result of this scan
        """
        matches = self.rules.match(data=content)
        if matches:
            return ScanResult(bit=True, verdict=True)

        return ScanResult(bit=True, verdict=False)


class Microengine(AbstractMicroengine):
    """Microengine which matches samples against yara rules"""

    def __init__(self, client, testing=0, scanner=None, chains=None):
        """Initialize a Yara microengine

        Args:
            client (`Client`): Client to use
            testing (int): How many test bounties to respond to
            chains (set[str]): Chain(s) to operate on
        """
        scanner = Scanner()
        super().__init__(client, testing, scanner, chains)
