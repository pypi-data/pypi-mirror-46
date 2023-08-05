from __future__ import absolute_import
from __future__ import print_function
import sys
import os

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from veriloggen import *
import veriloggen.thread as vthread


def mkLed():
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')

    datawidth = 32
    addrwidth = 10
    myram = vthread.RAM(m, 'myram', clk, rst, datawidth, addrwidth)

    read_size = 10
    write_size = read_size

    write_done = m.Reg('write_done', initval=0)
    write_addr = m.Reg('write_addr', addrwidth, initval=0)
    write_data = write_addr
    read_addr = m.Reg('read_addr', addrwidth, initval=0)
    sum = m.Reg('sum', datawidth, initval=0)

    fsm = FSM(m, 'fsm', clk, rst)
    fsm.If(write_done).goto_next()

    # write_rtl
    myram.write_rtl(write_addr, write_data, cond=fsm)
    fsm(
        write_addr.inc()
    )
    fsm(
        Display('wdata =  %d', write_data)
    )
    fsm.If(write_addr == write_size - 1).goto_next()

    # read_rtl
    read_data, read_valid = myram.read_rtl(read_addr, cond=fsm)
    fsm.goto_next()

    fsm(
        read_addr.inc()
    )
    read_data, read_valid = myram.read_rtl(read_addr, cond=fsm)
    fsm.If(read_valid)(
        Display('rdata =  %d', read_data),
        sum.add(read_data)
    )
    fsm.If(read_addr == read_size - 1).goto_next()

    fsm.If(read_valid)(
        Display('rdata =  %d', read_data),
        sum.add(read_data)
    )
    fsm.goto_next()

    fsm.If(read_valid)(
        Display('rdata =  %d', read_data),
        sum.add(read_data)
    )
    fsm.goto_next()

    fsm(
        Display('sum =  %d', sum)
    )
    fsm.goto_next()

    def blink(times):
        write_done.value = 0
        for i in range(times):
            wdata = i + 100
            myram.write(i, wdata)
            print('wdata = %d' % wdata)
        write_done.value = 1

    th = vthread.Thread(m, 'th_blink', clk, rst, blink)
    fsm = th.start(read_size)

    return m


def mkTest():
    m = Module('test')

    # target instance
    led = mkLed()

    # copy paras and ports
    params = m.copy_params(led)
    ports = m.copy_sim_ports(led)

    clk = ports['CLK']
    rst = ports['RST']

    uut = m.Instance(led, 'uut',
                     params=m.connect_params(led),
                     ports=m.connect_ports(led))

    simulation.setup_waveform(m, uut)
    simulation.setup_clock(m, clk, hperiod=5)
    init = simulation.setup_reset(m, rst, m.make_reset(), period=100)

    init.add(
        Delay(10000),
        Systask('finish'),
    )

    return m


if __name__ == '__main__':
    test = mkTest()
    verilog = test.to_verilog('tmp.v')
    print(verilog)

    sim = simulation.Simulator(test)
    rslt = sim.run()
    print(rslt)
