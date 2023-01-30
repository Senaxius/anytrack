from setuptools import setup

package_name = 'scanner'

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
            "test = scanner.test:main",
            "scanner = scanner.scanner:main",
            "camera_tracker = scanner.camera_tracker:main",
            "camera_info = scanner.camera_info:main",
            "camera_position = scanner.camera_position:main",
            "camera_vector = scanner.camera_vector:main",
            "foxglove_camera = scanner.foxglove_camera:main",
        ],
    },
)
