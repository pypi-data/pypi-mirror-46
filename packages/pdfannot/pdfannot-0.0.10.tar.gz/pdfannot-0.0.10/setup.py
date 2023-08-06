from setuptools import setup, find_packages
# import pdfannot

setup(name="pdfannot",
      install_requires=['pandas', 'pymupdf', 'xlrd'],
      # version=pdfannot.__version__,
      version = '0.0.10',
      description='PDF Annotation Utils',
      author='Arthur RENAUD ; Antoine MARULLAZ => Stackadoc',
      author_email='arthur.b.renaud@gmail.com',
      url='https://bitbucket.org/ArthurRenaud/pdfannot/0.0.10',
      packages=find_packages(),
      tests_require=["pytest"],
      python_requires='>=3.5',
      setup_requires=["pytest-runner"],
      long_description=open('README.md').read(),

      # Active la prise en compte du fichier MANIFEST.in
      include_package_data=True,
      package_data={'': ['ressources/pdf_annot_3_output.xlsx', 'ressources/pdf_test_annot.pdf',
                         'ressources/pdf_without_annot.pdf',
                         'ressources/pdf_test_annot.pdf-marked', 'ressources/pdf_test_annot_2.pdf',
                         'ressources/pdf_test_annot_2.pdf-marked', 'ressources/pdf_test_annot_2_output.xlsx',
                         'ressources/pdf_test_annot_3.pdf', 'ressources/pdf_test_annot_3.pdf-marked',
                         'ressources/pdf_test_annot_output.xlsx', ]},
      classifiers=[
            "Programming Language :: Python",
            "Development Status :: 1 - Planning",
            "License :: OSI Approved",
            "Natural Language :: French",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Topic :: Communications",
      ],

      )

