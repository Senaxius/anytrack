from setuptools import setup

package_name = 'anytrack'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='alexander.minor004@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "manager = anytrack.manager:main",
            "camera_detector = anytrack.camera_detector:main",
            "camera_driver = anytrack.camera_driver:main",
            "camera_info = anytrack.camera_info:main",
            "camera_vector = anytrack.camera_vector:main",
            "position_manager = anytrack.position_manager:main",
            "calibration = anytrack.calibration:main",
            "test = anytrack.test:main",
            "simulation_publisher = anytrack.simulation_publisher:main",
            "pointcloud_publisher = anytrack.pointcloud_publisher:main",
            "optical_flow = anytrack.optical_flow:main",
        ],
    },
)
