import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from geometry_msgs.msg import TransformStamped

class PoseListener(Node):
    def __init__(self):
        super().__init__('pose_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.get_robot_pose)

    def get_robot_pose(self):
        try:
            transform: TransformStamped = self.tf_buffer.lookup_transform(
                'map', 'base_footprint', rclpy.time.Time()
            )
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            z = transform.transform.translation.z
            qx = transform.transform.rotation.x
            qy = transform.transform.rotation.y
            qz = transform.transform.rotation.z
            qw = transform.transform.rotation.w

        except Exception as e:
            self.get_logger().warn(f"Transform not available: {str(e)}")

        return [x, y, z, qx, qy, qz, qw]