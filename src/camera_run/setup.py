from setuptools import find_packages, setup

package_name = 'camera_run'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='samet',
    maintainer_email='sametd@hotmail.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "intel_pub = camera_run.intel_pub:main",
            "intel_sub = camera_run.intel_sub:main"
        ],
    },
)
