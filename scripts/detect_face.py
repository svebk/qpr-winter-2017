import json
import os
import sys
from PIL import Image

def init(facenet_root, data_dir):
  """
  Initialize face detector.
  :param facenet_root: path to facenet package
  :param data_dir: path to data directory where onet, rnet, pnet networks weights are saved.
  :return: initialized MTCNNFaceDetector object.
  """
  sys.path.append(facenet_root)
  from src.detectors.mtcnn import MTCNNFaceDetector
  conf = dict()
  conf['data_dir'] = data_dir
  mtfd = MTCNNFaceDetector(conf)
  return mtfd

# A common approach for blurriness detection is a thresholding of the variance on the laplacian filtered image
# But how to get the threshold value? Compute statistics on LFW images with/without blur?
# how should we deal with other faces obfuscation? painting, overlay
def blurriness(img):
  from PIL.ImageFilter import Kernel
  from PIL.ImageStat import Stat
  lap = Kernel((3,3), [0, 1, 0, 1, -4, 1, 0, 1,0 ])
  img.copy().filter(lap)
  img_stat = Stat(img)
  return img_stat.var

if __name__ == '__main__':
  """
  Returns the faces detected in the images listed in sys.argv.
  """

  if len(sys.argv) < 5:
    print 'Usage: detect_face.py facenet_root detect_data_dir image_data_dir images_sha1s...'
    sys.exit(1)
  else:
    mtfd = init(facenet_root=sys.argv[1], data_dir=sys.argv[2])


    for image_id in sys.argv[4:]:
      try:
        # read image
        img = Image.open(os.path.join(sys.argv[3],image_id[:3],image_id))
        if len(img.size) == 2:
          rgbimg = Image.new("RGB", img.size)
          rgbimg.paste(img)
          img = rgbimg
        # detect faces
        bboxes = mtfd.detect_faces(img)
        #print bboxes
        # get crops?
        #crops = crop_face_with_margin(img, bounding_boxes)
        # format faces bounding boxes
        out_dict = {}
        dict_bbox = {}
        for i,bbox in enumerate(bboxes):
          face_id = image_id+'_'+'-'.join([str(int(x)) for x in bbox[:4]])
          dict_bbox[face_id] = {}
          dict_bbox[face_id]['bbox'] = ','.join([str(x) for x in bbox[:4]])
          dict_bbox[face_id]['score'] = str(bbox[4])
        out_dict[image_id] = dict_bbox
        print json.dumps(out_dict)
      except Exception as e:
        # axes don't match arrary?
        pass
        #print str(e)
        #sys.exit(5)
