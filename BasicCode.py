from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Button, Color, Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X, broadcast_channel=0, observe_channels=[1])
Right = Motor(Port.E, Direction.COUNTERCLOCKWISE)
Left = Motor(Port.B, Direction.CLOCKWISE)
DriveTrain = DriveBase(Right, Left, 62, 114)

# Initialize variables.
Current_program = 1
Straight_Speed = 620
Straight_Acceleration = 500
Turn_Speed = 250
Turn_Acceleration = 500
Attachment_Speed = 810
In_Leg = 0

async def Leg_1():
    await wait(1)
    await Start_Task()
    prime_hub.light.on(Color.YELLOW)
    DriveTrain.straight(0)
    await prime_hub.speaker.beep(550, 200)
    await wait(200)
    DriveTrain.drive(100, 0)
    while not 3 == 4:
        await wait(1)

async def Leg_2():
    await wait(1)
    await Start_Task()
    print('Works')
    await End_Task()

async def Leg_3():
    await wait(1)
    await Start_Task()
    prime_hub.light.on(Color.VIOLET)
    DriveTrain.straight(0)
    await prime_hub.speaker.beep(550, 200)
    await wait(200)
    await DriveTrain.straight(1000)
    await DriveTrain.turn(90)
    await DriveTrain.straight(900)
    await End_Task()

async def Start_Task():
    global In_Leg
    await wait(1)
    In_Leg = 1
    prime_hub.display.off()
    prime_hub.display.pixel(2, 2, 25)

async def End_Task():
    global In_Leg
    await wait(1)
    In_Leg = 0

async def main1():
    global Current_program, In_Leg
    prime_hub.system.set_stop_button(None)
    DriveTrain.settings(straight_speed=Straight_Speed)
    DriveTrain.settings(straight_acceleration=Straight_Acceleration)
    DriveTrain.settings(turn_rate=Turn_Speed)
    DriveTrain.settings(turn_acceleration=Turn_Acceleration)
    prime_hub.imu.reset_heading(0)
    DriveTrain.brake()
    DriveTrain.use_gyro(True)
    while True:
        await wait(1)
        prime_hub.display.number(Current_program)
        prime_hub.light.on(Color.BLUE)
        if Button.RIGHT in prime_hub.buttons.pressed():
            Current_program = Current_program + 1
            await wait(350)
        elif Button.LEFT in prime_hub.buttons.pressed():
            Current_program = Current_program - 1
            await wait(350)
        elif Button.CENTER in prime_hub.buttons.pressed():
            if Current_program == 1:
                await Leg_1()
                await wait(300)
            elif Current_program == 2:
                await Leg_2()
                await wait(300)
            elif Current_program == 3:
                await Leg_3()
                await wait(300)
            elif Current_program == 4:
                pass
            else:
                pass
        else:
            await wait(10)
        In_Leg = 0

async def main2():
    while True:
        await wait(1)
        print(prime_hub.imu.heading())
        await wait(1000)

async def main3():
    while True:
        await wait(1)
        if In_Leg == 1:
            await wait(200)
            prime_hub.system.set_stop_button(Button.CENTER)
        else:
            prime_hub.system.set_stop_button(None)


async def main():
    await multitask(main1(), main2(), main3())

run_task(main())
