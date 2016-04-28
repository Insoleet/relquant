import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation

growth = 0.1
members = 10
mass = 0
du = 100
account_sup = 0.9*mass
account_less = 0.01*mass

fig, ax = plt.subplots()
line_mass, = ax.plot([], [], color='black')
line_account_sup = ax.plot([], [], color='red', lw=2)[0]
line_account_less = ax.plot([], [], color='blue', lw=2)[0]
ax.grid()
quant = [[], []]
sup = [[], []]
less = [[], []]
dividend = []
col = []

start = 30

def data_gen(t=0):
    global growth
    global mass
    global du
    global account_sup
    global account_less
    cnt = 0
    while cnt < 80:
        cnt += 1
        t += 1
        if t == start:
            account_sup = 0.9 * mass
            account_less = 0.01 * mass
        mass = mass + members * du
        account_sup = account_sup + du
        account_less = account_less + du
        du = max(du, growth*mass/members)
        yield ((t, mass), (t, du*members), (t, account_less), (t, account_sup))


def init():
    ax.set_xlim(0, 81-start)
    ax.set_ylim(0, 1000)
    color_iter = iter(colors.cnames.items())
    next(color_iter)
    for i in range(0, 10):
        dividend.append(([], []))
        col.append(next(color_iter))

    line_mass.set_data(quant)
    line_account_less.set_data(less)
    line_account_sup.set_data(sup)
    return line_account_less, line_account_sup, line_mass


def run(data):
    global mass
    # update the data
    m, d, acc_less, acc_sup = data
    if m[0] > start - 5:
        quant[0].append(m[0]-start)
        quant[1].append(m[1])
        sup[0].append(acc_sup[0]-start)
        sup[1].append(acc_sup[1])
        less[0].append(acc_less[0]-start)
        less[1].append(acc_less[1])

        for i in range(0, 10):
            dividend[i][0].append(d[0]-start)
            dividend[i][1].append(m[1]*(i+1)/10)

        ax.set_ylim(0, mass)
        ax.figure.canvas.draw()
        line_mass.set_data(quant[0], quant[1])
        line_account_sup.set_data(sup[0], sup[1])
        line_account_less.set_data(less[0], less[1])
        for i in range(0, 10):
            if i % 2 == 0:
                col = 'powderblue'
            else:
                col = 'paleturquoise'
            if i > 0:
                ax.fill_between(dividend[i][0], dividend[i-1][1], dividend[i][1], color=col, alpha=0.1)
            else:
                ax.fill_between(dividend[i][0], 0, dividend[i][1], color=col, alpha=0.1)

    return line_account_less, line_account_sup, line_mass

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=150,
                              repeat=False, init_func=init)


# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)

ani.save('quant.mp4', writer=writer)

#plt.show()