from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VcsConfiguration(object):
    """VCS configuration.
    :param url: VCS repository URL.
    :param ssh_key: Private SSH key in OpenSSH format.
    :param ssh_key_passphrase: SSH key passphrase.
    :param sync_token: OAuth token.
    :param vcs: VCS type ID, one of "git", mercurial", "perforce", "svn".
    :param pull_requests: Optional, enables "Import pull requests as branches".
    :param sync_comments: Optional, enables "Synchronize comments and pull requests".
    :param mapping: Repository mapping.
    :param server_type: VCS server type.
    :param id: ID of the first repository is "id", IDs of other repositories are arbitrary
               alphanumeric strings.
    """
    url: str
    ssh_key: str
    ssh_key_passphrase: str
    sync_token: str
    vcs: str = "git"
    pull_requests: str = "gitlab"
    sync_comments: str = "gitlab"
    mapping: str = "/"
    server_type: str = "gitlab"
    id: str = ""

    def __post_init__(self):
        if not self.url:
            raise ValueError('VCS repository URL is required parameter.')
        if not self.ssh_key:
            raise ValueError('Private SSH key is required parameter.')

    def asdict(self) -> Dict[str, str]:
        return {
            "vcs": self.vcs,
            "url": self.url,
            "key": self.ssh_key,
            "key-passphrase": self.ssh_key_passphrase,
            "pull-requests": self.pull_requests,
            "sync-comments": self.sync_comments,
            "sync-token": self.sync_token,
            "mapping": self.mapping,
            "server-type": self.server_type,
            "id": self.id
        }
