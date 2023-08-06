# tap-annie

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).


## Quick Start

1. This tap is written in python and works perfectly on Python 3.6. Make sure Python 3.6 is installed in your system.

2. Install

    It is highly recommended to use a virtualenv to isolate the process without interaction with other python modules.
    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    ```
    ```bash
    > pip install singer-python
    > pip install tap-annie
    ```
### Install the tap

  This tap is able to run in conjunction with a specific Singer target by piping the processes. 
       
1. Configure tap-viafoura
 
    Now, let's create a `config_tap_viafoura.json` in your working directory, following [sample_config.json](sample_config.json). Tap-Auth0 requires three keys `client_id`, `client_secret` and `include_initial_data`
    
     - `ios_account_id` - The account connection id that is integrated with iOS.
     - `android_account_id` - The account connection id that is integrated with Android.
     - `ios_product_id` - The account connection product that is integrated with iOS.
     - `android_product_id` - The account connection product that is integrated with Android.
     - `API_key` - This is your client_secret of Viafoura.
     - `delta_import` - This is your section_uuid of Viafoura.
     - `reload_new_user` - the value of `reload_new_user` will be `true` or `false`. If `true`, it will reload the new users in a few days ago based on `days`
     - `days` - This field determines that you will retrieve new users in how many days ago. 

Note: At the first run, tap-viafoura will create `initial_load.txt` file with value is `True`, after done the first run, the value will be automatically changed to `False`, then the tap-viafoura will take only new users into the stream at the second run.

2. Run

  ```bash
› tap-viafoura -c config_tap_viafoura.json | target-some-api
```

---

Copyright &copy; 2018 Stitch
