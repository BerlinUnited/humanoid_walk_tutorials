
# Description:  A controller running a race stopwatch.
# this is a minimal adjusted version of the supervisor race_stopwatch.c

from controller import Supervisor

def stopwatch_init(robot):
  #snprintf(digit_name, 8, "digit__");
  
  # get the list of devices
  #digit_actuators = 
  
  # number of digits
  N_DIGIT = 6
  
  value_ids = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', '_']
  
  digit = []
  for i in range(0, N_DIGIT):
    value_actators = []
    for v in value_ids:
        value_actators += [robot.getDevice(f"digit{i}{v}")]
        
    digit += [value_actators]
  
  #print(digit)
  return digit
  

digit_value = [0, 0, 0, 0, 0, 0]
  
def stopwatch_set_time(digit, t):

    # hide old digit
    for i, d in enumerate(digit):
        d[digit_value[i]].setPosition(0)

    digit_value[0] = int(t * 100) % 10
    
    if t >= 0.1:
        digit_value[1] = int(t * 10) % 10
        if t >= 1:
            digit_value[2] = int(t) % 10
            if t >= 10:
                digit_value[3] = int(t / 10) % 6
                if t >= 60:
                    digit_value[4] = int(t / 60) % 10
                    if t >= 600:
                        digit_value[5] = int(t / 600) % 10
    
    # show new digit
    #print(digit_value)
    for i, d in enumerate(digit):
        d[digit_value[i]].setPosition(0.1)
    

def main():

    robot = Supervisor()
    digit = stopwatch_init(robot)
  
    time_step = int(robot.getBasicTimeStep() * 4)
    
    # enable the sensor
    detector = robot.getDevice("detector")
    detector.enable(time_step)
    
    nao = robot.getFromDef("NAO")
    translation = nao.getField('translation')
    
    record = 0
    time_limit = 5999.99 # 99 min 59 s 99'
    previous_time_limit = time_limit - time_step / 1000.0 # time limit minus one time step period, in seconds.
    
    
    while robot.step(time_step) != -1:
        
        # get the current time and robots position
        t = robot.getTime()
        v = translation.getSFVec3f()
        #print(v)
        
        # z too low => the robot has fallen down => disqualified.
        if v[2] < 0.2:
            print("The robot is down, the robot is disqualified.\n")
            stopwatch_set_time(digit, time_limit)
            robot.wwiSendText("time:5999.99")  # 99 min 59 s 99'
            break
        
        if t > previous_time_limit:
            t = previous_time_limit
        
        # to avoid discrepancy with Webots time
        stopwatch_set_time(digit, t + time_step / 1000)
        
        # send time to the website
        robot.wwiSendText("time:{:-24.3f}".format(t))
        
        if detector.getValue() < 2.4:
            record = t
            m = int(t / 60)
            s = t - 60 * m
            print("Time is: {:d}.{:05.2f}\n".format(m, s))

            #display actual time
            stopwatch_set_time(digit, t)
            break
    
    
    # stop benchmark
    robot.wwiSendText("stop")
    
    # not necessary
    # get record information
    #while robot.step(time_step) != -1:
    #    message = robot.wwiReceiveText()
    #    print(message)
    
    robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
    

main()