import pyglet,copy
from .vector import Vector

window = ...
update = ...
keys = ...
world = ...

def init(win,upd,kb,wrld):
	global window, update, keys, world
	window = win
	update = upd
	keys = kb
	world = wrld

class statehandler:
	class _Statehandler:
		def __init__(self,state,item):
			self.properties = state
			self.item = item

		def __repr__(self):
			return str(self.properties)

	def __init__(self):
		self.states = []

	def __setitem__(self,key,item):
		s = self._Statehandler(key,item)
		self.states.append(s)

	def __getitem__(self,thing):
		possibilities = copy.copy(self.states)
		for i in self.states:
			for key,item in thing.items():
				if i.properties[key] != item and i in possibilities:
					possibilities.remove(i)
		return possibilities
	
	def __repr__(self):
		return repr(self.states)


class Enemy:
	def __init__(self,x,y):
		assert window
		self.textures = statehandler()
		self.v = Vector(0,0)
		self.x = Vector(x,y)
		self.part = 0
		self.parts = 0
		self.maxxv = 150
		self.keys = {"left":False,"right":False,"jump":False}
		self.flipped = True
		self.partcounter = 0
		self.in_jump = False

	def post_init(self):
		self.sprite = pyglet.sprite.Sprite(self.get_texture(),self.x.x,self.x.y, usage='dynamic', subpixel=False)

	def get_texture(self):
		
		print(self.state)

		t = self.textures[{"state":self.state}]
		if self.parts != t[0].properties["parts"]:
			self.parts = t[0].properties["parts"]
			self.part = 0
		t = self.textures[{"state":self.state,"part":self.part}]
		assert len(t) == 1
		return t[0].item

	def update(self,dt):
		changed = False

		self.partcounter += 1
		if self.partcounter > 10:
			self.partcounter = 0
			self.part += 1

		if self.part >= self.parts:
			self.part = 0

		if self.keys["jump"] and not self.in_jump:
			self.v.y = 500
			self.in_jump = True
		if self.keys["left"]:
			if self.v.x > 0:
				self.v.x -= 25
			else:
				self.v.x -= 10
		if self.keys["right"]:
			if self.v.x < 0:
				self.v.x += 25
			else:
				self.v.x += 10
	
		if self.in_jump:
			self.v.y -= 10

		if self.x.y + (self.v.y * dt) <= 0:
			while True:
				if self.v.y > 90:
					self.v.y -= 90
				elif self.v.y < -90:
					self.v.y += 90
				elif not (self.x.y + (self.v.y * dt) <= 0):
					break
				else:
					self.in_jump = False
					self.v.y = 0
					break
		
		if self.x.x + (self.v.x * dt) <= 0:
			while True:
				if self.v.x > 90:
					self.v.x -= 90
				elif self.v.x < -90:
					self.v.x += 90
				elif not (self.x.x + (self.v.x * dt) <= 0):
					break
				else:
					self.v.x = 0
					break
		
		
		if self.x.x + (self.v.x * dt) >= world.width - self.sprite.width:
			while True:
				if self.v.x > 90:
					self.v.x -= 90
				elif self.v.x < -90:
					self.v.x += 90
				elif not (self.x.x + (self.v.x * dt) >= world.width - self.sprite.width):
					break
				else:
					self.v.x = 0
					break
		x,y = world.check_colision(self.x.x + (self.v.x * dt),self.x.y,self.sprite.width,self.sprite.height,"<")
		if x != None and self.x.x + (self.v.x * dt) > x:
			while True:
				if self.v.x > 90:
					self.v.x -= 90
				elif self.v.x < -90:
					self.v.x += 90
				elif not (self.x.x + (self.v.x * dt) > x):
					break
				else:
					self.v.x = 0
					break	

		x,y = world.check_colision(self.x.x + (self.v.x * dt),self.x.y,self.sprite.width,self.sprite.height,">")
		if x != None and self.x.x + self.sprite.width + (self.v.x * dt) > x:
			while True:
				if self.v.x > 90:
					self.v.x -= 90
				elif self.v.x < -90:
					self.v.x += 90
				elif not (self.x.x + self.sprite.width + (self.v.x * dt) > x):
					break
				else:
					self.v.x = 0
					break			

		x,y = world.check_colision(self.x.x + (self.v.x * dt),self.x.y,self.sprite.width,self.sprite.height,"v")
		if x != None and self.x.y + (self.v.y * dt) <= y:
			while True:
				if self.v.y > 90:
					self.v.y -= 90
				elif self.v.y < -90:
					self.v.y += 90
				elif not (self.x.y + (self.v.y * dt) <= y):
					break
				else:
					self.in_jump = False
					self.v.y = 0
					break		

		x,y = world.check_colision(self.x.x + (self.v.x * dt),self.x.y,self.sprite.width,self.sprite.height,"^")
		if x != None and self.x.y + self.sprite.height + (self.v.y * dt) > y:
			while True:
				if self.v.y > 50:
					self.v.y -= 50
				elif self.v.y < -50:
					self.v.y += 50
				elif not (self.x.y + self.sprite.height > y):
					break
				else:
					self.v.y = 0
					break	

		x,y = world.check_colision(self.x.x,self.x.y + (self.v.y * dt),self.sprite.width,self.sprite.height,"v")
		if x != None and self.x.y + (self.v.y * dt) <= y:
			while True:
				if self.v.y > 90:
					self.v.y -= 90
				elif self.v.y < -90:
					self.v.y += 90
				elif not (self.x.y + (self.v.y * dt) <= y):
					break
				else:
					self.in_jump = False
					self.v.y = 0
					break		

		x,y = world.check_colision(self.x.x,self.x.y + (self.v.y * dt),self.sprite.width,self.sprite.height,"^")
		if x != None and self.x.y + self.sprite.height + (self.v.y * dt) > y:
			while True:
				if self.v.y > 50:
					self.v.y -= 50
				elif self.v.y < -50:
					self.v.y += 50
				elif not (self.x.y + self.sprite.height > y):
					break
				else:
					self.v.y = 0
					break	
	

		x,y = world.check_colision(self.x.x,self.x.y + (self.v.y * dt),self.sprite.width,self.sprite.height,"<")
		if x != None and self.x.x + (self.v.x * dt) > x:
			while True:
				if self.v.x > 90:
					self.v.x -= 90
				elif self.v.x < -90:
					self.v.x += 90
				elif not (self.x.x + (self.v.x * dt) > x):
					break
				else:
					self.v.x = 0
					break	

		x,y = world.check_colision(self.x.x,self.x.y + (self.v.y * dt),self.sprite.width,self.sprite.height,">")
		if x != None and self.x.x + self.sprite.width + (self.v.x * dt) > x:
			while True:
				if self.v.x > 90:
					self.v.x -= 90
				elif self.v.x < -90:
					self.v.x += 90
				elif not (self.x.x + self.sprite.width + (self.v.x * dt) > x):
					break
				else:
					self.v.x = 0
					break			



		if world.overlap(self.x.x,self.x.y-1,self.sprite.width,self.sprite.height) == 0 and not self.in_jump:
			self.in_jump = True			

		if not (self.keys["left"] or self.keys["right"]):
			if self.v.x > 10:
				self.v.x -= 10
			elif self.v.x < -10:
				self.v.x += 10
			else:
				self.v.x = 0

		self.v.x = self.maxxv if self.v.x > self.maxxv else self.v.x
		self.v.x = -self.maxxv if self.v.x < -self.maxxv else self.v.x
		self.x += self.v.mult(dt)

		self.sprite.set_position(self.x.x, self.x.y)

		if abs(self.v.x) > 0.5 and not self.in_jump:
			self.state = "move"
			changed = True
		if self.in_jump:
			self.state = "jump"
			changed = True
		if self.v.x < -0.2:
			self.flipped = True
		elif self.v.x > 0.2:
			self.flipped = False
	
		if not changed:
			self.state = "standing"

		t = self.get_texture()
		t.anchor_x = 0
		if self.flipped:
			t.anchor_x = t.width//2
			t = t.get_texture().get_transform(flip_x = True)
			t.anchor_x = 0		
		self.sprite.image = t

		self.AI()

	def draw(self):
		self.sprite.draw()