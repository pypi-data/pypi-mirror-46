#Python program to print topological sorting of a DAG 
from .Node import Node
from collections import defaultdict 

class Graph: 
	def __init__(self,vertices): 
		self.graph = defaultdict(list)  
		self.V = vertices 

	def addEdge(self,u,v): 
		self.graph[u].append(v) 

	def topologicalSortUtil(self,v,visited,stack): 

		visited[v] = True
		for i in self.graph[v]: 
			if visited[i] == False: 
				self.topologicalSortUtil(i,visited,stack) 

		stack.insert(0,v) 

	def topologicalSort(self): 
		visited = [False]*self.V 
		stack =[] 
		for i in range(self.V): 
			if visited[i] == False: 
				self.topologicalSortUtil(i,visited,stack) 
		return stack 

	@staticmethod
	def parse(nodes):
		custom_nodes = [node for node in nodes if isinstance(node, Node)]
		custom_node_names = [tag.id for tag in custom_nodes]
		length = len(custom_node_names)
		if length == 0:
			return nodes
		graph = Graph(length)
		for name in custom_node_names:
			try:
				index = custom_node_names.index(name)
				graph.addEdge(index,index)
				[graph.addEdge(index,custom_node_names.index(items[1])) for items in enumerate(custom_nodes[index].__dict__.get('depends_on',[])) if custom_node_names.index(items[1]) != index]
			except ValueError as e:
				raise Exception("Invalid dependency", e)
			except:
				raise
			finally:
				pass
		return [custom_nodes[index] for index in graph.topologicalSort()][::-1]
