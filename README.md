# OS X HW Monitoring scripts

A collections of scripts for OS X that can be used to monitor sensors and stats in OS X. The stats can be used to collect data for Cacti/Zabbix etc.

The script makes use of two binaries to read the SMC. These are automatically fetched by the boostrap.py script.

## Requirements

Tested on Mac OS X 10.8 and Python 2.7.2

## Usage

To use, simply clone the repository and run the bootstrap script to download binary dependencies:

    git clone git@github.com:eripa/osx_monitoring.git
    cd osx_monitoring
    pip install -r requirements.txt
    ./bootstrap.py

Then run the individual scripts, example:

    $ ./temps.py
    gpu_diode:55 left_palm_rest:33 cpu_a_proximity:52 battery:34 battery_position_2:34 battery_position_3:33 main_heat_sink_2:53 gpu_1_chip:54 ssd_bay:40 platform_controller_hub:52 main_logic_board:40 main_heat_sink_3:51 cpu_a_diode:59

# Credits

 * ["tempmonitor" CLI binary from TemperatureMonitor](http://www.bresink.de/osx/0TemperatureMonitor/details.html)
 * ["smc" CLI binary from smcFanControl 2](http://81.169.182.62/~eidac/software/smcfancontrol2/index.html)

# License

 This script is delivered "as is" and is [unlicensed](http://unlicense.org).