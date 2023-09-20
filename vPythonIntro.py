from vpython import *
import random
import math

scene = canvas(width=1523, height=693)

width = 0.1
height = 5
thickness = 0.1
current_angle = 0
plate_pressed = 0

sleep1 = 0.001
sleep2 = 0.12
sleep3 = 0.1

wall1 = box(pos=vector(-5,5,-10), size=vector(10,10,1))
wall2 = box(pos=vector(5,5,-10), size=vector(10,10,1))
wall3 = box(pos=vector(-10,5,-2.5), size=vector(1,10,15))
wall4_1 = box(pos=vector(10.5,5,-7.5), size=vector(1,10,5))
wall4_2 = box(pos=vector(10.5,7,-2.5), size=vector(1,6,5))
wall4_3 = box(pos=vector(10.5,5,2.5), size=vector(1,10,5))
floor1 = box(pos=vector(-5, 0, -2.5), size=vector(10,0.1,15))
floor2 = box(pos=vector(5, 0, -2.5), size=vector(10,0.1,15))
distant_light(direction=vector(1, 0, 0), color=color.white, intensity=0.5, attenuation=0.2)
distant_light(direction=vector(-1, 0, 0), color=color.white, intensity=0.5, attenuation=0.2)
isaac1 = box(pos=vector(0,0.5,0), size=vector(1,1,1), color=color.orange)
isaac2 = box(pos=vector(0.51,0.75,-0.15), size=vector(0.1,0.1,0.1), color=color.black)
isaac3 = box(pos=vector(0.51,0.75,0.15), size=vector(0.1,0.1,0.1), color=color.black)
v1 = sphere(pos=vector(-0.5,1,-0.5), radius=0.1)
v2 = sphere(pos=vector(0.5,1,-0.5), radius=0.1)
v3 = sphere(pos=vector(0.5,1,0.5), radius=0.1)
v4 = sphere(pos=vector(-0.5,1,0.5), radius=0.1)
v1.visible = False
v2.visible = False
v3.visible = False
v4 .visible = False

isaac = compound([isaac1, isaac2, isaac3])
isaac.rotate(angle=radians(-90),axis=vector(0,1,0))
v1.rotate(angle=radians(-90),axis=vector(0,1,0),origin=isaac.pos)
v2.rotate(angle=radians(-90),axis=vector(0,1,0),origin=isaac.pos)
v3.rotate(angle=radians(-90),axis=vector(0,1,0),origin=isaac.pos)
v4.rotate(angle=radians(-90),axis=vector(0,1,0),origin=isaac.pos)

# isaac.axis.x = 0
# isaac.axis.z = 1

plate = box(pos=vector(-8,0.1,-8), size=vector(2,0.1,2), color=color.green)
rod1 = cylinder(pos=vector(10+0.1,0.1,-0.5), axis=vector(0,4-0.1,0), radius=0.1, color=color.red)
rod2 = cylinder(pos=vector(10+0.1,0.1,-1.5), axis=vector(0,4-0.1,0), radius=0.1, color=color.red)
rod3 = cylinder(pos=vector(10+0.1,0.1,-2.5), axis=vector(0,4-0.1,0), radius=0.1, color=color.red)
rod4 = cylinder(pos=vector(10+0.1,0.1,-3.5), axis=vector(0,4-0.1,0), radius=0.1, color=color.red)
rod5 = cylinder(pos=vector(10+0.1,0.1,-4.5), axis=vector(0,4-0.1,0), radius=0.1, color=color.red)
rods = compound([rod1,rod2,rod3,rod4,rod5])
temp_floor = box(pos=vector(10.5,0,-2.5), size=vector(1,0.1,15))

def translate(dx, dy, dz):
    isaac.pos.x += dx
    isaac.pos.y += dy
    isaac.pos.z += dz
    v1.pos.x += dx
    v1.pos.z += dz
    v2.pos.x += dx
    v2.pos.z += dz
    v3.pos.x += dx
    v3.pos.z += dz
    v4.pos.x += dx
    v4.pos.z += dz
    sleep(sleep1)

def rounder():
    isaac.pos.x = round(isaac.pos.x, 2)
    isaac.pos.z = round(isaac.pos.z, 2)
    v1.pos.x = round(v1.pos.x, 2)
    v1.pos.z = round(v1.pos.z, 2)
    v2.pos.x = round(v2.pos.x, 2)
    v2.pos.z = round(v2.pos.z, 2)
    v3.pos.x = round(v3.pos.x, 2)
    v3.pos.z = round(v3.pos.z, 2)
    v4.pos.x = round(v4.pos.x, 2)
    v4.pos.z = round(v4.pos.z, 2)

def room_bounds(dx,dy,dz):
    pos1 = v1.pos
    pos2 = v2.pos
    pos3 = v3.pos
    pos4 = v4.pos
    x_range = (-9.5, 10)
    z_range = (-9.5, 100) 

    if all(
    x_range[0] < vertex.x+dx < x_range[1] and z_range[0] < vertex.z+dz < z_range[1]
    for vertex in [pos1, pos2, pos3, pos4]):
        return True
    else:
        return False
    
def is_cube_over_edge():
    edge_position = 5.5
    aor = vector(isaac.pos.x,isaac.pos.y-0.5,isaac.pos.z) # angle of rotation
    if aor.z - edge_position >= 0:
        angle = -1
        while(angle<=0):
            isaac.rotate(angle=-0.1, axis=vector(-1,0,0), origin=aor)
            angle += 1/10
            sleep(0.01)
        while(angle<=10):
            isaac.pos.y -= 1*0.1
            isaac.rotate(angle=-0.15, axis=vector(-1,0,0))
            angle+=0.15
            sleep(0.01)
        return True
    else:
        return False  

def apply_movement(move, current_angle):
    if move == 'jump':
        if isaac.pos.y == 0.5:
            while isaac.pos.y <=2.5:
                isaac.pos.y += 9.0*0.01
                sleep(sleep1)
            sleep(sleep2)
        if isaac.pos.y > 0.5:
            while(isaac.pos.y > 0.5):
                isaac.pos.y += -9.3 * 0.01
                sleep(sleep1)
        isaac.pos.y = 0.5
    
    elif move == 'back':
        dx = -isaac.axis.x # Invert axis for backward movement
        dz = -isaac.axis.z
        t = isaac.pos.x
        s = isaac.pos.z

        while (t - 1 < isaac.pos.x < t + 1) and (s - 1 < isaac.pos.z < s + 1):
            if room_bounds(dx*0.1, 0, dz*0.1) and not is_cube_over_edge():
                translate(dx*0.1, 0, dz*0.1)
                rounder()
            else:
                break            
            
    elif move == 'front':
        dx = round(isaac.axis.x,2)
        dz = round(isaac.axis.z,2)
        t = isaac.pos.x
        s = isaac.pos.z

        while (t-1< isaac.pos.x < t+1) and (s-1< isaac.pos.z< s+1):
            if room_bounds(dx*0.05, 0, dz*0.05) and not is_cube_over_edge():
                translate(dx*0.05, 0, dz*0.05)
                rounder()
            else:
                break
    
    elif move == 'turn':
        angle = random.randint(-180, 180)
        angle = -90 # --------------------------------------------------------------------
        t = angle * 0.1
        while angle != 0:
            isaac.rotate(angle=radians(t), axis=vector(0, 1, 0))
            angle -= t
            angle = round(angle, 2)
            sleep(sleep3)
    
    elif move == 'jump turn':
        angle = random.randint(-180, 180)
        t = angle/70
        sum = 1
        if isaac.pos.y == 0.5:
            deceleration = 0
            while isaac.pos.y <=2.5 and sum <= 35:
                isaac.pos.y += (10.0-deceleration)*0.01
                isaac.rotate(angle=radians(t), axis=vector(0, 1, 0))
                angle -= t

                angle = round(angle, 2)
                deceleration += 0.25
                sum+=1
                sleep(sleep1)
            isaac.pos.y = 2.5

        if isaac.pos.y > 0.5:
            acceleration = 9
            while(isaac.pos.y > 0.5) and sum<=70:
                isaac.pos.y += (-10+acceleration) * 0.01
                isaac.rotate(angle=radians(t), axis=vector(0, 1, 0))
                angle -= t
                angle = round(angle, 2)
                acceleration -= 0.25               
                sum+=1
                sleep(sleep1)
            isaac.pos.y = 0.5

    elif move == 'jump front':
        if isaac.pos.y == 0.5:
            deceleration = 0
            dx = isaac.axis.x/70
            dz = isaac.axis.z/70
            t = isaac.pos.x
            s = isaac.pos.z
            while isaac.pos.y <=2.5 and t-0.5< isaac.pos.x < t+0.5 and s-0.5< isaac.pos.z< s+0.5:
                isaac.pos.y += (10-deceleration)*0.01
                deceleration += 0.25
                isaac.pos.x += dx#*0.025
                isaac.pos.z += dz#*0.025
                isaac.pos.x = round(isaac.pos.x, 5)
                isaac.pos.z = round(isaac.pos.z, 5)
                sleep(sleep1)
            isaac.pos.y = 2.5
        if isaac.pos.y > 0.5:
            acceleration = 9
            while isaac.pos.y > 0.5 and t-1< isaac.pos.x < t+1 and s-1< isaac.pos.z< s+1:

                isaac.pos.y += (-10+acceleration) * 0.01
                acceleration -= 0.25 
                isaac.pos.x += dx#*0.025
                isaac.pos.z += dz#*0.025
                isaac.pos.x = round(isaac.pos.x, 5)
                isaac.pos.z = round(isaac.pos.z, 5) 
                sleep(sleep1)
        isaac.pos.y = 0.5
    
    elif move == 'jump back':
        if isaac.pos.y == 0.5:
            dx = isaac.axis.x*(-1)/70
            dz = isaac.axis.z*(-1)/70
            t = isaac.pos.x
            s = isaac.pos.z
            deceleration = 0
            while isaac.pos.y <=2.5 and t - 0.5 < isaac.pos.x < t + 0.5 and s - 0.5 < isaac.pos.z < s + 0.5:
                isaac.pos.y += (10.0-deceleration)*0.01
                deceleration += 0.25
                isaac.pos.x += dx
                isaac.pos.z += dz
                isaac.pos.x = round(isaac.pos.x, 5)
                isaac.pos.z = round(isaac.pos.z, 5)
                sleep(sleep1)
            isaac.pos.y = 2.5

        if isaac.pos.y > 0.5:
            acceleration = 9
            while isaac.pos.y > 0.5 and t - 1 < isaac.pos.x < t + 1 and s - 1 < isaac.pos.z < s + 1:
                isaac.pos.y += (-10+acceleration) * 0.01
                acceleration -= 0.25  
                isaac.pos.x += dx
                isaac.pos.z += dz
                isaac.pos.x = round(isaac.pos.x, 5)
                isaac.pos.z = round(isaac.pos.z, 5)             
                sleep(sleep1)
            isaac.pos.y = 0.5

    else:
        print("WAIT WHAT-------------------------------------------------------------->")

while True:
    rate(60)

    if plate.pos.x-1.5<=isaac.pos.x <=plate.pos.x+1.5 and plate.pos.z-1-0.5<=isaac.pos.z <=plate.pos.z+1+0.5 and plate.pos.y+0.4 == isaac.pos.y:
                plate.pos.y = 0.01
                plate.color = color.cyan
                plate_pressed = 1
                t = (10.5-rods.pos.x)/5
                while rods.pos.x <= 10.5:
                    rods.pos.x += t
                    sleep(sleep3)
                rods.pos.x = 10.5
                t = (7-rods.pos.y)/50
                while rods.pos.y <= 7:
                    rods.pos.y += t
                    sleep(sleep3)
                rods.pos.y = 7
    sleep(1)
    move = random.choice(['front'])#,'front','turn','jump','jump turn','jump front','jump back'])
    print("MOVE:",move)
    apply_movement(move, current_angle)


    

