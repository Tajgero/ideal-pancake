import numpy as np
from matplotlib import pyplot as plt

class KMeans:
    def __init__(self, treshold=1, seed=None):
        self.rng = np.random.default_rng(seed)
        self.treshold = treshold
        self.clusters = None
    
    def fit(self, X_train, n_clusters=3):
        self.data = X_train
        self.centroids, self.clusters = self.__build(n_clusters)
        
    def __build(self, n_clusters):
        k = self.data.shape[1] # Dimensions
        dist = np.linalg.norm # Shorter form
        check_centroids = True

        # 1. Generate random centroids
        min_data = self.data.min(axis=0)
        max_data = self.data.max(axis=0)
        centroids = self.rng.integers(min_data, max_data, 
                                      size=(n_clusters,k), endpoint=True)
        
        while check_centroids: # TODO: All distances are not optimal solution
            # 2. Assign points to centroids
            # Row - centroid idx, column - point idx
            distances = np.array(
                [dist(self.data - cent, axis=1) for cent in centroids]
            )
            assigned = distances.argmin(axis=0)
            clusters_mask = np.unique(assigned)
            
            # 3. Move centroids - calculate mean == new centroids
            # Additionaly it automatically deletes not used centroids and clusters
            mean = np.array(
                [self.data[assigned == label].mean(axis=0) for label in clusters_mask]
            )
            # 4. End when centroids move less than treshold
            diff = abs(centroids[clusters_mask] - mean)
            centroids = mean.copy() # For next iteration
            
            if diff[diff > self.treshold].size == 0:
                clusters_mask = np.arange(clusters_mask.size) # New numerings
                check_centroids = False
        
        return centroids, assigned


if __name__ == '__main__':
    data = np.array([
        [3,6],
        [1,8],
        [9,2],
        [2,8],
        [15,35],
        [17,31],
        [87,93],
        [75,18]
    ])
    
    model = KMeans()
    model.fit(data)
    
    x, y = data[:,0], data[:,1]
    
    labels = model.clusters
    colors = np.array(['red', 'green', 'blue'])
    
    plt.scatter(x, y, color=colors[labels], marker='o')
    plt.scatter(model.centroids[:,0], model.centroids[:,1], 
                color='purple', marker='x')
    plt.show()
