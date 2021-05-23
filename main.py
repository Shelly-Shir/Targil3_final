import sys
from data import Data
from agglomerativeClustering import AgglomerativeClustering
from link import SingleLink, CompleteLink


def main(argv):
    data = Data(argv[1])
    # run the algorithm in single link method
    print("single link:")
    link = SingleLink()
    single_link = AgglomerativeClustering(link, data.create_samples())
    single_link.run(7)
    # run the algorithm in complete link method
    print("complete link:")
    link = CompleteLink()
    complete_link = AgglomerativeClustering(link, data.create_samples())
    complete_link.run(7)


if __name__ == '__main__':
    main(sys.argv)

