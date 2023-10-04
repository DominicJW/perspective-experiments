from math import atan, sqrt,degrees, acos, pi
import plotly.express as px
import pandas as pd


incscale = 720/90
aziscale = 720/90

class Node:
	def __init__(self,coords):
		self.coords = coords
		
		x = self.coords[0]
		y = self.coords[1]
		z = self.coords[2]
		
		r = sqrt(x**2+y**2+z**2)

		theta = acos(z/r)

		sgn = lambda a: a/abs(a)

		def sgn(a):
			return a/abs(a)
			
		
		if y != 0: azi = sgn(y)*acos(x/sqrt(x**2+y**2))
		elif x > 0: 
			azi = atan(y/x)
		elif x < 0 and y >= 0:
			azi = atan(y/x) + pi
		else:
			azi = 2*pi # why? Because if x and y are zero then the point is at the centre, so could be thought of as all way round, but could alos be thought of as zero.



		self.pers = (degrees(theta),degrees(azi))
		print(self.pers)


	def __hash__(self):
		return hash(str(self.coords))

	def __sub__(self,other):
		out = [0,0,0]
		for x in range(len(self.coords)):
			out[x] = abs(self.coords[x] - other.coords[x])
		return sum(out)


class Edge:
	def __init__(self,node1,node2):
		self.node1 = node1
		self.node2 = node2
	def __hash__(self):
		# fine for my purposes
		return hash(f'{hash(self.node1)},{hash(self.node2)}')



import turtle
# Set up the turtle
turtle.speed(0)  # Set the fastest drawing speed
turtle.hideturtle()  # Hide the turtle icon

# Define a function to draw a point
def draw_point(x, y):
	turtle.penup()
	turtle.goto(x, y)
	turtle.pendown()
	turtle.dot(5)  # Adjust the size of the dot as needed


# Example usage
#for n in nodes:
	#draw_point(*n.pers)

def draw_node(n):
	draw_point(*scale(n.pers))
	#turtle.write(str(n.coords)+" " + str(n.pers), align="left", font=("Arial", 4, "normal"))


def scale(args):
	return args[0] * incscale, args[1] * aziscale
	


def draw_edge(e):
	turtle.penup()
	turtle.goto(*scale(e.node1.pers))
	turtle.pendown()
	turtle.goto(*scale(e.node2.pers))
	



turtle.pu()
turtle.goto(-720,-720)
turtle.pd()
turtle.goto(-720,720)
turtle.goto(720,720)
turtle.goto(720,-720)
turtle.goto(-720,-720)




'''
edges = [
    Edge(Node((500, 500, 500)),Node((500, 500, 1000))),
    Edge(Node((500, 500, 500)),Node((500, 1000, 500))),
    Edge(Node((500, 500, 500)),Node((1000, 500, 500))),
    Edge(Node((500, 500, 1000)),Node((500, 1000, 1000))),
    Edge(Node((500, 500, 1000)),Node((1000, 500, 1000))),
    Edge(Node((500, 1000, 500)),Node((500, 1000, 1000))),
    Edge(Node((500, 1000, 500)),Node((1000, 1000, 500))),
    #Edge(Node((500, 1000, 1000)),Node((1000, 1000, 1000))),
    Edge(Node((1000, 500, 500)),Node((1000, 500, 1000))),
    Edge(Node((1000, 500, 500)),Node((1000, 1000, 500))),
    #Edge(Node((1000, 500, 1000)),Node((1000, 1000, 1000))),
    #Edge(Node((1000, 1000, 500)),Node((1000, 1000, 1000)))
]

'''


nodes = [Node((x,y,z)) for x in range(20) for y in range(20) for z in range(1,20)]


def theta_calc_df(row):
	x = row['x']
	y = row['y']
	z = row['z']
	r = sqrt(x**2+y**2+z**2)
	return degrees(acos(z/r))

def azi_calc_df(row):
	x = row['x']
	y = row['y']
	z = row['z']
	r = sqrt(x**2+y**2+z**2)
	sgn = lambda a: a/abs(a)

	if y != 0: azi = sgn(y)*acos(x/sqrt(x**2+y**2))
	elif x > 0: 
		azi = atan(y/x)
		
	elif x < 0 and y >= 0:
		azi = atan(y/x) + pi
	else:
		azi = 2*pi # why? Because if x and y are zero then the point is at the centre, so could be thought of as all way round, but could alos be thought of as zero.
		
	return degrees(azi)


def get_r(row):
	x = row['x']
	y = row['y']
	z = row['z']
	r = sqrt(x**2+y**2+z**2)
	return r


points = pd.DataFrame(data = [(x,y,z) for x in range(20) for y in range(20) for z in range(1,20)], columns = ["x","y","z"])
points['theta'] = points.apply(theta_calc_df,axis =1)
points['azi'] = points.apply(azi_calc_df,axis =1)
points['one'] = 1
points['r'] = points.apply(get_r,axis=1)




fig = px.scatter(points, x= 'azi',y='theta',size_max = 4,size = 'one',color = 'r')



# Set aspect ratio to be square
fig.update_layout(
    autosize=False,
    width=500,  # You can adjust the width if needed
    height=500,  # You can adjust the height if needed
    yaxis=dict(scaleanchor='x', scaleratio=1),
    xaxis=dict(scaleanchor='y', scaleratio=1)
)

# Show the plot
fig.show()
