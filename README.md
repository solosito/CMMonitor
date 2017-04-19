## Configuration
Add a cron task that which launches the script for logging data:
1. In a terminal run:
        ```
          crontab -e
        ```
        Edit this file and add a new line containing:
        ```
          * * * * * while true; do path_to_folder/ps.sh & sleep secs_for repeating; done
        ```
        
## Visualization
1. Go to the folder where the usage_plot.py script is and run it. It will generate 2 images representing the cpu and mem usage for the last 30 minutes. This time can be changed with the parameter ```t_win``` placed in the ps.sh file.