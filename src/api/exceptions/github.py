class GithubException(Exception):
    """GitHub base exception"""
    pass


class CouldNotFetchGithubUser(GithubException):
    pass
