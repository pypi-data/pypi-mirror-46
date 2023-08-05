# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keras_nalu', 'keras_nalu.pretrained']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.2,<3.0']

setup_kwargs = {
    'name': 'keras-nalu',
    'version': '1.3.0',
    'description': 'Keras implementation of a NALU layer',
    'long_description': "# Keras NALU (Neural Arithmetic Logic Units)\n\n[![CircleCI](https://circleci.com/gh/genesant/keras-nalu/tree/master.svg?style=shield)](https://circleci.com/gh/genesant/keras-nalu/tree/master)\n\nKeras implementation of a NALU layer (Neural Arithmetic Logic Units).\nSee: https://arxiv.org/pdf/1808.00508.pdf.\n\n## Installation\n\n```\npip install keras-nalu\n```\n\n## Usage\n\n```py\nfrom keras.layers import Input\nfrom keras.models import Model\nfrom keras.optimizers import RMSprop\nfrom keras_nalu.nalu import NALU\n\n# Your dataset\nX_test = ... # Interpolation data\nY_test = ... # Interpolation data\n\nX_validation = ... # Extrapolation data (validation)\nY_validation = ... # Extrapolation data (validation)\n\nX_test = ... # Extrapolation data (test)\nY_test = ... # Extrapolation data (test)\n\n# Hyper parameters\nepoch_count = 1000\nlearning_rate = 0.05\nsequence_len = 100\n\ninputs = Input(shape=(sequence_len, ))\nhidden = NALU(units=2)(inputs)\nhidden = NALU(units=2)(hidden)\noutputs = NALU(units=1)(hidden)\n\nmodel = Model(inputs=inputs, outputs=outputs)\nmodel.summary()\nmodel.compile(loss='mse', optimizer=RMSprop(lr=learning_rate))\n\nmodel.fit(\n    batch_size=256,\n    epochs=epoch_count,\n    validation_data=(X_validation, Y_validation),\n    x=X_train,\n    y=Y_train,\n)\n\nextrapolation_loss = model.evaluate(\n    batch_size=256,\n    x=X_test,\n    y=Y_test,\n)\n```\n\n## Options\n\n### cell\n\nCell to use in the NALU layer. May be 'a' (addition/subtraction), 'm' (multiplication/division/power), or None which, will apply a gating function to toggle between 'a' or 'm'.\n\n-   Default: `None`\n-   Type: `?('a' | 'm' | None)`\n\n### e\n\nEpsilon value added to inputs in order to prevent calculating the log of zero.\n\n-   Default: `1e-7`\n-   Type: `?float`\n",
    'author': 'Dennis Torres',
    'author_email': 'djtorres0@gmail.com',
    'url': 'https://github.com/genesant/keras-nalu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
