from p5 import *

lasers = []
asteroids = []

def setup(): 
  createCanvas(windowWidth, windowHeight)
  global ship
  ship = Ship()
  for x in range(5):
    pos = createVector(random(width), random(height))
    r = 55
    asteroids.append(Asteroid(pos, r))  

def draw():
  global asteroids
  background('black')

  for roid in asteroids:
    if ship.hits(roid):
      print('ooops!')
    roid.render()
    roid.update()
    roid.edges()

  for shot in lasers:
    shot.render()
    shot.update()
    if shot.offscreen():
      lasers.remove(shot)
    else:
      for roid in asteroids:
        if shot.hits(roid):
          if roid.r > 20:
            newAsteroids = roid.breakup()
            asteroids = asteroids + newAsteroids
          asteroids.remove(roid)
          lasers.remove(shot)
          break

  ship.render()
  ship.update()
  ship.edges()


# could possibly try adding a distance to the vector, not just an angle (if blank is assumened to be 1)

#  extension - improve controls, supe up the ship
  # make 3 different classes of ships
class Ship:
  def __init__(self): 
    self.pos = createVector(width/2, height/2)
    self.heading = 0
    self.r = 20
    # vector has x and y components
    self.vel = createVector(0, 0)
    self.fireTime = 0
  
  def update(self):
    if keyIsDown(SHIFT):
      if millis() - self.fireTime > 500:
        self.fireTime = millis()
        lasers.append(Laser(self.pos, self.heading))

    if keyIsDown(UP_ARROW):
      self.boost()      
    
    if keyIsDown(LEFT_ARROW):
      self.heading += 1
    
    if keyIsDown(RIGHT_ARROW):
      self.heading -= 1
      
    # add one vector to another (change in position)
    self.pos.add(self.vel.y, self.vel.x)  
   
  def boost(self):
    #determine the new vector direction to add to the current one, based on the angle that has been turned, since the last boost/thrust

    # explain difference between radians and degrees
    force = p5.Vector.fromAngle(radians(self.heading))
    #not sure why necessary to make this negative here
    force.mult(-1, 1)
    # just to reduce the speed
    force.mult(0.01) 
    self.vel.add(force)  
    # suggest they print out force, vel, heading, rotation etc
 
  def render(self):
    push()
    translate(self.pos.x, self.pos.y)
    rotate(self.heading)
    fill(0)
    stroke(255)  
    triangle(-self.r, self.r, self.r, self.r, 0, -self.r)
    pop()

  # so it doesnt go off the screen
  def edges(self):
    if self.pos.x > width + self.r:
      self.pos.x = -self.r
    elif self.pos.x < -self.r:
      self.pos.x = width + self.r
    
    if self.pos.y > height + self.r:
      self.pos.y = -self.r
    elif self.pos.y < -self.r:
      self.pos.y = height + self.r

  def hits(self, asteroid):
    d = self.pos.dist(asteroid.pos)
    if d < self.r + asteroid.r:
      return 1
    else:
      return 0

 
class Laser:
  def __init__(self, pos, angle): 
    self.pos = pos.copy()
    # whey do we need to deduct 90 degrees here?
    self.vel = p5.Vector.fromAngle(radians(angle-90))
    self.vel.mult(10)

  def update(self):
    self.pos.add(self.vel)   

  def render(self): 
    push()
    stroke(255)
    strokeWeight(4)
    point(self.pos.x, self.pos.y)
    pop()

  def hits(self, asteroid):
    d = self.pos.dist(asteroid.pos)
    if d < asteroid.r:
      return 1
    else:
      return 0 

  def offscreen(self):
    if self.pos.x > width or self.pos.x < 0:
      return 1
    if self.pos.y > height or self.pos.y < 0:
      return 1
    return 0


class Asteroid:
  def __init__(self, pos, r):
    self.pos = pos.copy()
    self.r = r * 0.5
    self.vel = p5.Vector.random2D()  
  
  def update(self):
    self.pos.add(self.vel)

  def render(self):
    push()
    rectMode(CENTER)
    stroke(255)
    noFill()
    translate(self.pos.x, self.pos.y)
    square(0, 0, self.r)
    # extension - student can make different regular polygons
    pop()
    
  def breakup(self):
    roids = []
    roids.append(Asteroid(self.pos, self.r))
    roids.append(Asteroid(self.pos, self.r))
    return roids
    
  def edges(self):
    if self.pos.x > width + self.r:
      self.pos.x = -self.r
    elif self.pos.x < -self.r:
      self.pos.x = width + self.r
    
    if self.pos.y > height + self.r:
      self.pos.y = -self.r
    elif self.pos.y < -self.r:
      self.pos.y = height + self.r
