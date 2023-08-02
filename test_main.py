# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:10:24 2023

@author: Paul
"""

import pytest
import main

def test_request_prediction():
    URL = "https://credi-predic-490718cd231c.herokuapp.com/predict"
    result = main.request_prediction(URL, {'customer': str(456248)})
    assert(result.status_code==200)