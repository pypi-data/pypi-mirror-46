from Utilities.Console import Console

from Protocols.Git.GitRepoHandler import GitRepoHandler
from Protocols.Hg.HgRepoHandler import HgRepoHandler

SUPPORTED_PROTOCOLS = [GitRepoHandler.GIT_ID, HgRepoHandler.HG_ID]


def resolve_repo_handler(resolved_repo=None, full_repo_path=None):
    """
    Given a resolved repo, find the protocol implementation it should use.  The caller may specify either a resolved
    repo object or a path to a repo on disk.  If a path is specified, the available functional command are limited to
    add, commit, tag, and push.
    :param resolved_repo: A previously resolved repo.
    :param full_repo_path: The path to a possible repo on disk but without the resolved info like revision, url, etc
    :return: A protocol provider or None if it can't find a match.
    """

    if resolved_repo:
        if resolved_repo.protocol == GitRepoHandler.GIT_ID:
            if GitRepoHandler.have_git():
                return GitRepoHandler(resolved_repo=resolved_repo, full_repo_path=full_repo_path)
            else:
                Console.error("Repo " + str(resolved_repo.repo_path) + " requires GIT but it is not available.")
                return None
        elif resolved_repo.protocol == HgRepoHandler.HG_ID:
            if HgRepoHandler.have_hg():
                return HgRepoHandler(resolved_repo=resolved_repo, full_repo_path=full_repo_path)
            else:
                Console.error("Repo " + str(resolved_repo.repo_path) + " requires HG but it is not available.")
                return None
        else:
            Console.error("Could not resolve a handler for protocol: " + resolved_repo.protocol)
            return None

    if full_repo_path:
        if GitRepoHandler.have_git() and GitRepoHandler.is_git_dir(full_repo_path):
            return GitRepoHandler(full_repo_path=full_repo_path)
        elif HgRepoHandler.have_hg() and HgRepoHandler.is_hg_dir(full_repo_path):
            return HgRepoHandler(full_repo_path=full_repo_path)
        else:
            return None

    return None


def get_protocol_status():
    git_status = GitRepoHandler.GIT_ID

    if GitRepoHandler.have_git():
        git_status += " [OK]: " + GitRepoHandler.get_git_version_string()
    else:
        git_status += " [MISSING]"

    hg_status = HgRepoHandler.HG_ID

    if HgRepoHandler.have_hg():
        hg_status += " [OK]: " + HgRepoHandler.get_hg_version_string()
    else:
        hg_status += " [MISSING]"

    return [git_status, hg_status]
