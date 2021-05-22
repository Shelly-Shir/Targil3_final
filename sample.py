class Sample:
    """
        Constructor for class. initialize all values
        :param1 s_id: sample's id
        :param2 genes: list of genes
        :param3 label: sample's label
        :returns: sample's in value
    """
    def __init__(self, s_id, genes, label):
        self.s_id = s_id
        self.genes = genes
        self.label = label

    """
        Computes euclidean distance between two samples 
        :param other: another sample
        :returns: euclidean distance
    """
    def compute_euclidean_distance(self, other):
        sum_difference = 0
        for gene1, gene2 in zip(self.genes, other.genes):
            sum_difference += (gene1-gene2)**2
        return sum_difference**0.5

    """
       gets sample's id
       :param: None
       :returns: sample's id
   """
    def get_s_id(self):
        return self.s_id

    """
       gets sample's label
       :param: None
       :returns: sample's label
   """
    def get_label(self):
        return self.label

