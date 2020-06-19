import argparse
import rospy
from autoware_msgs.msg import DetectedObject
from autoware_msgs.msg import DetectedObjectArray
from matlab_msgs.msg import DetectedBoundingBox
from matlab_msgs.msg import DetectedBoundingBoxArray

parser = argparse.ArgumentParser()
parser.add_argument("matlab_topic")
parser.add_argument("autoware_topic")
args = parser.parse_args()

pub = rospy.Publisher(args.autoware_topic, DetectedObjectArray, queue_size=10)

def callback(box_array):
  autoware_array = DetectedObjectArray()
  autoware_array.header = box_array.header
  for box in box_array.boxes:
    autoware_object = DetectedObject()
    autoware_object.header = box.header
    autoware_object.pose = box.pose
    autoware_object.dimensions = box.dimensions
    autoware_array.objects.append(autoware_object)
  pub.publish(autoware_array)


rospy.init_node('matlab_proxy')
rospy.Subscriber(args.matlab_topic, DetectedBoundingBoxArray, callback)
rospy.spin()
