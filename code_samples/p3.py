class Calculator:
    def __init__(self, value=0):
        self.value = value  # declaration of an instance variable

    def add(self, amount):
        self.value += amount
        return self.value

    def subtract(self, amount):
        self.value -= amount
        return self.value


# Example usage
calc = Calculator(10)
print(calc.add(5))  # Output: 15
print(calc.subtract(3))  # Output: 12





# def extract_points_of_interest_grouped(self, node: Node, file_extension: str, current_depth: int = 0, max_depth: int = 2) -> List[List[List[Tuple[Node, str]]]]:
#         """
#         Args:
#             node (Node): The current AST node.
#             file_extension (str): The file extension to determine language-specific node types.
#             current_depth (int): The current depth in the node hierarchy.
#             max_depth (int): The maximum depth to process nodes.

#         Returns:
#             List[List[List[Tuple[Node, str]]]]: A list of groups, where each group contains
#                                                 sublists of tuples (Node, Type).
#         """
#         grouping_types = self._get_node_types_of_interest(file_extension)
#         grouped_points = []

#         # Base case: Stop processing if maximum depth is exceeded
#         if current_depth > max_depth:
#             return grouped_points

#         # Process the current node
#         if node.type in grouping_types.keys():
#             # Create a group for the current node
#             current_group = [[(node, grouping_types[node.type])]]
            
#             # Process child nodes and group them recursively
#             for child in node.children:
#                 child_groups = self.extract_points_of_interest_grouped(
#                     child, file_extension, current_depth + 1, max_depth
#                 )
#                 if child_groups:
#                     current_group.extend(child_groups)
            
#             grouped_points.append(current_group)
#         else:
#             # Process children independently if the current node isn't a grouping node
#             for child in node.children:
#                 grouped_points.extend(
#                     self.extract_points_of_interest_grouped(
#                         child, file_extension, current_depth + 1, max_depth
#                     )
#                 )

#         return grouped_points
