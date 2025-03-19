from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
# from collections import deque
from bs4 import Tag, Doctype, NavigableString
import numpy as np

base_path = 'clones_2/clones/tier1'

def construct_tree(document):
    return BeautifulSoup(document, "html.parser")


def calculate_tag(tag):
    if isinstance(tag, Doctype):
        return 0

    if isinstance(tag, NavigableString):
        return sum( [ord(c) for  c in tag.strip()] )

    result = tag.name

    if hasattr(tag, 'get_text'):
        result +=  tag.get_text()
    if hasattr(tag, 'attrs'):
        for attr, value in tag.attrs.items():
            result += attr + str(value)

    return sum([ ord(c) for c in result])

def euclidean_distance(a, b):
    return abs(a - b)


def assign_clusters(points, centroids):
    '''
    :param points: Lista de puncte
    :param centroids: Lista cu pozitia centroizilor
    :return:
        O lista care o sa contina indecsi corespunzatori pentru centroidul ales

        Adica daca
        Am o lista de 100 de puncte si 3 centroids
        Atunci o sa am o lista de 100 de valori cu valori intre 0 si 2
        0 fiind centroidul 1, 1 fiind centroidul 2, si 2 fiind centroidul 3

        label[0] => 1
        pentru elementul de pe pozitia 0, inseamna punctul din lista de points de pe pozitia 0,
        are centroidul 1 din lista de centroids

    '''

    # pentru fiecare punct
    labels = []

    for point in points:
        centroid_distances = [euclidean_distance(point['tree_score'], centroid) for centroid in centroids]
        min_index = np.argmin(centroid_distances)
        labels.append(min_index)

    return labels

def recalculate_centroids(X, labels, k):
    new_centroids = np.zeros(k)

    for i in range(k):
        # Find all points that belong to cluster i
        points_in_cluster = []
        # Calculate the mean of those points and update the centroid
        # [0, 0, 0, 0, 1, 2, 2]
        # [x1, x2, x3, x4, x5, x6, x7]

        for index in labels:
            if index == i:
                points_in_cluster.append(X[i]['tree_score'])

        if len(points_in_cluster):
            new_centroids[i] = sum(points_in_cluster) / len(points_in_cluster)

    return new_centroids

def k_means_clustering(X, k, max_iterations=100):
    centroids = np.random.rand(k)

    for iteration in range(max_iterations):

        labels = assign_clusters(X, centroids)


        new_centroids = recalculate_centroids(X, labels, k)


        if np.allclose(centroids, new_centroids, atol=1e-6):
            break

        centroids = new_centroids

    return centroids, labels

def calculate_tree(tag, depth=1):
    total_sum = 0

    if isinstance(tag, Tag):
        for child in list(tag.children):
            total_sum += calculate_tree(child, depth + 1)

    total_sum += calculate_tag(tag)

    return total_sum

def extract_files(dir):
    return [file for file in listdir(dir) if isfile(join(dir, file))]

def read_file(directory, filename):
    file_path = join(directory, filename)
    f = open(file_path, 'r', encoding='utf-8')
    return f.read()


def scale_to_01(values):
    tree_scores = [item['tree_score'] for item in values]
    min_val = min(tree_scores)
    max_val = max(tree_scores)


    for tree in values:
        x = tree['tree_score']
        tree['tree_score'] = (x - min_val) / (max_val - min_val)


def main():
    list_of_trees = [ { 'tree' : construct_tree(read_file(base_path, filename)), 'filename' : filename } for filename in extract_files(base_path)  ]

    list_of_trees = [ {'tree_score' : calculate_tree(tree['tree']), 'filename' : tree['filename']} for tree in list_of_trees]

    scale_to_01(list_of_trees)


    centroids, labels = k_means_clustering(list_of_trees, 3, 100)




    answer = [[] for _ in range(len(centroids))]


    for i in range(len(labels)):
        answer[labels[i]].append(list_of_trees[i]['filename'])

    print(answer)

if __name__ == '__main__':
    main()



