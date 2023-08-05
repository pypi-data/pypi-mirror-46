# -*- coding unix -*-

import lmrt4u.renderer as renderer
import lmrt4u.loader as loader
import lmrt4u.validator as validator
import lmrt4u.parser as parser

def process(input):
    """Proceses and passes input between modules"""
    if input is None:
        return
    activity = input["activity"]
    if (activity == "Burndown Chart" or activity == "Burnup Chart" or activity == "Burndown Exit"):
        contents = loader.loadDocument()
        if (validator.validate(contents)):
                backlog = parser.parseBacklogContents(contents)
                for sprintKey in backlog.sprints:
                    sprint = backlog.sprints[sprintKey]
                    renderer.renderAscii(sprint.totalPoints, sprint.pointList, sprint.totalDays)
