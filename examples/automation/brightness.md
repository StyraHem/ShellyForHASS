```yaml
- alias: 'Trig on brightness and change to full if above 140 (55%)'
  trigger:
    - platform: numeric_state
      entity_id: light.shelly_shdm_1_xxxxxxx
      value_template: '{{ state.attributes.brightness }}'
      above: 140
  action:
    - service: light.turn_on
      data:
        entity_id: light.shelly_shdm_1_xxxxxx
        brightness: "255"
```
