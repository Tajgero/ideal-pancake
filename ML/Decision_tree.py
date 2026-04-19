import numpy as np

class BinaryDecisionTree():
    def __init__(self, verbose=False):
        """Initialization of decision_tree object"""
        self.tree = []
        self.verbose = verbose


    def __str__(self):
        return "=" * 10


    def entropy(self, y):
        """Calculates crossentropy for given node data"""
        
        entropy = 0.0
        if len(y) > 0:
            
            # p = len(y[y==1]) / len(y) # Probability calculation
            p = np.mean(y)
            if 0< p < 1:
                entropy = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
                
        return entropy
        
        
    def split_dataset(self, X, node_indices, index_feature):
        """
        Given a dataset, node indices and a index feature, 
        return two lists for the two split nodes, 
        the left node has the animals that have that feature = 1 
        and the right node those that have the feature = 0 
        
        Args:
            X (np.array[shape(n,3)]): Data
            node_indices (list[int,])
            
            ex.
            index feature = 0 => ear shape
            index feature = 1 => face shape
            index feature = 2 => whiskers
        
        Returns:
            left_indices (list): Left node with data indices
            right_indices (list): Right node with data indices
        """
        left_indices, right_indices = [], []
        
        for index in node_indices:
            if X[index][index_feature] == 1:
                left_indices.append(index)
            else:
                right_indices.append(index)
                
        return left_indices, right_indices
    

    def information_gain(self, X, y, node_indices, feature):
        """
        This function takes the splitted dataset, the indices we chose to 
        split and returns the weighted entropy.
        
        Args:
            X (np.array[shape(n,m)]): Data
            y (np.array[shape(n,)]): Ground truth data
            left_indices (list): Left node with data indices
            right_indices (list): Right node with data indices
            
        Returns:
            information_gain (float): Information gain on node
        """
        left_indices, right_indices = self.split_dataset(X, node_indices, feature)
        
        X_node, y_node = X[node_indices], y[node_indices]
        X_left, y_left = X[left_indices], y[left_indices]
        X_right, y_right = X[right_indices], y[right_indices]
        
        w_left = len(X_left) / len(X_node)
        w_right = len(X_right) / len(X_node)
        
        weighted_entropy = w_left * self.entropy(y_left) + w_right * self.entropy(y_right)
        information_gain = self.entropy(y_node) - weighted_entropy
        
        return information_gain    
    
    
    def get_best_split(self, X, y, node_indices):
        """
        Finds best split from data
        
        Args:
            X (np.array[shape(n,m)]): Data
            y (np.array[shape(n,)]): Ground truth data
            node_indices (list): List of node indices
            
        Returns:
            best_feature
        """
        num_features = X.shape[1]
        best_feature = None
        max_info_gain = 0
        
        for feature in range(num_features):
            info_gain = self.information_gain(X, y, node_indices, feature)
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                best_feature = feature
            
        return best_feature
    
    
    def fit(self, X_train, y_train, max_depth=10):
        self.X = X_train
        self.y = y_train
        self.max_depth = max_depth
        self.node_indices = [i for i in range(X_train.shape[0])]
        
        self.build_tree_recursive(self.X, self.y, "Root", self.node_indices)
        
    
    def build_tree_recursive(self, X, y, branch_name, node_indices, current_depth=0):
        """
        The process is recursive, which means we must perform these 
        calculations for each node until we meet a stopping criteria:

        If the tree depth after splitting exceeds a threshold
        If the resulting node has only 1 class # TODO
        If the information gain of splitting is below a threshold # TODO
        """
        if current_depth == self.max_depth:
            if self.verbose:
                formatting = " " * current_depth + "-" * current_depth
                print(f"{formatting} {branch_name} leaf node with indices {node_indices}")
            return
        
        best_feature = self.get_best_split(X, y, node_indices)
        if best_feature is None:
            return
        
        if self.verbose:
            formatting = "-" * current_depth
            print(f"{formatting} Depth {current_depth}, {branch_name}: Split on feature: {best_feature}")

        left_indices, right_indices = self.split_dataset(X, node_indices, best_feature)
        self.tree.append((left_indices, right_indices, best_feature))

        self.build_tree_recursive(X, y, "Left", left_indices, current_depth + 1)
        self.build_tree_recursive(X, y, "Right", right_indices, current_depth + 1)
        

if __name__ == '__main__':
    
    # ear_shape, face_shape, whiskers - one hot encoding
    X_train = np.array([
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ])
    y_train = np.array([1, 1, 0, 0, 1, 1, 0, 1, 0, 0])
    
    # Making tree
    model = BinaryDecisionTree(verbose=True)
    model.fit(X_train, y_train, max_depth=2)
    print(model)
