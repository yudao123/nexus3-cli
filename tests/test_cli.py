import itertools
import pytest

import nexuscli


def test_login(mocker):
    mocker.patch('nexuscli.cli.do_login')
    mocker.patch('nexuscli.cli.get_client')

    nexuscli.cli.main(argv=['login'])

    nexuscli.cli.do_login.assert_called_once()
    nexuscli.cli.get_client.assert_called_once()


def test_repo_list(mocker):
    mocker.patch('nexuscli.cli.get_client')
    mocker.patch('nexuscli.cli.cmd_repo_do_list')

    argv = 'repo list'.split(' ')
    nexuscli.cli.main(argv=argv)

    nexuscli.cli.get_client.assert_called_once()
    nexuscli.cli.cmd_repo_do_list.assert_called_with(
        nexuscli.cli.get_client.return_value)


@pytest.mark.parametrize(
    'repo_format, w_policy, strict', itertools.product(
        ['npm', 'pypi', 'raw', 'rubygems', 'yum'],  # format
        list(nexuscli.cli.NexusClient.POLICIES['write']),  # w_policy
        ['', '--strict-content'],  # strict
    ))
@pytest.mark.integration
def test_repo_create_hosted(repo_format, w_policy, strict, nexus_client):
    strict_name = strict[2:8]
    repo_name = 'hosted-{repo_format}-{w_policy}-{strict_name}'.format(
        **locals())
    argv = ('repo create hosted {repo_format} {repo_name} '
            '--write={w_policy} {strict}'.format(**locals())).split(' ')

    nexuscli.cli.main(argv=list(filter(None, argv)))

    repositories = nexus_client.repo_list()

    assert any(r['name'] == repo_name for r in repositories)
