class Cluster:
    def __init__(self, samples, c_id):
        """
            Constructor for class. initialize all values
            :param1 samples: a list of samples
            :param2 c_id: cluster's id
            :returns: None
        """
        self.c_id = c_id
        self.samples = samples

    def dominate_label(self):
        """
            finds the dominate label in the cluster
            :param: None
            :returns: dominate label
        """

        labels_dict = {}
        label_lst = []
        for sample in self.samples:
            label_lst.append(sample.get_label())
        for key in label_lst:
            labels_dict.setdefault(key, 0)
        for sample in self.samples:
            labels_dict[sample.get_label()] += 1
        max_label = 0
        dominate_str = ""
        first = True
        for value in labels_dict.values():
            if value > max_label:
                max_label = value
        for key, value in labels_dict.items():
            if value == max_label:
                if first:
                    first = False
                    dominate_str = key
                elif key < dominate_str:
                    dominate_str = key
        return dominate_str

    def get_c_id(self):
        """
            returns c_id of the cluster
            :param: None
            :returns: c_id of a certain cluster
        """
        return self.c_id

    def get_samples(self):
        """
             returns samples of a cluster
             :param: None
             :returns: samples of a certain cluster
         """
        return self.samples

    def merge(self, other):
        """
             merges two clusters to a single cluster
             :param: other: cluster we want to merge
             :returns: None
         """
        self.c_id = min(self.c_id, other.get_c_id())
        self.samples += other.get_samples()
        self.samples.sort(key=lambda x: x.s_id)
        del other

    def print_details(self, silhouette):
        """
             prints details about a certain cluster
             :param: silhouette: silhouette value of the cluster
             :returns: None
         """
        s_id_lst = []
        for sample in self.samples:
            s_id_lst.append(sample.get_s_id())
        print(f"Cluster {self.c_id}: {s_id_lst}, "
              f"dominant label = {self.dominate_label()}, silhouette = {round(silhouette, 3)}")
