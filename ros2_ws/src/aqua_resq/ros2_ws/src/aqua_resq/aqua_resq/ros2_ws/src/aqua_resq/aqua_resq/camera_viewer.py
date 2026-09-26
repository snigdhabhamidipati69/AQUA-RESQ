import time
import json
import os

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from sensor_msgs.msg import Image
from px4_msgs.msg import VehicleGlobalPosition

from cv_bridge import CvBridge
from ultralytics import YOLO

import cv2


JSON_DIR = os.path.expanduser("~/aqua_gazebo_test")
JSON_PATH = os.path.join(JSON_DIR, "latest_detections.json")


class CameraYOLO(Node):

    def __init__(self):
        super().__init__('camera_yolo')

        os.makedirs(JSON_DIR, exist_ok=True)

        self.bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')

        self.current_lat = None
        self.current_lon = None
        self.current_alt = None
        self.position_valid = False

        px4_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        self.position_subscription = self.create_subscription(
            VehicleGlobalPosition,
            '/fmu/out/vehicle_global_position',
            self.position_callback,
            px4_qos
        )

        self.camera_subscription = self.create_subscription(
            Image,
            '/aqua_resq/camera/image',
            self.image_callback,
            10
        )

        self.last_detection_time = 0.0

        self.get_logger().info(
            'AQUA-RESQ YOLO + GPS + Dashboard Started'
        )

    def position_callback(self, msg):

        if msg.lat_lon_valid and msg.alt_valid:
            self.current_lat = msg.lat
            self.current_lon = msg.lon
            self.current_alt = msg.alt
            self.position_valid = True

    def save_detection(self, confidence):

        if not self.position_valid:
            return

        detection = {
            "class": "person",
            "confidence": confidence,
            "priority": "HIGH",
            "source": "UAV_Aerial_Cam",
            "bbox": [],
            "location": {
                "latitude": self.current_lat,
                "longitude": self.current_lon
            }
        }

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(detection, f, indent=2)

    def image_callback(self, msg):

        try:

            frame = self.bridge.imgmsg_to_cv2(
                msg,
                'bgr8'
            )

            results = self.model(
                frame,
                verbose=False
            )

            for box in results[0].boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                if class_id == 0:

                    current_time = time.time()

                    if current_time - self.last_detection_time >= 1.0:

                        print()
                        print("================================")
                        print("PERSON DETECTED")
                        print(f"Confidence: {confidence:.2%}")

                        if self.position_valid:

                            print("UAV POSITION")
                            print(f"Latitude : {self.current_lat:.6f}")
                            print(f"Longitude: {self.current_lon:.6f}")
                            print(f"Altitude : {self.current_alt:.2f} m")

                            self.save_detection(confidence)

                            print("✅ Detection saved for dashboard")

                        else:
                            print("UAV POSITION: unavailable")

                        print("================================")
                        print()

                        self.last_detection_time = current_time

            annotated_frame = results[0].plot()

            cv2.imshow(
                'AQUA-RESQ - YOLO Detection',
                annotated_frame
            )

            cv2.waitKey(1)

        except Exception as e:

            self.get_logger().error(
                f'Error: {e}'
            )


def main():

    rclpy.init()

    node = CameraYOLO()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
