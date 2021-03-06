# -*- encoding: utf-8 -*-
#
# Copyright © 2018 Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from unittest import mock

from mergify_engine import duplicate_pull
from mergify_engine import mergify_pull


def fake_get_github_pulls_from_sha(repo, sha):
    if sha.startswith("rebased_c"):
        return [mock.Mock(number=6)]
    else:
        return []


@mock.patch(
    "mergify_engine.duplicate_pull.utils.get_github_pulls_from_sha",
    side_effect=fake_get_github_pulls_from_sha,
)
@mock.patch(
    "mergify_engine.mergify_pull.MergifyPull.g_pull", return_value=mock.PropertyMock
)
@mock.patch(
    "mergify_engine.mergify_pull.MergifyPull.commits", new_callable=mock.PropertyMock
)
def test_get_commits_to_cherry_pick_rebase(commits, g_pull, _):
    c1 = {"sha": "c1f", "parents": [], "commit": {"message": "foobar"}}
    c2 = {"sha": "c2", "parents": [c1], "commit": {"message": "foobar"}}
    commits.return_value = [c1, c2]

    client = mock.Mock()
    client.auth.get_access_token.return_value = "<token>"

    pull = mergify_pull.MergifyPull(
        client,
        {
            "number": 6,
            "merged": True,
            "state": "closed",
            "html_url": "<html_url>",
            "base": {"ref": "ref", "repo": {"name": "name", "private": False}},
            "user": {"login": "user"},
            "merged_by": None,
            "merged_at": None,
            "mergeable_state": "clean",
        },
    )

    base_branch = {"sha": "base_branch", "parents": []}
    rebased_c1 = {"sha": "rebased_c1", "parents": [base_branch]}
    rebased_c2 = {"sha": "rebased_c2", "parents": [rebased_c1]}

    assert duplicate_pull._get_commits_to_cherrypick(pull, rebased_c2) == [
        rebased_c1,
        rebased_c2,
    ]


@mock.patch(
    "mergify_engine.mergify_pull.MergifyPull.g_pull", return_value=mock.PropertyMock
)
@mock.patch(
    "mergify_engine.mergify_pull.MergifyPull.commits", new_callable=mock.PropertyMock
)
def test_get_commits_to_cherry_pick_merge(commits, g_pull):
    c1 = {"sha": "c1f", "parents": [], "commit": {"message": "foobar"}}
    c2 = {"sha": "c2", "parents": [c1], "commit": {"message": "foobar"}}
    commits.return_value = [c1, c2]

    client = mock.Mock()
    client.auth.get_access_token.return_value = "<token>"

    pull = mergify_pull.MergifyPull(
        client,
        {
            "number": 6,
            "merged": True,
            "state": "closed",
            "html_url": "<html_url>",
            "base": {"ref": "ref", "repo": {"name": "name", "private": False}},
            "user": {"login": "user"},
            "merged_at": None,
            "merged_by": None,
            "mergeable_state": "clean",
        },
    )

    base_branch = {"sha": "base_branch", "parents": []}
    merge_commit = {"sha": "merge_commit", "parents": [base_branch, c2]}

    assert duplicate_pull._get_commits_to_cherrypick(pull, merge_commit) == [c1, c2]
