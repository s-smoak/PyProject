import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import datetime as dt
import requests

class dataPoint():
	def __init__(self,time,price):
		self.time = time
		self.price =price



tick_url=f"https://api.exchange.coinbase.com/products/BTC-USD/ticker"

def get_data():
	#get time stamp
	timestamp = dt.datetime.now().strftime('%H:%M:%S')
	
	#get rates
	try:
		response = requests.get(tick_url)
		response = response.json()
		price = float(response['price'])
	except:
		raise Exception("Error fetching BTC-USD price")
	
	data = dataPoint(timestamp,price)
	return data



#intial request for plot setting use
stats_url = "https://api.exchange.coinbase.com/products/BTC-USD/stats"
try:
	response = requests.get(stats_url)
	response = response.json()
 
	high = float(response['high'])
	low = float(response['low'])
except:
	raise Exception("Error fetching BTC-USD stats")

h_list = [high]
l_list = [low]

t0 = dt.datetime.now().strftime('%H:%M:%S')

xs=[t0]
ys=[float(response['last'])]

x_len = 20
y_range = [low-100, high+500]

#plot settings and labels
style.use('dark_background')

fig = plt.figure(figsize=(14,7))
ax = fig.add_subplot(1,1,1)

ax.set_ylim(y_range)
plt.subplots_adjust(bottom=0.20)

plt.title('Bitcoin (BTC) Price')
plt.xlabel('Time (Hour:Minute:Second)')
plt.ylabel('Price USD')
plt.grid(color= '#0ff2f2',linestyle='--', linewidth=0.5)

line, = ax.plot(xs,ys,color='#96e1ff',label='BTC price') 
h_line, = ax.plot(xs,high,linestyle=':',color='#48de1f',label='Price High (last 24hrs)')
l_line, = ax.plot(xs,low,linestyle=':',color='#de1f47',label='Price Low (last 24hrs)')

def animate(frame,xs,ys,h_list,l_list):
	data = get_data()
	xs.append(data.time)
	
	#limit length of time (x) list
	xs=xs[-x_len:]
	ax.set_xlim(xs[0],xs[-1])

	#limit length of rate (y) lists
	ys.append(data.price)
	ys=ys[-x_len:]	

	#adjust y limits for new data point
	y_limits = ax.get_ylim()
	up_lim = y_limits[1]
	low_lim = y_limits[0]

	if(data.price < low_lim):
		low_lim = data.price-100	
	if(data.price > up_lim):
		up_lim = data.price+100

	ax.set_ylim(low_lim, up_lim)

	ax.set_xticks(xs)
	plt.xticks(rotation=45, ha='right')
	
	h_list.append(high)
	l_list.append(low)

	h_list = h_list[-x_len:]
	l_list = l_list[-x_len:]	

	#update line
	line.set_data(xs,ys)	
	h_line.set_data(xs,h_list)
	l_line.set_data(xs,l_list)

def main():	
	ani = animation.FuncAnimation(fig=fig,
		func=animate,
		interval=30000,
		fargs=(xs,ys,h_list,l_list),
		cache_frame_data=False
		)

	ax.legend()
	plt.show()
		

if __name__ == "__main__":
	main()


