def NelderMead(foo, x_list, alpha=0.5, dim=2):
    assert len(x_list) == dim + 1
    f = [foo(x) for x in x_list]
    x = sorted(x, key=lambda e: foo(e))
    x0 = mean(x[:-1])
    xr = x0 + alpha * (x0 - x[-1])
    fr = foo(xr)
    if foo(x1) <= fr < fn:
        pass
    elif fr < foo(x[0]):
        xe = x0 + 