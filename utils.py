"""Helpers for the Prycing notebooks"""

def gauss_first_formula(n):
    """Gauss first formula to sum the first n integers."""
    return n * (n + 1) // 2

class Tree():
    """Models a binomial tree."""
    def __init__(self, height, value=float('NaN')):
        """Create a tree as a list filled with the value of value."""
        if height < 0:
            raise Exception('height should be nonnegative')
        self.height = height
        self._nodes = [value] * gauss_first_formula(height)

    def get_level(self, level):
        """Get all nodes on a certain level."""
        if level < 0:
            raise Exception('level should be nonnegative')

        last_node = gauss_first_formula(level)
        if last_node > len(self._nodes):
            raise Exception('tree lower than given level')

        return self._nodes[gauss_first_formula(level - 1):last_node]

    def get_node(self, level, element):
        """Get the ith node from level"""
        if element > level:
            raise Exception('element out of bounds')
        return self._nodes[gauss_first_formula(level) + element]

    def set_node(self, level, element, value):
        """Set an element in the tree by reference and returns it."""
        if element > level:
            raise Exception('element out of bounds')
        self._nodes[gauss_first_formula(level) + element] = value

    def __repr__(self):
        output = ""
        for i in range(0, self.height + 1):
            level = self.get_level(i)
            output += "\n" + ', '.join(str(val) for val in reversed(level))
        return output
