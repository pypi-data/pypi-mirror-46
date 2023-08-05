# -*- coding unix -*-

from collections import namedtuple 

Story = namedtuple('Story', ['name', 'description', 'points', 'completed'])
Sprint = namedtuple('Sprint', ['name', 'pointList', 'totalPoints', 'totalDays', 'stories'])
Backlog = namedtuple('Backlog', ['sprints'])
