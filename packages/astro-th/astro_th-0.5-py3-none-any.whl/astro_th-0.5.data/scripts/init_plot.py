import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from astropy.visualization import ZScaleInterval,ImageNormalize

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] =15
plt.rcParams['axes.labelsize'] = 15
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['figure.titlesize'] = 13

class GenerateArray():

    def __init__(self, Part, Cell, dir, nout, xwid ,zwid, xcenter,ycenter,zcenter):
        start = time.time()
        ywid=xwid
        self.dir = dir
        self.nout = nout
        self.xwid=xwid
        self.ywid=xwid
        self.zwid=zwid

        print('reading finished , t = %.2f [sec]' %(time.time()-start))

        start= time.time()


        pc = 3.08e18

        mindx = np.min(Cell.dx)

        maxgrid = int(np.log2(np.max(Cell.dx) / mindx))

        xind = Cell.x / mindx - 0.5
        yind = Cell.y / mindx - 0.5
        zind = Cell.z / mindx - 0.5

        #center = int(Part.boxpc / 2 / mindx)
        xcenter = int(xcenter/mindx)
        ycenter = int(ycenter/mindx)
        zcenter = int(zcenter/mindx)

        self.xfwd = 2 * int(xwid)
        self.yfwd = 2 * int(ywid)
        self.zfwd = 2 * int(zwid)

        xini = xcenter - xwid
        yini = ycenter - ywid
        zini = zcenter - zwid
        xfin = xcenter + xwid
        yfin = ycenter + ywid
        zfin = zcenter + zwid
        # print(max(self.Cell.cell[0][4][0]))

        self.leafcell = np.zeros((self.xfwd, self.yfwd, self.zfwd))

        ind_1 = np.where((Cell.dx == mindx) & (xind >= xini) & (xind < xfin)
                         & (yind >= yini) & (yind < yfin) & (zind >= zini) & (zind < zfin))[0]

        self.leafcell[xind[ind_1].astype(int) - int(xini), yind[ind_1].astype(int) - int(yini), zind[ind_1].astype(int) - int(zini)] = ind_1.astype(int)

        print('leaf cells are allocated (n=%d)' % len(ind_1))

        mul1 = np.arange(2 ** (maxgrid - 1)) + 0.5
        mul2 = np.arange(2 ** (maxgrid - 1)) * (-1) - 0.5
        mul = np.zeros(2 ** maxgrid)
        for k in range(2 ** (maxgrid - 1)):
            mul[2 * k] = mul1[k]
            mul[2 * k + 1] = mul2[k]
        nn = 0

        for n in range(maxgrid):
            nnn = 0
            ind = np.where(
                (Cell.dx == mindx * 2 ** (n + 1)) & (xind + Cell.dx / 2 / mindx >= xini) & (xind - Cell.dx / 2 / mindx <= xfin) & (
                        yind + Cell.dx / 2 / mindx >= yini) & (yind - Cell.dx / 2 / mindx <= yfin) & (
                        zind + Cell.dx / 2 / mindx >= zini) & (zind - Cell.dx / 2 / mindx <= zfin))[0]
            print(len(ind), len(ind) * (2 ** (n + 1)) ** 3)
            for a in range(2 ** (n + 1)):
                for b in range(2 ** (n + 1)):
                    for c in range(2 ** (n + 1)):
                        xx = xind[ind] - xini + mul[a]
                        yy = yind[ind] - yini + mul[b]
                        zz = zind[ind] - zini + mul[c]
                        xyzind = np.where(
                            (xx >= 0) & (xx <= self.xfwd - 1) & (yy >= 0) & (yy <= self.yfwd - 1) & (zz >= 0) & (zz <= self.zfwd - 1))[0]
                        self.leafcell[xx[xyzind].astype(int), yy[xyzind].astype(int), zz[xyzind].astype(int)] = ind[xyzind]
                        ##   print('zerocell')
                        nnn = nnn + len(xyzind)
            nn = nn + nnn
            print('level %d grids are allocated(n = %d)' % (n + 2, nnn))
            if nnn == 0:
                break
        nonzero = len(np.where(self.leafcell != 0)[0])
        print('total allocated cells are = ', len(ind_1) + nn)
        print('total box cells are = ', self.xfwd * self.yfwd * self.zfwd)
        print('total non zero cell in the box are = ', nonzero)

        if len(ind_1) + nn != self.xfwd * self.yfwd * self.zfwd:
            raise ValueError("allocation failure")
        else:
            print('no error in allocation')
        self.mindx = mindx
        self.xcenter = xcenter
        self.ycenter = ycenter
        self.zcenter = zcenter

        self.xwid = xwid
        self.ywid = ywid
        self.zwid = zwid

        print('Calculation for discomposing , t = %.2f [sec]' %(time.time()-start))


    def projectionPlot(self, Cell, ax, cm, direction, field, rullen, ruler,rulerswitch,vmin,vmax,rulercolor):
        start=time.time()
        if field == 'nH':
            var = Cell.nH
            if direction == 'xy':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)], axis=2) / self.zfwd)

            if direction == 'yz':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)], axis=0) / self.xfwd)

            if direction == 'zx':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)], axis=1) / self.yfwd)
            cax = ax.imshow(np.rot90(plane), cmap=cm,
                            extent=[-self.xwid * self.mindx / 1000, self.xwid * self.mindx / 1000, -self.ywid * self.mindx/ 1000,
                                    self.ywid * self.mindx/ 1000], vmin=vmin, vmax=vmax, aspect='auto')

        if field == 'nHI':
            var = Cell.nHI
            if direction == 'xy':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)], axis=2) / self.zfwd)

            if direction == 'yz':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)], axis=0) / self.xfwd)

            if direction == 'zx':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)], axis=1) / self.yfwd)
            cax = ax.imshow(np.rot90(plane), cmap=cm,
                            extent=[-self.xwid * self.mindx / 1000, self.xwid * self.mindx / 1000,
                                    -self.ywid * self.mindx / 1000,
                                    self.ywid * self.mindx / 1000], vmin=vmin, vmax=vmax, aspect='auto')

        if field == 'T':
            var = Cell.T
            if direction == 'xy':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)]*Cell.nH[self.leafcell[:, :, :].astype(int)], axis=2) / np.sum(Cell.nH[self.leafcell[:, :, :].astype(int)], axis=2)/self.zfwd)
                cax = ax.imshow(np.rot90(plane), cmap=cm,
                            extent=[-self.xwid * self.mindx / 1000, self.xwid * self.mindx / 1000, -self.ywid *self.mindx / 1000,
                                    self.ywid * self.mindx / 1000], vmin=vmin, vmax=vmax)
            if direction == 'yz':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)]*Cell.nH[self.leafcell[:, :, :].astype(int)], axis=0) / np.sum(Cell.nH[self.leafcell[:, :, :].astype(int)], axis=0)/self.zfwd)
                cax = ax.imshow(np.rot90(plane), cmap=cm,
                                extent=[-self.ywid * 9.1 / 1000, self.ywid * 9.1 / 1000, -self.zwid * 9.1 / 1000,
                                        self.zwid * 9.1 / 1000], vmin=1, vmax=7)
            if direction == 'zx':
                plane = np.log10(np.sum(var[self.leafcell[:, :, :].astype(int)]*Cell.nH[self.leafcell[:, :, :].astype(int)], axis=1) / np.sum(Cell.nH[self.leafcell[:, :, :].astype(int)], axis=1)/self.zfwd)
                cax = ax.imshow(np.rot90(plane), cmap=cm,
                            extent=[-self.xwid * 9.1 / 1000, self.xwid * 9.1 / 1000, -self.ywid * 9.1 / 1000,
                                    self.ywid * 9.1 / 1000], vmin=1, vmax=7)

        print('projection finished , t = %.2f [sec]' %(time.time()-start))
        if rulerswitch==True:
            cbaxes = inset_axes(ax, width="30%", height="3%", loc=2)
            cbar = plt.colorbar(cax, cax=cbaxes, ticks=[vmin, vmax], orientation='horizontal', cmap=cm)
            cbar.set_label('log '+field, color=rulercolor, labelpad=-1, fontsize=12)

            cbar.ax.xaxis.set_tick_params(color=rulercolor,labelsize=10)
            cbar.ax.xaxis.set_ticks_position('bottom')
            plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='w')
            rectangles = {
                '%d pc'%ruler: patches.Rectangle(xy=(0.3 * self.xwid * self.mindx / 1000, -0.96 * self.xwid * self.mindx / 1000),
                                           width=(2 * self.xwid * self.mindx / 1000) *rullen,
                                           height=0.03 * (2 * self.ywid * self.mindx / 1000), facecolor=rulercolor)}
            for r in rectangles:
                ax.add_artist(rectangles[r])
                rx, ry = rectangles[r].get_xy()
                cx = rx + rectangles[r].get_width() / 2.0
                cy = ry + rectangles[r].get_height() / 2.0

                ax.annotate(r, (cx, cy + 0.07 * (2 * self.ywid * self.mindx / 1000)), color=rulercolor, weight='bold',
                            fontsize=12, ha='center', va='center')
        return cax

    def star_plot(self, Part, ax,index):

        start=time.time()

        print('star plotting...')
        sxind = Part.xp[0] / self.mindx - self.xcenter + self.xwid
        syind = Part.xp[1] / self.mindx - self.ycenter + self.ywid
        szind = Part.xp[2] / self.mindx - self.zcenter + self.zwid
        sind = np.where(
            (sxind >= 3) & (sxind < self.xfwd - 3) & (syind >= 3) & (syind < self.yfwd - 3) & (szind >= 3) & (szind < self.zfwd - 3))[
            0]
        # sind = np.where((sxind >= 0) & (sxind < xfwd) & (syind >= 0) & (syind < yfwd) & (szind >= 0) & (
        # szind < zfwd))[0]
        sxind = sxind[sind]
        syind = syind[sind]
        szind = szind[sind]

        sxplot = (sxind - self.xwid) * self.mindx
        syplot = (syind - self.ywid) * self.mindx
        szplot = (szind - self.zwid) * self.mindx
        cax1 = ax.scatter(sxplot/1000, syplot/1000,  c='grey', s=1,alpha=0.7)

        sxind = Part.xp[0][index.astype(int)] / self.mindx - self.xcenter + self.xwid
        syind = Part.xp[1][index.astype(int)] / self.mindx - self.ycenter + self.ywid
        szind = Part.xp[2][index.astype(int)] / self.mindx - self.zcenter + self.zwid
        #sind = np.where(
        #    (sxind >= 1) & (sxind < self.xfwd - 1) & (syind >= 3) & (syind < self.yfwd - 3) & (szind >= 1) & (
        #                szind < self.zfwd - 1))[
        #    0]
        # sind = np.where((sxind >= 0) & (sxind < xfwd) & (syind >= 0) & (syind < yfwd) & (szind >= 0) & (
        # szind < zfwd))[0]
        #sxind = sxind[sind]
        #syind = syind[sind]
        #szind = szind[sind]

        sxplot = (sxind - self.xwid) * self.mindx
        syplot = (syind - self.ywid) * self.mindx
        szplot = (szind - self.zwid) * self.mindx
        cax2 = ax.scatter(sxplot/1000, syplot/1000,  c='cyan', marker='*',s=50)
        ax.set_xlim(-self.xwid*self.mindx/1000,self.mindx*self.xwid/1000)
        ax.set_ylim(-self.ywid*self.mindx/1000,self.mindx*self.ywid/1000)

        print('plotting stars finished , t = %.2f [sec]' %(time.time()-start))
        return cax1, cax2


    def clump_plot(self,Clump,ax,member):
        #for appropriate description of size of clump, dpi = 144, figsize * size of axis = size
        size=1.5*9*0.12
        # clump finding
        start=time.time()
        print('finding gas clumps...')


        xclumpind = Clump.xclump / self.mindx - self.xcenter + self.xwid
        yclumpind = Clump.yclump / self.mindx - self.ycenter + self.ywid
        zclumpind = Clump.zclump / self.mindx - self.zcenter + self.zwid

        #clumpind = np.where(
        #    (xclumpind >= 0) & (xclumpind < self.xfwd ) & (yclumpind >= 4) & (yclumpind < self.yfwd - 4) & (zclumpind >= 1) & (
        #                zclumpind < self.zfwd - 1))[0]

        #xclumpind = xclumpind[clumpind]
        #yclumpind = yclumpind[clumpind]
        #zclumpind = zclumpind[clumpind]

        xclumpplot = (xclumpind - self.xwid) * self.mindx
        yclumpplot = (yclumpind - self.ywid) * self.mindx
        zclumpplot = (zclumpind - self.zwid) * self.mindx

        cax1 = ax.scatter(xclumpplot/1000, yclumpplot/1000 ,edgecolor='k', marker='o', s=(Clump.rclump*144*size/self.mindx/self.xfwd)**2,linewidths=1,facecolors='none')

        xclumpplot=Clump.xclump[member.astype(int)] - self.mindx * self.xcenter
        yclumpplot=Clump.yclump[member.astype(int)] - self.mindx * self.ycenter

        cax2 = ax.scatter(xclumpplot/1000, yclumpplot/1000 ,edgecolor='purple', marker='o', s=(Clump.rclump[member.astype(int)]*144*size/self.mindx/self.xfwd)**2,linewidths=3,facecolors='none')
        ax.set_xlim(-self.xwid * self.mindx / 1000, self.mindx * self.xwid / 1000)
        ax.set_ylim(-self.ywid * self.mindx / 1000, self.mindx * self.ywid / 1000)

        return cax1,cax2

class GenerateArray2():

    def __init__(self, Cell, dir, nout, xwid, ywid, zwid, xcenter, ycenter, zcenter, levelmin, levelmax, field,
                 direction, density_weight):
        """
        This class basically divide all the cells into minimum level
        use this for large projected image

        :param Cell: the name of Cell class ex) if you declare Cell1 = Cell(read, nout) then insert Cell1.
        :param dir: directory
        :param nout: snapshot number
        :param xwid: xwidth (in pc scale)
        :param ywid: ywidth
        :param zwid: zwidth
        :param xcenter: xcenter (in pc scale)
        :param ycenter: ycenter
        :param zcenter: zcenter
        :param levelmin: minimum refinement level
        :param levelmax: maximum
        :param field: choose vairable 'nH' or 'T' you can add
        :param direction: projected direction "xy" or "yz" or "zx"
        """
        start1 = time.time()
        start = time.time()

        self.dir = dir
        self.nout = nout
        self.xwid = xwid
        self.ywid = ywid
        self.zwid = zwid

        pc = 3.08e18

        mindx = np.min(Cell.dx)
        self.mindx = mindx
        maxgrid = int(np.log2(np.max(Cell.dx) / mindx))

        xind = Cell.x / mindx - 0.5
        yind = Cell.y / mindx - 0.5
        zind = Cell.z / mindx - 0.5

        # center = int(Part.boxpc / 2 / mindx)
        self.xcenter = int(xcenter / mindx)
        self.ycenter = int(ycenter / mindx)
        self.zcenter = int(zcenter / mindx)

        dlevel = levelmax - levelmin

        xcen_ind_minlev = int(self.xcenter / 2 ** (dlevel))
        ycen_ind_minlev = int(self.ycenter / 2 ** (dlevel))
        zcen_ind_minlev = int(self.zcenter / 2 ** (dlevel))

        xl_ind_minlev = int((xcenter - xwid) / mindx / 2 ** (dlevel))
        xr_ind_minlev = int((xcenter + xwid) / mindx / 2 ** (dlevel))
        yl_ind_minlev = int((ycenter - ywid) / mindx / 2 ** (dlevel))
        yr_ind_minlev = int((ycenter + ywid) / mindx / 2 ** (dlevel))
        zl_ind_minlev = int((zcenter - zwid) / mindx / 2 ** (dlevel))
        zr_ind_minlev = int((zcenter + zwid) / mindx / 2 ** (dlevel))

        xnumiter = xr_ind_minlev - xl_ind_minlev + 1
        ynumiter = yr_ind_minlev - yl_ind_minlev + 1
        znumiter = zr_ind_minlev - zl_ind_minlev + 1

        for i in range(xnumiter):
            for j in range(ynumiter):

                print('segmentation of box (%d/%d),(%d/%d)' % (i + 1, xnumiter, j + 1, xnumiter))
                leafcell = np.zeros((2 ** dlevel, 2 ** dlevel, znumiter * 2 ** dlevel))  # no truncation in vertical
                xini_minlev = xl_ind_minlev + i
                yini_minlev = yl_ind_minlev + j
                zini_minlev = zl_ind_minlev

                if xini_minlev < 0 or yini_minlev < 0 or zini_minlev < 0:
                    raise ValueError('out of boundary!')

                xini = xini_minlev * 2 ** dlevel;
                yini = yini_minlev * 2 ** dlevel;
                zini = zini_minlev * 2 ** dlevel

                xfin = xini + 2 ** dlevel
                yfin = yini + 2 ** dlevel
                zfin = zini + znumiter * 2 ** dlevel
                # print(xini,xfin)

                ind_1 = np.where(
                    (Cell.dx == mindx) & (xind >= xini) & (xind < xfin) & (yind >= yini) & (yind < yfin) & (
                                zind >= zini) & (zind < zfin))[0]
                leafcell[xind[ind_1].astype(int) - int(xini), yind[ind_1].astype(int) - int(yini), zind[ind_1].astype(
                    int) - int(zini)] = ind_1.astype(int)
                print('leaf cells are allocated (n=%d)' % len(ind_1))

                mul1 = np.arange(2 ** (maxgrid - 1)) + 0.5
                mul2 = np.arange(2 ** (maxgrid - 1)) * (-1) - 0.5
                mul = np.zeros(2 ** maxgrid)
                for k in range(2 ** (maxgrid - 1)):
                    mul[2 * k] = mul1[k]
                    mul[2 * k + 1] = mul2[k]
                nn = 0

                for n in range(maxgrid):
                    nnn = 0
                    """
                    ind = np.where(
                        (Cell.dx == mindx * 2 ** (n + 1)) & (xind + Cell.dx / 2 / mindx >= xini) & (
                                    xind - Cell.dx / 2 / mindx < xfin) & (
                                yind + Cell.dx / 2 / mindx >= yini) & (yind - Cell.dx / 2 / mindx < yfin) & (
                                zind + Cell.dx / 2 / mindx >= zini) & (zind - Cell.dx / 2 / mindx < zfin))[0]
                                """
                    ind = np.where(
                        (Cell.dx == mindx * 2 ** (n + 1)) & (xind >= xini) & (xind < xfin) & (yind >= yini) & (
                                    yind < yfin) & (zind >= zini) & (zind < zfin))[0]
                    if len(ind) == 0:
                        print('no cells in level %d (n = %d), t = %.2f [sec]' % (n + 2, 0, time.time() - start))
                        start = time.time()
                        continue
                    print(len(ind), len(ind) * (2 ** (n + 1)) ** 3)
                    if 2 ** (3 * n + 3) < len(ind):
                        for a in range(2 ** (n + 1)):
                            for b in range(2 ** (n + 1)):
                                for c in range(2 ** (n + 1)):
                                    xx = xind[ind] - xini + mul[a]
                                    yy = yind[ind] - yini + mul[b]
                                    zz = zind[ind] - zini + mul[c]
                                    if len(np.where(leafcell[xx.astype(int), yy.astype(int), zz.astype(int)] != 0)[
                                               0]) > 0:
                                        raise ValueError('overlap in allocation')
                                    leafcell[xx.astype(int), yy.astype(int), zz.astype(int)] = ind
                                    if len(np.where(ind == 0)[0]) > 0:
                                        raise ValueError('zero in ind')
                                    ##   print('zerocell')
                                    nnn = nnn + len(ind)
                        print('level %d grids are allocated (n = %d), t = %.2f [sec]' % (
                        n + 2, len(ind) * 2 ** (3 * n + 3), time.time() - start))

                    else:
                        mul_lv1 = np.arange(2 ** (n)) + 0.5
                        mul_lv2 = np.arange(2 ** (n)) * (-1) - 0.5
                        mul_lv = np.zeros(2 ** (n + 1))

                        for k in range(2 ** n):
                            mul_lv[2 * k] = mul_lv1[k]
                            mul_lv[2 * k + 1] = mul_lv2[k]
                        xxx, yyy, zzz = np.meshgrid(mul_lv, mul_lv, mul_lv)
                        # print(n+1,len(xxx.flatten()))
                        for a in range(len(ind)):
                            xx = xind[ind[a]] - xini + xxx.flatten()
                            yy = yind[ind[a]] - yini + yyy.flatten()
                            zz = zind[ind[a]] - zini + zzz.flatten()
                            # rint(leafcell[xx.astype(int), yy.astype(int), zz.astype(int)])
                            if len(np.where(leafcell[xx.astype(int), yy.astype(int), zz.astype(int)] != 0)[0]) > 0:
                                raise ValueError('overlap in allocation')
                            leafcell[xx.astype(int), yy.astype(int), zz.astype(int)] = ind[a]
                            # print(    leafcell[xx.astype(int), yy.astype(int), zz.astype(int)])
                            if ind[a] == 0:
                                print(ind[a])
                            ##   print('zerocell')
                            nnn = nnn + len(xx)
                            # print(2**(3*(n+1)),len(xx))

                        print('level %d grids are allocated (n = %d), t = %.2f [sec]' % (
                        n + 2, len(xx) * len(ind), time.time() - start))
                    start = time.time()
                    nn = nn + nnn
                    # nonzero_lv = len(np.where(leafcell != 0)[0])
                    # print('nonzero_lv,nn',nonzero_lv,nn)
                    """

                    if nonzero_lv != nn:
                        print(nonzero_lv, nn)
                        raise ValueError('error')
                    print('level %d grids are allocated(n = %d)' % (n + 2, nnn))


                    if nnn == 0:
                        break
                    """
                num_allot = len(ind_1) + nn
                num_boxcell = 2 ** dlevel * 2 ** dlevel * znumiter * 2 ** dlevel
                # nonzero = len(np.where(leafcell != 0)[0])
                print('the # of allocated cells = ', num_allot)
                print('the # of box cells  = ', num_boxcell)
                # print('the # of non zero cells in the box = ', nonzero)
                print(leafcell.shape)
                # if num_allot!=num_boxcell or num_allot!=nonzero :
                #    raise ValueError('error in allocation')

                # print('minmax',np.min(Cell.nH[leafcell[:,:,:].astype(int)]), np.max(Cell.nH[leafcell[:,:,:].astype(int)]))

                if field == 'nH':
                    var = Cell.nH
                if field == 'T':
                    var = Cell.T
                if field == 'nHI':
                    var = Cell.nHI
                if field == 'xHI':
                    var = Cell.xHI
                if field == 'xHII':
                    var = Cell.xHII
                if direction == 'xy':
                    axis = 2
                if direction == 'yz':
                    axis = 0
                if direction == 'zx':
                    axis = 1
                if density_weight == True:
                    plane = np.log10(np.sum(var[leafcell[:, :, :].astype(int)] * Cell.nH[leafcell[:, :, :].astype(int)],
                                            axis=axis) / np.sum(Cell.nH[leafcell[:, :, :].astype(int)], axis=axis))


                else:
                    plane = np.log10(np.sum(var[leafcell[:, :, :].astype(int)], axis=axis) / (znumiter * 2 ** dlevel))

                    # print(znumiter*2**dlevel)
                    # print(np.sum(var[leafcell[:, :, :].astype(int)], axis=2))
                    # print(np.log10(np.sum(var[leafcell[:, :, :].astype(int)], axis=2) / (znumiter*2**dlevel)))
                    # print('minmax(plane) = ',np.min(plane),np.max(plane))

                if j == 0:
                    iniplane = plane
                    # print('iniplane',iniplane, iniplane.shape)

                else:
                    iniplane = np.column_stack((iniplane, plane))
                    # print('iniplane',iniplane.shape)
                print('finishing projection, t = %.2f [sec]' % (time.time() - start))
                start = time.time()

            if i == 0:
                iniiniplane = iniplane
                # print('iniiniplane', iniiniplane.shape)

            else:
                iniiniplane = np.row_stack((iniiniplane, iniplane))
                # print('iniiniplane', iniiniplane.shape)

        print('finishing patches assembling, t = %.2f [sec]' % (time.time() - start))
        start = time.time()
        # plane truncation for centering
        self.xl_trunc = self.xcenter - int(xwid / mindx) - xl_ind_minlev * (2 ** dlevel)
        print(self.xcenter, int(xwid / mindx), xl_ind_minlev * (2 ** dlevel))
        self.xr_trunc = self.xcenter + int(xwid / mindx) - xl_ind_minlev * (2 ** dlevel)
        self.yl_trunc = self.ycenter - int(ywid / mindx) - yl_ind_minlev * (2 ** dlevel)
        self.yr_trunc = self.ycenter + int(ywid / mindx) - yl_ind_minlev * (2 ** dlevel)
        print(self.xl_trunc, self.xr_trunc, self.yl_trunc, self.yr_trunc)
        # print(iniiniplane)
        self.plane = iniiniplane[self.xl_trunc:self.xr_trunc, self.yl_trunc:self.yr_trunc]
        print(np.min(self.plane), np.max(self.plane))
        # print(self.plane)

        # print(self.plane.shape)
        print('finisihing truncation, t=%.2f [sec]' % (time.time() - start))
        print('Calculation for discomposing , t = %.2f [sec]' % (time.time() - start1))

        self.field = field

    def projectionPlot(self, ax, cm, ticks):
        start = time.time()
        im = ax.imshow(np.rot90(self.plane), cmap=cm,
                       extent=[-self.xwid / 1000, self.xwid / 1000, -self.ywid / 1000,
                               self.ywid / 1000], vmin=np.min(ticks), vmax=np.max(ticks), aspect='equal')
        ax.set_xlim(-self.xwid / 1000, self.xwid / 1000)
        ax.set_ylim(-self.ywid / 1000, self.ywid / 1000)

        cbaxes = inset_axes(ax, width="25%", height="3%", loc=3)
        cbar = plt.colorbar(im, cax=cbaxes, ticks=ticks, orientation='horizontal', cmap=cm)
        cbar.set_label('log(' + self.field + ')', color='w', labelpad=-11, fontsize=10)
        cbar.ax.xaxis.set_tick_params(color='w')
        cbar.ax.xaxis.set_ticks_position('top')
        plt.setp(plt.getp(cbar.ax.axes, 'xticklabels'), color='w')

        """
        you have to insert appropriate number for below 'rectangles' 
        this is ruler which indicates the size of projected image
        ex) if you want to draw 5 kpc width projected image and want to insert ruler with 3 kpc size, then 
        replace 5 kpc into 3 kpc and you have to multiply 3/5 instead of 5/14 in width. 
        """

        rectangles = {
            '5 kpc': patches.Rectangle(xy=(0.1 * self.xwid / 1000, -0.95 * self.xwid / 1000),
                                       width=(2 * self.xwid / 1000) * 5 / 14,
                                       height=0.01 * (2 * self.ywid / 1000), facecolor='white')}
        for r in rectangles:
            ax.add_artist(rectangles[r])
            rx, ry = rectangles[r].get_xy()
            cx = rx + rectangles[r].get_width() / 2.0
            cy = ry + rectangles[r].get_height() / 2.0

            ax.annotate(r, (cx, cy + 0.02 * (2 * self.ywid / 1000)), color='w', weight='bold',
                        fontsize=15, ha='center', va='center')

        return im

    def star_plot(self, Part, ax):

        start = time.time()

        print('star plotting...')

        ex_xcenter = self.xcenter * self.mindx + 0.5 * self.mindx
        ex_ycenter = self.ycenter * self.mindx + 0.5 * self.mindx
        ex_zcenter = self.zcenter * self.mindx + 0.5 * self.mindx

        sxplot = (Part.xp[0] - ex_xcenter) / 1000
        syplot = (Part.xp[1] - ex_ycenter) / 1000
        szplot = (Part.xp[2] - ex_zcenter) / 1000
        cax1 = ax.scatter(sxplot, syplot, c='grey', s=0.1, alpha=0.3)

        print('plotting stars finished , t = %.2f [sec]' % (time.time() - start))
        return cax1

    def star_plot2(self, Part, ax, Fesc_indSED, filter):

        start = time.time()

        print('star plotting...')

        ex_xcenter = self.xcenter * self.mindx + 0.5 * self.mindx
        ex_ycenter = self.ycenter * self.mindx + 0.5 * self.mindx
        ex_zcenter = self.zcenter * self.mindx + 0.5 * self.mindx

        sxplot = (Part.xp[0] - ex_xcenter) / 1000
        syplot = (Part.xp[1] - ex_ycenter) / 1000
        szplot = (Part.xp[2] - ex_zcenter) / 1000



        rflux = Fesc_indSED.rflux
        gflux = Fesc_indSED.gflux
        bflux = Fesc_indSED.bflux

        vmin1, vmax1 = zscale(rflux)
        vmin2, vmax2 = zscale(gflux)
        vmin3, vmax3 = zscale(bflux)

        rflux = rflux / vmax1
        gflux = gflux / vmax2
        bflux = bflux / vmax3

        rflux[rflux > 1] = 1.0
        gflux[gflux > 1] = 1.0
        bflux[bflux > 1] = 1.0

        rflux[rflux < vmin1 / vmax1] = 0
        gflux[gflux < vmin2 / vmax2] = 0
        bflux[bflux < vmin3 / vmax3] = 0

        print(np.min(rflux), np.max(rflux))
        print(np.min(gflux), np.max(gflux))
        print(np.min(bflux), np.max(bflux))

        flux = np.transpose(np.array([rflux, gflux, bflux]))

        flux_t = tuple((map(tuple, flux)))
        print(flux_t)

        cax1 = ax.scatter(sxplot, syplot, c=flux_t, s=0.1, alpha=0.2)

        print('plotting stars finished , t = %.2f [sec]' % (time.time() - start))
        ax.set_xlim(-self.xwid / 1000, self.xwid / 1000)
        ax.set_ylim(-self.ywid / 1000, self.ywid / 1000)
        return cax1

    def clump_plot(self, Clump, ax):
        # for appropriate description of size of clump, dpi = 144, figsize * size of axis = size
        size = 6.3
        # clump finding
        start = time.time()
        print('finding gas clumps...')

        xclumpind = Clump.xclump / self.mindx - self.xcenter + self.xwid
        yclumpind = Clump.yclump / self.mindx - self.ycenter + self.ywid
        zclumpind = Clump.zclump / self.mindx - self.zcenter + self.zwid

        clumpind = np.where(
            (xclumpind >= 0) & (xclumpind < self.xfwd) & (yclumpind >= 4) & (yclumpind < self.yfwd - 4) & (
                        zclumpind >= 1) & (
                    zclumpind < self.zfwd - 1))[0]

        xclumpind = xclumpind[clumpind]
        yclumpind = yclumpind[clumpind]
        zclumpind = zclumpind[clumpind]

        xclumpplot = (xclumpind - self.xwid) * self.mindx
        yclumpplot = (yclumpind - self.ywid) * self.mindx
        zclumpplot = (zclumpind - self.zwid) * self.mindx

        cax1 = ax.scatter(xclumpplot / 1000, yclumpplot / 1000, edgecolor='k', marker='o',
                          s=(Clump.rclump[clumpind] * 144 * size / self.mindx / self.xfwd) ** 2, linewidths=1,
                          facecolors='none')

        return cax1


def zscale(arr):
    interval = ZScaleInterval()
    vmin, vmax = interval.get_limits(arr)

    return vmin, vmax


def CoM_check_plot(Part1, Cell1, wid, depth, xcen, ycen, zcen):
    fig = plt.figure(figsize=(8, 8), dpi=144)

    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    cm1 = plt.get_cmap('rainbow')

    a = GenerateArray2(Part1, Cell1, xcen, ycen, zcen, wid, depth)
    ss1 = a.projectionPlot(Cell1, ax1, cm1, 'xy', 'nH', -3, 2)
    a.star_plot(Part1, ax1)
    ax1.scatter((xcen - a.mindx * a.xcenter) / 1000, (ycen - a.mindx * a.ycenter) / 1000, s=100, marker='*')

    ax1.set_xlabel('X(kpc)')
    ax1.set_ylabel('Y(kpc)')
    cax1 = fig.add_axes([0.9, 0.1, 0.02, 0.3])

    plt.colorbar(ss1, cax=cax1, cmap=cm1)
    plt.show()
    plt.close()


def getr(x, y, z, xcenter, ycenter, zcenter):
    return np.sqrt((x - xcenter) ** 2 + (y - ycenter) ** 2 + (z - zcenter) ** 2)


def get2dr(x, y, xcen, ycen):
    return np.sqrt((x - xcen) ** 2 + (y - ycen) ** 2)


def getmass(marr, rarr, r):
    ind = np.where(rarr < r)
    return np.sum(marr[ind])


def mxsum(marr, xarr, ind):
    return np.sum(marr[ind] * xarr[ind])


def msum(marr, ind):
    return np.sum(marr[ind])


def simpleCoM(x, y, z, marr, rarr, r):
    ind = np.where(rarr < r)
    xx = np.sum(x[ind] * marr[ind]) / np.sum(marr[ind])
    yy = np.sum(y[ind] * marr[ind]) / np.sum(marr[ind])
    zz = np.sum(z[ind] * marr[ind]) / np.sum(marr[ind])

    return xx, yy, zz


# half-mass CoM

def CoM_pre(Part1, Cell1, rgrid, totmass, xcen, ycen, zcen, gasonly):
    rstar = getr(Part1.xp[0], Part1.xp[1], Part1.xp[2], xcen, ycen, zcen)
    rpart = getr(Part1.dmxp[0], Part1.dmxp[1], Part1.dmxp[2], xcen, ycen, zcen)
    rcell = getr(Cell1.x, Cell1.y, Cell1.z, xcen, ycen, zcen)

    for i in range(len(rgrid)):
        mstar = getmass(Part1.mp0, rstar, rgrid[i])
        mpart = getmass(Part1.dmm, rpart, rgrid[i])
        mcell = getmass(Cell1.m, rcell, rgrid[i])
        summass = mstar + mpart + mcell
        if summass > totmass / 2:
            rrr = rgrid[i]
            break
        if i == len(rgrid) - 1:
            rrr = rgrid[-1]

    if gasonly == False:

        indstar = np.where(rstar < rrr)
        indpart = np.where(rpart < rrr)
        indcell = np.where(rcell < rrr)

        totalmx = mxsum(Part1.xp[0], Part1.mp0, indstar) + mxsum(Part1.dmxp[0], Part1.dmm, indpart) + mxsum(Cell1.x,
                                                                                                            Cell1.m,
                                                                                                            indcell)
        totalmy = mxsum(Part1.xp[1], Part1.mp0, indstar) + mxsum(Part1.dmxp[1], Part1.dmm, indpart) + mxsum(Cell1.y,
                                                                                                            Cell1.m,
                                                                                                            indcell)
        totalmz = mxsum(Part1.xp[2], Part1.mp0, indstar) + mxsum(Part1.dmxp[2], Part1.dmm, indpart) + mxsum(Cell1.z,
                                                                                                            Cell1.m,
                                                                                                            indcell)
        totalm = msum(Part1.mp0, indstar) + msum(Part1.dmm, indpart) + msum(Cell1.m, indcell)

    else:
        indcell = np.where(rcell < rrr)

        totalmx = mxsum(Cell1.x, Cell1.m, indcell);
        totalmy = mxsum(Cell1.y, Cell1.m, indcell);
        totalmz = mxsum(Cell1.z, Cell1.m, indcell)

        totalm = msum(Cell1.m, indcell)
    xx = totalmx / totalm
    yy = totalmy / totalm
    zz = totalmz / totalm

    return xx, yy, zz


def CoM_main(Part1, Cell1, diskmass):
    rgrid1 = np.linspace(100, 4000, num=40)
    boxcen = Part1.boxpc / 2
    x1, y1, z1 = CoM_pre(Part1, Cell1, rgrid1, 1e11, boxcen, boxcen, boxcen, False)
    x2, y2, z2 = CoM_pre(Part1, Cell1, rgrid1, diskmass, x1, y1, z1, True)
    x3, y3, z3 = CoM_pre(Part1, Cell1, rgrid1, diskmass, x2, y2, z2, True)

    # print(x2,y2,z2)
    return x3, y3, z3