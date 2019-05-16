import random as r
import pygame
from pygame.locals import *

class Vertex():

	def __init__(self, edges=[], value=0):
		self.incident_edges = edges
		self.value = value

class Edge():

	def __init__(self, vertices=[], weight=0):
		self.incident_vertices = vertices
		self.weight = weight

class Graph():

	def __init__(self):
		self.vertices = []
		self.edges = []

	def is_adjacent(self, a, b):
		adjacent = False
		for edge in a.incident_edges:
			if b in edge.incident_vertices:
				adjacent = True
		return adjacent

	def neighbours(self, a):
		neighbours = []
		for edge in a.incident_edges:
			for vertex in edge.incident_vertices:
				neighbours.append(vertex)
		return neighbours

	def add_vertex(self, value):
		self.vertices.append(Vertex(value=value))
		
	def remove_vertex(self, a):
		if a in self.vertices:
			for edge in self.edges:
				if a in edge.incident_vertices:
					self.edges.remove(edge)
			self.vertices.remove(a)
		else raise ValueError("Vertex does not exist")

	def add_edge(self, a, b, weight):
		if not is_adjacent(a, b):
			edge = Edge([a,b], weight)
			self.edges.append(edge)
			a.incident_edges.append(edge)
			b.incident_edges.append(edge)

	def remove_edge(self, a, b):
		if is_adjacent(a, b):
			edge = set(a).intersection(b)
			a.incident_edges.remove(edge)
			b.incident_edges.remove(edge)
			self.edges.remove(edge)
		else:
			raise ValueError("Edge does not exist")

	def get_vertex_value(self, a):
		return a.value

	def set_vertex_value(self, a, value):
		a.value = value

	def get_edge_value(self, a, b):






