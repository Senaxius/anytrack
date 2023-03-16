from setuptools import setup

package_name = 'scannerV2'

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
            "manager = scannerV2.manager:main",
            "tracker2D = scannerV2.tracker2D:main",
            "camera_info = scannerV2.camera_info:main",
            "camera_vector = scannerV2.camera_vector:main",
            "position_manager = scannerV2.position_manager:main",
            "test = scannerV2.test:main",
        ],
    },
)
