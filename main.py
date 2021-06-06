import sys
from data import Data
from agglomerativeClustering import AgglomerativeClustering
from link import SingleLink, CompleteLink

def main(argv):
    """
        prints clusters details
        :param: argv: array of parameters
        :returns: None
    """
    data = Data(argv[1])
    sample_dict = {}
    for sample in data.create_samples():
        for other_sample in data.create_samples():
            if sample.get_s_id() < other_sample.get_s_id():
                sample_dict[tuple([sample.get_s_id(), other_sample.get_s_id()])] = sample.compute_euclidean_distance(other_sample)

    # run the algorithm in single link method
    print("single link:")
    link = SingleLink()
    single_link = AgglomerativeClustering(link, data.create_samples(), sample_dict)
    single_link.run(7)
    # run the algorithm in complete link method
    print("complete link:")
    link = CompleteLink()
    complete_link = AgglomerativeClustering(link, data.create_samples(), sample_dict)
    complete_link.run(7)

if __name__ == '__main__':
    main(sys.argv)

