from cluster import Cluster


class AgglomerativeClustering:

    def __init__(self, link, samples, distance_dict):
        """
            Constructor for class- divides all samples to cluster so that each cluster contains one sample
            :param1 link: single link or complete link
            :param2 samples: list of all samples
            :returns: None
        """
        self.link = link
        self.distance_dict = distance_dict
        self.cluster_lst = []
        self.samples = samples
        for sample in samples:
            new_cluster = Cluster([sample], sample.get_s_id())
            self.cluster_lst.append(new_cluster)

    def in_xi(self, sample, cluster, cluster_size):
        """
            Calculates sample's in value
            :param1 sample: certain point in cluster- xi
            :param2 cluster: cluster which sample belongs to
            :param3 cluster_size: the received cluster's size
            :returns: sample's in value
        """
        sum_distance = 0
        for cur_sample in cluster.get_samples():
            if sample.get_s_id() != cur_sample.get_s_id():
                if cur_sample.get_s_id() < sample.get_s_id():
                    sum_distance += self.distance_dict[(cur_sample.get_s_id(), sample.get_s_id())]
                elif cur_sample.get_s_id() > sample.get_s_id():
                    sum_distance += self.distance_dict[(sample.get_s_id(), cur_sample.get_s_id())]
        return sum_distance / (cluster_size - 1)

    def out_xi(self, sample, cluster):
        """
             Calculates sample's out value
             :param1 sample: certain point in cluster- xi
             :param2 cluster: cluster which sample belongs to
             :returns: sample's out value
         """
        min_distance = 0
        first = True
        for cur_cluster in self.cluster_lst:
            sum_distance = 0
            if cur_cluster.get_c_id() != cluster.get_c_id():
                for cur_sample in cur_cluster.get_samples():
                    if cur_sample.get_s_id() < sample.get_s_id():
                        sum_distance += self.distance_dict[(cur_sample.get_s_id(), sample.get_s_id())]
                    elif cur_sample.get_s_id() > sample.get_s_id():
                        sum_distance += self.distance_dict[(sample.get_s_id(), cur_sample.get_s_id())]
                cluster_size = len(cur_cluster.get_samples())
                temp_distance = sum_distance / cluster_size
                if first:
                    min_distance = temp_distance
                    first = False
                min_distance = min(temp_distance, min_distance)
        return min_distance

    def calculate_silhouette(self, cluster, sample):
        """
            Calculates certain sample's silhouette
            :param1 cluster: cluster which sample belongs to
            :param2 sample: certain point in cluster- xi
            :returns: sample's silhouette
        """
        cluster_size = len(cluster.get_samples())
        if cluster_size <= 1:
            return 0
        in_xi = self.in_xi(sample, cluster, cluster_size)
        out_xi = self.out_xi(sample, cluster)
        return (out_xi-in_xi) / max(in_xi, out_xi)

    def compute_silhouette(self):
        """
            Creates dictionary with all samples' s_id as keys and silhouette as values
            :param: None
            :returns: described dictionary
        """
        silhouette_dic = {}
        for cur_cluster in self.cluster_lst:
            for cur_sample in cur_cluster.get_samples():
                silhouette_dic[cur_sample.get_s_id()] = self.calculate_silhouette(cur_cluster, cur_sample)
        return silhouette_dic

    def calculate_cluster_silhouette(self, cluster):
        """
            Calculates certain cluster's silhouette
            :param cluster: cluster which we need to calculate its' silhouette
            :returns: cluster's silhouette
        """
        cluster_size = len(cluster.get_samples())
        return self.sum_silhouette(cluster) / cluster_size

    def sum_silhouette(self, cluster):
        """
            Sums all samples' silhouette in certain cluster
            :param cluster: cluster which we need to sum its' samples' silhouette
            :returns: described sum
        """
        silhouette_dic = self.compute_silhouette()
        sum_silhouette = 0
        for sample in cluster.get_samples():
            sum_silhouette += silhouette_dic[sample.get_s_id()]
        return sum_silhouette

    def calculate_sample_silhouette(self):
        """
           Calculates all samples' silhouette
           :param: None
           :returns: all samples' silhouette
       """
        sum_samples = 0
        for cluster in self.cluster_lst:
            sum_samples += self.sum_silhouette(cluster)
        sample_size = len(self.samples)
        return sum_samples/sample_size

    def compute_summery_silhouette(self):
        """
            Created a dictionary with clusters' c_id as keys and silhouette as values, and all data silhouette
            :param: None
            :returns: described dictionary
        """
        silhouette_cluster_dic = {}
        for cluster in self.cluster_lst:
            silhouette_cluster_dic.setdefault(cluster.get_c_id(), self.calculate_cluster_silhouette(cluster))
        silhouette_cluster_dic[0] = self.calculate_sample_silhouette()
        return silhouette_cluster_dic

    def find_cluster_sample(self, sample):
        """
           Computes rand index value, according to definition
           :param: sample: single sample
           :returns: cluster that the sample belongs to
       """
        for cluster in self.cluster_lst:
            if sample in cluster.get_samples():
                return cluster.get_c_id()

    def compute_rand_index(self):
        """
           Computes rand index value, according to definition
           :param: None
           :returns: rand index value
       """
        true_positive = 0
        true_negative = 0
        for i, sample1 in enumerate(self.samples):
            for j, sample2 in enumerate(self.samples):
                if i < j:
                    sample1_cluster = self.find_cluster_sample(sample1)
                    sample2_cluster = self.find_cluster_sample(sample2)
                    if sample1.get_label() != sample2.get_label() and \
                            sample1_cluster != sample2_cluster:
                        true_negative += 1
                    if sample1.get_label() == sample2.get_label() and \
                            sample1_cluster == sample2_cluster:
                        true_positive += 1
        sample_size = len(self.samples)
        return (true_negative + true_positive) / (sample_size * (sample_size - 1) / 2)

    def run(self, max_clusters):
        """
           Manages clustering process
           :param max_clusters: the max allowed clusters after clustering
           :returns: None
       """
        min_distance = 0

        while len(self.cluster_lst) > max_clusters:
            first = True

            # Each iteration looks for two clusters with minimal distance and merges them
            for i, cluster in enumerate(self.cluster_lst):
                for j, other in enumerate(self.cluster_lst):
                    if i < j:
                        temp_distance = self.link.compute(cluster, other, self.distance_dict)
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
