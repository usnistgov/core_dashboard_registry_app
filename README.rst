Core Dashboard Registry App
===========================

Resource management via a dashboard for the registry core project.

Quickstart
==========

1. Add "core_dashboard_registry_app" to your INSTALLED_APPS setting
-------------------------------------------------------------------

.. code:: python

      INSTALLED_APPS = [
          ...
          'core_dashboard_registry_app',
      ]

2. Include the core_dashboard_registry_app URLconf in your project urls.py
--------------------------------------------------------------------------

.. code:: python

      url(r'^dashboard/', include('core_dashboard_registry_app.urls')),
