import numpy as np
from scipy.io import FortranFile
from scipy.io import readsav
import os.path
read_old_01Zsun = '/Volumes/THYoo/RHD_10pc/'

read_old_002Zsun = '/Volumes/THYoo/RHD_10pc_lowZ/'

read_new_01Zsun = '/Volumes/THYoo/kisti/RHD_10pc_0.1Zsun/'

read_new_1Zsun = '/Volumes/THYoo/kisti/RHD_10pc_1Zsun/'

read_new_01Zsun_re = '/blackwhale/dbahck37/kisti/0.1Zsun/'

read_new_1Zsun_re = '/blackwhale/dbahck37/kisti/1Zsun/'

read_new_gasrich = '/Volumes/THYoo/kisti/RHD_10pc_gasrich/G9_gasrich/'

read_new_1Zsun_highSN_old = '/Volumes/gdrive/1Zsun_SNen_old/'
read_new_1Zsun_highSN_new = '/Volumes/gdrive/1Zsun_SNen_new/'

read_new_03Zsun_highSN = '/Volumes/gdrive/0.3Zsun_SNen/'

read_new_01Zsun_05pc = '/Volumes/gdrive/0.1Zsun_5pc/'

class Part():
    def __init__(self, dir, nout):
        self.dir = dir
        self.nout = nout
        partdata = readsav(self.dir + '/SAVE/part_%05d.sav' % (self.nout))
        self.snaptime = partdata.info.time*4.70430e14/365/3600/24/1e6
        pc = 3.08e18
        self.boxpc = partdata.info.boxlen * partdata.info.unit_l / pc
        self.boxlen = partdata.info.boxlen
        xp = partdata.star.xp[0]
        self.xp = xp * partdata.info.unit_l / 3.08e18
        self.unit_l = partdata.info.unit_l
        self.unit_d = partdata.info.unit_d
        self.starage = self.snaptime - partdata.star.tp[0]*4.70430e14/365/3600/24/1e6
        self.starid = np.abs(partdata.star.id[0])
        self.mp0 = partdata.star.mp0[0] * partdata.info.unit_d * partdata.info.unit_l / 1.989e33 * partdata.info.unit_l*partdata.info.unit_l

        tp = (partdata.info.time-partdata.star.tp[0]) * 4.70430e14 / 365. /24./3600/1e6
        sfrindex = np.where((tp >= 0) & (tp < 10))[0]
        self.SFR = np.sum(self.mp0[sfrindex]) / 1e7
        self.dmxp = partdata.part.xp[0] * partdata.info.unit_l / 3.08e18
        dmm = partdata.part.mp[0]

        self.dmm = dmm * partdata.info.unit_d * partdata.info.unit_l / 1.989e33 * partdata.info.unit_l * partdata.info.unit_l
        dmindex = np.where(dmm > 2000)
        self.dmxpx = self.dmxp[0][dmindex]
        self.dmxpy = self.dmxp[1][dmindex]
        self.dmxpz = self.dmxp[2][dmindex]


class Fesc_rjus():
    def __init__(self,read,nout,rjus):

        dat = FortranFile(read+'ray_nside4_%3.2f/ray_%05d.dat' % (rjus, nout), 'r')
        npart, nwave2 = dat.read_ints()
        wave = dat.read_reals(dtype=np.double)
        sed_intr = dat.read_reals(dtype=np.double)
        sed_attH = dat.read_reals(dtype=np.double)
        sed_attD = dat.read_reals(dtype=np.double)
        npixel = dat.read_ints()
        tp = dat.read_reals(dtype='float32')
        fescH = dat.read_reals(dtype='float32')
        self.fescD = dat.read_reals(dtype='float32')
        self.photonr = dat.read_reals(dtype=np.double)
        self.fesc = np.sum(self.fescD*self.photonr)/np.sum(self.photonr)

class Fesc_indSED():
    def __init__(self, dir, nout):
        dat2 = FortranFile(dir + 'ray_indSED/ray_%05d.dat' % (nout), 'r')
        npart, nwave2, version = dat2.read_ints()
        wave = dat2.read_reals(dtype=np.double)
        sed_intr = dat2.read_reals(dtype=np.double)
        sed_attHHe = dat2.read_reals(dtype=np.double)
        sed_attHHeD = dat2.read_reals(dtype=np.double)
        sed_attHHI = dat2.read_reals(dtype=np.double)
        sed_attHH2 = dat2.read_reals(dtype=np.double)
        sed_attHHe= dat2.read_reals(dtype=np.double)
        sed_attD= dat2.read_reals(dtype=np.double)

        npixel = dat2.read_ints()
        tp = dat2.read_reals(dtype='float32')
        self.fescH = dat2.read_reals(dtype='float32')
        self.fescD = dat2.read_reals(dtype='float32')
        self.photonr = dat2.read_reals(dtype=np.double)
        idp = dat2.read_ints()
        self.rflux = dat2.read_reals(dtype=np.double)
        self.gflux = dat2.read_reals(dtype=np.double)
        self.bflux = dat2.read_reals(dtype=np.double)

        self.fesc = np.sum(self.fescD * self.photonr) / np.sum(self.photonr)
        self.fesc2 = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)

        self.fescwodust = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)


class Cell():
    def __init__(self, dir, nout, Part):
        self.dir = dir
        self.nout = nout
        celldata = readsav(self.dir + '/SAVE/cell_%05d.sav' % (self.nout))
        self.nH = celldata.cell[0][4][0] * 30.996344
        self.x = celldata.cell.x[0] * Part.boxpc
        self.y = celldata.cell.y[0] * Part.boxpc
        self.z = celldata.cell.z[0] * Part.boxpc
        self.dx = celldata.cell.dx[0] * Part.boxpc
        self.mindx = np.min(celldata.cell.dx[0])
        self.nHI = self.nH * celldata.cell[0][4][7]
        nHII = self.nH * celldata.cell[0][4][8]
        nH2 = self.nH * (1 - celldata.cell[0][4][7] - celldata.cell[0][4][8])/2
        YY= 0.24/(1-0.24)/4
        nHeII = self.nH * YY*celldata.cell[0][4][9]
        nHeIII = self.nH * YY*celldata.cell[0][4][10]
        nHeI = self.nH * YY*(1 - celldata.cell[0][4][9] - celldata.cell[0][4][10])
        ne = nHII + nHeII + nHeIII *2
        ntot = self.nHI + nHII + nHeI + nHeII + nHeIII + ne + nH2
        mu = celldata.cell[0][4][0] * Part.unit_d / 1.66e-24 / ntot
        self.m = celldata.cell[0][4][0] *Part.unit_d * Part.unit_l / 1.989e33 * Part.unit_l *Part.unit_l *(celldata.cell.dx[0]*Part.boxlen)**3

        self.T = celldata.cell[0][4][5]/celldata.cell[0][4][0] * 517534.72 * mu
        self.xHI =celldata.cell[0][4][7]
        self.xHII=celldata.cell[0][4][8]

class Cellfromdat():
    def __init__(self, dir, nout, Part):
        celldata = FortranFile(dir + 'dat/cell_%05d.dat' % nout, 'r')
        nlines,xx,nvarh=celldata.read_ints(dtype=np.int32)

        xc = celldata.read_reals(dtype=np.double)
        yc = celldata.read_reals(dtype=np.double)
        zc = celldata.read_reals(dtype=np.double)
        dxc = celldata.read_reals(dtype=np.double)

        self.x = xc * Part.boxpc
        self.y = yc * Part.boxpc
        self.z = zc * Part.boxpc
        self.dx = dxc * Part.boxpc

        var = np.zeros((nlines,nvarh))
        for i in range(nvarh):

            var[:,i] = celldata.read_reals(dtype=np.double)

        self.nH = var[:, 0] * 30.996344
        self.m = var[:, 0] * Part.unit_d * Part.unit_l / 1.989e33 * Part.unit_l * Part.unit_l * (
                    dxc * Part.boxlen) ** 3
        xHI = var[:,7]
        xHII = var[:,8]
        self.mHIH2 = self.m * (1-xHII)


class GasrichCell():
    def __init__(self, dir, nout, Part):
        self.dir = dir
        self.nout = nout
        print(nout)
        celldata = readsav(self.dir + '/SAVE/cell_%05d.sav' % (self.nout))
        self.nH = celldata.cell.nh[0] * 30.996344
        self.x = celldata.cell.x[0] * Part.boxpc
        self.y = celldata.cell.y[0] * Part.boxpc
        self.z = celldata.cell.z[0] * Part.boxpc
        self.dx = celldata.cell.dx[0] * Part.boxpc
        self.mindx = np.min(celldata.cell.dx[0])
        self.m = celldata.cell.nh[0] *Part.unit_d * Part.unit_l / 1.989e33 * Part.unit_l *Part.unit_l *(celldata.cell.dx[0]*Part.boxlen)**3

class Clump():
    def __init__(self, dir, nout, Part):
        self.dir = dir
        self.nout = nout
        unit_d = Part.unit_d
        unit_l = Part.unit_l
        clumpdata = np.loadtxt(self.dir + '/clump3/clump_%05d.txt' % (self.nout),
                               dtype=np.double)
        self.xclump = clumpdata[:, 4] * Part.unit_l / 3.08e18
        self.yclump = clumpdata[:, 5] * Part.unit_l / 3.08e18
        self.zclump = clumpdata[:, 6] * Part.unit_l / 3.08e18

        self.massclump = clumpdata[:,
                    10] * unit_d * unit_l / 1.989e33 * unit_l * unit_l
        self.rclump = (clumpdata[:, 10] / clumpdata[:, 9] / 4 / np.pi * 3) ** (0.333333) * unit_l / 3.08e18
        self.nclump = len(self.xclump)

class Fesc_old():
    def __init__(self, dir, nout):
        dat2 = FortranFile(dir + 'ray_nside4/ray_%05d.dat' % (nout), 'r')
        npart, nwave2 = dat2.read_ints()
        wave = dat2.read_reals(dtype=np.double)
        sed_intr = dat2.read_reals(dtype=np.double)
        sed_attH = dat2.read_reals(dtype=np.double)
        sed_attD = dat2.read_reals(dtype=np.double)
        npixel = dat2.read_ints()
        tp = dat2.read_reals(dtype='float32')
        self.fescH = dat2.read_reals(dtype='float32')
        self.fescD = dat2.read_reals(dtype='float32')
        self.photonr = dat2.read_reals(dtype=np.double)
        self.fesc = np.sum(self.fescD * self.photonr) / np.sum(self.photonr)
        self.fescwodust = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)


class Fesc_new():
    def __init__(self, dir, nout):
        dat2 = FortranFile(dir + 'ray_nside4_laursen/ray_%05d.dat' % (nout), 'r')
        npart, nwave2, version = dat2.read_ints()
        wave = dat2.read_reals(dtype=np.double)
        sed_intr = dat2.read_reals(dtype=np.double)
        sed_attHHe = dat2.read_reals(dtype=np.double)
        sed_attHHeD = dat2.read_reals(dtype=np.double)
        sed_attHHI = dat2.read_reals(dtype=np.double)
        sed_attHH2 = dat2.read_reals(dtype=np.double)
        sed_attHHe= dat2.read_reals(dtype=np.double)
        sed_attD= dat2.read_reals(dtype=np.double)

        npixel = dat2.read_ints()
        tp = dat2.read_reals(dtype='float32')
        self.fescH = dat2.read_reals(dtype='float32')
        self.fescD = dat2.read_reals(dtype='float32')
        self.photonr = dat2.read_reals(dtype=np.double)
        self.fesc = np.sum(self.fescD * self.photonr) / np.sum(self.photonr)
        self.fesc2 = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)
        self.fescwodust = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)

class Fesc_new8():
    def __init__(self, dir, nout):
        dat2 = FortranFile(dir + 'ray_nside8_laursen/ray_%05d.dat' % (nout), 'r')
        npart, nwave2, version = dat2.read_ints()
        wave = dat2.read_reals(dtype=np.double)
        sed_intr = dat2.read_reals(dtype=np.double)
        sed_attHHe = dat2.read_reals(dtype=np.double)
        sed_attHHeD = dat2.read_reals(dtype=np.double)
        sed_attHHI = dat2.read_reals(dtype=np.double)
        sed_attHH2 = dat2.read_reals(dtype=np.double)
        sed_attHHe= dat2.read_reals(dtype=np.double)
        sed_attD= dat2.read_reals(dtype=np.double)

        npixel = dat2.read_ints()
        tp = dat2.read_reals(dtype='float32')
        self.fescH = dat2.read_reals(dtype='float32')
        self.fescD = dat2.read_reals(dtype='float32')
        self.photonr = dat2.read_reals(dtype=np.double)
        self.fesc = np.sum(self.fescD * self.photonr) / np.sum(self.photonr)
        self.fesc2 = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)

        self.fescwodust = np.sum(self.fescH * self.photonr) / np.sum(self.photonr)