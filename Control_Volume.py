'''
This program is to automate the volume control  of one's computer using:
1. Arduino UNO Board : For reading the ultrasonic sensor values .
2. Ultrasonic sensor : For finding out one's position in range of 2cm to 400cm  
3. Python: Python language is used to process and analyze the data coming from Arduino UNO.

'''
import serial
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#NOTE: -6.0 dB = half volume , 0 dB is max , -63 dB set to  min

arduinoSerialData = serial.Serial('com5',9600) #Create Serial port object called arduinoSerialData
 
 
while (True):
    if (arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        distance = float(myData)
        print("Distance: " , distance)

        #If object/Person is in range of 20 cm , lower the volume
        if distance<20:
            # Get current volume
            currentVolumeDb = volume.GetMasterVolumeLevel()
            print('Volume: ', currentVolumeDb , end='\n\n')

            if currentVolumeDb < -63:
                print('Minimum volume...!!')
                continue

            volume.SetMasterVolumeLevel(currentVolumeDb - 1.0, None)
        

        #If object/Person  is in range of 100 cm to 20 cm , increment the volume    
        elif (distance < 400 and distance>20):
            # Get current volume
            currentVolumeDb = volume.GetMasterVolumeLevel()
            print('Volume: ', currentVolumeDb , end='\n\n')

            if currentVolumeDb > -1:
                print('Maximum volume...!!')
                continue

            volume.SetMasterVolumeLevel(currentVolumeDb + 1, None)
        
'''
Procedure: 
1. Make the required connections .
2. Upload "ino" file to the Arduino uno board . 
3. Run the Python ("py") file in your system .
4. Analyze the output using the python shell .
 
'''
       
        