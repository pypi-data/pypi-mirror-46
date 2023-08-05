# -*- coding: utf-8 -*-
from wait_for import wait_for

from widgetastic.widget import View
from widgetastic_patternfly import AboutModal, Button

# Values from testing_page.html modal
modal_id = 'about-modal'
title = 'Widgetastic About Modal'
trademark = 'Widget Trademark and Copyright Information'

ITEMS = {'Field1': 'Field1Value', 'Field2': 'Field2Value', 'Field3': 'Field3Value'}


def test_modal_close(browser):
    """
    Test the about modal, including all methods/properties

    Test against modal defined in testing_page.html
    :param browser: browser fixture
    """
    class TestView(View):
        """ Dummy page matching testing_page.html elements"""
        button = Button('Launch about modal')
        about = AboutModal(id=modal_id)

    view = TestView(browser)
    assert not view.about.is_open

    # Open the modal
    assert view.button.title == 'Launch Modal'
    assert not view.button.disabled
    view.button.click()

    view.flush_widget_cache()
    wait_for(lambda: view.about.is_open, delay=0.1, num_sec=5)

    assert view.about.title == title

    assert view.about.trademark == trademark

    assert view.about.items() == ITEMS

    # close the modal
    view.about.close()
    wait_for(lambda: not view.about.is_open, delay=0.1, num_sec=5)
