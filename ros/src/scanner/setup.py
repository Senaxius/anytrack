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
            "test_vec_publisher = scanner.test_vec_publisher:main",
            "tf_broadcaster = scanner.tf_broadcaster:main",
            "ball_scanner = scanner.ball_scanner:main",
            "camera_publisher = scanner.camera_publisher:main",
            "camera_info_publisher = scanner.camera_info_publisher:main",
        ],
    },
)
