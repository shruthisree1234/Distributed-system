+from client import defprot
def count_to(n):
    print(f"counting to {n}.............")
    for a in range(1, n + 1):
        print(a)
def main():
    print("defer sync request for add(i, j)")
    a = input("Input first value: ")
    b = input("Input second value : ")
    def_var = defprot("add", args=[int(a), int(b)])
    def_var.invoke(par_fn=count_to, args=[6])

    arr =[4,5,8,3,1,5,2]
    print("Request for sorting in deferred sync")
    def_var = defprot("sort", args=[arr])
    def_var.invoke(par_fn=count_to, args=[6])
if __name__ == "__main__":
    main()
