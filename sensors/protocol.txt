MAC format
    0xAABBBBCCCC
        AA - prefix
        BBBB - source address
        CCCC - destination address
Address format
    0xAABB
        AA - device level (01 - root server )
        BB - No of device on this level
Packet format
    Total packet size 32 bytes (hardware limit)
    AAAABCCdata
        AAAA - destination address (needed for relay between levels)
        B - flags
        CC - command
        data - variable length payload

    Flags are:
        B & 1 = 1 : end of message
        other - future use

    Commands are:
        0 : in request from server - request device capabilities. In response from device - 2 bytes of capabilities in payload.
            Capabilities are:
                1 - Thermal sensor;
                2 - LCD display
                4 - Alarm capabilities
                8 - boiler relay
                16 - buzzer
                32... - future use
        1 : in request - thermostat request; in payload 1 byte fix value. In response - thermostat data in payload ( 2 bytes signed integer )
        2 : in request - LCD content update; payload is:
            LLdata
                LL - row number
                data - string to display
        3 : in request from server: set boiler relay; in payload relay status to set ( 1 - turn off, 0 - turn on ). In response payload: LHR
            L - low temp, after which boiler is turning on in autonomous mode
            H - high temp, after wich boiler is turning off in autonomous mode
            R - relay status ( 0 - on, 1 - off )

