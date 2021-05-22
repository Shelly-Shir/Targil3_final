import pandas
from sample import Sample


class Data:

    """
       Initialize Data object
       :param path: contains a path to csv
       :returns: None
    """
    def __init__(self, path):
        df = pandas.read_csv(path)
        self.data = df.to_dict(orient="list")

    """
       Creates a list of samples objects 
       :param: None
       :returns: list of samples
    """
    def create_samples(self):
        samples_lst = []
        for i, sample in enumerate(self.data["samples"]):
            genes_lst = []
            s_id = sample
            label = self.data["type"][i]
            for key in list(self.data.keys())[2:]:
                genes_lst.append(self.data[key][i])
            samples_lst.append(Sample(s_id, genes_lst, label))
        return samples_lst
