Tesults
=======================

Tesults is a test automation results reporting service.  `https://www.tesults.com
<https://www.tesults.com>`_

This API library makes it easier to upload your test results in your python application.

----

---------------
 Installation
---------------

::

    pip install tesults

---------------
 Configuration
---------------

::

    import tesults


---------------
 Documentation
---------------

Documentation is available at `https://www.tesults.com/docs
<https://www.tesults.com/docs>`_.


---------------
 API Overview
---------------

Upload test results using the results method:

::

    tesults.results(data)
    
This call returns a dictionary indicating success or failure along with a reason for failure.

::

    ret = tesults.results(data)
    # ret['success'] is a bool, true if results successfully uploaded, false otherwise
    # ret['message'] is a string, if success is false, check message to see why upload failed

The data param in results is a dictionary containing your test results in the form:

::

    data = {
        'target': 'token',
        'results': {
            'cases': [
                {'name': 'Test 1', 
                 'desc':'Test 1 description.',
                 'suite': 'Suite A',
                 'result': 'pass'
                },
                {'name': 'Test 2', 
                 'desc':'Test 2 description.',
                 'suite': 'Suite A',
                 'result': 'fail',
                 'reason': 'Assert fail in line 203, example.py'
                },
                {'name': 'Test 3', 
                 'desc':'Test 3 description.',
                 'suite': 'Suite B',
                 'result': 'pass'
                }
            ]
        }
    }

The target value, 'token' above should be replaced with your Tesults target token. If you have lost your token you can regenerate one at https://www.tesults.com/config. The cases array should contain your test cases.

---------------
 Support
---------------

support@tesults.com