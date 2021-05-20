from sample import Sample
from data import Data

class Cluster:
    def __init__(self,samples,c_id):
        self.c_id = c_id
        self.samples = samples

    def dominate_label(self):
        labels_dict={}
        label_lst = []
        for sample in self.samples:
            label_lst.append(sample.get_label())
        for key in label_lst:
            labels_dict.setdefault(key,0)
        for sample in self.samples:
            labels_dict[sample.get_label()]+=1
        max_label=0
        dominate_str=""
        first = True
        for value in labels_dict.values():
            if value>max_label:
                max_label=value
        for key,value in labels_dict.items():
            if value == max_label:
                 if first:
                    first=False
                    dominate_str=key
                 elif key<dominate_str:
                     dominate_str=key
        return dominate_str


    def get_c_id(self):
        return self.c_id

    def get_samples(self):
        return self.samples

    def merge(self, other):
        self.c_id = min(self.c_id, other.get_c_id())
        self.samples += other.get_samples()
        self.samples.sort(key=lambda x: x.s_id)
        del other

    def print_details(self, silhouette):
        s_id_lst = []
        for sample in self.samples:
            s_id_lst.append(sample.get_s_id())
        print(f"Cluster {self.c_id}: {s_id_lst}, "
              f"dominant label = {self.dominate_label()}, silhouette = {round(silhouette, 3)}")
