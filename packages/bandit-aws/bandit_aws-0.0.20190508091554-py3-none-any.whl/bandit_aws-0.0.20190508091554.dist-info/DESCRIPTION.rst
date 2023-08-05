==========
bandit-aws
==========

This is a `Bandit <https://pypi.org/project/bandit/>`_ plugin to scan for
strings in your source code that look like AWS keys.

Usage
-----

Bandit plugins are automatically activated once they are installed. To use this
plugin, you simply need to install the plugin::

    $ pip install bandit-aws

To verify the installation, display the bandit help text::

    $ bandit --help

It will display a list of tests that were discovered and loaded. Verify that
you see "C100 - hardcoded_aws_key" in the list.

You can then run bandit in the normal way. For example::

    $ bandit -r myproject/

If any strings that look like AWS keys are found, they will be reported::

    >> Issue: [C100:hardcoded_aws_key] Possible hardcoded AWS secret access key: 'JalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY'
       Severity: Medium   Confidence: Medium
       Location: myproject/example.py:11
       More Info: https://bandit.readthedocs.io/en/latest/plugins/c100_hardcoded_aws_key.html
    10	AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
    11	AWS_SECRET_ACCESS_KEY = "JalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY"
    12
    13
    14	class MyClass:



