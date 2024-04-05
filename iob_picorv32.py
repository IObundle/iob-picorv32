#!/usr/bin/env python3

from iob_core import iob_core


class iob_picorv32(iob_core):
    def __init__(self, *args, **kwargs):
        self.set_default_attribute("version", "0.1")
        self.set_default_attribute("generate_hw", False)

        self.create_conf(
            name='ADDR_W',
            type='P',
            val='32',
            min='1',
            max='?',
            descr='description here',
        )
        self.create_conf(
            name='DATA_W',
            type='P',
            val='32',
            min='1',
            max='?',
            descr='description here',
        )
        self.create_conf(
            name='USE_COMPRESSED',
            type='P',
            val='1',
            min='0',
            max='1',
            descr='description here',
        )
        self.create_conf(
            name='USE_MUL_DIV',
            type='P',
            val='1',
            min='0',
            max='1',
            descr='description here',
        )
        self.create_conf(
            name='USE_EXTMEM',
            type='P',
            val='0',
            min='0',
            max='1',
            descr='Select if configured for usage with external memory.',
        )

        self.create_port(
            name="clk_rst",
            type="slave",
            port_prefix="",
            wire_prefix="",
            descr="Clock and reset",
            signals=[],
        ),
        self.create_port(
            name='general',
            type="master",
            port_prefix="",
            wire_prefix="",
            descr='General interface signals',
            signals=[
                {
                    'name': "boot",
                    'direction': "input",
                    'width': '1',
                    'descr': "CPU boot input"
                },
                {
                    'name': "trap",
                    'direction': "output",
                    'width': '1',
                    'descr': "CPU trap output"
                },
            ]
        ),
        self.create_port(
            name='instruction_bus',
            type="master",
            port_prefix="",
            wire_prefix="",
            descr='Instruction bus',
            signals=[
                {
                    'name': "ibus_req",
                    'direction': "output",
                    'width': '`REQ_W',
                    'descr': "Instruction bus request"},
                {
                    'name': "ibus_resp",
                    'direction': "input",
                    'width': '`RESP_W',
                    'descr': "Instruction bus response"
                },
            ]
        ),
        self.create_port(
            name='data_bus',
            type="master",
            port_prefix="",
            wire_prefix="",
            descr='Data bus',
            signals=[
                {
                    'name': "dbus_req",
                    'direction': "output",
                    'width': '`REQ_W',
                    'descr': "Data bus request"
                },
                {
                    'name': "dbus_resp",
                    'direction': "input",
                    'width': '`RESP_W',
                    'descr': "Data bus response"
                },
            ]
        )

        self.create_instance(
            "iob_reg",
            "iob_reg_inst",
        )

        self.create_instance(
            "iob_edge_detect",
            "iob_edge_detect_inst",
        )

        super().__init__(*args, **kwargs)
