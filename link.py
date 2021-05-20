from sample import Sample
from cluster import Cluster

class Link:

    def compute(self, cluster, other):
        raise NotImplemented("subclass must implement abstract method")

class SingleLink(Link):
    def compute(self, cluster, other, sample_distance_dict):
        first = True
        min_distance = 0
        for cluster_sample in cluster.get_samples():
            for other_sample in other.get_samples():
                for inner_lst in sample_distance_dict[cluster_sample.get_s_id()]:
                    if inner_lst[0] == other_sample.get_s_id():
                        result = inner_lst
                temp_distance = result[1]
                if first:
                    first = False
                    min_distance = temp_distance
                min_distance = min(temp_distance, min_distance)
        return min_distance

class CompleteLink(Link):
    def compute(self, cluster, other, sample_distance_dict):
        max_distance = 0
        for cluster_sample in cluster.get_samples():
            for other_sample in other.get_samples():
                for inner_lst in sample_distance_dict[cluster_sample.get_s_id()]:
                    if inner_lst[0] == other_sample.get_s_id():
                        result = inner_lst
                temp_distance = result[1]
                max_distance = max(temp_distance, max_distance)
        return max_distance
