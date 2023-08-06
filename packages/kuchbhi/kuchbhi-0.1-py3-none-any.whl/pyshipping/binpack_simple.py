

from pyshipping.package import Package
#
#
#
# scriptpath = "../Test/MyModule.py"
#
# # Add the directory containing your module to the Python path (wants absolute paths)
# sys.path.append(os.path.abspath(scriptpath))



from setuptools import setup, find_packages
from distutils.extension import Extension
import codecs
import time
import random



def packstrip(bin, p):
    """Creates a Strip which fits into bin.

    Returns the Packages to be used in the strip, the dimensions of the strip as a 3-tuple
    and a list of "left over" packages.
    """
    # This code is somewhat optimized and somewhat unreadable
    s = []                # strip
    r = []                # rest
    ss = sw = sl = 0      # stripsize
    bs = bin.heigth       # binsize
    sapp = s.append       # speedup
    rapp = r.append       # speedup
    ppop = p.pop          # speedup
    while p and (ss <= bs):
        n = ppop(0)
        nh, nw, nl = n.size
        if ss + nh <= bs:
            ss += nh
            sapp(n)
            if nw > sw:
                sw = nw
            if nl > sl:
                sl = nl
        else:
            rapp(n)
    # print("s {}, (ss {}, sw {}, sl {}), r + p {}".format(s,ss, sw, sl,r + p))
    return s, (ss, sw, sl), r + p


def packlayer(bin, packages):
    strips = []
    layersize = 0
    layerx = 0
    layery = 0
    binsize = bin.width
    while packages:
        strip, (sizex, stripsize, sizez), rest = packstrip(bin, packages)
        if layersize + stripsize <= binsize:
            packages = rest
            if not strip:
                # we were not able to pack anything
                break
            layersize += stripsize
            layerx = max([sizex, layerx])
            layery = max([sizez, layery])
            strips.extend(strip)
        else:
            # Next Layer please
            packages = strip + rest
            break
    # print("strips {}, (layerx {}, layersize {}, layery {}), packages {}".format(strips,layerx,layersize,layery,packages))
    return strips, (layerx, layersize, layery), packages





def packit(bin, originalpackages):
    packedbins = []
    packages = sorted(originalpackages)
    while packages:
        packagesinbin, (binx, biny, binz), rest = packbin(bin, packages)
        if not packagesinbin:
            # we were not able to pack anything
            break
        packedbins.append(packagesinbin)
        packages = rest
    # we now have a result, try to get a better result by rotating some bins

    # print("inside packit function, packedbins = {} and rest = {}".format(packedbins,rest))
    return packedbins, rest


# In newer Python versions these van be imported:
# from itertools import permutations
def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = list(map(tuple, args)) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def permutations(iterable, r=None):
    pool = tuple(iterable)
    # print("pool", pool)
    n = len(pool)
    r = n if r is None else r
    for indices in product(list(range(n)), repeat=r):
        if len(set(indices)) == r:
            yield tuple(pool[i] for i in indices)


class Timeout(Exception):
    pass


def allpermutations_helper(permuted, todo, maxcounter, callback, bin, bestpack, counter):
    if not todo:
        return counter + callback(bin, permuted, bestpack)
    else:

        others = todo[1:]
        # print("others:",others)

        thispackage = todo[0]
        # print("this package",thispackage)
        a = str(thispackage)
        # print("str",a)
        thispackage_weight = float(a.split()[1])
        # print("weight",thispackage_weight)
        for dimensions in set(permutations((thispackage[0], thispackage[1], thispackage[2]))):
            thispackage = Package(dimensions,thispackage_weight, nosort=True)
            # print("this package in for loop", set(permutations((thispackage[0], thispackage[1], thispackage[2]))))
            if thispackage in bin:
                counter = allpermutations_helper(permuted + [thispackage], others, maxcounter, callback,
                                                 bin, bestpack, counter)
            if counter > maxcounter:
                raise Timeout('more than %d iterations tries' % counter)
        # print("counter = {}".format(counter))
        return counter


def trypack(bin, packages, bestpack):
    bins, rest = packit(bin, packages)
    if len(bins) < bestpack['bincount']:
        bestpack['bincount'] = len(bins)
        bestpack['bins'] = bins
        bestpack['rest'] = rest
    if bestpack['bincount'] < 2:
        raise Timeout('optimal solution found')
    return len(packages)


def allpermutations(todo, bin, iterlimit=5000):    #a,b,c = allpermutations(packages, bin, iterlimit)
    random.seed(1)
    random.shuffle(todo)
    bestpack = dict(bincount=len(todo) + 1)
    # print("bestpack",bestpack)
    try:
        # First try unpermuted
        trypack(bin, todo, bestpack)
        # now try permutations
        allpermutations_helper([], todo, iterlimit, trypack, bin, bestpack, 0)
    except Timeout:
        pass
    # print(bestpack)
    return bestpack['bins'], bestpack['rest'], bestpack

# trucks = "600x400x400"


def binpack(packages,trucks, iterlimit=5000):

    bin  = Package(trucks,10000)
    # print("bin of binpack are", bin)
    # print("packges of binpack are", packages)
    # print(allpermutations(packages, bin, iterlimit))
    # print("value of packages in binpack is" + str(packages))
    a,b,c = allpermutations(packages, bin, iterlimit)
    # print("a of binpack are", a)
    # print("b of binpack are", b)
    # print("c of binpack are", c)
    return a,b,c



def packbin(bin, packages):
    # packages = [Package(pack) for pack in packages.strip().split()]
    packages.sort()
    layers = []
    contentheigth = 0
    contentx = 0
    contenty = 0
    binsize = bin.length
    while packages:
        layer, (sizex, sizey, layersize), rest = packlayer(bin, packages)
        if contentheigth + layersize <= binsize:
            packages = rest
            if not layer:
                # we were not able to pack anything
                break
            contentheigth += layersize
            contentx = max([contentx, sizex])
            contenty = max([contenty, sizey])
            layers.extend(layer)
        else:
            # Next Bin please
            packages = layer + rest
            break
    # print(layers, (contentx, contenty, contentheigth), packages)
    return layers, (contentx, contenty, contentheigth), packages



def packer(packages,weights, trucks):

    vorher = 0
    nachher = 0
    trucks = trucks
    pack = [ro for ro in packages.split()]
    weight = [ro for ro in weights.split()]
    # print(packages)
    packagess = [Package(m,n) for m,n in zip(pack,weight)]
    # print("packeges are ", packagess)
    bins, rest, c = binpack(packagess, trucks)
    if rest:
        print(("invalid data"))
    else:
        vorher += len(packages)
        nachher += len(bins)
    # print((time.time() - start))
    return nachher, c


#

def __lt__(self, other):
    return self.volume < other.volume

# if __name__ == '__main__':
#     import cProfile
#     cProfile.run('test()')
# test()


# print(packbin(Package("600x400x400"),"400x300x200 470x390x120 300x200x200"))

# a = list()
# '[[6.0, 5.16, 6.6, 5.0], [8.75, 5.6, 6.6, 7.0], [8.75, 5.6, 6.6, 7.0], [8.75, 5.6, 6.6, 7.0], [8.75, 5.6, 6.6, 7.0], ' \
# '[8.75, 5.6, 6.6, 7.0], [8.75, 5.6, 6.6, 7.0]]'
# # print(type(a))
# packer(a,Package("800x400x400"))

#
# items = ["4.6x4.3x4.3","4.6x4.3x4.3 6x5.16x6.6","6x5.6x9 6x5.16x6.6 6x5.6x9 6x5.16x6.6 6x5.6x9 6x5.16x6.6 6x5.6x9 8.75x5.6x6.6",
#          "6x5.6x9 6x5.16x6.6","8.75x5.6x6.6 6x5.6x9","6x5.16x6.6 6x5.16x6.6","8.75x5.6x6.6","6.0x5.6x9.0 6.0x5.16x6 6.0x5.16x6",
#          "8.75x5.6x6.6","6x5.6x9","8.75x5.6x6.6 6x5.6x9","6x5.16x6.6","6x5.6x9"]
# weights = ["1","2 25","3 5 6 9 13 16 19 41","10 22","11 17","12 35",'15','20 29 38','21','26','28 40','42','43']
# trucks  = ["9.35x5.5x5.5","18x7x7","19x7x7","22x7.5x8","22x7.5x8","22x7.5x8","17x6x7","22.0x7.5x8.0","22.0x7.5x8.0",
#            "22.0x7.5x8.0","22.0x7.5x8.0","14.0x6.0x6.0","22.0x7.5x8.0"]



#
#
# for i in range(len(items)):
#     print(packer(items[i], weights[i], trucks[i]))


# packlayer(bin, packages)

# print(a.strip().split())

# '(32.0, 9.0, 10.0, 30.0)':