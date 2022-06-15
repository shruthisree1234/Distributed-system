from client import asynprot
import time

def main():
    a = input("Input first value: ")
    b = input("Input second value : ")
    print("asynchronous request for add(a,b)")
    add_ = asynprot("add", args=[int(a),int(b)])
    add_.invoke()

    arr=[5,8,63,4,1]
    sort_=asynprot("sort", args=[arr])
    sort_.invoke()
    print("\nProcessing2...\n")
    time.sleep(1)

    print("fetching results for add(a,b) = {}".format(add_.get_result()))
    print("fetching results for sort = {}".format(sort_.get_result()))

if __name__ == "__main__":
    main()
