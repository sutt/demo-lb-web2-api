class GithubException(Exception):
    """GitHub base exception"""
    pass


class CouldNotFetchGithubUser(GithubException):
    pass


class CouldNotFetchGithubIssue(GithubException):
    pass


class GithubIssueNotFound(GithubException):
    pass


class PullRequestException(GithubException):
    pass


class CouldNotFetchPullRequest(PullRequestException):
    pass


class PullRequestNotFound(PullRequestException):
    pass


class PullRequestNotMerged(PullRequestException):
    pass


class MergedIntoWrongBranch(PullRequestException):
    pass
