from pacemakers import Pacemakers

def test_normal_VOO():
    pacemaker = Pacemakers()
    values = {
        "-PM_IN-" : "VOO",
        "-LRL_IN-" : "50",
        "-URL_IN-" : "150",
        "-VA_IN-" : "3.5",
        "-VPW_IN-" : "1.2"
    }
    pacemaker.set_param(values)
    assert pacemaker.get_param() == {
        '-PM-': 'VOO', 
        '-LRL-': '50', 
        '-URL-': '150', 
        '-AA-': None, 
        '-VA-': '3.5', 
        '-APW-': None,
        '-VPW-': '1.2', 
        '-ARP-': None, 
        '-VRP-': None
    }

def test_normal_AAI():
    pacemaker = Pacemakers()
    values = {
        "-PM_IN-" : "AAI",
        "-LRL_IN-" : "60",
        "-URL_IN-" : "160",
        "-AA_IN-" : "3.5",
        "-APW_IN-" : "1.2",
        "-ARP_IN-" : "150"
    }
    pacemaker.set_param(values)
    assert pacemaker.get_param() == {
        '-PM-': 'AAI', 
        '-LRL-': '60', 
        '-URL-': '160', 
        '-AA-': '3.5', 
        '-VA-': None, 
        '-APW-': '1.2',
        '-VPW-': None, 
        '-ARP-': '150', 
        '-VRP-': None
    }

def test_normal_with_extra_AAI():
    pacemaker = Pacemakers()
    values = {
        "-PM_IN-" : "AAI",
        "-LRL_IN-" : "80",
        "-URL_IN-" : "175",
        "-AA_IN-" : "4.0",
        "-APW_IN-" : "1.5",
        "-ARP_IN-" : "150",
        "-VA_IN-" : "3.5",
        "-VRP-" : "160"
    }
    pacemaker.set_param(values)
    assert pacemaker.get_param() == {
        '-PM-': 'AAI', 
        '-LRL-': '80', 
        '-URL-': '175', 
        '-AA-': '4.0', 
        '-VA-': None, 
        '-APW-': '1.5',
        '-VPW-': None, 
        '-ARP-': '150', 
        '-VRP-': None
    }

def test_wrong_empty_AAI():
    pacemaker = Pacemakers()
    values = {
        "-PM_IN-" : None,
        "-LRL_IN-" : "60",
        "-URL_IN-" : "160",
        "-AA_IN-" : "3.6",
        "-APW_IN-" : "1.2",
        "-ARP_IN-" : "150"
    }
    assert pacemaker.set_param(values) == False

def test_wrong_limit_AAI():
    pacemaker = Pacemakers()
    values = {
        "-PM_IN-" : "AAI",
        "-LRL_IN-" : "160",
        "-URL_IN-" : "60",
        "-AA_IN-" : "3.5",
        "-APW_IN-" : "1.2",
        "-ARP_IN-" : "150"
    }
    assert pacemaker.set_param(values) == False

def test_wrong_range_AAI():
    pacemaker = Pacemakers()
    values = {
        "-PM_IN-" : "AAI",
        "-LRL_IN-" : "60",
        "-URL_IN-" : "160",
        "-AA_IN-" : "3.6",
        "-APW_IN-" : "1.2",
        "-ARP_IN-" : "150"
    }
    assert pacemaker.set_param(values) == False

