# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 16:02:57 2025

@author: joach
"""
from enum import Enum

class CrosshairMode(Enum):
	Normal = 0
	Magnet = 1
	Hidden = 2
	MagnetOHLC = 3

class LineStyle(Enum):
	Solid = 0
	Dotted = 1
	Dashed = 2
	LargeDashed = 3
	SparseDotted = 4
	
class MismatchDirection(Enum):
	NearestLeft = -1
	NoSearch = 0
	NearestRight = 1