# -*- coding: utf-8 -*-
# Copyright (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations


from ansible.utils.display import Display
from unittest.mock import MagicMock


def test_display_with_fake_cowsay_binary(capsys, mocker):
    display = Display()

    mocker.patch("ansible.constants.ANSIBLE_COW_PATH", "./cowsay.sh")

    mock_popen = MagicMock()
    mock_popen.return_value.returncode = 1
    mocker.patch("subprocess.Popen", mock_popen)

    assert not hasattr(display, "cows_available")
    assert display.b_cowsay is None


def test_display_with_fake_cowsay_binary2(mocker):
    # Mock subprocess.Popen to simulate a command failure
    mock_popen = MagicMock()
    mock_popen.return_value.communicate.return_value = (b"", b"Error")
    mock_popen.return_value.returncode = 1
    mocker.patch('subprocess.Popen', return_value=mock_popen)

    # Optionally mock os.path.exists if it affects the test outcome
    mocker.patch('os.path.exists', return_value=False)

    # Ensure C.ANSIBLE_COW_PATH does not return a valid path
    mocker.patch('ansible.constants.ANSIBLE_COW_PATH', new_callable=mocker.PropertyMock, return_value=None)

    # Instantiate Display
    display = Display()

    # Assert 'cows_available' attribute should not be set
    assert not hasattr(display, 'cows_available'), "cows_available should not be set if cowsay command fails"
    assert display.b_cowsay is None
