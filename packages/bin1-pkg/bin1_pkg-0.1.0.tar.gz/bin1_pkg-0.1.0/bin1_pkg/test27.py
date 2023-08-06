def mxmul(mx1,mx2,nrow,nk,ncol):
    rst=[[0 for y in range(ncol)]for x in range(nrow)]
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nk):
                rst[i][j]=mx1[i][k]*mx2[k][j]
    return rst
def mxsum(mx,nrow,ncol):
    s=0
    for i in range(nrow):
        for j in range(ncol):
            s +=mx[i][j]
    return s
if __name__ == "__main__":
    import time
    nrow,nk,ncol=5,3,5
    mx1=[[y for y in range(nk)] for  x in range(nrow)]
    print(mx1)
    mx2=[[y for y in range(ncol)] for x in range(nk)]
    print(mx2)
    strat = time.perf_counter()
    rst = mxmul(mx1,mx2,nrow,nk,ncol)
    end = time.perf_counter()
    print(rst)
    print("运算时间为{:.8f}s".format(end-strat))
