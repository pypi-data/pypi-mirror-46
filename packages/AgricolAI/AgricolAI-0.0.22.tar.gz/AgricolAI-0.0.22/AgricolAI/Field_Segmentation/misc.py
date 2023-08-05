import io
import urllib.request

def get_demo():
    '''
    '''
    path_map = "http://www.zzlab.net/James_Demo/seg_map.csv"
    path_img = "http://www.zzlab.net/James_Demo/seg_img.jpg"
    map = pd.read_csv(path_map, header=None)
    with urllib.request.urlopen(path_img) as url:
        file = io.BytesIO(url.read())
        img = np.array(Image.open(file))
    return img, map
