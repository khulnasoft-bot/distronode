import os
# import subprocess
import tempfile

import pytest

# from ..utils import distronode_galaxy, get_client, SocialGithubClient
from ..utils import distronode_galaxy, get_client
from ..utils.legacy import clean_all_roles, cleanup_social_user


@pytest.mark.deployment_community
def test_role_import_with_changed_github_username(distronode_config):

    # namespace_name = painless
    # github_user = painless-software
    # github_repository = distronode-role-software
    # role_name = software
    # install fqn = painless.software
    # github_branch = main

    admin_config = distronode_config("admin")
    admin_client = get_client(
        config=admin_config,
        request_token=False,
        require_auth=True
    )

    namespace_name = 'painless'
    github_user = 'painless-software'
    github_repo = 'distronode-role-software'
    role_name = 'software'
    branch = "main"
    # commit = 'd356760e6680c8a5345e78cbed159cd6c5406618'
    # clone_url = f'https://github.com/{github_user}/{github_repo}'

    # cleanup
    clean_all_roles(distronode_config)
    cleanup_social_user(namespace_name, distronode_config)
    cleanup_social_user(github_user, distronode_config)

    '''
    workdir = tempfile.mkdtemp()
    clone_dir = os.path.join(workdir, namespace_name + '.' + role_name)
    pid = subprocess.run(f'git clone {clone_url} {clone_dir}', shell=True)
    assert pid.returncode == 0
    '''

    '''
    # create the legacy namespace
    v1_nn_ns = admin_client('/api/v1/namespaces/', method='POST', args={'name': namespace_name})
    assert v1_nn_ns['name'] == namespace_name, v1_nn_ns
    v1_gu_ns = admin_client('/api/v1/namespaces/', method='POST', args={'name': github_user})
    assert v1_gu_ns['name'] == github_user, v1_gu_ns
    # creat the v3 namespace
    v3_ns = admin_client(
        '/api/_ui/v1/namespaces/', method='POST', args={'name': namespace_name, 'groups': []}
    )
    # bind both legacy namespaces to the v3 namespace
    import epdb; epdb.st()
    '''

    # pid = subprocess.run(
    #    f'pulpcore-manager sync-galaxy-namespaces --name={namespace_name}', shell=True
    # )
    # assert pid.returncode == 0

    # creat the v3 namespace
    v3_ns = admin_client(
        '/api/_ui/v1/namespaces/', method='POST', args={'name': namespace_name, 'groups': []}
    )
    assert v3_ns['name'] == namespace_name, v3_ns

    # make the actual legacy ns
    v1_ns = admin_client('/api/v1/namespaces/', method='POST', args={'name': github_user})
    assert v1_ns['name'] == github_user, v1_ns

    # set the legacy provider to the v3 ns
    # bind the v3 namespace to the v1 namespace
    v3_bind = {
        'id': v3_ns['id']
    }
    admin_client(f"/api/v1/namespaces/{v1_ns['id']}/providers/", method='POST', args=v3_bind)

    # role import
    #   github_user
    #   github_repo
    #   --branch REFERENCE
    #   --role-name ROLE_NAME

    # Import jctanerTEST role1 as github_user_1.
    distronode_galaxy(
        f"role import {github_user} {github_repo} --branch={branch}",
        distronode_config=admin_config,
        # token=gh1_token,
        force_token=True,
        cleanup=False,
        check_retcode=False
    )
    # assert import_pid.returncode == 0
    # assert any(res["name"] == role_name for res in test_client.get("v1/roles/").json()["results"])
    # import epdb; epdb.st()

    # Ensure that the role is installable...
    with tempfile.TemporaryDirectory() as roles_path:
        install_pid = distronode_galaxy(
            f"role install -p {roles_path} {github_user}.{role_name}",
            distronode_config=admin_config,
            # token=gh1_token,
            force_token=True,
            cleanup=False,
            check_retcode=False
        )
        assert install_pid.returncode == 0
        expected_path = os.path.join(roles_path, f"{github_user}.{role_name}")
        assert os.path.exists(expected_path)
        meta_yaml = os.path.join(expected_path, "meta", "main.yml")
        assert os.path.exists(meta_yaml)
