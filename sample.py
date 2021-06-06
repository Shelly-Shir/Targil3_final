class Sample:

    def __init__(self, s_id, genes, label):
        """
            Constructor for class. initialize all values
            :param1 s_id: sample's id
            :param2 genes: list of genes
            :param3 label: sample's label
            :returns: sample's in value
        """
        self.s_id = s_id
        self.genes = genes
        self.label = label

    def compute_euclidean_distance(self, other):
        """
            Computes euclidean distance between two samples
            :param other: another sample
            :returns: euclidean distance
        """
        sum_difference = 0
        for gene1, gene2 in zip(self.genes, other.genes):
            sum_difference += (gene1-gene2)**2
        return sum_difference**0.5

    def get_s_id(self):
        """
           gets sample's id
           :param: None
           :returns: sample's id
       """
        return self.s_id

    def get_label(self):
        """
           gets sample's label
           :param: None
           :returns: sample's label
       """
        return self.label

