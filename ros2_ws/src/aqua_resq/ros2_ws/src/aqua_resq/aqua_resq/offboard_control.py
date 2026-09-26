import rclpy
from rclpy.node import Node

from px4_msgs.msg import (
    OffboardControlMode,
    TrajectorySetpoint,
    VehicleCommand,
)


class OffboardControl(Node):

    def __init__(self):
        super().__init__('offboard_control')

        self.offboard_control_mode_publisher = self.create_publisher(
            OffboardControlMode,
            '/fmu/in/offboard_control_mode',
            10
        )

        self.trajectory_setpoint_publisher = self.create_publisher(
            TrajectorySetpoint,
            '/fmu/in/trajectory_setpoint',
            10
        )

        self.vehicle_command_publisher = self.create_publisher(
            VehicleCommand,
            '/fmu/in/vehicle_command',
            10
        )

        self.counter = 0

        self.timer = self.create_timer(
            0.1,
            self.timer_callback
        )

    def publish_offboard_control_mode(self):

        msg = OffboardControlMode()

        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False

        msg.timestamp = self.get_clock().now().nanoseconds // 1000

        self.offboard_control_mode_publisher.publish(msg)

    def publish_position(self, x, y, z):

        msg = TrajectorySetpoint()

        msg.position = [
            float(x),
            float(y),
            float(z)
        ]

        msg.yaw = 0.0

        msg.timestamp = self.get_clock().now().nanoseconds // 1000

        self.trajectory_setpoint_publisher.publish(msg)

    def publish_vehicle_command(
        self,
        command,
        param1=0.0,
        param2=0.0
    ):

        msg = VehicleCommand()

        msg.command = command
        msg.param1 = param1
        msg.param2 = param2

        msg.target_system = 1
        msg.target_component = 1

        msg.source_system = 1
        msg.source_component = 1

        msg.from_external = True

        msg.timestamp = self.get_clock().now().nanoseconds // 1000

        self.vehicle_command_publisher.publish(msg)

    def timer_callback(self):

        self.publish_offboard_control_mode()

        # ----------------------------------------------
        # TAKEOFF SETPOINT
        # ----------------------------------------------

        if self.counter < 30:

            self.publish_position(
                0.0,
                0.0,
                -3.0
            )

        # ----------------------------------------------
        # SWITCH TO OFFBOARD
        # ----------------------------------------------

        elif self.counter == 30:

            self.get_logger().info(
                'Switching to OFFBOARD mode'
            )

            self.publish_vehicle_command(
                VehicleCommand.VEHICLE_CMD_DO_SET_MODE,
                1.0,
                6.0
            )

        # ----------------------------------------------
        # ARM
        # ----------------------------------------------

        elif self.counter == 40:

            self.get_logger().info(
                'Arming UAV'
            )

            self.publish_vehicle_command(
                VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM,
                1.0
            )

        # ----------------------------------------------
        # HOVER AT 3 METRES
        # ----------------------------------------------

        else:

            self.publish_position(
                0.0,
                0.0,
                -3.0
            )

        self.counter += 1


def main(args=None):

    rclpy.init(args=args)

    node = OffboardControl()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
