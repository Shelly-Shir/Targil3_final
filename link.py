class Link:

    def compute(self, cluster, other):
        """
        Calculates the distance between two clusters in single/complete link method
        :param1 cluster: cluster
        :param2 other:cluster to merge
        :return: distance between two clusters in single/compete link method
        """
        raise NotImplemented("subclass must implement abstract method")


class SingleLink(Link):
    def compute(self, cluster, other, distance_dict):
        """
        Calculates the distance between two clusters in single link method
        :param1 cluster: cluster
        :param2 other:cluster to merge
        :param2 distance_dict: dictionary containing the euclidean distance between two samples in the database
        :return: distance between two clusters in single link method
        """
        first = True
        min_distance = 0
        for cluster_sample in cluster.get_samples():
            for cur_sample in other.get_samples():
                if cluster_sample.get_s_id() != cur_sample.get_s_id():
                    if cur_sample.get_s_id() < cluster_sample.get_s_id():
                        current_distance = distance_dict[(cur_sample.get_s_id(), cluster_sample.get_s_id())]
                    elif cur_sample.get_s_id() > cluster_sample.get_s_id():
                        current_distance = distance_dict[(cluster_sample.get_s_id(), cur_sample.get_s_id())]
                    if first:
                        first = False
                        min_distance = current_distance
                    min_distance = min(current_distance, min_distance)
        return min_distance


class CompleteLink(Link):
    def compute(self, cluster, other, distance_dict):
        """
        Calculates the distance between two clusters in complete link method
        :param1 cluster: cluster
        :param2 other:cluster to merge
        :param2 distance_dict: dictionary containing the euclidean distance between two samples in the database
        :return: distance between two clusters in complete link method
        """
        max_distance = 0
        for cluster_sample in cluster.get_samples():
            for other_sample in other.get_samples():
                if cluster_sample.get_s_id() != other_sample.get_s_id():
                    if other_sample.get_s_id() < cluster_sample.get_s_id():
                        current_distance = distance_dict[(other_sample.get_s_id(), cluster_sample.get_s_id())]
                    elif other_sample.get_s_id() > cluster_sample.get_s_id():
                        current_distance = distance_dict[(cluster_sample.get_s_id(), other_sample.get_s_id())]
                    max_distance = max(current_distance, max_distance)
        return max_distance
