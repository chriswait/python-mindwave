Some scripts to access the data streamed by the **Neurosky Mindwave Mobile** Headset over Bluetooth on Linux.

Requirements:
* [PyBluez](http://code.google.com/p/pybluez/), see their [documentation](http://code.google.com/p/pybluez/wiki/Documentation) for installation instructions :)

Usage:

* Initilaise the background daemon which logs to the database:
```python dbLogger.py <name> <activity>

	where 	<name> 		corresponds to the user_id (guest=0)
		<activity>	corresponds to current activity (	other=0,
									revising=1,
									programming=2, 
									meditating=3, 
									relaxing=4)
```



Original usage example:

```python
mindwaveDataPointReader = MindwaveDataPointReader()
# connect to the mindwave mobile headset...
mindwaveDataPointReader.start()
# read one data point, data point types are specified in  MindwaveDataPoints.py'
dataPoint = mindwaveDataPointReader.readNextDataPoint()
``` 
