class Sample:
    def __init__(self,s_id,genes,label):
        self.s_id= s_id
        self.genes= genes
        self.label= label


    def compute_euclidean_distance(self, other):
        sum=0
        for gene1, gene2 in zip(self.genes, other.genes):
            sum += (gene1-gene2)**2
        return sum**0.5

    def get_s_id(self):
        return self.s_id

    def get_label(self):
        return self.label

