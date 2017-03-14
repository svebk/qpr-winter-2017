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


if __name__ == '__main__':
  """
  Returns the faces detected in the images listed in sys.argv.
  """

  if len(sys.argv) < 5:
    print 'Usage: detect_face.py facenet_root detect_data_dir image_data_dir images_sha1s...'
    sys.exit(1)
  else:
    mtfd = init(facenet_root=sys.argv[1], data_dir=sys.argv[2])

    try:
      for image_id in sys.argv[4:]:
        # read image
        img = Image.open(os.path.join(sys.argv[3],image_id[:3],image_id))
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
      print str(e)
      sys.exit(5)
