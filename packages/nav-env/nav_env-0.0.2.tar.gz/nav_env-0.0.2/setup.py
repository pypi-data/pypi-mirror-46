import setuptools
from lgblkb_tools.global_support import ConfigReader
from lgblkb_tools.log_support import create_logger,with_logging
from lgblkb_tools.folder_utils import Folder
import ruamel.yaml as raml
from setuptools import setup

simple_logger=create_logger('setup_logs')

with open("README.md","r") as fh:
	long_description=fh.read()

install_requires=[
	'gym',
	'lgblkb-tools',
	]

def get_update_version(info_filepath):
	# yaml.dump(dict(version='0.0.8'),open(info_filepath,'w'))
	info_data=ConfigReader(info_filepath)
	current_version=[int(x) for x in info_data.version.obj.split('.')]
	current_version[-1]+=1
	info_data['version']='.'.join(map(str,current_version))
	return info_data

@simple_logger.with_logging()
def setup(version):
	setuptools.setup(
		name="nav_env",
		version=version,
		author="Dias Bakhtiyarov",
		author_email="dbakhtiyarov@nu.edu.kz",
		description="nav_env",
		long_description='long_description',
		long_description_content_type="text/markdown",
		# url="https://bitbucket.org/lgblkb/lgblkb_tools",
		packages=setuptools.find_packages(),
		classifiers=(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
			),
		install_requires=install_requires
		)

# setup(name='nav_env',
#       version='0.0.1',
#       install_requires=[
# 	      'gym',
# 	      'lgblkb-tools',
# 	      ]  # And any other dependencies foo needs
#       )

def main():
	base_dir=Folder(__file__)
	build_dir=base_dir.create('build')
	dist_dir=base_dir.create('dist')
	info_filepath=base_dir.get_filepath('package_info.yaml')
	info_data=get_update_version(info_filepath)
	simple_logger.info('New version: %s',info_data.version.obj)
	build_dir.delete()
	dist_dir.delete()
	setup(info_data.version.obj)
	info_data.update()
	pass

if __name__=='__main__':
	main()
