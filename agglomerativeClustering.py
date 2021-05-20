from cluster import Cluster
from sample import Sample
from data import Data

class AgglomerativeClustering:
    def __init__(self, link, samples):
        self.link = link
        self.cluster_lst = []
        self.samples = samples
        for sample in samples:
            new_cluster = Cluster([sample], sample.get_s_id())
            self.cluster_lst.append(new_cluster)

    def in_xi(self, sample, cluster, cluster_size):
        sum = 0
        for cur_sample in cluster.get_samples():
            if sample.get_s_id() != cur_sample.get_s_id():
                sum += cur_sample.compute_euclidean_distance(sample)
        return sum/(cluster_size-1)

    def out_xi(self, sample, cluster):
        min_distance = 0
        first = True
        for cur_cluster in self.cluster_lst:
            sum = 0
            if cur_cluster.get_c_id() != cluster.get_c_id():
                for temp_sample in cur_cluster.get_samples():
                    sum += temp_sample.compute_euclidean_distance(sample)
                cluster_size = len(cur_cluster.get_samples())
                temp_distance = sum/cluster_size
                if first:
                    min_distance = temp_distance
                    first = False
                min_distance = min(temp_distance, min_distance)
        return min_distance

    def calculate_silhoeutte(self, cluster, sample):
        cluster_size = len(cluster.get_samples())
        if cluster_size <= 1:
            return 0
        in_xi = self.in_xi(sample, cluster, cluster_size)
        out_xi = self.out_xi(sample, cluster)
        return (out_xi-in_xi) / max(in_xi, out_xi)

    def compute_silhoeutte(self):
        silhoeutte_dic = {}
        #for sample in self.samples:
            #silhoeutte_dic.setdefault(sample.get_s_id(), 0)
        for cur_cluster in self.cluster_lst:
            for cur_sample in cur_cluster.get_samples():
                silhoeutte_dic[cur_sample.get_s_id()] = self.calculate_silhoeutte(cur_cluster, cur_sample)
        return silhoeutte_dic

    def calculate_cluster_silhoeutte(self,cluster):
        cluster_size = len(cluster.get_samples())
        return self.sum_silhoeutte(cluster)/cluster_size

    def sum_silhoeutte(self, cluster):
        silhoeutte_dic = self.compute_silhoeutte()
        sum = 0
        for sample in cluster.get_samples():
            sum += silhoeutte_dic[sample.get_s_id()]
        return sum

    def calculate_sample_silhoeutte(self):
        sum = 0
        for cluster in self.cluster_lst:
            sum += self.sum_silhoeutte(cluster)
        sample_size = len(self.samples)
        return sum/sample_size

    def compute_summery_silhoeutte(self):
        silhoeutte_cluster_dic = {}
        for cluster in self.cluster_lst:
            silhoeutte_cluster_dic.setdefault(cluster.get_c_id(), self.calculate_cluster_silhoeutte(cluster))
        silhoeutte_cluster_dic[0] = self.calculate_sample_silhoeutte()
        return silhoeutte_cluster_dic

    def create_dict_sample_distance(self):
        sample_dict = {}
        for key in self.samples:
            s_id_lst = []
            for sample in self.samples:
                s_id_lst.append([sample.get_s_id(), sample.compute_euclidean_distance(key)])
            sample_dict.setdefault(key.get_s_id(), s_id_lst)
        return sample_dict

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

    def compute_rand_index(self):
        sample_size = len(self.samples)
        true_positive = self.compute_true_positive()
        true_negative = self.compute_true_negative()
        return (true_negative + true_positive) / (sample_size * (sample_size - 1) / 2)

    def run(self, max_clusters):
        sample_distance_dict = self.create_dict_sample_distance()
        while len(self.cluster_lst) > max_clusters:
            first = True
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
        silhouette_dic = self.compute_summery_silhoeutte()
        self.cluster_lst.sort(key=lambda x: x.c_id)

        for cluster in self.cluster_lst:
            silhouette = silhouette_dic[cluster.get_c_id()]
            cluster.print_details(silhouette)
        print(f"Whole data: silhouette = {round(silhouette_dic[0], 3)}, RI = {round(self.compute_rand_index(),3)}")


