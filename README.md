Known issues 

socket stops working after BrokenPipeError

Installation

Using the tool of choice open the directory (folder) for your HA configuration (where you find configuration.yaml).
If you do not have a custom_components directory (folder) there, you need to create it.
In the custom_components directory (folder) create a new folder called kincony-sha.
Download all the files from the `custom_components/kincony-sha/` directory (folder) in this repository.
Place the files you downloaded in the new directory (folder) you created.

Add to `configuration.yaml`

```
switch:
  - platform: kincony-sha
    switches:
        ls_1:
            k_id: 1
            friendly_name: LS 1
        ls_2:
            k_id: 2
            friendly_name: LS 2
        ls_3:
            k_id: 3
            friendly_name: LS 3
        ls_4:
            k_id: 4
            friendly_name: LS 4
        ls_5:
            k_id: 5
            friendly_name: LS 5
        ls_6:
            k_id: 6
            friendly_name: LS 6
        ls_7:
            k_id: 7
            friendly_name: LS 7
        ls_8:
            k_id: 8
            friendly_name: LS 8
        ls_9:
            k_id: 9
            friendly_name: LS 9
        ls_10:
            k_id: 10
            friendly_name: LS 10
        ls_11:
            k_id: 11
            friendly_name: LS 11
        ls_12:
            k_id: 12
            friendly_name: LS 12
        ls_13:
            k_id: 13
            friendly_name: LS 13
        ls_14:
            k_id: 14
            friendly_name: LS 14
        ls_15:
            k_id: 15
            friendly_name: LS 15
        ls_16:
            k_id: 16
            friendly_name: LS 16
        ls_17:
            k_id: 17
            friendly_name: LS 17
        ls_18:
            k_id: 18
            friendly_name: LS 18
        ls_19:
            k_id: 19
            friendly_name: LS 19
        ls_20:
            k_id: 20
            friendly_name: LS 20
        ls_21:
            k_id: 21
            friendly_name: LS 21
        ls_22:
            k_id: 22
            friendly_name: LS 22
        ls_23:
            k_id: 23
            friendly_name: LS 23
        ls_24:
            k_id: 24
            friendly_name: LS 24
        ls_25:
            k_id: 25
            friendly_name: LS 25
        ls_26:
            k_id: 26
            friendly_name: LS 26
        ls_27:
            k_id: 27
            friendly_name: LS 27
        ls_28:
            k_id: 28
            friendly_name: LS 28
        ls_29:
            k_id: 29
            friendly_name: LS 29
        ls_30:
            k_id: 30
            friendly_name: LS 30
        ls_31:
            k_id: 31
            friendly_name: LS 31
        ls_32:
            k_id: 32
            friendly_name: LS 32
```


Restart Home Assistant
