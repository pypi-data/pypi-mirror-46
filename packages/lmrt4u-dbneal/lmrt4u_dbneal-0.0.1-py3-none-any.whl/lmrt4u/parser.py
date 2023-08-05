# -*- coding unix -*-

import lmrt4u.tuples as tuples
import lmrt4u.helpers as helpers
import datetime

def parseBacklogContents(rawData):
    """Load validated raw dictionary content into structure of named tuples"""
    sprints = {}
    rawSprints = rawData['sprints']
    for sprintKey in rawSprints:
        # Ignore inactive sprints
        if not rawSprints[sprintKey]['active']:
            continue
        pointsByDate = {}
        totalPoints = 0
        stories = []
        for attr in rawSprints[sprintKey]['stories']:
            # Stories are stored as lists, so we can load them into tuple positionally
            story = tuples.Story(*attr)
            stories.append(story)
            totalPoints += story.points
            if story.completed in pointsByDate.keys():
                pointsByDate[story.completed] += story.points
            else:
                pointsByDate[story.completed] = story.points
        name = sprintKey
        start = rawSprints[sprintKey]['start']
        end = rawSprints[sprintKey]['end']
        pointList = []
        startDate = helpers.to_date(start)
        endDate = helpers.to_date(end)
        delta = endDate - startDate
        mutablePoints = totalPoints
        # Iterate between the two dates
        for i in range(delta.days):
            dateString = (startDate + datetime.timedelta(i)).strftime("%Y-%m-%d")
            if dateString in pointsByDate.keys():
                mutablePoints -= pointsByDate[dateString]
            pointList.append(mutablePoints)
        # Create sprint tuple object and add object to dictionary
        sprint = tuples.Sprint(name, pointList, totalPoints, delta.days, stories)
        sprints[sprintKey] = sprint
    # Create backlog tuple consisting of dictionary of sprint tuples
    backlog = tuples.Backlog(sprints)
    return backlog
