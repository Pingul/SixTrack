import matplotlib.pyplot as plt

def plot_energy(dump, dynksets, penergy):
    data = {'turn' : [], 'dE' : [], 'E' : [], 'realE' : []}

    with open(dump, 'r') as f:
        for line in f.readlines():
            if line.lstrip().startswith("#"): continue
            pID, turn, s, x, xp, y, yp, z, dE, ktrack = line.rstrip('\n').split()
            if int(turn) in data['turn']:
                continue
            data['turn'].append(int(turn))
            data['dE'].append(float(dE))

    with open(dynksets, 'r') as f:
        dynk_turn = -1
        for turn in data['turn']:
            energy = 0
            while int(dynk_turn) < turn:
                line = f.readline()
                if line.lstrip().startswith("#") or not line.rstrip(): 
                    continue
                d_turn, var1, var2, v, function, value = line.rstrip('\n').split()
                energy = float(value)
                dynk_turn = int(d_turn)
            data['E'].append(float(energy))

    with open(penergy, 'r') as f:
        dynk_turn = 1
        for turn in data['turn']:
            energy = 0
            while int(dynk_turn) < turn:
                line = f.readline()
                if line.lstrip().startswith("#") or not line.rstrip(): 
                    continue
                energy = float(line.rstrip('\n').split()[4])
                dynk_turn += 1
            data['realE'].append(float(energy))

    print(len(data['turn']), len(data['realE']))

    energy = [data['E'][i] + data['E'][i]*data['dE'][i] for i in range(len(data['turn']))]
    # print(data['turn'][0:10])
    # print(energy[0:10])
    # print(data['E'][0:10])
    fig, ax = plt.subplots()
    ax.plot(data['turn'], energy, color='b', zorder=1, label='particle')
    ax.plot(data['turn'], data['E'], color='black', zorder=10, label='reference particle')
    ax.plot(data['turn'], data['realE'], color='r', zorder=11, label='Real value', linestyle='--')
    ax.legend(loc='lower right')
    ax.set_ylabel("Energy (MeV)")
    ax.set_xlabel("Turn")
    plt.show()

# plot_energy("data/no_coll/DUMP.txt", "data/no_coll/dynksets.dat", "data/no_coll/penergy_sixtrack.txt")
plot_energy("data/coll/DUMP.txt", "data/coll/dynksets.dat", "data/coll/penergy_sixtrack.txt")
