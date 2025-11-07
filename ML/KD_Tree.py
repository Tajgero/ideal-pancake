class KDNode:
    """
    Node data structure for KD-Tree implementation
    
    Args:
        point (tuple): k-dimensional point.
        k (int): Axis of comparison.
        left (KDNode, optional): Left subtree. The default is None.
        right (KDNode, optional): Right subtree. The default is None.
    """
    def __init__(self, point, k, left=None, right=None):
        self.point = point
        self.k = k
        self.left = left
        self.right = right
    
    
class KDTree:
    """
    Simple KD-Tree based on KDNodes
    
    Args:
        data (iterable (tuple)): Data to be used ex. [(1,3), (2,5)] 
        
    Methods:
        build(): Builds KD-Tree based upon data dimensions used
            Returns: KDNode
            
        distance_euclidean(): Calculates euclidean distance between 2 points   
            Returns: int
            
        nearest_neighbor(): Find nearest neighbor point
            Returns: tuple
    """
    def __init__(self, data):
        self.data = data
        
        
    def build(self, points=None, depth=0):
        if not self.data:
            raise Exception("No data points")
            
        if points is None:
            points = self.data
        elif not points:
            return None
        
        k = len(points[0]) # Number of dimensions
        axis = depth % k
        
        # Sort points by axis and find median value
        sorted_points = sorted(points, key=lambda p: p[axis])
        median_idx = len(sorted_points) // 2
        median_pt = sorted_points[median_idx]
        
        # Build tree where median_pt is not part of next nodes
        node = KDNode(median_pt, axis)
        node.left = self.build(sorted_points[:median_idx], depth + 1)
        node.right = self.build(sorted_points[median_idx + 1:], depth + 1)
        
        return node


    def distance_euclidean(self, pt1, pt2):
        return sum((x - y) ** 2 for x, y in zip(pt1, pt2)) ** 0.5
    
    
    def nearest_neighbor(self, root, target, depth=0, best=None):
        if root is None: # Base case
            return best
        
        k = len(target) # Number of dimensions
        axis = depth % k
        
        next_best = None
        next_branch = None
        
        # Check if distance node < best
        root_dist = self.distance_euclidean(root.point, target)
        if best is None or root_dist < self.distance_euclidean(best.point, target):
            next_best = root
        else:
            next_best = best
            
        # Traverse through KDTree by axis
        if target[axis] < root.point[axis]:
            next_branch = root.left
            other_branch = root.right
        else:
            next_branch = root.right
            other_branch = root.left
            
        # Recursively find best on branch
        best = self.nearest_neighbor(next_branch, target, depth + 1, next_best)
        
        # Recursively find best on other branch if closer
        best_dist = self.distance_euclidean(best.point, target)
        root_dist = abs(root.point[axis] - target[axis])
        if root_dist < best_dist:
            best = self.nearest_neighbor(other_branch, target, depth + 1, best)
            
        return best

if __name__ == '__main__':
    points = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7)]
    kd = KDTree(points)
    root = kd.build()

    target = (8, 8)
    nearest = kd.nearest_neighbor(root, target)
    print("Nearest neighbor:", nearest.point)
    
    # MatPlotLib
    import matplotlib.pyplot as plt
    
    if len(root.point) == 2: # If 2D representation in possible
        # Distance
        X = (target[0], nearest.point[0]) 
        Y = (target[1], nearest.point[1])
        distance = kd.distance_euclidean(target, nearest.point)
        plt.plot(X, Y, c="purple")
        plt.text((X[0] + X[1]) // 2, (Y[0] + Y[1]) // 2, f"Dist {distance:.2f}",
                 fontsize=8,
                 color="purple"
        )
    
        # Points
        X = [p[0] for p in points]
        Y = [p[1] for p in points]
    
        plt.scatter(X, Y, color="blue")
        for x, y in zip(X, Y):
            plt.text(x + 0.2, y, f"{x, y}", fontsize=8)
    
        # Target point
        plt.scatter(target[0], target[1], color="orange")
        plt.text(target[0] + 0.2, target[1], f"{target[0], target[1]}", fontsize=8)    
        
        plt.show()
