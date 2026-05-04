import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import datetime as dt
import requests


class rates():
	def __init__(self, ask, bid):
		self.ask = float(ask)
		self.bid = float(bid)



api_url=f"https://api.n.exchange/en/api/v1/price/BTCLTC/latest/"

def get_data():
	#get time stamp
	timestamp = dt.datetime.now().strftime('%H:%M:%S')
	
	#get rates
	try:
		response = requests.get(api_url)
		body = response.json()
		if isinstance(body,list) and isinstance(body[0], dict):
			body = body[0] #unwrap from list
		data = rates(body['ticker']['ask'],body['ticker']['bid'])
	except:
		raise Exception("Error fetching BTC LTC rates")
	
	return timestamp, data



#intial request to set up plot
timestamp, data = get_data()

#intialize variables for data collection
alim = data.ask
blim = data.bid

#timestamp =dt.datetime.now().strftime('%H:%M:%S')
xs=[timestamp]
ya=[None]
yb=[None]

x_len = 10
y_range = [blim-1, alim+1]

#plot settings and labels
style.use('dark_background')

fig = plt.figure(figsize=(14,7))
ax = fig.add_subplot(1,1,1)

ax.set_ylim(y_range)
plt.subplots_adjust(bottom=0.20)

#labels
plt.title('Bitcoin (BTC) to Litecoin (LTC) rates')
plt.xlabel('Time (Hour:Minute:Second)')
plt.ylabel('LTC per BTC')
plt.grid(color= 'green',linestyle='--', linewidth=0.5)

#blank line to be updated
line1, = ax.plot(xs,ya,color='#ff8c00',label='Ask price')
line2, = ax.plot(xs,yb,color='#0070ff', label='Bid price') 
ax.legend()

	
def animate(frame,xs,ya,yb):
	timestamp, data = get_data()
	xs.append(timestamp)
	
	#limit length of time (x) list
	xs=xs[-x_len:]
	ax.set_xlim(xs[0],xs[-1])

	#limit length of rate (y) lists
	ya.append(data.ask)
	yb.append(data.bid)
	ya=ya[-x_len:]
	yb=yb[-x_len:]	

	#adjust y limits for new data point
	y_limits = ax.get_ylim()
	up_lim = y_limits[1]
	low_lim = y_limits[0]

	if(data.bid < low_lim):
		low_lim = data.bid-1
	if(data.ask > up_lim):
		up_lim = data.ask+1

	ax.set_ylim(low_lim, up_lim)

	ax.set_xticks(xs)
	plt.xticks(rotation=45, ha='right')
	
	#update line
	line1.set_data(xs,ya)
	line2.set_data(xs,yb)
	

def main():
	ani = animation.FuncAnimation(fig=fig,
		func=animate,
		interval=1000,
		fargs=(xs,ya,yb),
		cache_frame_data=False
		)

	plt.show()
		

if __name__ == "__main__":
	main()


