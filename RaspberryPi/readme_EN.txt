/*****************************************************************************
* | File      	:   Readme_EN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0 EdwinGH
* | Date        :   2021-12-21
* | Info        :   Here is an English version of the documentation for your quick use.
******************************************************************************/
This file is to help you use this routine.
1. Basic information:
This routine was developed based on Raspberry Pi 3B, and the routines were verified on Raspberry Pi 3B.
This routine was verified using the 12.48inch e-Paper Module.
This example uses an analog SPI.

2. Pin connection:
Pin connections can be viewed in Config.py or config.h, and are repeated here:
OLED              => RPI(BCM)
VCC               -> 3.3
GND               -> GND
EPD_SCK_PIN       -> 11
EPD_MOSI_PIN      -> 10

EPD_M1_CS_PIN     -> 8
EPD_S1_CS_PIN     -> 7
EPD_M2_CS_PIN     -> 17
EPD_S2_CS_PIN     -> 18

EPD_M1S1_DC_PIN   -> 13
EPD_M2S2_DC_PIN   -> 22

EPD_M1S1_RST_PIN  -> 6
EPD_M2S2_RST_PIN  -> 23

EPD_M1_BUSY_PIN   -> 5
EPD_S1_BUSY_PIN   -> 19
EPD_M2_BUSY_PIN   -> 27
EPD_S2_BUSY_PIN   -> 24

3. Basic use:

Python
            This program needs to connect to the network
            Show_EN_Weather.py both show weather programs and need to connect to the network.
            So make sure your Raspberry Pi connects to the Internet before using it:
                Run: sudo python Show_EN_Weather.py help
            Can see help information

Weather
                In the Weather folder, Show_EN_Weather.py uses crawling webpage data to get global weather,
                both through IP address to determine the city.
                https://www.msn.com/en-us/Weather

4. Statement
    This program is provided for educational purposes only and should not be used for any commercial purpose. If there is any infringement, please contact me to delete.
    Http://www.waveshare.net

5. Python program analysis
    Find directory
        Picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
        Libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

    Set the output log level
    logging.basicConfig(level=logging.INFO)
        Log level
        DEBUG details, which are typically of interest when debugging problems. Detailed debug information.
        INFO proves that things work as expected. Key events.
        WARNING indicates that some accident has occurred, or that a problem will occur in the near future (such as 'disk full'). The software is still working.
        ERROR Due to a more serious problem, the software is no longer able to perform some functions. General error message.
        CRITICAL is a serious error indicating that the software is no longer working.
        NOTICE is not an error, but it may need to be processed. Ordinary but important event.
        ALERT needs to be fixed immediately, such as a system database corruption.
        EMERGENCY In case of emergency, the system is not available (for example, the system crashes) and all users are generally notified.
        (You can try changing to logging.basicConfig(level=logging.DEBUG) to see what happened)
