import pytest
from sib.project import Project

def test_load_project_for_development():

    # load project from previous testing phase
    project = Project('sibproject', '/tmp/sib-dev', [])

    assert project.load('test', 'test', 'test@test.io')
