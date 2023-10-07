# Week 1
## Timer interrupt
### difference between timer interrupts and loop
Timer interrupt allows a task to be performed at a very specific moment in time while loop() does not since it is difficult to tell how long a statement takes.
### Definition
Arduino timer interrupt pauses the normal sequence of events and executes the set of commands specified at a certain point in time.
### Application
Interrupts are useful for measuring an incoming signal at equally spaced intervals, sending out a signal periodically etc.
## CTC mode (Clear Timer on Compare Match)
- There are six timers in MEGA, namely, timer0−5.
- Each timer has a counter and is incremented on each clock tick.
- interrupt is triggered when the counter reaches a specific value, stored in the compare match register.
- the counter will be reset to 0 after reaching the value.
- how often interrupts occur depend on the **compare match value**.
## Timers for Arduino (MEGA)
- timer0 (8 bit): used for timer functions such as delay( ), millis( ), and micros( ). If you change time0 registers, this may affect the Arduino timer function.
- time1 (16 bit): servo library uses timer1 on Arduino UNO and timer5 on Arduino MEGA.
- timer2 (8 bit): it acts like timer0. The tone( ) function uses timer2.
- timer3, timer4, timer 5 (16 bit): These 16-bit timers are only available on MEGA boards. 
## Timer Interrupt Program Structure
### In setup()
- setup up the right frequency of the timer by specifying the parameters
appropriately.

### Define interrupt function
- The interrupt function of TimerX is ISR(TIMERX_COMPA_vect)
- e.g. the interrupt function of Timer1 is ISR(TIMER1_COMPA_vect)
- put the tasks you want to perform periodically inside the interrupt function

### In loop()
- no statement is needed here if everything you want to do is in the interrupt function
## Timer parameters
### clock speed
- Arduino clock runs at 16 MHz (clock ticks every 1/16,000,000 second = 62.5 ns).（这个是时钟速度，固定的）
- Fastest speed the interrupt can occur.
### maximum counter value
- timer0 and timer2 are 8-bit timers (maximum counter value = 255).
- timer1, timer3, timer4 and timer5 are 16-bit timers (at most 65535). [65535 = 2^16-1]
### prescaler (slow down counter increment)
- timer speed (how often the counter increments) = Arduino clock speed / prescaler.
<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1f86ff77a5ef407080c66fbf80b23a41~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=2078&h=964&s=113945&e=png&b=ffffff" alt="螢幕截圖 2023-10-07 下午7.04.13.png"  width="70%"/></p>

### Setting the right value
ref: https://www.instructables.com/Arduino-Timer-Interrupts/
```
Desired interrupt frequency = Arduino clock speed/ (prescaler*(compare match register + 1))

Compare match register = Arduino clock speed/ (prescaler * desired interrupt frequency) – 1
```
当使用Timer0和Timer2时， 比较匹配暂存器（CMR）必须小于256.
### Timer setup code
```
TCCR0A |= (1 << WGM01);//for timer0  
TCCR1B |= (1 << WGM12);//for timer1  
TCCR2A |= (1 << WGM21);//for timer2  
This follows directly from the datasheet of the ATMEL 328/168.  
  
Finally, notice how the setup for the prescalers follows the tables in the last step (the table for timer 0 is repeated above),  
TCCR2B |= (1 << CS22);  // Set CS#2 bit for 64 prescaler for timer 2  
TCCR1B |= (1 << CS11);  // Set CS#1 bit for 8 prescaler for timer 1  
TCCR0B |= (1 << CS02) | (1 << CS00);  // Set CS#2 and CS#0 bits for 1024 prescaler for timer 0
```
# Week 2
## Servo motors伺服电机
The **rotation angle** of the servo motor is controlled by applying a **PWM** signal to it.  By varying the width of the PWM signal, we can change
the rotation angle and direction of motion of the motor. 
### Structure
- motor
- potentiometer (variable resister)
- control board.
### Wires
- power (Red)
- ground (Brown)
- signal(Yellow/Orange/White)
### Classcification
- continuous rotation: can rotate all the way around in either direction, where pulse tells servo which way to spin & how fast to spin.
- positional: can only rotate 180 degrees, where pulse tells servo which position to hold.
## Control signal
### Classcification
- Pulse frequency is fixed (Typical: 20 ms)
- Pulse width determines position (Typical: 1ms to 2 ms)
### Function
- If M+ is low and M- is high, the motor goes to one direction.
- If M+ is high and M- is low, the motor goes to another direction.
- If M+ and M- have the same voltage level, the motor stop.
<p align=center><img src="https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/c01e2c385dd7492f9ea31bd8d0b583c3~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=652&h=452&s=146663&e=png&b=fcfbfb" alt="螢幕截圖 2023-10-07 下午7.57.00.png"  width="50%"/></p>

### Attention
Motor power should be separated from the controller power because the motor draws a (comparatively) large current and there is a lot of noise generated when there is a direction change.

# Week3
## Principles of PV cells
### Traditional PV
- Traditional PV uses semiconductor materials such as Silicon to fabricate PV cells which generate direct current under sunlight.
- First PV cell: 1954.
- Early applications: space for power supply in satellites.
- It is now commonly used on rooftop for supplementing electricity from utility grid.
### Electrical Properties of a PV cell
<p align=center><img src="https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/5b6942a2150643e897eb8041f571c9c7~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1616&h=1056&s=283710&e=png&b=dde0e0" alt="螢幕截圖 2023-10-07 下午8.07.20.png"  width="70%"/></p>

- MPP的变化：MPP是光伏电池能够提供的最大功率点，通常对应于电流和电压的某个特定组合。在I-V图像中，随着光照强度的增加，MPP的位置会向右上方移动。这是因为更高的光照强度会导致光伏电池产生更多的电流和电压，从而使MPP点向电流和电压坐标轴的正方向移动。

- 电阻性负载的影响：电阻性负载是将光伏电池连接到外部电路中的负载元件。在I-V图像中，电阻性负载会改变电流和电压的分布。较大的负载电阻会导致更高的电压降，并限制电流的流动，从而导致电流降低。因此，电阻性负载会使整个I-V曲线向左下方移动，减小了MPP的功率输出。

- 光照强度的影响：光照强度是光照射在光伏电池上的功率密度，通常以W/m^2为单位。光照强度的增加会导致整个I-V曲线上的电流和电压都增加。更高的光照强度意味着更多的光能被转换成电能，因此整个曲线会向右上方移动。

### Maximum power point tracking (MPPT)
- The maximum power occurring at Im and Vm which are constantly shifting according to different environmental conditions. Continuous adjustment is needed to capture the maximum output from the PV Cell, and the process is called maximum power point tracking (MPPT).
- After regulating the output current and voltage of the PV cell, the power available would then be fixed according to the solar resources and other physical conditions.
- For stand-alone system, the charging voltage and current will be regulated after the MPPT process. In a grid-connecting PV systems, the DC power will be converted to AC and then fed into the electricity grid. 

## Noise
### Noise through the cables
- Cable 1: Two separated wires. (最差)
- Cable 2: Two‐wire flat cable.
    - 由于两根导线之间的相邻性，可能会存在串扰（crosstalk）现象，即一根线上的信号对另一根线上的信号产生干扰。
- Cable 3: A short twisted pair cable.
    - 双绞线的设计有助于减少外部电磁干扰对信号的影响，并且能够减轻串扰的问题。因此，Cable 3 可以提供较好的噪声抑制能力，适用于需要较高抗干扰性能的应用。
- Cable 4: Four‐wire flat cable.（抗干扰性能最好）
    - 四线平行电缆通常用于传输差分信号，例如差分信号传输的网络或数据通信应用。相较于 Cable 2，Cable 4 具有更好的抗干扰能力，能够提供更高的信号完整性和抗干扰性。
### Checking the noise through cables
Use an oscilloscope to examine the noise voltage VDE waveforms. 
# Week 4
## MQTT
- Designed for data exchange with constrained devices.
- Bandwidth-efficient and consumes less power.
### Publish/subscribe paradigm.
- Topic is the routing information, instead of IP address
- Clients do not have to know each other
- One-to-many and many-to-one data transmission can be done efficiently
- Two connections have to be maintained by broker.
- **MQTT client maintains a permanent TCP connection with the broker**
- **Client sends PING request to broker periodically**
### Programming architecture
- `server`: IP address of the server
- `port`: port to connect to server (default: 1883)
- `callback`: method called when a message arrives for a subscription
- `client`: an instance of Client
- `stream`: an instance of Stream used for storing received messages
## Long Range Radio
### Feature
- RF modulation technology
- Long-range, Low-power, wide area networks (LPWANs) 
### Comparasion
<p align=center><img src="https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/1a34e1ca1dca46e0ac07e4f8406fb206~tplv-k3u1fbpfcp-jj-mark:0:0:0:0:q75.image#?w=1638&h=878&s=422272&e=png&b=d9dbdc" alt="螢幕截圖 2023-10-07 下午8.40.36.png"  width="70%"/></p>

### Lora for wide area networks
LoRaWAN
– LoRa for Wide Area Networks
- extended the LoRa® physical communication layer into the Internet by adding a MAC (Medium access control) layer
- A software layer that defines devices for use
- Example : when they transmit or receive messages
- Open-source supported and maintained by LoRa Alliance® since 2015
- data rates ranging from 300 bps to 5 kbps for a 125 kHz bandwidth
- depend on Range, i.e. Time on-Air,