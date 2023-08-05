from sys import platform
if platform == 'darwin':
    import matplotlib
    matplotlib.use("Qt5Agg")
import pandas as pd
import numpy as np
import cv2, gdal, os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import find_peaks, convolve2d
from PIL import Image
from tqdm import tqdm
Image.MAX_IMAGE_PIXELS = 1e+9
from .Agents import *
from .GUI_crop import *

# sudo cp /Users/jameschen/Dropbox/James_Git/pypi/AgricolAI/AgricolAI/Field_Segmentation/*.py /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/AgricolAI/Field_Segmentation/

class Model():
    def __init__(self,\
            k=3, ratio_veg=0.3,\
            n_denoise=30, n_smooth=100,\
            tol=3, coef_grid=.2):
        '''
        '''
        self.k, self.ratio_veg = k, ratio_veg
        self.n_denoise, self.n_smooth = n_denoise, n_smooth
        self.tol, self.coef_grid = tol, coef_grid
        self.field = -1
        print("Field_Segmentation(k=%d, n_denoise=%d, coef_grid=%.2f)"%(self.k, self.n_denoise, self.coef_grid))
    def fit(self, img, map, ch_NIR=1, ch_Red=0):
        '''
        '''
        self.ch_NIR, self.ch_Red = ch_NIR, ch_Red
        self.load_data(img=img, map=map, ch_NIR=self.ch_NIR, ch_Red=self.ch_Red)
        self.to_binary(k=self.k, ratio_veg=self.ratio_veg)
        try:
            self.put_anchors(n_denoise=self.n_denoise, n_smooth=self.n_smooth, tol=self.tol)
        except:
            print("Number of detected plots can't match the provided map!")
        self.search_by_agent(coef_grid=self.coef_grid)
        print("<Done>")
    def load_data(self, img, map, ch_NIR=1, ch_Red=0):
        '''
        '''
        print("<Loading Data>")
        self.ch_Red = ch_Red
        self.ch_NIR = ch_NIR
        token_img = False
        # token_map = False
        # load img
        if isinstance(img, str):
            try:
                _, ext = os.path.splitext(img)
                if "tif" in ext:
                    img = read_tiff(img)
                else:
                    img = np.array(Image.open(img))
                token_img = True
            except:
                print("Try loading images as a numpy array")
            if not token_img:
                try:
                    img = np.load(img)
                except:
                    print("Input image can't be recognized!")
                    return 0
        elif isinstance(img, np.ndarray):
            img = img
        else:
            print("Input image can't be recognized!")
            return 0
        # load map
        if isinstance(map, str):
            map = pd.read_csv(map, header=None)
        elif isinstance(map, np.ndarray):
            map = pd.DataFrame(map)
        elif isinstance(map, pd.DataFrame):
            map = map
        else:
            print("Input map can't be recognized!")
            return 0
        # crop the image
        print("<Please assign four anchors to crop the image>")
        img = get_cropped_img(img)
        # standardization
        print("<Standardizing the Image>")
        means, stds = img.mean(axis=(0, 1)), img.std(axis=(0, 1))
        img_std = (img-means)/stds
        img_max, img_min = img_std.max(axis=(0, 1)), img_std.min(axis=(0, 1))-(1e-8)
        img_std2 = (img_std-img_min)/(img_max-img_min)
        # instantiate filed class
        img_ndvi = (img_std2[:,:,ch_NIR]-img_std2[:,:,ch_Red])/(img_std2[:,:,ch_NIR]+img_std2[:,:,ch_Red])
        self.field = Field(img=img, img_std=img_std2, img_ndvi=img_ndvi, map=map)
    def to_binary(self, k=3, ratio_veg=0.3):
        '''
        '''
        print("<Detecting Boundaries>")
        # data type conversion for opencv
        img_std = self.field.img_std.copy()[:,:,[self.ch_NIR, self.ch_Red]]
        img_z = img_std.reshape((-1, img_std.shape[2])).astype(np.float32)
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
        param_k = dict(data=img_z,\
                       K=k,\
                       bestLabels=None,\
                       criteria=criteria,\
                       attempts=30,\
                       flags=cv2.KMEANS_PP_CENTERS)
        _, img_k_temp, center = cv2.kmeans(**param_k)
        # Convert back
        img_k_temp = img_k_temp.astype(np.uint8).reshape((img_std.shape[0], -1))
        # Find proper label for NIR
        prop_g = [center[i, 0]/center[i, :].sum() for i in range(k)]
        rank_g = np.flip(np.argsort(prop_g), 0)
        idx_k = 1
        while idx_k<=k:
            idx_select = rank_g[:idx_k]
            if np.isin(img_k_temp, idx_select).mean() > ratio_veg:
                img_k = (np.isin(img_k_temp, idx_select))*1
                break
            else:
                idx_k += 1
        self.field.img_bin = denoise(img_k, n_denoise=2)
    def put_anchors(self, n_denoise=60, n_smooth=100, tol=3, debug=None):
        '''
        '''
        print("<Assigning Plots>")
        img = self.field.img_bin.copy()
        map = self.field.map
        img = denoise(img, n_denoise=n_denoise)
        # img = debound(img, n_debound=n_debound)
        self.field.img_bin_sm = img
        pks_row, mean_h = get_peak(img=img, map=map, n_smooth=n_smooth, axis=0)
        pks_col, mean_v = get_peak(img=img, map=map, n_smooth=n_smooth, axis=1)
        self.field.set_pre_anchors(pks_row, pks_col)
        self.field.set_adj_anchors(tol=tol)
        if debug!=None:
            plt.subplot(211),plt.plot(mean_h),plt.plot(pks_row, mean_h[pks_row], "x")
            plt.subplot(212),plt.plot(mean_v),plt.plot(pks_col, mean_v[pks_col], "x")
            plt.savefig(debug+"_peaks.png", dpi=300)
            plt.close()
    def search_by_agent(self, coef_grid=.2):
        '''
        '''
        print("<Finalizing>")
        # self.field.cpu_pre_dim(tol=tol)
        self.field.cpu_bound(coef_grid=coef_grid)
    def get_plots(self, path_out, raw=True, kmeans=True, anchors=True, seg=True):
        if raw:
            plt.figure()
            plt.imshow(self.field.img_std[:,:,:3])
            plt.savefig(path_out+"_raw.png", dpi=300)
            plt.close()
        if kmeans:
            plt.figure()
            plt.imshow(self.field.img_bin)
            plt.savefig(path_out+"_kmean.png", dpi=300)
            plt.close()
        if anchors:
            plt.figure()
            x=[]
            y=[]
            for row in range(self.field.nrow):
                for col in range(self.field.ncol):
                    agent_tp = self.field.get_agent(row, col)
                    pt = agent_tp.get_coordinate()
                    x.append(pt[1])
                    y.append(pt[0])
            plt.plot(x, y, "x", ms=2)
            plt.imshow(self.field.img_bin_sm)
            plt.savefig(path_out+"_anchor.png", dpi=300)
            plt.close()
        if seg:
            plt.figure()
            currentAxis = plt.gca()
            for row in range(self.field.nrow):
                for col in range(self.field.ncol):
                    agent = self.field.get_agent(row, col)
                    east = agent.get_border(Dir.EAST)
                    west = agent.get_border(Dir.WEST)
                    north = agent.get_border(Dir.NORTH)
                    south = agent.get_border(Dir.SOUTH)
                    rec = Rectangle((west, north), east-west, south-north, fill=None, linewidth=.3, color="red")
                    currentAxis.add_patch(rec)
            img_bin = self.field.img_bin
            img_bin = img_bin.reshape(img_bin.shape[0], img_bin.shape[1], 1)
            img_seg = np.multiply(self.field.img_std[:,:,:3], img_bin)
            img_seg[(img_seg.mean(axis=2)==0), :] = 1
            plt.imshow(img_seg)
            plt.savefig(path_out+"_seg.png", dpi=300)
            plt.close()
    def get_DF(self):
        return self.field.get_DF()
    def get_index(self, ch_1, ch_2):
        return self.field.get_index(ch_1, ch_2)


def read_tiff(filename, bands=None, xBSize=5000, yBSize=5000):
    ds = gdal.Open(filename)
    gdal.UseExceptions()
    nrow = ds.RasterYSize
    ncol = ds.RasterXSize
    if bands==None:
        bands = range(ds.RasterCount)
    data = np.zeros((nrow, ncol, len(bands)))
    for b in bands:
        band = ds.GetRasterBand(b+1)
        print("Channel %d"%(b))
        for i in tqdm(range(0, nrow, yBSize)):
            if i + yBSize < nrow:
                numRows = yBSize
            else:
                numRows = nrow - i
            for j in range(0, ncol, xBSize):
                if j + xBSize < ncol:
                    numCols = xBSize
                else:
                    numCols = ncol - j
                data[i:(i+numRows), j:(j+numCols), b] = band.ReadAsArray(j, i, numCols, numRows)
    # data = (data - data.min(axis=(0,1)))/(data.max(axis=(0,1))-data.min(axis=(0,1)))
    return data.astype(np.uint8)

def print_two_img(img1, img2, outname=None):
    '''
    '''
    plt.subplot(211)
    plt.imshow(img1)
    plt.subplot(212)
    plt.imshow(img2)
    if outname==None:
        plt.show()
    else:
        plt.savefig(outname+".png", dpi=300)
def conlv2d(img, kernel, sigmoid=True):
    '''
    '''
    img_out = convolve2d(img, kernel, mode='same')
    img_std = (img_out-img_out.min(axis=(0, 1)))/(img_out.max(axis=(0, 1))-img_out.min(axis=(0, 1)))
    img_std2 = img_std.copy()
    if sigmoid:
        img_std2[img_std>.5] = 1
        img_std2[img_std<=.5] = 0
        return img_std2.astype(np.int)
    else:
        return img_std2
def denoise(img, n_denoise=1):
    '''
    '''
    k_blur = np.array((
        [1, 4, 1],\
        [4, 9, 4],\
        [1, 4, 1]), dtype='int')/29
    img_conv = conlv2d(img, k_blur, sigmoid=False)
    print("<Smoothing the Image>")
    for i in tqdm(range(n_denoise-1)):
        img_conv = conlv2d(img_conv, k_blur, sigmoid=False)
    img_conv[img_conv>0.5] = 1
    img_conv[img_conv<=0.5] = 0
    return img_conv
def debound(img, n_debound=1):
    '''
    '''
    k_edge = np.array((\
        [-1, -1, -1],\
        [-1, 8, -1],\
        [-1, -1, -1]), dtype='int')
    for i in range(n_debound):
        edge = conlv2d(img, k_edge)
        img -= edge
        img[img<0] = 0
    return img
def get_peak(img, map, n_smooth=100, axis=0):
    '''
    '''
    # compute signal
    ls_mean = img.mean(axis=(not axis)*1) # 0:nrow
    # gaussian smooth signal
    for i in range(n_smooth):
        ls_mean = np.convolve(np.array([1, 2, 4, 2, 1])/10, ls_mean, mode='same')
    # find the peaks
    # interval = round(img.shape[axis]/(map.shape[axis]*2+img.shape[axis]*.01))
    peaks, _ = find_peaks(ls_mean)
    # eliminate reduncdent peaks
    while len(peaks) > map.shape[axis]:
        # if len(np.where(ls_mean[peaks]<.5)[0]):
        #     idx_kick = np.where(ls_mean[peaks]<.5)[0][0]
        # else:
        ls_diff = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
        idx_diff = np.argmin(ls_diff)
        idx_kick = idx_diff if (ls_mean[peaks[idx_diff]] < ls_mean[peaks[idx_diff+1]]) else (idx_diff+1)
        peaks = np.delete(peaks, idx_kick)
    # peaks += n_smooth*2
    return peaks, ls_mean
def get_adj(img, field, axis=0):
    # axis = 0 # row: adj toward right or left
    axis_rev = (not axis)*1
    #
    # axs1 = 0
    # axs2 = 1
    dir1 = Dir(1-axis) # axis:0, return W and E
    dir2 = Dir((1-axis)+2) # axis:1, return N and S
    adj_axis = []
    for axs1 in range(field.map.shape[axis]):
        adj_temp = []
        if axis:
            pt_1d = field.get_agent(0, axs1).get_coordinate()[axis]
        else:
            pt_1d = field.get_agent(axs1, 0).get_coordinate()[axis]
        img_1d = img[:,pt_1d] if axis else img[pt_1d,:]
        for axs2 in range(1, field.map.shape[axis_rev]-1):
            # determine axis direction
            idx_row = axs2 if axis else axs1
            idx_col = axs1 if axis else axs2
            # extract agents
            agent_self = field.get_agent(idx_row, idx_col)
            agent_neig1 = field.get_agent_neighbor(idx_row, idx_col, dir1)
            agent_neig2 = field.get_agent_neighbor(idx_row, idx_col, dir2)
            # calculate coordinate and boundary
            pt_self = agent_self.get_coordinate()[axis_rev]
            pt_neig1 = agent_neig1.get_coordinate()[axis_rev]
            pt_neig2 = agent_neig2.get_coordinate()[axis_rev]
            pt_mid = int((pt_neig1+pt_neig2)/2)
            pt_bd1 = int((pt_neig1+pt_mid)/2)
            pt_bd2 = int((pt_neig2+pt_mid)/2)
            # negtive side
            score_1 = 0
            pt_temp = pt_self-1
            while img_1d[pt_temp]:
                pt_temp -= 1
                score_1 += 1
            score_1 = min(score_1, pt_self-pt_bd1)
            # postive side
            score_2 = 0
            pt_temp = pt_self+1
            while img_1d[pt_temp]:
                pt_temp += 1
                score_2 += 1
            score_2 = min(score_2, pt_bd2-pt_self)
            # get final score
            adj_temp.append(score_2 - score_1)
        adj_axis.append(int(np.array(adj_temp).mean()))
    return adj_axis
