from cluster import Cluster


class AgglomerativeClustering:

    """
        Constructor for class- divides all samples to cluster so that each cluster contains one sample
        :param1 link: single link or complete link
        :param2 samples: list of all samples
        :returns: None
        """
    def __init__(self, link, samples):
        self.link = link
        self.cluster_lst = []
        self.samples = samples
        for sample in samples:
            new_cluster = Cluster([sample], sample.get_s_id())
            self.cluster_lst.append(new_cluster)

    """
        Calculates sample's in value
        :param1 sample: certain point in cluster- xi
        :param2 cluster: cluster which sample belongs to
        :param3 cluster: the received cluster's size
        :returns: sample's in value
    """
    def in_xi(self, sample, cluster, cluster_size):
        sum_distance = 0
        for cur_sample in cluster.get_samples():
            if sample.get_s_id() != cur_sample.get_s_id():
                sum_distance += cur_sample.compute_euclidean_distance(sample)
        return sum_distance / (cluster_size - 1)

    """
        Calculates sample's out value
        :param1 sample: certain point in cluster- xi
        :param2 cluster: cluster which sample belongs to
        :returns: sample's out value
    """
    def out_xi(self, sample, cluster):
        min_distance = 0
        first = True
        for cur_cluster in self.cluster_lst:
            sum_distance = 0
            if cur_cluster.get_c_id() != cluster.get_c_id():
                for temp_sample in cur_cluster.get_samples():
                    sum_distance += temp_sample.compute_euclidean_distance(sample)
                cluster_size = len(cur_cluster.get_samples())
                temp_distance = sum_distance / cluster_size
                if first:
                    min_distance = temp_distance
                    first = False
                min_distance = min(temp_distance, min_distance)
        return min_distance

    """
        Calculates certain sample's silhouette
        :param1 cluster: cluster which sample belongs to
        :param2 sample: certain point in cluster- xi
        :returns: sample's silhouette
    """
    def calculate_silhouette(self, cluster, sample):
        cluster_size = len(cluster.get_samples())
        if cluster_size <= 1:
            return 0
        in_xi = self.in_xi(sample, cluster, cluster_size)
        out_xi = self.out_xi(sample, cluster)
        return (out_xi-in_xi) / max(in_xi, out_xi)

    """
        Creates dictionary with all samples' s_id as keys and silhouette as values
        :param: None
        :returns: described dictionary
    """
    def compute_silhouette(self):
        silhouette_dic = {}
        for cur_cluster in self.cluster_lst:
            for cur_sample in cur_cluster.get_samples():
                silhouette_dic[cur_sample.get_s_id()] = self.calculate_silhouette(cur_cluster, cur_sample)
        return silhouette_dic

    """
        Calculates certain cluster's silhouette
        :param cluster: cluster which we need to calculate its' silhouette
        :returns: cluster's silhouette
    """
    def calculate_cluster_silhouette(self, cluster):
        cluster_size = len(cluster.get_samples())
        return self.sum_silhouette(cluster) / cluster_size

    """
        Sums all samples' silhouette in certain cluster
        :param cluster: cluster which we need to sum its' samples' silhouette
        :returns: described sum
    """
    def sum_silhouette(self, cluster):
        silhouette_dic = self.compute_silhouette()
        sum_silhouette = 0
        for sample in cluster.get_samples():
            sum_silhouette += silhouette_dic[sample.get_s_id()]
        return sum_silhouette

    """
        Calculates all samples' silhouette 
        :param: None
        :returns: all samples' silhouette
    """
    def calculate_sample_silhouette(self):
        sum_samples = 0
        for cluster in self.cluster_lst:
            sum_samples += self.sum_silhouette(cluster)
        sample_size = len(self.samples)
        return sum_samples/sample_size

    """
        Created a dictionary with clusters' c_id as keys and silhouette as values, and all data silhouette
        :param: None
        :returns: described dictionary 
    """
    def compute_summery_silhouette(self):
        silhouette_cluster_dic = {}
        for cluster in self.cluster_lst:
            silhouette_cluster_dic.setdefault(cluster.get_c_id(), self.calculate_cluster_silhouette(cluster))
        silhouette_cluster_dic[0] = self.calculate_sample_silhouette()
        return silhouette_cluster_dic

    """
        Created a dictionary that contains samples as keys, and for each sample saves its' distance from all other 
        samples
        :param: None
        :returns: described dictionary 
    """
    def create_dict_sample_distance(self):
        sample_dict = {}
        for key in self.samples:
            s_id_lst = []
            for sample in self.samples:
                s_id_lst.append([sample.get_s_id(), sample.compute_euclidean_distance(key)])
            sample_dict.setdefault(key.get_s_id(), s_id_lst)
        return sample_dict

    """
        Computes total true positive pairs according to definition
        :param: None
        :returns: true positive number 
    """
    def compute_true_positive(self):
        true_positive_counter = 0
        sample_lst = []
        for cluster in self.cluster_lst:
            for sample1 in cluster.get_samples():
                for sample2 in cluster.get_samples():
                    if sample1.get_s_id() != sample2.get_s_id() and sample2 not in sample_lst:
                        if sample1.get_label() == sample2.get_label():
                            true_positive_counter += 1
                sample_lst.append(sample1)
        return true_positive_counter

    """
       Computes total true negative pairs according to definition
       :param: None
       :returns: true negative number 
   """
    def compute_true_negative(self):
        true_negative_counter = 0
        cluster_lst = []
        for cluster in self.cluster_lst:
            for other_cluster in self.cluster_lst:
                if cluster.get_c_id() != other_cluster.get_c_id() and other_cluster not in cluster_lst:
                    for sample1 in cluster.get_samples():
                        for sample2 in other_cluster.get_samples():
                            if sample1.get_label() != sample2.get_label():
                                true_negative_counter += 1
            cluster_lst.append(cluster)
        return true_negative_counter

    """
       Computes rand index value, according to definition
       :param: None
       :returns: rand index value
   """
    def compute_rand_index(self):
        sample_size = len(self.samples)
        true_positive = self.compute_true_positive()
        true_negative = self.compute_true_negative()
        return (true_negative + true_positive) / (sample_size * (sample_size - 1) / 2)

    """
       Manages clustering process
       :param max clusters: the max allowed clusters after clustering 
       :returns: None
   """
    def run(self, max_clusters):
        min_distance = 0

        # Creates a dictionary with all the distances' between all samples
        sample_distance_dict = self.create_dict_sample_distance()
        while len(self.cluster_lst) > max_clusters:
            first = True

            # Each iteration looks for two clusters with minimal distance and merges them
            for cluster in self.cluster_lst:
                for other in self.cluster_lst:
                    if other.get_c_id() != cluster.get_c_id():
                        temp_distance = self.link.compute(cluster, other, sample_distance_dict)
                        if first:
                            first = False
                            min_distance = temp_distance
                            cluster1 = cluster
                            cluster2 = other
                        if temp_distance < min_distance:
                            min_distance = temp_distance
                            cluster1 = cluster
                            cluster2 = other
            cluster1.merge(cluster2)
            self.cluster_lst.remove(cluster2)
        silhouette_dic = self.compute_summery_silhouette()
        self.cluster_lst.sort(key=lambda x: x.c_id)

        # Prints all wanted details
        for cluster in self.cluster_lst:
            silhouette = silhouette_dic[cluster.get_c_id()]
            cluster.print_details(silhouette)
        print(f"Whole data: silhouette = {round(silhouette_dic[0], 3)}, RI = {round(self.compute_rand_index(),3)}")
