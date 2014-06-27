import sys



if __name__ == "__main__":
    first_file = sys.argv[1]
    second_file = sys.argv[2]
    with open(first_file) as inp1:
        with open(second_file) as inp2:
            for line in inp1:
                print line.strip().split("\t")[0]
            for line in inp2:
                print line.strip().split("\t")[0]

