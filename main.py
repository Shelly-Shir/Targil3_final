import sys
from data import Data
from agglomerativeClustering import AgglomerativeClustering
from link import SingleLink, CompleteLink

def main(argv):
    data = Data(argv[1])
    print("single link:")
    link = SingleLink()
    single_link = AgglomerativeClustering(link, data.create_samples())
    single_link.run(7)
    print("complete link:")
    link = CompleteLink()
    complete_link = AgglomerativeClustering(link, data.create_samples())
    complete_link.run(7)


if __name__ == '__main__':
    main(sys.argv)


