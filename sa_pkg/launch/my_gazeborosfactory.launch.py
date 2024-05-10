import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    #urdf = get_package_share_directory('my_robot_description') + '/urdf/simple_robot.urdf'
    
    # urdf = os.path.join(get_package_share_directory('my_pkg') , 'urdf','my_robot.urdf.xacro')
    # print("-----------------URDF file path:---=================================", urdf)  # Print the URDF file path
    #Environment Variable
    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(get_package_prefix("sa_pkg"), "share")

    start_gazebo_server_cmd = ExecuteProcess(
       cmd=[
            'gzserver',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            
        ],        
        output='screen',
    )
    start_gazebo_client_cmd = ExecuteProcess(
        cmd=[
            'gzclient',
            '-s',
            'libgazebo_ros_init.so',
            '-s',
            'libgazebo_ros_factory.so',
            
        ],
        output='screen',
       # arguments=[os.path.join(get_package_prefix("my_robot_bringup"), "share","my_world.world")],
    )
    joint_trajectory_arm_controller = Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "fr5_arm_controller",
                "--controller-manager", "/controller_manager",
            ]
    )
    joint_trajectory_gripper_controller = Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "fr5_gripper_controller",
                "--controller-manager", "/controller_manager",
            ]
    )
    joint_state_broadcaster = Node(
            package="controller_manager",
            executable="spawner",
            arguments=[
                "joint_state_broadcaster",
                "--controller-manager", "/controller_manager",
            ]
    )
    

    # robot_description = {'robot_description': open(urdf).read()}
    # robot_description = {"command 'xacro $(var urdf)'"}

    #gazebo needs spawn node, server and client(gui) node
    return LaunchDescription([
        # Node(
        #     package='robot_state_publisher',
        #     executable='robot_state_publisher',
        #     name='robot_state_publisher',
        #     output='screen',
        #     parameters=[robot_description],
        # ),
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen',
        #     arguments=['-d',"/home/aksoni/Documents/projects/ros2/rviz_all.rviz"]
        # ),
        start_gazebo_server_cmd,
        start_gazebo_client_cmd,
        joint_trajectory_arm_controller,
        joint_trajectory_gripper_controller,
        joint_state_broadcaster
        # Node(
        #     package='gazebo_ros',
        #     executable='spawn_entity.py',
        #     arguments=['-entity', 'my_robot', '-topic',"robot_description"],
        #     name='spawn_entity',
        #     output='screen',
        # )
        
    ])