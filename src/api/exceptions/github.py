class GithubException(Exception):
    """GitHub base exception"""
    pass


class CouldNotFetchGithubUser(GithubException):
    pass


class CouldNotFetchGithubIssue(GithubException):
    pass


class GithubIssueNotFound(GithubException):
    pass
