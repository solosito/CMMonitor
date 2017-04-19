# CMMonitor
Simple script for measuring and plotting over time the CPU and RAM usages in Unix machines.

## Settings
Add a cron task that which launches the script for logging data:

1. In a terminal run  
        
          crontab -e
        
        
2. Edit this file and add a new line with the following text:

        * * * * * while true; do path_to_folder/ps.sh & sleep <<<executing_freq>>>; done
          
## Plotting data
1. Go to the folder where the ```plot_usage.py``` is and run it:
    - Whether executing ```python plot_usage.py``` 
    - Whether making it executable with ```chmod 777 plot_usage.py``` and  executing it with ```./plot_usage.py```
    
2. It will generate 2 images representing the cpu and mem usage for the last ```t_win``` minutes. 
 
## Parameters
- ```CPU_TRESHOLD```: set in ```plot_usage.py```. Minimum process CPU usage (in percentage) for being considered when plotting data. Default = 1.0.
- ```MEM_TRESHOLD```: set in ```plot_usage.py```. Minimum process RAM usage (in percentage) for being considered when plotting data. Default = 1.0.
- ```t_win```: set in ```ps.sh```. Time window in minutes for data storing. Default = 30
- ```executing_freq```: set in the cron task. Frequency in Hz for measuring the CPU and MEM usages.

***Note that the size of the log file will be proportional to the temporal window size and to the measuring frequency.***
