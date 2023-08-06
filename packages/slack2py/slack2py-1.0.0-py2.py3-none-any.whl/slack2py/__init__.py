"""
Simple Slack notification python package,
currently supports sending notification by webhook.
Next Features:-
1) workspace integration
2) send to multiple channels

"""
import os,sys
name = "Python Slack Notification"
__version__="1.0.0"
# from builtins import input  # Python 3 compatibility


# add to PYTHONPATH, used by Sphinx doc system
sys.path.insert(1, os.path.dirname(__file__))

