import requests
from pygass import constants as st
from pygass.helper import make_request, global_params


__license__ = "GPL-3"

# https://developers.google.com/analytics/devguides/collection/analyticsjs/enhanced-ecommerce#measuring-transactions
# https://developers.google.com/analytics/devguides/collection/protocol/v1/devguide#enhancedecom
# https://ga-dev-tools.appspot.com/hit-builder/


def track_enhanced_ecommerce_impression(
    client_id,
    page,
    product_id,
    product_name,
    hostname=None,
    title=None,
    **kwargs,
):
    """ Enhanced ecommerce track product impression.

    Parameters
    ----------
    client_id : str
        Anonymous client id
    product_id : str
        Product ID or SKU
    product_name : str
        Product name
    list : str, optional
        List or collection that this product belongs to
    brand : str, optional
        Products  brand
    category : str, optional
        Products category can take multiple seperrated with /
    variant : str, optional
        Variantion of the product different colour capacity
    position : int, optional
        Position inside the list or collection
    price : currency, optional
        Products price

    Returns
    -------
    response
        json response or image response if live url
    """

    st.enhanced_ecommerce_immpression[st.CLIENT_ID_ATTR] = client_id
    st.enhanced_ecommerce_immpression[st.PAGEVIEW_PAGE_ATTR] = page
    st.enhanced_ecommerce_immpression[st.PAGEVIEW_HOSTNAME_ATTR] = hostname
    st.enhanced_ecommerce_immpression[st.PAGEVIEW_TITLE_ATTR] = title
    st.enhanced_ecommerce_immpression[st.ECOMMERCE_ID] = product_id
    st.enhanced_ecommerce_immpression[st.ECOMMERCE_NAME] = product_name
    st.enhanced_ecommerce_immpression[
            st.ECOMMERCE_CATEGORY
        ] = kwargs.get("product_category")

    return make_request(
        params=global_params(st.enhanced_ecommerce_immpression, **kwargs)
    )


def track_enhanced_ecommerce_action(
    client_id,
    category,
    action,
    page,
    product_id,
    product_name,
    product_action,
    hostname=None,
    title=None,
    label=None,
    value=None,
    **kwargs,
):
    """ Enhanced ecommerce track product impression.

    Parameters
    ----------
    category : str
        The events category "video" for example
    action : str, optional
        The action applied "click" for example
    product_id : str
        Product ID or SKU
    product_name : str
        Product name
    product_action : str
        Product action "add" to cart or "click" on product
    hostname : str, optional
    title : str, optional
        The page title human friendly version "Page one"
    label : str, optional
        The events label "holiday" for example
    value : str, optional
        The events value "300" for example

    Returns
    -------
    response
        json response or image response if live url
    """
    st.enhanced_ecommerce_action[st.PAGEVIEW_PAGE_ATTR] = page
    st.enhanced_ecommerce_action[st.PAGEVIEW_HOSTNAME_ATTR] = hostname
    st.enhanced_ecommerce_action[st.PAGEVIEW_TITLE_ATTR] = title

    st.enhanced_ecommerce_action[st.TRANSACTION_ID_ATTR] = kwargs.get('transaction_id')
    st.enhanced_ecommerce_action[st.TRANSACTION_AFFILIATION_ATTR] = kwargs.get('affiliation')
    st.enhanced_ecommerce_action[st.TRANSACTION_REVENUE_ATTR] = kwargs.get('revenue')
    st.enhanced_ecommerce_action[st.TRANSACTION_CURRENCY_CODE_ATTR] = kwargs.get('currency_code')

    st.enhanced_ecommerce_action[st.CLIENT_ID_ATTR] = client_id
    # st.enhanced_ecommerce_action[st.EVENT_CATEGORY_ATTR] = category
    # st.enhanced_ecommerce_action[st.EVENT_ACTION_ATTR] = action
    # st.enhanced_ecommerce_action[st.EVENT_LABEL_ATTR] = label
    # st.enhanced_ecommerce_action[st.EVENT_VALUE_ATTR] = value

    if "product_category" in kwargs:
        st.enhanced_ecommerce_action[
            st.ECOMMERCE_ACTION_PRODUCT_CATEGORY
        ] = kwargs.get("product_category")

    st.enhanced_ecommerce_action[st.ECOMMERCE_ACTION_PRODUCT_ID] = product_id
    st.enhanced_ecommerce_action[
        st.ECOMMERCE_ACTION_PRODUCT_NAME
    ] = product_name
    st.enhanced_ecommerce_action[
        st.ECOMMERCE_ACTION_PRODUCT_ACTION
    ] = product_action

    return make_request(
        params=global_params(st.enhanced_ecommerce_action, **kwargs)
    )


def track_enhanced_ecommerce_product_detail(*args, **kwargs):
    """ See track_enhanced_ecommerce_action for parameters
    Helper just sets the product action"""
    kwargs['product_action'] = 'detail'
    return track_enhanced_ecommerce_action(*args, **kwargs)


def track_enhanced_ecommerce_product_click(*args, **kwargs):
    """ See track_enhanced_ecommerce_action for parameters
    Helper just sets the product action"""

    kwargs['product_action'] = 'click'
    return track_enhanced_ecommerce_action(*args, **kwargs)


def track_enhanced_ecommerce_add_to_basket(*args, **kwargs):
    """ See track_enhanced_ecommerce_action for parameters
    Helper just sets the product action"""

    kwargs['product_action'] = 'add'
    return track_enhanced_ecommerce_action(*args, **kwargs)


def track_enhanced_ecommerce_checkout(*args, **kwargs):
    """ See track_enhanced_ecommerce_action for parameters
    Helper just sets the product action"""
    kwargs['product_action'] = 'checkout'
    return track_enhanced_ecommerce_action(*args, **kwargs)


def track_enhanced_ecommerce_purchase(*args, **kwargs):
    """ See track_enhanced_ecommerce_action for parameters
    Helper just sets the product action"""
    kwargs['product_action'] = 'purchase'
    return track_enhanced_ecommerce_action(*args, **kwargs)
