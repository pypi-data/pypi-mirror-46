
Developer install
=================


To install a developer version of floatview, you will first need to clone
the repository::

    git clone https://github.com/denphi/jupyterlab-floatview
    cd floatview

Next, install it with a develop install using pip::

    python3 setup.py sdist bdist_wheel --universal
	twine register dist/floatview-0.1.11.tar.gz -r <- not needed anymore
	twine upload dist/* -r testpypi <- only needed for testing
    twine upload dist/*
    npm publish --access=public .
    

Install the JupyterLab extension with::

    jupyter labextension install .


.. links

.. _`appropriate flag`: https://jupyter-notebook.readthedocs.io/en/stable/extending/frontend_extensions.html#installing-and-enabling-extensions
