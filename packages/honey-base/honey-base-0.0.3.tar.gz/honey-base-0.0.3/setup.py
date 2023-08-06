#coding:utf8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="honey-base",
    version="0.0.3",
    author="geekbruce",
    author_email="bruce.shaoheng@mgail.com",

    description="it's a useful common toolkit for pythoner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",

    # 启用清单文件MANIFEST.in
    include_package_data=True,
    exclude_package_data={'':['.gitignore','*.sh',".pypirc"]},
    packages=setuptools.find_packages(),

    # 需要安装的依赖
    install_requires=[
        'setuptools>=16.0',
    ],

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3"
    ],

    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
